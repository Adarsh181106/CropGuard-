from deep_translator import GoogleTranslator

# --- English treatment tips (our source of truth) ---
TREATMENT_TIPS = {
    "healthy": "No treatment needed — plant looks healthy.",
    "default": "Remove affected leaves, avoid overhead watering, and consult a local agricultural extension officer for a targeted fungicide/pesticide recommendation.",
}

# Map our internal language codes to deep-translator's expected codes
LANGUAGE_CODES = {
    "en": "en",
    "hi": "hi",  # Hindi
    "mr": "mr",  # Marathi
}

def clean_label(raw_label):
    """
    Turns 'Tomato___Late_blight' into 'Tomato - Late blight'
    """
    parts = raw_label.split("___")
    crop = parts[0].replace("_", " ")
    disease = parts[1].replace("_", " ") if len(parts) > 1 else ""
    if disease.lower() == "healthy":
        return f"{crop} — Healthy"
    return f"{crop} — {disease}"

def get_treatment_english(raw_label):
    if "healthy" in raw_label.lower():
        return TREATMENT_TIPS["healthy"]
    return TREATMENT_TIPS["default"]

def translate_text(text, target_lang_code):
    """
    Translates English text into the target language.
    Falls back to English text if translation fails (e.g. no internet)
    so the app never crashes just because translation didn't work.
    """
    if target_lang_code == "en":
        return text
    try:
        translated = GoogleTranslator(source="en", target=target_lang_code).translate(text)
        return translated
    except Exception as e:
        print(f"Translation failed, falling back to English: {e}")
        return text

def get_localized_result(raw_label, target_lang_code):
    """
    Main function app.py will call.
    Returns (disease_name_localized, treatment_localized)
    """
    disease_name_en = clean_label(raw_label)
    treatment_en = get_treatment_english(raw_label)

    disease_name = translate_text(disease_name_en, target_lang_code)
    treatment = translate_text(treatment_en, target_lang_code)

    return disease_name, treatment