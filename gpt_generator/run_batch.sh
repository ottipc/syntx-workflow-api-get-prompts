#!/bin/bash
COUNT=${1:-20}

source /opt/syntx-workflow-api-get-prompts/venv/bin/activate

cd /opt/syntx-workflow-api-get-prompts/gpt_generator

python3 batch_generator.py $COUNT
