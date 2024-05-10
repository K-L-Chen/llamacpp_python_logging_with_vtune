import glob
from os import path
import platform
import subprocess

path_separator = {"Windows":["/",r"\\"], "Darwin":[r"\\", "/"], "Linux":[r"\\","/"]}
movecmd = {"Windows":"move", "Darwin":"mv", "Linux":"mv"}

def bruteforce_update_name(llm_output:str = None, spec_directory:str = ""):
    if not llm_output:
        raise ValueError("No value was inputted. Quitting.")
    
    system = platform.system()
    #brute force updates the name of the last csv
    newest_csv = max(glob.glob(rf".{path_separator[system][1]}*csv"), key=path.getctime)
    (temp:=newest_csv.split("_")).insert(4, str(len(llm_output.split(" ")))+"_"+str(len(llm_output)))    #TODO add length in number of words as well
    print(f"Moving {newest_csv} to {spec_directory}{'_'.join(temp)[2:]}")
    #print(path.curdir)
    subprocess.Popen(f"{movecmd[system]} {newest_csv} {spec_directory}{'_'.join(temp)[2:]}",shell=True)#[movecmd[system], newest_csv, "_".join(temp)], shell=True).wait()
    return 0

def get_out_len():
    system = platform.system()

    llmout = ""
    newest_outfile = max(glob.glob(rf".{path_separator[system][1]}*out"), key=path.getctime)
    print(newest_outfile)
    try:
        with open(newest_outfile, encoding='utf-16-le') as log:
            fd = log.read()
            #print(log.read())
            llmout = fd[fd.find("stdout!") + 8:fd.find("main.log found!")]
    except:
        with open(newest_outfile, encoding='utf-8') as log:
            fd = log.read()
            #print(log.read())
            llmout = fd[fd.find("stdout!") + 8:fd.find("main.log found!")]
    print(f"******\n{llmout}")
    return llmout

def main():
    out = get_out_len()
    bruteforce_update_name(out)
    print("Done!")

if __name__ == "__main__":
    main()