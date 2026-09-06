from deep_translator import GoogleTranslator, MyMemoryTranslator

# --- English treatment tips (our source of truth) ---
TREATMENT_TIPS = {
    "Apple___Apple_scab": "Remove fallen leaves and prune for airflow. Apply a fungicide like captan or myclobutanil starting at bud break.",
    "Apple___Black_rot": "Prune out dead or cankered wood and remove mummified fruit. Apply fungicide sprays through the growing season.",
    "Apple___Cedar_apple_rust": "Remove nearby juniper/cedar trees if possible. Apply fungicide from pink bud stage; consider resistant varieties.",
    "Apple___healthy": "No treatment needed — plant looks healthy.",
    "Blueberry___healthy": "No treatment needed — plant looks healthy.",
    "Cherry_(including_sour)___Powdery_mildew": "Apply a sulfur-based fungicide. Prune for better airflow and avoid excess nitrogen fertilizer.",
    "Cherry_(including_sour)___healthy": "No treatment needed — plant looks healthy.",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Rotate crops and use resistant hybrids. Apply a fungicide if the infection is severe.",
    "Corn_(maize)___Common_rust_": "Plant rust-resistant hybrids. Apply fungicide only if infection appears early and severe.",
    "Corn_(maize)___Northern_Leaf_Blight": "Rotate crops and till crop residue. Use resistant hybrids; fungicide if needed.",
    "Corn_(maize)___healthy": "No treatment needed — plant looks healthy.",
    "Grape___Black_rot": "Remove mummified berries and infected leaves. Apply fungicide (e.g. mancozeb) starting early season.",
    "Grape___Esca_(Black_Measles)": "Prune out and destroy infected wood. Avoid pruning during wet weather — no full cure exists, focus on prevention.",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Remove infected leaves and apply a copper-based fungicide. Improve canopy airflow.",
    "Grape___healthy": "No treatment needed — plant looks healthy.",
    "Orange___Haunglongbing_(Citrus_greening)": "No cure exists. Remove and destroy infected trees to prevent spread, and control the psyllid insect that spreads it.",
    "Peach___Bacterial_spot": "Apply a copper-based bactericide. Avoid overhead irrigation; consider resistant varieties.",
    "Peach___healthy": "No treatment needed — plant looks healthy.",
    "Pepper,_bell___Bacterial_spot": "Apply a copper-based spray. Avoid working with wet plants and rotate crops each season.",
    "Pepper,_bell___healthy": "No treatment needed — plant looks healthy.",
    "Potato___Early_blight": "Apply a fungicide (chlorothalonil or mancozeb). Rotate crops and remove infected plant debris.",
    "Potato___Late_blight": "Apply fungicide promptly — this spreads fast. Destroy infected plants and avoid overhead watering.",
    "Potato___healthy": "No treatment needed — plant looks healthy.",
    "Raspberry___healthy": "No treatment needed — plant looks healthy.",
    "Soybean___healthy": "No treatment needed — plant looks healthy.",
    "Squash___Powdery_mildew": "Apply a sulfur-based fungicide. Improve air circulation and avoid overhead watering.",
    "Strawberry___Leaf_scorch": "Remove infected leaves after harvest. Apply fungicide and avoid overhead irrigation.",
    "Strawberry___healthy": "No treatment needed — plant looks healthy.",
    "Tomato___Bacterial_spot": "Apply a copper-based bactericide. Avoid overhead watering and rotate crops.",
    "Tomato___Early_blight": "Remove lower infected leaves. Apply fungicide (chlorothalonil) and mulch to prevent soil splash.",
    "Tomato___Late_blight": "Apply fungicide immediately — this spreads fast. Remove and destroy infected plants.",
    "Tomato___Leaf_Mold": "Improve ventilation and reduce humidity. Apply fungicide and avoid wetting the foliage.",
    "Tomato___Septoria_leaf_spot": "Remove infected leaves. Apply fungicide, mulch, and avoid overhead watering.",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Use insecticidal soap or a miticide. Increase humidity and consider natural predators like ladybugs.",
    "Tomato___Target_Spot": "Apply fungicide and remove infected foliage. Improve air circulation around plants.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "No cure exists. Remove infected plants and control the whitefly insect that spreads this virus.",
    "Tomato___Tomato_mosaic_virus": "No cure exists. Remove and destroy infected plants, disinfect tools, and control aphids.",
    "Tomato___healthy": "No treatment needed — plant looks healthy.",
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

TREATMENT_TIPS = {
    "Apple___Apple_scab": "Remove fallen leaves and prune for airflow. Apply a fungicide like captan or myclobutanil starting at bud break.",
    "Apple___Black_rot": "Prune out dead or cankered wood and remove mummified fruit. Apply fungicide sprays through the growing season.",
    "Apple___Cedar_apple_rust": "Remove nearby juniper/cedar trees if possible. Apply fungicide from pink bud stage; consider resistant varieties.",
    "Apple___healthy": "No treatment needed — plant looks healthy.",
    "Blueberry___healthy": "No treatment needed — plant looks healthy.",
    "Cherry_(including_sour)___Powdery_mildew": "Apply a sulfur-based fungicide. Prune for better airflow and avoid excess nitrogen fertilizer.",
    "Cherry_(including_sour)___healthy": "No treatment needed — plant looks healthy.",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Rotate crops and use resistant hybrids. Apply a fungicide if the infection is severe.",
    "Corn_(maize)___Common_rust_": "Plant rust-resistant hybrids. Apply fungicide only if infection appears early and severe.",
    "Corn_(maize)___Northern_Leaf_Blight": "Rotate crops and till crop residue. Use resistant hybrids; fungicide if needed.",
    "Corn_(maize)___healthy": "No treatment needed — plant looks healthy.",
    "Grape___Black_rot": "Remove mummified berries and infected leaves. Apply fungicide (e.g. mancozeb) starting early season.",
    "Grape___Esca_(Black_Measles)": "Prune out and destroy infected wood. Avoid pruning during wet weather — no full cure exists, focus on prevention.",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Remove infected leaves and apply a copper-based fungicide. Improve canopy airflow.",
    "Grape___healthy": "No treatment needed — plant looks healthy.",
    "Orange___Haunglongbing_(Citrus_greening)": "No cure exists. Remove and destroy infected trees to prevent spread, and control the psyllid insect that spreads it.",
    "Peach___Bacterial_spot": "Apply a copper-based bactericide. Avoid overhead irrigation; consider resistant varieties.",
    "Peach___healthy": "No treatment needed — plant looks healthy.",
    "Pepper,_bell___Bacterial_spot": "Apply a copper-based spray. Avoid working with wet plants and rotate crops each season.",
    "Pepper,_bell___healthy": "No treatment needed — plant looks healthy.",
    "Potato___Early_blight": "Apply a fungicide (chlorothalonil or mancozeb). Rotate crops and remove infected plant debris.",
    "Potato___Late_blight": "Apply fungicide promptly — this spreads fast. Destroy infected plants and avoid overhead watering.",
    "Potato___healthy": "No treatment needed — plant looks healthy.",
    "Raspberry___healthy": "No treatment needed — plant looks healthy.",
    "Soybean___healthy": "No treatment needed — plant looks healthy.",
    "Squash___Powdery_mildew": "Apply a sulfur-based fungicide. Improve air circulation and avoid overhead watering.",
    "Strawberry___Leaf_scorch": "Remove infected leaves after harvest. Apply fungicide and avoid overhead irrigation.",
    "Strawberry___healthy": "No treatment needed — plant looks healthy.",
    "Tomato___Bacterial_spot": "Apply a copper-based bactericide. Avoid overhead watering and rotate crops.",
    "Tomato___Early_blight": "Remove lower infected leaves. Apply fungicide (chlorothalonil) and mulch to prevent soil splash.",
    "Tomato___Late_blight": "Apply fungicide immediately — this spreads fast. Remove and destroy infected plants.",
    "Tomato___Leaf_Mold": "Improve ventilation and reduce humidity. Apply fungicide and avoid wetting the foliage.",
    "Tomato___Septoria_leaf_spot": "Remove infected leaves. Apply fungicide, mulch, and avoid overhead watering.",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Use insecticidal soap or a miticide. Increase humidity and consider natural predators like ladybugs.",
    "Tomato___Target_Spot": "Apply fungicide and remove infected foliage. Improve air circulation around plants.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "No cure exists. Remove infected plants and control the whitefly insect that spreads this virus.",
    "Tomato___Tomato_mosaic_virus": "No cure exists. Remove and destroy infected plants, disinfect tools, and control aphids.",
    "Tomato___healthy": "No treatment needed — plant looks healthy.",
}

def get_treatment_english(raw_label):
    return TREATMENT_TIPS.get(
        raw_label,
        "Remove affected leaves, avoid overhead watering, and consult a local agricultural extension officer for a targeted fungicide/pesticide recommendation."
    )
def translate_text(text, target_lang_code):
    if target_lang_code == "en":
        return text

    clean_text = text.replace("—", "-").replace("–", "-")

    try:
        return GoogleTranslator(source="en", target=target_lang_code).translate(clean_text)
    except Exception as e:
        print(f"GoogleTranslator failed: {e}. Trying backup translator...")
        try:
            locale_map = {"hi": "en-hi", "mr": "en-mr"}
            return MyMemoryTranslator(source="en-GB", target=locale_map.get(target_lang_code, target_lang_code)).translate(clean_text)
        except Exception as e2:
            print(f"Backup translator also failed: {e2}. Falling back to English.")
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