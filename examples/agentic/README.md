# Agentic Data Agent Experiments

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation Guide](#installation-guide)
3. [Usage](#usage)


## Project Overview

This project focuses on automating the integration of Large Language Models (LLM) based workflow in the data access.
It contains the following notebooks:

- [Planning_DPK_agent.ipynb](Planning_DPK_agent.ipynb): Planner for Data-Prep-Kit tasks with code generation.
- [dpk_langchain.ipynb](dpk_tools.ipynb): Use DPK transforms defined as [langchain tools](https://python.langchain.com/v0.1/docs/modules/tools/) or  [llama-index tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/). 
This notebook leverages LLM to generate a DPK transforms pipeline based on natural language inputs. 
The LLM processes the provided input and produces the pipeline in the correct format, making it ready for execution.
Subsequently, each transform in the pipeline is invoked by calling its lang-chain or llama-index implementations.


## Before you begin

Ensure that you have python 3.11

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

To lunch a notebook execute the following command:
```bash
Jupyter notebook
```

