# run_hls4ml
Repository to store scripts for running hls4ml via apptainer

## Setup
Simply run the following command to point to apptainer image:
```
source setup.sh
```

## Running scripts
Run python scripts with hls4ml (oneAPI backend) using:
```
./run_oneapi.sh file.py
```

You can check setup is working with:
```
./run_oneapi.sh check_hls4ml.py
```
