#!/bin/bash

# Anzahl der Prompts (Default: 20)
COUNT=${1:-20}

# API Key direkt setzen
export OPENAI_API_KEY=$(grep OPENAI_API_KEY ~/.bashrc | cut -d'"' -f2)

# Ins richtige Verzeichnis
cd /opt/syntx-workflow-api-get-prompts

# Virtual Environment aktivieren
source ./venv/bin/activate

# Batch generieren
python3 -c "from batch_generator import generate_batch; generate_batch($COUNT)"
