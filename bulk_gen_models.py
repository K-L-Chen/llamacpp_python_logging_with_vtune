import sys
import subprocess
import platform
import re
import os.path as path
import pathlib

path_separator = {"Windows":["/",r"\\","\\"], "Darwin":[r"\\", "/", "/"], "Linux":[r"\\", "/", "/"]}

#convert f*.gguf file to Q4 and Q5 types
def main(quant:str, model_dir:str, system=platform.system()):
    if system == "Windows" and ".exe" not in quant:
        quant = quant + ".exe"
    model_file = [str(pt) for pt in list(pathlib.Path(model_dir).rglob("*.gguf")) if re.match(r".+f\d+\.gguf", str(pt))]
    print(model_file)
    
    subprocess.Popen([quant, model_file[0], path.join(model_dir,"ggml-model-Q4_K_M.gguf"), "Q4_K_M"]).wait()
    subprocess.Popen([quant, model_file[0], path.join(model_dir,"ggml-model-Q5_K_M.gguf"), "Q5_K_M"]).wait()
    subprocess.Popen([quant, model_file[0], path.join(model_dir,"ggml-model-Q5_K_S.gguf"), "Q5_K_S"]).wait()
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Usage: python benchmark_model_gen.py [Path to quantize.exe e.g. llama.cpp] [Path to Folder with F16 Model]")
    
    system = platform.system()
    quant = re.sub(path_separator[system][0], path_separator[system][1], sys.argv[1])
    model_dir = re.sub(path_separator[system][0], path_separator[system][1], sys.argv[2])
    main(quant, model_dir, system)