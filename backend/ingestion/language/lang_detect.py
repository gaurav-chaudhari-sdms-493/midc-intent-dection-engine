import fasttext
import os
from typing import Literal

# --- IMPORTANT ---
# To use this module, you need to:
# 1. Install the fastText library: pip install fasttext
# 2. Download the fastText language identification model (lid.176.bin) from:
#    https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
# 3. Create a 'models' directory inside backend/ingestion/language/
#    (e.g., /home/stark/PycharmProjects/midc-intent-dection-engine/backend/ingestion/language/models/)
# 4. Place the downloaded 'lid.176.bin' file into this 'models' directory.
# This 'lid.176.bin' file should be added to your .gitignore.

# Load the model once at module level for performance
_model_path = os.path.join(os.path.dirname(__file__), "models", "lid.176.bin")
_model = None
try:
    _model = fasttext.load_model(_model_path)
except ValueError:
    print(f"Warning: fastText model not found at {_model_path}. Language detection will always return 'en'. "
          "Please ensure the model is downloaded and placed correctly.")
except Exception as e:
    print(f"Error loading fastText model: {e}. Language detection will always return 'en'.")

# Define a confidence threshold for language detection
_CONFIDENCE_THRESHOLD = 0.5

def detect_language(text: str) -> Literal["en", "hi", "mr"]:
    """
    Detects the language of the given text using fastText's lid.176 model.

    Args:
        text: The input string whose language needs to be detected.

    Returns:
        One of "en", "hi", or "mr". If the model's confidence for the top
        prediction is below the defined threshold (0.5), or if detection
        fails/throws an error, it falls back to "en". Empty or whitespace-only
        input also defaults to "en".
    """
    if not _model:
        return "en" # Fallback if model failed to load

    if not text or not text.strip():
        return "en" # Default to English for empty or whitespace-only text

    try:
        # Predict the language, k=1 means top 1 prediction
        predictions = _model.predict(text, k=1)
        label = predictions[0][0] # e.g., ['__label__en']
        confidence = predictions[1][0] # e.g., [0.99999]

        # Check confidence threshold
        if confidence < _CONFIDENCE_THRESHOLD:
            return "en" # Fallback due to low confidence

        # Map fastText labels to desired output format
        if label == '__label__en':
            return "en"
        elif label == '__label__hi':
            return "hi"
        elif label == '__label__mr':
            return "mr"
        else:
            # If detected language is not one of the target languages, fall back
            return "en"
    except Exception as e:
        print(f"Error during fastText language detection: {e}. Falling back to 'en'.")
        return "en"

if __name__ == "__main__":
    print("--- Language Detection Examples ---")

    # Test cases
    text_en = "This is a sample English text."
    text_hi = "यह एक नमूना हिंदी पाठ है।"
    text_mr = "हे एक नमुना मराठी मजकूर आहे."
    text_low_conf = "asdfghjkl" # Likely low confidence
    text_empty = ""
    text_unknown = "Bonjour le monde!" # Should fall back to 'en'

    print(f"'{text_en}' -> {detect_language(text_en)}")
    print(f"'{text_hi}' -> {detect_language(text_hi)}")
    print(f"'{text_mr}' -> {detect_language(text_mr)}")
    print(f"'{text_low_conf}' -> {detect_language(text_low_conf)}")
    print(f"'{text_empty}' -> {detect_language(text_empty)}")
    print(f"'{text_unknown}' -> {detect_language(text_unknown)}")

    print("\nNote: For accurate results, ensure 'lid.176.bin' is downloaded and placed correctly.")
    print("If you see 'Warning: fastText model not found...', language detection will default to 'en'.")
