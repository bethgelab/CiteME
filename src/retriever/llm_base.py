import os
from langchain_openai import ChatOpenAI

from langchain_anthropic import ChatAnthropic
from langchain_together import ChatTogether

DEFAULT_TEMPERATURE = 0.95

def get_model_by_name(model_name: str, temperature: float = DEFAULT_TEMPERATURE):
    if model_name.startswith("gpt-"):
        return ChatOpenAI(model=model_name, temperature=temperature)
    if model_name.startswith("claude-"):
        return ChatAnthropic(
            temperature=temperature,
            model_name="claude-3-opus-20240229",
            timeout=60*10,
            api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        )
    if "llama" in model_name.lower() or "phi" in model_name.lower() or "mistral" in model_name.lower():
        return ChatTogether(
            temperature=temperature,
            model=model_name,
        )
    raise ValueError(f"Model {model_name} not found")
