# -*- coding: utf-8 -*-

import subprocess
import platform
import sys
import re
from datetime import datetime
import psutil
import time

#Windows, MacOS, Linux
#first ele in list is what we don't want, second ele is what we want to replace it with
path_separator = {"Windows":["/",r"\\","\\"], "Darwin":[r"\\", "/", "/"], "Linux":[r"\\", "/", "/"]}

def write_csv_log(pathmain:str = None, pathmodel:str = None, threads:str = "8", tokens_predict:str = "128", prompt:str = None):
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

    #reference command
    #.\main -m 'C:\Users\tankk\Documents\llmresearch\openllama_3b_v2\open_llama_3b_v2\ggml-model-f16.gguf' -n 256 -p "Good morning." -t 16 --log-test --log-file test
    #run process (run model file)
    proc = subprocess.Popen([pathmain, "-m", pathmodel, "-t", threads, "-n", tokens_predict, "-p", prompt, "-c", "2048", "--log-test", "--log-file", "test"])

    #check if proc has completed (poll not None)
    #if proc not complete, log usage w/ interval 1 second to mimic Task Manager Normal usage logging
    #once complete, close file and output time taken
    #checks nvidia-smi in case it uses the GPU and not the integrated graphics system
    while (poll := proc.poll()) is None:
        write_to_file_str += f"{time.time()-starttime},{','.join([str(x) for x in psutil.cpu_percent(percpu=True, interval=1)])},{(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024.0 ** 3)}\n"
        #subprocess.Popen(f"nvidia-smi >> llm_runlog_gpu_{datetime.today().strftime(r'%Y%m%d%H%M')}.log", shell=True).wait()
    #f.close()

    #bulk write to the csv file
    #pathmodel.split(path_separator[system][2]) splits the string along "\\". I do not know why r"\\" doesn't work
    #It's pretty awful
    with open(f"llm_runlog_thr{threads}_tok{tokens_predict}_{pathmodel.split(path_separator[system][2])[-2]}_{pathmodel.split('-')[-1][:-5]}_{datetime.today().strftime(r'%Y%m%d%H%M')}.csv", "w", encoding="utf-16-le") as logfile:
        logfile.write(write_to_file_str)

    print(f"Time elapsed: {time.time() - starttime}")
    
    return 0

def get_time(system:str = platform.system()):
    #get tokens for running model, script used changes based on OS
    if system == "Windows":
        subprocess.Popen([r".\log_benchmark_condense.bat"], shell=True).wait()
    else:
        subprocess.Popen([r"./log_benchmark_condense.sh"], shell=True).wait()

def main(pathmain:str = None, pathmodel:str = None, threads:str = "8", tokens_predict:str = "128", prompt:str = None, system:str = platform.system()):
    write_csv_log(pathmain, pathmodel, threads, tokens_predict, prompt)
    get_time(system)
    
    return 0
    
#ex python3 .\benchmark_model_run.py ".\llama_cpp\llama.cpp\main.exe" ".\openllama_3b_v2\open_llama_3b_v2\ggml-model-f16.gguf" 8 128 hello
if __name__ == "__main__":
    if len(sys.argv) < 6:
        raise ValueError("Usage: python benchmark_model_run.py [Path to Main executable e.g. llama.cpp] [Path to Model] [Number of Threads] [Number of Tokens to Predict] [Prompt]")

    if not sys.argv[3].isnumeric():
        raise ValueError("Number of threads must be a valid number")
    if not sys.argv[4].isnumeric():
        raise ValueError("Output size must be a valid number")

    system = platform.system()
    main_exec = re.sub(path_separator[system][0], path_separator[system][1], sys.argv[1])
    model_file = re.sub(path_separator[system][0], path_separator[system][1], sys.argv[2])
    main(main_exec, model_file, sys.argv[3], sys.argv[4], sys.argv[5], system)