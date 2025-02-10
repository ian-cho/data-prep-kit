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
   1. If you plan to work with Olama:
      1.  install ollama, see https://ollama.com/download
      2.  pull a model e.g. `ollama pull llama3.1:70b`
   2. In order to work with WatsonX, you have to create a `.env` file in the root directory of the project with the following fields:
```python
WATSONX_APIKEY="Your WatsonX API key"
WATSON_PROJECT_ID="Your WatsonX project"
WATSONX_URL="WatsonX access point"
```
See [WatsonX documentation](https://www.ibm.com/watsonx), how to obtain the values.

## Usage
**TBD**

## Notes
- [Planning_DPK_agent.ipynb](Planning_DPK_agent.ipynb): Planner for Data-Prep-Kit tasks with code generation.
- [dpk_langchain.ipynb](dpk_tools.ipynb): Invoke DPK transforms defined as [langchain tools](https://python.langchain.com/v0.1/docs/modules/tools/) or  [llama-index tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/).
