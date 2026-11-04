"""Read-only environment probe; no credentials or model downloads."""
import ctypes,importlib.util,json,platform,shutil,sys
from ctypes import wintypes
class Memory(ctypes.Structure):
 _fields_=[('length',wintypes.DWORD),('load',wintypes.DWORD)]+[(n,ctypes.c_ulonglong) for n in ['total','available','page','availpage','virt','availvirt','extended']]
m=Memory();m.length=ctypes.sizeof(Memory)
if platform.system()=='Windows':ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print(json.dumps({'python':sys.version,'platform':platform.platform(),'ram_gb':m.total/2**30,'available_gb':m.available/2**30,'modules':{n:bool(importlib.util.find_spec(n)) for n in ['torch','transformers','soundfile','qwen_tts']},'disk_free_gb':shutil.disk_usage('.').free/2**30},indent=2))
