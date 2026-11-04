#include "SPlisHSPlasH/Simulation.h"
#include "SPlisHSPlasH/TimeManager.h"
#include "SPlisHSPlasH/TimeStep.h"
#include "SPlisHSPlasH/BoundaryModel_Akinci2012.h"
#include "SPlisHSPlasH/StaticRigidBody.h"
#include "Utilities/Logger.h"
#include "Utilities/Timing.h"
#include "Utilities/Counting.h"
#include "json.hpp"
#include <fstream>
#include <cmath>
#include <iostream>

INIT_LOGGING
INIT_TIMING
INIT_COUNTING
using namespace SPH;
static_assert(sizeof(Real) == 8, "Match the core double-precision ABI");
using json = nlohmann::json;

int main(int argc, char** argv) {
  if (argc != 2) {std::cerr << "Usage: bake_fluid output.json\n"; return 2;}
  auto sim = new Simulation();
  Simulation::setCurrent(sim);
  sim->init(0.025, true);
  // In 2D the precomputed 3D default has no enum entry: choose valid 2D kernels.
  sim->setKernel(0);
  sim->setGradKernel(0);
  sim->setBoundaryHandlingMethod(BoundaryHandlingMethods::Akinci2012);
  sim->setValue<int>(Simulation::CFL_METHOD, 0);
  sim->setValue<bool>(Simulation::ENABLE_Z_SORT, false);
  Vector3r gravity(0, -4, 0);
  sim->setVecValue<Real>(Simulation::GRAVITATION, gravity.data());
  auto tm = TimeManager::getCurrent(); tm->initParameters(); tm->setTime(0);
  constexpr int frames = 90, fps = 30, substeps = 8;
  const Real dt = Real(1) / Real(fps * substeps);
  tm->setTimeStepSize(dt);
  std::vector<Vector3r> points, velocities;
  std::vector<unsigned int> ids;
  for (int row = 0; row < 14; row++) for (int col = 0; col < 12; col++) {
    points.emplace_back(-0.95 + col * 0.05, 0.10 + row * 0.05, 0);
    velocities.emplace_back(0, 0, 0); ids.push_back(0);
  }
  sim->addFluidModel("Fluid", points.size(), points.data(), velocities.data(), ids.data(), 0);
  auto model = sim->getFluidModel(0);
  model->setViscosityMethod(0u);
  std::vector<Vector3r> wall;
  for (int layer = 0; layer < 2; layer++) {
    const Real bottom = -0.05 * layer, top = 1.6 + 0.05 * layer;
    for (int col = 0; col <= 46 + 2 * layer; col++) {
      const Real x = -1.15 - 0.05 * layer + 0.05 * col;
      wall.emplace_back(x, bottom, 0); wall.emplace_back(x, top, 0);
    }
    for (int row = 1; row < 32 + 2 * layer; row++) {
      const Real y = -0.05 * layer + row * 0.05;
      wall.emplace_back(-1.15 - 0.05 * layer, y, 0); wall.emplace_back(1.15 + 0.05 * layer, y, 0);
    }
  }
  auto body = new StaticRigidBody();
  body->setPosition(Vector3r::Zero()); body->setPosition0(Vector3r::Zero());
  body->setRotation(Quaternionr::Identity()); body->setRotation0(Quaternionr::Identity());
  auto boundary = new BoundaryModel_Akinci2012();
  boundary->initModel(body, wall.size(), wall.data());
  sim->addBoundaryModel(boundary);
  sim->setSimulationMethod(static_cast<int>(SimulationMethods::DFSPH));
  // Match SimulatorBase: register each fluid point set once, then boundaries.
  sim->setSimulationInitialized(true);
  boundary->deferredInit();
  sim->updateBoundaryVolume();
  json data = {{"schemaVersion",1},{"engine","SPlisHSPlasH"},{"engineVersion","2.19.1"},{"solver","DFSPH"},{"backend","cpu-double"},{"fps",fps},{"substeps",substeps},{"dt",dt},{"particleRadius",0.025},{"bounds",{-1.15,0,1.15,1.6}},{"frames",json::array()},{"times",json::array()}};
  Real initialMass = 0, finalMass = 0, maxDensity = 0;
  for (unsigned int i = 0; i < model->numActiveParticles(); i++) initialMass += model->getMass(i);
  for (int frame = 0; frame < frames; frame++) {
    if (frame) for (int step = 0; step < substeps; step++) sim->getTimeStep()->step();
    json snapshot = json::array();
    for (unsigned int i = 0; i < model->numActiveParticles(); i++) {
      const auto &p = model->getPosition(i);
      if (!std::isfinite(p.x()) || !std::isfinite(p.y())) {std::cerr << "Non-finite fluid position\n"; return 3;}
      snapshot.push_back({std::round(p.x()*1e6)/1e6, std::round(p.y()*1e6)/1e6});
      maxDensity = std::max(maxDensity, model->getDensity(i));
    }
    data["frames"].push_back(snapshot); data["times"].push_back(tm->getTime());
  }
  for (unsigned int i = 0; i < model->numActiveParticles(); i++) finalMass += model->getMass(i);
  data["metrics"] = {{"particles",model->numActiveParticles()},{"initialMass",initialMass},{"finalMass",finalMass},{"maxDensity",maxDensity}};
  std::ofstream output(argv[1]); output << data.dump() << '\n';
  if (!output) return 4;
  std::cout << "Baked " << frames << " fluid frames with " << model->numActiveParticles() << " particles\n";
  delete sim;
  return 0;
}
