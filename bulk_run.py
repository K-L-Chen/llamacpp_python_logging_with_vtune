#import get_llm_output
#import benchmark_model_run
import os
from glob import glob
import pathlib
import subprocess
import sys
import platform
import re
import get_llm_output
import time
path_separator = {"Windows":["/",r"\\","\\"], "Darwin":[r"\\", "/", "/"], "Linux":[r"\\", "/", "/"]}


def run_as_wanted(pathmain, list_of_gguf_files, strlist_of_gguf_files, num_threads=8, num_tokens_gen=128, prompt="", auto=False, system=platform.system()):
    existing_vtune = [x for x in os.listdir() if re.search(r"^r\d+.+",x)]
    print(pathmain, num_threads, num_tokens_gen, prompt, auto, system)
    print(existing_vtune)
    
    for i in range(len(list_of_gguf_files)):
        decomp_info = strlist_of_gguf_files[i].split(path_separator[system][2])
        gguf_info = decomp_info[-1].split("-")
        print(decomp_info[-2], gguf_info[-1][:-5])
        #print([x for x in existing_vtune if decomp_info[-2] in x and gguf_info[-1][:-5] in x])
        newest_vtune_dir = (lambda y: "r0ma" if y == [] else max(y, key=os.path.getctime))([x for x in existing_vtune if decomp_info[-2] in x and gguf_info[-1][:-5] in x])
        #print(newest_vtune_dir)
        number = (lambda y: int(y.group(1)) if y != None else 0)(re.search(r"^r(\d+).*", newest_vtune_dir))
        #print(number)

        #generate new name based on most recent folder created
        name_construct = f"r{number + 1}ma_thr{num_threads}_tok{num_tokens_gen}_{decomp_info[-2]}_{gguf_info[-1][:-5]}_memaccess"

        print(name_construct)
        if not auto:
            run = input(f"Run file | {list_of_gguf_files[i].name} |  [Y/N] ? ")
            if "q" in run or "stop" in run or "STOP" in run:
                break
            if run == "Y" or run == "y":
                subprocess.Popen(["vtune", "-collect", "memory-access", "--result-dir", name_construct, "python3", "benchmark_model_run.py", pathmain, f".{path_separator[system][1]}{strlist_of_gguf_files[i]}", num_threads, num_tokens_gen, prompt, ">", f"vtune{number}_{gguf_info[-1][:-5]}.out"],shell=True).wait()
                #os.system(" ".join(["vtune", "-collect", "memory-access", "--result-dir", name_construct, "python3", "benchmark_model_run.py", pathmain, f".{path_separator[system][1]}{strlist_of_gguf_files[i]}", num_threads, num_tokens_gen, prompt, ">", "vtune.out"]))
                out = get_llm_output.get_out_len()
                get_llm_output.bruteforce_update_name(out,"." + path_separator[system][2] + name_construct + path_separator[system][2])
        else:
            subprocess.Popen(["vtune", "-collect", "memory-access", "--result-dir", name_construct, "python3", "benchmark_model_run.py", pathmain, f".{path_separator[system][1]}{strlist_of_gguf_files[i]}", num_threads, num_tokens_gen, prompt, ">", f"vtune{number}_{gguf_info[-1][:-5]}.out"],shell=True).wait()
            #os.system(" ".join(["vtune", "-collect", "memory-access", "--result-dir", name_construct, "python3", "benchmark_model_run.py", pathmain, f".{path_separator[system][1]}{strlist_of_gguf_files[i]}", num_threads, num_tokens_gen, prompt, ">", "vtune.out"]))
            out = get_llm_output.get_out_len()
            get_llm_output.bruteforce_update_name(out,"." + path_separator[system][2] + name_construct + path_separator[system][2])
        time.sleep(1)


    print("Stopping.")
    return 0

def main(pathmain:str = None, threads:str = "8", tokens_predict:str = "128", prompt:str = None, system:str = platform.system(), auto=False):
    #exclude example files, since we only care about llama models
    models = [pt for pt in list(pathlib.Path(".").rglob("*.gguf")) if "llama" in str(pt) and "llama_cpp" not in str(pt)]
    models_str = [str(pt) for pt in models]
    #print(models, "\n",models_str)
    run_as_wanted(pathmain, models, models_str, threads, tokens_predict, prompt, auto, system)
    return

if __name__ == "__main__":
    if len(sys.argv) < 5:
        #automatic run is an optional value that just syas whether or not we should run it w/o input (will take a long time)
        raise ValueError("Usage: python bulk.py [Path to Main executable e.g. llama.cpp] [Number of Threads] [Number of Tokens to Predict] [Prompt] [automatic (optional)]")

    if not sys.argv[2].isnumeric():
        raise ValueError("Number of threads must be a valid number")
    if not sys.argv[3].isnumeric():
        raise ValueError("Output size must be a valid number")

    system = platform.system()
    main_exec = re.sub(path_separator[system][0], path_separator[system][1], sys.argv[1])
    main(main_exec, sys.argv[2], sys.argv[3], sys.argv[4], system, 6 <= len(sys.argv))