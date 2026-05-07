import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

st.set_page_config(
    page_title="Food Ingredient Scanner",
    layout="centered"
)

LANG = {
    "bg": {
        "title": "Скенер за хранителни съставки",
        "upload": "Качи снимка",
        "camera": "Направи снимка",
        "ocr_text": "Разпознат текст",
        "dangerous": "Открити потенциално вредни съставки",
        "safe": "Не са открити вредни съставки",
        "processing": "Обработка...",
    },
    "en": {
        "title": "Food Ingredient Scanner",
        "upload": "Upload image",
        "camera": "Take photo",
        "ocr_text": "Recognized text",
        "dangerous": "Detected potentially harmful ingredients",
        "safe": "No harmful ingredients found",
        "processing": "Processing...",
    }
}

language = st.sidebar.selectbox(
    "Language / Език",
    ["bg", "en"]
)

T = LANG[language]

st.title(T["title"])

harmful_ingredients = {
    "e621": {
        "bg": "E621 (мононатриев глутамат)",
        "en": "E621 (Monosodium Glutamate)"
    },
    "palm oil": {
        "bg": "Палмово масло",
        "en": "Palm Oil"
    },
    "палмово масло": {
        "bg": "Палмово масло",
        "en": "Palm Oil"
    },
    "e250": {
        "bg": "E250 (Натриев нитрит)",
        "en": "E250 (Sodium Nitrite)"
    },
    "e951": {
        "bg": "E951 (Аспартам)",
        "en": "E951 (Aspartame)"
    },
    "aspartame": {
        "bg": "Аспартам",
        "en": "Aspartame"
    },
    "high fructose corn syrup": {
        "bg": "Глюкозо-фруктозен сироп",
        "en": "High Fructose Corn Syrup"
    }
}

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_reader()

uploaded_file = st.file_uploader(
    T["upload"],
    type=["jpg", "jpeg", "png"]
)

camera_image = st.camera_input(T["camera"])

image = None

if uploaded_file:
    image = Image.open(uploaded_file)

elif camera_image:
    image = Image.open(camera_image)

if image is not None:

    st.image(image, use_container_width=True)

    with st.spinner(T["processing"]):

        img_array = np.array(image)

        results = reader.readtext(img_array)

        extracted_text = " ".join([res[1] for res in results])

        extracted_text_lower = extracted_text.lower()

        st.subheader(T["ocr_text"])
        st.write(extracted_text)

        found = []

        for ingredient_key, labels in harmful_ingredients.items():

            pattern = re.escape(ingredient_key.lower())

            if re.search(pattern, extracted_text_lower):
                found.append(labels[language])

        st.subheader(T["dangerous"])

        if found:
            unique_found = list(set(found))

            for item in unique_found:
                st.error(f"⚠️ {item}")

        else:
            st.success(f"✅ {T['safe']}")

st.markdown("---")
st.caption("EasyOCR + Streamlit")
