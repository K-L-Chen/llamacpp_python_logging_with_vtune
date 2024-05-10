# llama.cpp Logging Using Python and VTune
A basic set of scripts designed to log llama.cpp's CPU core and memory usage over time using Python logging systems and Intel VTune.  
  
Output of the script is saved to a CSV file which contains the time stamp (incremented in one second increments), CPU core usage in percent, and RAM usage in GiB.  

## Required Files
  -benchmark_model_run.py
  -bulk_run.py, bulk_run_no_vtune.py
  -get_llm_output.py
  -log_benchmark_condense.bat, log_benchmark_condense.sh  
  
Other files are optional for logging
