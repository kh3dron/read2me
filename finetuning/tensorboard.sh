#!/bin/bash

# Find the most recent run directory
RUN_PATH=$(ls -d run-* | sort -r | head -n 1)

tensorboard --bind_all --logdir=$RUN_PATH
