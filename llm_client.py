import re

import openai
from google import genai
from google.genai import types

from prompts import TEMPERATURE


class LLMError(Exception):
    def __init__(self, provider: str, message: str):
        self.provider = provider
        self.message = message
        super().__init__(f"[{provider}] {message}")


def _clean_code_output(text: str) -> str:
    """Strip markdown code fences from LLM output."""
    cleaned = re.sub(r"^```(?:sql|python|py)?\s*\n?", "", text.strip())
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)
    return cleaned.strip()


def _generate_openai(messages: list[dict], api_key: str) -> str:
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=messages,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        raise LLMError("OpenAI", "Invalid API key. Check your OpenAI API key.")
    except openai.RateLimitError:
        raise LLMError("OpenAI", "Rate limit exceeded. Please wait and try again.")
    except openai.APIConnectionError:
        raise LLMError("OpenAI", "Network error. Could not reach the OpenAI API.")
    except openai.APIError as e:
        raise LLMError("OpenAI", f"API error: {e}")


def _generate_gemini(messages: list[dict], api_key: str) -> str:
    try:
        client = genai.Client(api_key=api_key)

        # Flatten OpenAI messages format into a single prompt for Gemini
        parts = []
        for msg in messages:
            if msg["role"] == "system":
                parts.append(f"Instructions: {msg['content']}")
            else:
                parts.append(msg["content"])
        prompt = "\n\n".join(parts)

        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=TEMPERATURE),
        )
        return response.text
    except Exception as e:
        err = str(e).lower()
        if "api key" in err or "authentication" in err or "403" in err:
            raise LLMError("Gemini", "Invalid API key. Check your Google API key.")
        if "rate limit" in err or "429" in err or "quota" in err:
            raise LLMError("Gemini", "Rate limit exceeded. Please wait and try again.")
        raise LLMError("Gemini", f"API error: {e}")


def generate(model_name: str, messages: list[dict], api_keys: dict) -> str:
    """Generate a response from the specified model.

    Args:
        model_name: "gpt-5.4" or "gemini-3.1-pro-preview"
        messages: OpenAI-format messages list
        api_keys: dict with "openai" and/or "google" keys

    Returns:
        Cleaned code output string.
    """
    if model_name == "gpt-5.4":
        key = api_keys.get("openai", "")
        if not key:
            raise LLMError("OpenAI", "API key not provided.")
        raw = _generate_openai(messages, key)
    elif model_name == "gemini-3.1-pro-preview":
        key = api_keys.get("google", "")
        if not key:
            raise LLMError("Gemini", "API key not provided.")
        raw = _generate_gemini(messages, key)
    else:
        raise LLMError("Unknown", f"Unsupported model: {model_name}")

    return _clean_code_output(raw)
