#!/bin/bash

# Anzahl der Prompts (Default: 20)
COUNT=${1:-20}

# Virtual Environment aktivieren
source /opt/syntx-workflow-api-get-prompts/venv/bin/activate

# Batch generieren
cd /opt/syntx-workflow-api-get-prompts
python3 -c "from batch_generator import generate_batch; generate_batch($COUNT)"
