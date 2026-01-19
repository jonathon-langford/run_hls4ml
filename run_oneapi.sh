#!/bin/bash
apptainer exec $APPTAINER_IMAGE_PATH \
    bash -c "source /opt/intel/oneapi/2025.0/oneapi-vars.sh --force && source /opt/intel/oneapi/2025.0/opt/oclfpga/fpgavars.sh --force && source /home/oneapi/miniconda3/etc/profile.d/conda.sh && conda run -n oneapi-env python "$@""
