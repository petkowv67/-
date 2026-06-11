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
        "ocr_text": "Разпознат текст",
        "dangerous": "Открити потенциално вредни съставки",
        "safe": "Не са открити вредни съставки",
        "processing": "Обработка..."
    },
    "en": {
        "title": "Food Ingredient Scanner",
        "upload": "Upload image",
        "ocr_text": "Recognized text",
        "dangerous": "Detected potentially harmful ingredients",
        "safe": "No harmful ingredients found",
        "processing": "Processing..."
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
    return easyocr.Reader(['en'], gpu=False)

try:
    reader = load_reader()
except Exception as e:
    st.error(f"EasyOCR Error: {e}")
    st.stop()

uploaded_file = st.file_uploader(
    T["upload"],
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file).convert("RGB")

        st.image(image)

        with st.spinner(T["processing"]):

            img_array = np.array(image)

            results = reader.readtext(img_array)

            extracted_text = " ".join(
                [res[1] for res in results]
            )

            extracted_text_lower = extracted_text.lower()

            st.subheader(T["ocr_text"])
            st.write(extracted_text)

            found = []

            for ingredient_key, labels in harmful_ingredients.items():

                if ingredient_key.lower() in extracted_text_lower:
                    found.append(labels[language])

            st.subheader(T["dangerous"])

            if found:

                for item in sorted(set(found)):
                    st.error(f"⚠️ {item}")

            else:
                st.success(f"✅ {T['safe']}")

    except Exception as e:
        st.error(f"Processing error: {e}")

st.markdown("---")
st.caption("EasyOCR + Streamlit")
