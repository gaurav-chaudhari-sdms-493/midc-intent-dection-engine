"""
Routes an inquiry through a tiered classification system using different LLMs.

This module exposes the primary function `classify_inquiry` which first uses a
fast, cheap model and escalates to a more powerful model if confidence is low.
"""
import os
import pathlib
import logging
import json
import argparse
from typing import Dict, Any

# Assumes llm_client.py is in the same directory
from .llm_client import call_llm, LLMResponseParseError

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default model names can be overridden by environment variables
MINI_MODEL_DEFAULT = "claude-3-haiku-20240307"
FRONTIER_MODEL_DEFAULT = "claude-3-sonnet-20240229"
CONFIDENCE_THRESHOLD = 0.6

# Base path for prompt templates
PROMPT_BASE_PATH = pathlib.Path(__file__).parent / "prompts"


def _get_prompt_template(lang: str) -> str:
    """
    Loads the appropriate prompt template for the given language.

    Args:
        lang: The language code ('en', 'hi', 'mr').

    Returns:
        The content of the prompt template as a string.
    """
    prompt_file = PROMPT_BASE_PATH / f"intent_classification_{lang}.txt"
    
    # Fallback to English if the specific language template doesn't exist
    if not prompt_file.exists():
        logging.warning(f"Prompt file for language '{lang}' not found. Falling back to 'en'.")
        prompt_file = PROMPT_BASE_PATH / "intent_classification_en.txt"
        if not prompt_file.exists():
            raise FileNotFoundError("Default English prompt file 'intent_classification_en.txt' is missing.")
            
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()


def classify_inquiry(text: str, lang: str) -> Dict[str, Any]:
    """
    Classifies an inquiry using a tiered model routing strategy.

    First, it uses a cheaper model. If the confidence score is below a set
    threshold, it escalates to a more powerful model for re-classification.

    Args:
        text: The inquiry text to classify.
        lang: The language of the inquiry ('en', 'hi', 'mr').

    Returns:
        A dictionary containing the classification result, including an 'escalated' flag.
    """
    # 1. Get model names from environment or use defaults
    mini_model = os.getenv("MINI_MODEL", MINI_MODEL_DEFAULT)
    frontier_model = os.getenv("FRONTIER_MODEL", FRONTIER_MODEL_DEFAULT)

    # 2. Prepare the prompt
    prompt_template = _get_prompt_template(lang)
    prompt = prompt_template.format(inquiry_text=text)

    # 3. Initial classification with the cheap model
    logging.info(f"Attempting classification with mini model: {mini_model}")
    result = call_llm(prompt, model=mini_model)
    result["escalated"] = False

    # 4. Escalate if confidence is low
    if result.get("confidence", 1.0) < CONFIDENCE_THRESHOLD:
        logging.warning(
            f"Confidence ({result.get('confidence')}) is below threshold of {CONFIDENCE_THRESHOLD}. "
            f"Escalating to frontier model: {frontier_model}"
        )
        
        # Re-run with the stronger model
        escalated_result = call_llm(prompt, model=frontier_model)
        escalated_result["escalated"] = True
        return escalated_result

    return result


if __name__ == '__main__':
    # This block allows for command-line testing of the module.
    # Example usage:
    # python -m backend.classification.model_router "I want to set up a new EV plant" --lang en
    
    # For local dev, load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass # python-dotenv is not a hard requirement

    parser = argparse.ArgumentParser(description="Classify an investor inquiry.")
    parser.add_argument("text", type=str, help="The inquiry text to classify.")
    parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "mr"], help="Language of the inquiry.")
    args = parser.parse_args()

    if not os.getenv("LLM_API_KEY"):
        logging.error("FATAL: LLM_API_KEY environment variable is not set. Cannot proceed.")
    else:
        try:
            print(f"Classifying text (lang={args.lang}): '{args.text}'")
            print("-" * 20)
            classification = classify_inquiry(args.text, args.lang)
            print("\n--- Classification Result ---")
            print(json.dumps(classification, indent=2))
        except (LLMResponseParseError, FileNotFoundError, ValueError) as e:
            logging.error(f"Pipeline failed: {e}")
