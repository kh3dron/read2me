#!/bin/bash

# Find the most recent run directory
RUN_PATH=$(ls -d run-* | sort -r | head -n 1)

MODEL_PATH="$RUN_PATH/best_model.pth"
CONFIG_PATH="$RUN_PATH/config.json"

tts --text "I love my bird! she is the worlds best bird. I tell her this every day." \
    --model_path "$MODEL_PATH" \
    --config_path "$CONFIG_PATH" \
    --out_path sample_output.wav
