from dotenv import dotenv_values
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import LLM
from llm_utils.callbacks import LoggingCallbackHandler
from typing import Optional, Any, Dict
from langchain_openai import ChatOpenAI

CONFIG_LOCATION = ".env"


def getLLM(inference: str, model_id: str = None, config: dict = None) -> LLM:
    loggingCallbackHandler = LoggingCallbackHandler()
    if config is None:
        config = dotenv_values(CONFIG_LOCATION)

    if inference == "ollama":
        from langchain_ollama.llms import OllamaLLM

        if model_id is None or len(model_id) == 0:
            model_id = "llama3.1:70b"
        return OllamaLLM(model=model_id, temperature=0, callbacks=[loggingCallbackHandler])

    elif inference == "bamllm":
        from llm import BAMLLM
        from genai.schema import TextGenerationParameters, DecodingMethod

        parameters = {
            "decoding_method": DecodingMethod.GREEDY,  # GREEDY or SAMPLE
            "max_new_tokens": 1024,  # 0 to 4096
            "min_new_tokens": 1,  # >=0
            "stop_sequence": None,
            "temperature": 0,  # 0.0 - 2.0, step 0.01
        }
        if model_id is None or len(model_id) == 0:
            model_id = "meta-llama/llama-3-70b-instruct"

        api_key = config["BAM_KEY"]
        api_base = config["API_BASE"]

        return BAMLLM(
            model_id=model_id,
            api_key=api_key,
            api_base=api_base,
            llm_params=TextGenerationParameters(**parameters),
            callbacks=[loggingCallbackHandler],
        )
    elif inference == "watsonx":
        from langchain_ibm import WatsonxLLM
        from genai.schema import DecodingMethod

        parameters = {
            "decoding_method": DecodingMethod.GREEDY,
            "max_new_tokens": 1024,
            "min_new_tokens": 1,
            "temperature": 0,
            "top_k": 50,
            "top_p": 1,
        }
        if model_id is None or len(model_id) == 0:
            # see supported models at https://dataplatform.cloud.ibm.com/samples?context=wx
            model_id = "meta-llama/llama-3-70b-instruct"
            # model_id = "meta-llama/llama-3-2-3b-instruct"
            # model_id = "meta-llama/llama-3-405b-instruct"

        return WatsonxLLM(
            model_id=model_id,
            apikey=config["WATSONX_APIKEY"],
            url=config["WATSONX_URL"],
            project_id=config["WATSON_PROJECT_ID"],
            params=parameters,
            callbacks=[loggingCallbackHandler],

        )
    else:
        raise ValueError(
            f"Inference type {inference} is wrong, supported values are [ollama, bamllm, watsonx]"
        )


def getChatLLM(
    inference: str, model_id: str = None, config: dict = None, params: Optional[Dict[str, Any]] = None
) -> BaseChatModel:
    loggingCallbackHandler = LoggingCallbackHandler()
    
    if config is None:
        config = dotenv_values(CONFIG_LOCATION)

    if inference == "ollama":
        from langchain_ollama import ChatOllama

        if model_id is None or len(model_id) == 0:
            model_id = "llama3.1:70b"
        return ChatOllama(model=model_id, temperature=0, callbacks=[loggingCallbackHandler])

    # elif inference == "bamllm": TODO
    #
    elif inference == "watsonx":
        from langchain_ibm import ChatWatsonx
        from genai.schema import DecodingMethod

        parameters = {
            "decoding_method": DecodingMethod.GREEDY,
            "max_new_tokens": 1024,
            "min_new_tokens": 1,
            "temperature": 0,
            "top_k": 50,
            "top_p": 1,
        }
        if model_id is None or len(model_id) == 0:
            # see supported models at https://dataplatform.cloud.ibm.com/samples?context=wx
            model_id = "meta-llama/llama-3-70b-instruct"
            # model_id = "meta-llama/llama-3-2-3b-instruct"
            # model_id = "meta-llama/llama-3-405b-instruct"

        return ChatWatsonx(
            model_id=model_id,
            apikey=config["WATSONX_APIKEY"],
            url=config["WATSONX_URL"],
            project_id=config["WATSON_PROJECT_ID"],
            params=parameters,
            callbacks=[loggingCallbackHandler],
        )
    elif inference == "rits":
        """Returns a configured LLM instance."""
        model_name = MODEL_PATH_PARAMS.get(model_id)
        if not model_name:
            raise ValueError(f"Model ID {model_id} not found in MODEL_PATH_PARAMS")
        loggingCallbackHandler = LoggingCallbackHandler()
        return ChatOpenAI(
            model=model_id,
            base_url=BASE_URL.format(model_name=model_name),
            api_key=config["RITS_API_KEY"],
            default_headers={"RITS_API_KEY": config["RITS_API_KEY"]},
            callbacks=[loggingCallbackHandler],
            temperature=0,
            **(params or {})
        )
    else:
        raise ValueError(
            f"Inference type {inference} is wrong, supported values are [ollama, watsonx]"
        )

