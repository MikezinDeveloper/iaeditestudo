"""Execute upstream warp and UNTRAINED networks. No pretrained quality claim."""
from pathlib import Path
import argparse,json,sys,time,hashlib
p=argparse.ArgumentParser();p.add_argument('checkout');a=p.parse_args();U=Path(a.checkout);sys.path.insert(0,str(U))
import torch
from model.warplayer import warp
from model.IFNet import IFNet
from model.IFNet_m import IFNet_m
torch.set_num_threads(2);torch.manual_seed(2026);torch.set_grad_enabled(False)
image=torch.rand(1,3,64,64);identity=warp(image,torch.zeros(1,2,64,64));err=(identity-image).abs().max().item();assert err<1e-5
x=torch.cat([image,image.flip(-1)],dim=1);result={'torch':torch.__version__,'device':'cpu','pretrained_weights':False,'scope':'Warp identity and neural architecture execution ONLY; random weights are not an interpolation model with validated quality','warp_identity_max_error':err,'models':[]}
for kind,cls in [('midpoint',IFNet),('arbitrary',IFNet_m)]:
 model=cls().eval();start=time.monotonic();a=model(x,timestep=.25)[2][2];b=model(x,timestep=.75)[2][2]
 assert list(a.shape)==[1,3,64,64] and torch.isfinite(a).all()
 difference=(a-b).abs().max().item()
 if kind=='midpoint':assert difference==0,'Basic IFNet unexpectedly used timestep'
 else:assert difference>0,'Arbitrary network did not use timestep'
 result['models'].append({'kind':kind,'shape':list(a.shape),'finite':True,'timestep_difference':difference,'elapsed_seconds':time.monotonic()-start})
 del model
R=Path(__file__).resolve().parents[1]/'estudo/rife/resultados';R.mkdir(parents=True,exist_ok=True);(R/'architecture-only.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
