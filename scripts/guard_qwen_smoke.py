"""Launch only our inference child and record memory; never stop other applications."""
from pathlib import Path
import argparse,ctypes,json,os,subprocess,time,sys
from ctypes import wintypes
import psutil
class Memory(ctypes.Structure):
 _fields_=[('length',wintypes.DWORD),('load',wintypes.DWORD)]+[(n,ctypes.c_ulonglong) for n in ['total','available','page','availpage','virt','availvirt','extended']]
def available_mb():
 m=Memory();m.length=ctypes.sizeof(Memory);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return m.available/2**20
class ProcessMemory(ctypes.Structure):
 _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage']]
def process_mb(child):
 p=ProcessMemory();p.cb=ctypes.sizeof(ProcessMemory)
 ok=ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(int(child._handle)),ctypes.byref(p),p.cb)
 return {'working_set_mb':round(p.WorkingSetSize/2**20,1),'peak_working_set_mb':round(p.PeakWorkingSetSize/2**20,1),'private_commit_mb':round(p.PrivateUsage/2**20,1)} if ok else {}
def main():
 p=argparse.ArgumentParser();p.add_argument('request');p.add_argument('--output',required=True);p.add_argument('--timeout',type=int,default=1200);a=p.parse_args()
 root=Path(__file__).resolve().parents[1];out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',PYTHONIOENCODING='utf-8',HF_HUB_DISABLE_TELEMETRY='1')
 cmd=[str(root/'.venv-qwen/Scripts/python.exe'),str(root/'scripts/qwen_voiceover.py'),a.request,'--output',str(out)]
 started=time.monotonic();samples=[];reason=None
 with out.with_suffix('.stdout.log').open('w',encoding='utf8') as stdout,out.with_suffix('.stderr.log').open('w',encoding='utf8') as stderr:
  child=subprocess.Popen(cmd,cwd=root,env=env,stdout=stdout,stderr=stderr)
  while child.poll() is None:
   owned=[psutil.Process(child.pid)]
   try:owned+=owned[0].children(recursive=True)
   except psutil.Error:pass
   members=[]
   for process in owned:
    try:
     mi=process.memory_info();members.append({'pid':process.pid,'rss_mb':round(mi.rss/2**20,1),'private_mb':round(getattr(mi,'private',0)/2**20,1)})
    except psutil.Error:pass
   sample={'elapsed':round(time.monotonic()-started,2),'available_ram_mb':round(available_mb(),1),'owned_processes':members};samples.append(sample)
   if sample['available_ram_mb']<768:reason='Low memory guard (<768MiB available)'
   if sample['elapsed']>a.timeout:reason='Bounded smoke timeout'
   if reason:
    # The Windows venv redirector may own the actual inference process. Stop
    # only this launcher's descendants, never arbitrary Python processes.
    for process in reversed(owned):
     try:process.terminate()
     except psutil.Error:pass
    _,alive=psutil.wait_procs(owned,timeout=5)
    for process in alive:
     try:process.kill()
     except psutil.Error:pass
    child.wait(timeout=30);break
   time.sleep(3)
  code=child.wait()
 result={'command':cmd,'exit_code':code,'elapsed_seconds':time.monotonic()-started,'termination_reason':reason,'samples':samples,'output_exists':out.exists(),'scope':'Windows process working-set/peak/private commit and system free memory sampled every3s; no GPU inference or cross-hardware benchmark.'}
 out.with_suffix('.guard.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k not in ('command','samples')}));return 0 if code==0 else 1
if __name__=='__main__':sys.exit(main())
