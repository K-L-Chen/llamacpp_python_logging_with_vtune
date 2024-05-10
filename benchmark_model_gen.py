# -*- coding: utf-8 -*-

import subprocess
import platform
import sys
#import re
from datetime import datetime
import psutil
import time
from datetime import datetime

# swap = [r"\\",r"\/"]

# def sanitize_input(pathgen:str=None, pathmodel:str = None):
#     if not pathgen or not pathmodel:
#         raise ValueError("Usage: python benchmark_model_gen.py [Path to Generator e.g. llama.cpp] [Path to Model]")
    
#     systemtype = platform.system()
#     swap_val = 0
#     if systemtype == "Windows":
#         swap_val = 1

#     re.sub(swap[swap_val], swap[(swap_val + 1) % 2], pathgen)
#     re.sub(swap[swap_val], swap[(swap_val + 1) % 2], pathmodel)

#     return (pathgen, pathmodel)

def main(pathgen:str = None, pathmodel:str = None):
    #log start time to get total runtime later
    starttime = time.time()
    
    #generate file
    f = open(f"llm_genlog_{datetime.today().strftime(r'%Y%m%d%H%M')}.csv", "w")

    #get individual CPU percent usage at start, convert all to strings
    cpupercent = [str(x) for x in psutil.cpu_percent(percpu=True)]
    headers = [f"CPU {x} Usage (%):" for x in range(len(cpupercent))]

    #write to file
    #f.write(f"Runtime (s):,CPU Usage (%):,Memory Usage (GiB):\n{time.time()-starttime},{psutil.cpu_percent()},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n")
    f.write(f"Runtime (s):,{','.join(headers)},Memory Usage (GiB):\n{time.time()-starttime},{','.join(cpupercent)},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n")

    #set up main process (generate model file)
    proc = subprocess.Popen(["python3", pathgen, pathmodel])
    poll = proc.poll()

    #check if proc has completed (poll not None)
    #if proc not complete, log usage w/ interval 1 second to mimic Task Manager Normal usage logging
    #once complete, close file and output time taken
    while poll is None:
        f.write(f"{time.time()-starttime},{','.join([str(x) for x in psutil.cpu_percent(percpu=True, interval=1)])},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n")
        poll = proc.poll()
        subprocess.Popen(f"nvidia-smi >> llm_genlog_gpu_{datetime.today().strftime(r'%Y%m%d%H%M')}.log", shell=True).wait()
    f.close()

    print(f"Time elapsed: {time.time() - starttime}")
    return 0

#ex. python3 .\benchmark_model_gen.py "C:\Users\tankk\Documents\llmresearch\llama_cpp\llama.cpp\convert.py" "C:\Users\tankk\Documents\llmresearch\openllama_3b_v2\open_llama_3b_v2\"
#or python3 .\benchmark_model_gen.py ".\llama_cpp\llama.cpp\convert.py" ".\openllama_3b_v2\open_llama_3b_v2\"
if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Usage: python benchmark_model_gen.py [Path to convert.py e.g. llama.cpp] [Path to Model]")

    main(sys.argv[1], sys.argv[2])