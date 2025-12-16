import json_repair
from langchain_community.adapters.openai import convert_openai_messages
from langchain_core.utils.json import parse_json_markdown
from loguru import logger

from gpt_researcher.config.config import Config
from gpt_researcher.utils.llm import create_chat_completion


def parse_model_string(model_str: str, fallback_provider: str = None) -> tuple[str, str]:
    """
    Parse a model string that may be in 'provider:model' or just 'model' format.
    
    Args:
        model_str: Model string like "xai:grok-3-mini" or just "grok-3-mini"
        fallback_provider: Provider to use if not specified in model_str
        
    Returns:
        Tuple of (provider, model_name)
    """
    if ":" in model_str:
        provider, model_name = model_str.split(":", 1)
        return provider, model_name
    else:
        # No provider specified, use fallback
        return fallback_provider, model_str


async def call_model(
    prompt: list,
    model: str,
    response_format: str | None = None,
):
    """
    Call an LLM with the given prompt.
    
    Args:
        prompt: List of message dicts with 'role' and 'content'
        model: Model specification - either "provider:model" (e.g., "xai:grok-3-mini")
               or just "model" (will use SMART_LLM provider from env)
        response_format: Optional "json" to parse response as JSON
        
    Returns:
        The model response (string or parsed JSON dict)
    """
    cfg = Config()
    lc_messages = convert_openai_messages(prompt)
    
    # Parse model string - supports both "provider:model" and just "model"
    llm_provider, model_name = parse_model_string(
        model, 
        fallback_provider=cfg.smart_llm_provider
    )

    try:
        response = await create_chat_completion(
            model=model_name,
            messages=lc_messages,
            temperature=0,
            llm_provider=llm_provider,
            llm_kwargs=cfg.llm_kwargs,
            # cost_callback=cost_callback,
        )

        if response_format == "json":
            return parse_json_markdown(response, parser=json_repair.loads)

        return response

    except Exception as e:
        print("⚠️ Error in calling model")
        logger.error(f"Error in calling model: {e}")
