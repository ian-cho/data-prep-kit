This directory contains implementation of DPK transforms as [langchain](https://python.langchain.com/v0.1/docs/modules/tools/) or [llama-index](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) tools.

- [`langchain_tools`](./langchain_tools) directory contains code to define DPK transforms as langchain tools similar to the tools defined in [here](https://github.com/langchain-ai/langchain/tree/master/libs/community/langchain_community/tools).
- [`llama_index_tools`](./llama_index_tools) directory contains code to define DPK transforms as llama-index tools similar to the tools defined in [here](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/tools).
- [dpk_common.py](./dpk_common.py) contains definitions used in both of the implementations defined above. 

For example usage please look at [dpk_as_tools.ipynb](../../dpk_as_tools.ipynb) notebook.
