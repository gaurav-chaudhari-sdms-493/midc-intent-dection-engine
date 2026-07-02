"""
Client for interacting with the Anthropic LLM API.

This module provides a function to call a specified Anthropic model,
handle response parsing, and implement a retry mechanism for invalid JSON.
"""
import os
import json
import re
import logging
from typing import Dict, Any

import anthropic
from anthropic import AnthropicError

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Custom Exception ---
class LLMResponseParseError(Exception):
    """Raised when the LLM response cannot be parsed into a dictionary, even after a retry."""
    def __init__(self, message: str, last_attempt_text: str = ""):
        self.message = message
        self.last_attempt_text = last_attempt_text
        super().__init__(f"{message}\n--- Last Attempt Text ---\n{last_attempt_text}")

def _strip_markdown_fences(text: str) -> str:
    """
    Removes markdown code fences (e.g., ```json ... ```) from a string.
    If no fences are found, it returns the original string, stripped of whitespace.
    """
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()

def call_llm(prompt: str, model: str = "claude-3-haiku-20240307") -> Dict[str, Any]:
    """
    Calls the specified Anthropic model with a prompt and returns a parsed JSON dictionary.

    It reads the API key from the `LLM_API_KEY` environment variable. If the initial
    response from the model is not valid JSON, it makes one retry attempt, asking
    the model to correct its output.

    Args:
        prompt: The complete prompt string to send to the model.
        model: The name of the Anthropic model to use (e.g., 'claude-3-sonnet-20240229').

    Returns:
        A dictionary parsed from the model's JSON response.

    Raises:
        ValueError: If the LLM_API_KEY environment variable is not set.
        LLMResponseParseError: If the model's response is not valid JSON after one retry.
        anthropic.AnthropicError: For other API-related errors.
    """
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        # First attempt
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.content[0].text
        cleaned_text = _strip_markdown_fences(response_text)
        data = json.loads(cleaned_text)
        
        logging.info(
            f"Model: {model} | Input Tokens: {response.usage.input_tokens}, "
            f"Output Tokens: {response.usage.output_tokens}"
        )
        return data

    except json.JSONDecodeError:
        logging.warning("Initial LLM response was not valid JSON. Retrying once.")
        
        # Construct a retry prompt asking the model to fix its output
        retry_prompt = (
            "Your previous response was not valid JSON. Please correct your mistake and "
            "return ONLY the valid JSON object, without any surrounding text or markdown fences.\n\n"
            f"The original request was:\n---\n{prompt}\n---\n\n"
            f"Your invalid response was:\n---\n{response_text}"
        )

        try:
            # Second and final attempt
            retry_response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": retry_prompt}]
            )
            retry_text = retry_response.content[0].text
            cleaned_retry_text = _strip_markdown_fences(retry_text)
            data = json.loads(cleaned_retry_text)

            logging.info(
                f"Model (Retry): {model} | Input Tokens: {retry_response.usage.input_tokens}, "
                f"Output Tokens: {retry_response.usage.output_tokens}"
            )
            return data
            
        except (json.JSONDecodeError, AnthropicError) as e:
            # If the second attempt also fails, raise the custom exception
            raise LLMResponseParseError(
                f"Failed to parse LLM response as JSON after one retry. Final error: {e}",
                last_attempt_text=retry_text if 'retry_text' in locals() else ""
            ) from e
            
    except AnthropicError as e:
        logging.error(f"An unrecoverable Anthropic API error occurred: {e}")
        raise e
