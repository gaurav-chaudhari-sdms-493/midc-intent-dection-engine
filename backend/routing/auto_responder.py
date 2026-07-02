"""
Generates automated, templated responses for simple, high-confidence inquiries.
"""
from typing import Dict, Any

# A dictionary of response templates organized by language and then by intent.
# This structure allows for easy addition of new languages or intents.
RESPONSE_TEMPLATES = {
    "en": {
        "general_faq": (
            "Thank you for your inquiry. For general information, you can visit our "
            "comprehensive FAQ page at https://www.midcindia.org/faq or call our "
            "toll-free number at 1-800-123-4567."
        ),
        "application_status": (
            "Thank you for your inquiry regarding your application. You can check the "
            "latest status of any application by entering your reference number on our "
            "official portal: https://www.midcindia.org/portal/status."
        ),
    },
    "hi": {
        "general_faq": (
            "आपकी पूछताछ के लिए धन्यवाद। सामान्य जानकारी के लिए, आप हमारे विस्तृत FAQ पेज "
            "https://www.midcindia.org/faq पर जा सकते हैं या हमारे टोल-फ्री नंबर "
            "1-800-123-4567 पर कॉल कर सकते हैं।"
        ),
        "application_status": (
            "आपके आवेदन के संबंध में आपकी पूछताछ के लिए धन्यवाद। आप हमारे आधिकारिक पोर्टल "
            "https://www.midcindia.org/portal/status पर अपना संदर्भ नंबर दर्ज करके "
            "किसी भी आवेदन की नवीनतम स्थिति देख सकते हैं।"
        ),
    },
    "mr": {
        "general_faq": (
            "तुमच्या चौकशीबद्दल धन्यवाद. सामान्य माहितीसाठी, तुम्ही आमच्या सर्वसमावेशक FAQ पेज "
            "https://www.midcindia.org/faq ला भेट देऊ शकता किंवा आमच्या टोल-फ्री क्रमांक "
            "1-800-123-4567 वर कॉल करू शकता."
        ),
        "application_status": (
            "तुमच्या अर्जाबद्दल चौकशी केल्याबद्दल धन्यवाद. तुम्ही आमच्या अधिकृत पोर्टल "
            "https://www.midcindia.org/portal/status वर तुमचा संदर्भ क्रमांक टाकून "
            "कोणत्याही अर्जाची नवीनतम स्थिती तपासू शकता."
        ),
    },
}

# A generic fallback response in English if a specific template is not found.
FALLBACK_RESPONSE = (
    "Thank you for contacting MIDC. Your inquiry has been received and will be "
    "reviewed by our team. You will receive a response shortly."
)

def generate_auto_response(classification: Dict[str, Any], lang: str) -> str:
    """
    Generates a language-specific, templated response based on classification.

    This function selects a response template based on the inquiry's language
    and primary intent. If a specific template for the given language or intent
    is not found, it gracefully falls back to a generic English acknowledgement.

    Args:
        classification: The classification result dictionary, containing the
                        'primary_intent'.
        lang: The language of the inquiry ('en', 'hi', or 'mr').

    Returns:
        A formatted string containing the automated response.
    """
    primary_intent = classification.get("primary_intent")

    # Safely get the template:
    # 1. Get the dictionary for the given language. If not found, return an empty dict.
    # 2. Get the specific intent template from that dictionary.
    # 3. If the intent is not found, use the FALLBACK_RESPONSE.
    response_template = RESPONSE_TEMPLATES.get(lang, {}).get(primary_intent, FALLBACK_RESPONSE)

    return response_template

if __name__ == '__main__':
    # --- DEMONSTRATION ---
    print("--- Auto Responder Demonstration ---")

    # Case 1: English, General FAQ
    classif_1 = {"primary_intent": "general_faq"}
    print(f"\nCase 1 (en, general_faq):\n  -> {generate_auto_response(classif_1, 'en')}")

    # Case 2: Hindi, Application Status
    classif_2 = {"primary_intent": "application_status"}
    print(f"\nCase 2 (hi, application_status):\n  -> {generate_auto_response(classif_2, 'hi')}")

    # Case 3: Marathi, General FAQ
    classif_3 = {"primary_intent": "general_faq"}
    print(f"\nCase 3 (mr, general_faq):\n  -> {generate_auto_response(classif_3, 'mr')}")

    # Case 4: Fallback - Unsupported Intent (e.g., 'land_allotment')
    classif_4 = {"primary_intent": "land_allotment"}
    print(f"\nCase 4 (Fallback - Unsupported Intent):\n  -> {generate_auto_response(classif_4, 'en')}")

    # Case 5: Fallback - Unsupported Language (e.g., 'fr')
    classif_5 = {"primary_intent": "general_faq"}
    print(f"\nCase 5 (Fallback - Unsupported Language):\n  -> {generate_auto_response(classif_5, 'fr')}")
