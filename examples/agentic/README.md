# Agentic Data Agent Experiments

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation Guide](#installation-guide)
3. [Usage](#usage)


## Project Overview

This project focuses on automating the integration of LLM based workflow in the data access.

## Installation Guide

1. Clone the repository:
```bash
git clone git@github.com:IBM/data-prep-kit.git
cd examples/agentic
```

2. Create Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install jupyter
pip install ipython && pip install ipykernel
pip install -r requirements.txt
```

3. Configure access to LLM
   Currently, we support [Watsonx](https://www.ibm.com/watsonx), [Replicate](https://replicate.com/), and locally running [Ollama](https://ollama.com/).
   - To use Ollama: 
      - Download Ollama](https://ollama.com/download).
      - Download one of the supported [modules](https://ollama.com/search).
      - update the `model_ollama_*` names in the cell below
   - To use Watsonx:
      - Register for Watsonx
      - Obtain its API key
      - Store the following values in the `.env` file located in your project directory:
         ```
            WATSONX_URL=<WatsonX entry point, e.g. https://us-south.ml.cloud.ibm.com>
            WATSON_PROJECT_ID=<your Watsonx project ID>
            WATSONX_APIKEY=<your Watsonx API key>
         ```
      - Uncomment the Watsonx configuration entries, update the Watsonx `model_watsonx_*` names, and comment out the Ollama configuration entries.
   - To use Replicate:
      - Obtain Replicate API token
      - Store the following value in the `.env` file located in your project directory:
         ```
            REPLICATE_API_TOKEN=<your Replicate API token>
         ```

## Usage
**TBD**

## Notes
- [Planning_DPK_agent.ipynb](Planning_DPK_agent.ipynb): Planner for Data-Prep-Kit tasks with code generation.
- [dpk_intro_1_langchain.ipynb](dpk_intro_1_langchain.ipynb): .
