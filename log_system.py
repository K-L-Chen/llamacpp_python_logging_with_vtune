# -*- coding: utf-8 -*-

import subprocess
import platform
import sys
import re
from datetime import datetime
import psutil
import time
from datetime import datetime

#Windows, MacOS, Linux
#first ele in list is what we don't want, second ele is what we want to replace it with
path_separator = {"Windows":["/",r"\\","\\"], "Darwin":[r"\\", "/", "/"], "Linux":[r"\\", "/", "/"]}

def write_csv_log(timer:int = 10):
    #start runtime, log to file llm_runlog_[YYYYMMDDHRMI].csv -- Year Month Day Hour Minute 
    
    starttime = time.time()
    
    #set up log csv with datetime of start of run
    #f = open(f"llm_runlog_thr{threads}_tok{outputsize}_{datetime.today().strftime(r'%Y%m%d%H%M')}.csv", "w")

    #starting memory usage
    #get individual CPU percent usage at start, convert all to strings
    cpupercent = [str(x) for x in psutil.cpu_percent(percpu=True)]
    headers = [f"CPU {x} Usage (%):" for x in range(len(cpupercent))]

    #setup string we write to so we don't waste time writing to file
    write_to_file_str = f"Runtime (s):,{','.join(headers)},Memory Usage (GiB):\n{time.time()-starttime},{','.join(cpupercent)},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n"

    #check if proc has completed (poll not None)
    #if proc not complete, log usage w/ interval 1 second to mimic Task Manager Normal usage logging
    #once complete, close file and output time taken
    while (i := i + 1) < timer:
        write_to_file_str += f"{time.time()-starttime},{','.join([str(x) for x in psutil.cpu_percent(percpu=True, interval=1)])},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n"
        subprocess.Popen(f"nvidia-smi >> llm_runlog_gpu_{datetime.today().strftime(r'%Y%m%d%H%M')}.log", shell=True).wait()
    #f.close()

    #bulk write to the csv file
    #pathmodel.split(path_separator[system][2]) splits the string along "\\". I do not know why r"\\" doesn't work
    #It's pretty awful
    with open(f"system_info.csv", "w", encoding="utf-16-le") as logfile:
        logfile.write(write_to_file_str)

    print(f"Time elapsed: {time.time() - starttime}")
    
    return 0

def main(timer:int, system:str = platform.system()):
    write_csv_log(timer, system)
    
    return 0
    
#ex python3 .\benchmark_model_run.py ".\llama_cpp\llama.cpp\main.exe" ".\openllama_3b_v2\open_llama_3b_v2\ggml-model-f16.gguf" 8 128 hello
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Usage: python log_use.py [time to run]")

    system = platform.system()
    main((lambda i: int(i) if i.isnumeric() else 10)(sys.argv[1]), system)