BASE_URL = "https://inference-3scale-apicast-production.apps.rits.fmaas.res.ibm.com/{model_name}/v1"

MODEL_PATH_PARAMS = {
    "codellama/CodeLlama-34b-Instruct-hf": "codellama-34b-instruct-hf",
    "deepseek-ai/DeepSeek-V2.5": "deepseek-v2.5",
    "deepseek-ai/deepseek-coder-33b-instruct": "deepseek-coder-33b-instruct",
    "ibm-fms/avengers-jamba-9b": "avengers-jamba-9b",
    "ibm-granite/granite-13b-chat-v2": "granite-13b-chat-v2",
    "ibm-granite/granite-13b-instruct-v2": "granite-13b-instruct-v2",
    "ibm-granite/granite-20b-code-base-content-linking": "granite-20b-cbcl",
    "ibm-granite/granite-20b-code-base-sql-gen": "granite-20b-cbsql",
    "ibm-granite/granite-20b-code-instruct-8k": "granite-20b-code-instruct-8k",
    "ibm-granite/granite-20b-code-instruct-r1.1": "granite-20b-ci-r1-1",
    "ibm-granite/granite-20b-code-instruct-unified-api": "granite-20b-code-instruct-uapi",
    "ibm-granite/granite-3.0-8b-instruct": "granite-3-0-8b-instruct",
    "ibm-granite/granite-3.1-8b-instruct": "granite-3-1-8b-instruct",
    "ibm-granite/granite-3-1-8b-tooltest": "granite-3-1-8b-tooltest",
    "ibm-granite/granite-34b-code-instruct-8k": "granite-34b-code-instruct-8k",
    "ibm-granite/granite-8b-code-instruct-128k": "granite-8b-code-instruct-128k",
    "ibm-granite/granite-8b-code-instruct-4k": "granite-8b-code-instruct-4k",
    "ibm-granite/granite-8b-instruct-preview-4k": "granite-8b-instruct-preview-4k",
    "ibm-granite/granite-8b-japanese-instruct": "granite-8b-japanese-instruct",
    "ibm/granite-20b-code-8k-ansible": "granite-20b-code-8k-ansible",
    "ibm/granite-20b-code-instruct-lh": "granite-20b-code-instruct-lh",
    "ibm/granite-20b-schema-sqlinstruct-granite-fine-vs": "granite-20b-cbsl",
    "ibm/granite-34b-content-linking": "granite-34b-content-linking",
    "ibm/granite-34b-question-gen": "granite-34b-question-gen",
    "ibm/granite-34b-schema-linking": "granite-34b-schema-linking",
    "ibm/granite-34b-sql-gen": "granite-34b-sql-gen",
    "ibm/granite-7b-lab": "granite-7b-lab",
    "meta-llama/Llama-3.1-8B-Instruct": "llama-3-1-8b-instruct",
    "meta-llama/Llama-3.2-11B-Vision-Instruct": "llama-3-2-11b-vision-instruct",
    "meta-llama/Llama-3.2-90B-Vision-Instruct": "llama-3-2-90b-instruct",
    "meta-llama/llama-3-1-405b-instruct-fp8": "llama-3-1-405b-instruct-fp8",
    "meta-llama/llama-3-1-70b-instruct": "llama-3-1-70b-instruct",
    "meta-llama/llama-3-3-70b-instruct": "llama-3-3-70b-instruct",
    "mistralai/mistral-large-instruct-2407": "mistral-large-instruct-2407",
    "mistralai/mixtral-8x22B-instruct-v0.1": "mixtral-8x22b-instruct-v01",
    "mistralai/mixtral-8x7B-instruct-v0.1": "mixtral-8x7b-instruct-v01",
    "Qwen/Qwen2.5-72B-Instruct": "qwen2-5-72b-instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen2-5-coder-32b-instruct",
    "Qwen/Qwen2-VL-72B-Instruct": "qwen2-vl-72b-instruct",
}
