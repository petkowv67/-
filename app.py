import streamlit as st
import re

st.set_page_config(
    page_title="Food Ingredient Scanner",
    layout="centered"
)

st.title("🥫 Food Ingredient Scanner")

harmful_ingredients = {
    "e621": "E621 (Мононатриев глутамат)",
    "e250": "E250 (Натриев нитрит)",
    "e951": "E951 (Аспартам)",
    "aspartame": "Аспартам",
    "palm oil": "Палмово масло",
    "палмово масло": "Палмово масло",
    "high fructose corn syrup": "Глюкозо-фруктозен сироп",
    "hydrogenated oil": "Хидрогенирани мазнини",
    "trans fat": "Транс мазнини",
    "e102": "Тартразин (E102)",
    "e110": "Жълто FCF (E110)",
    "e129": "Allura Red (E129)"
}

uploaded_file = st.file_uploader(
    "Качи снимка на етикета",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file)

st.subheader("Постави текста от етикета")

ingredients_text = st.text_area(
    "Съставки",
    height=200
)

if st.button("Провери съставките"):

    text = ingredients_text.lower()

    found = []

    for ingredient, label in harmful_ingredients.items():

        if re.search(re.escape(ingredient), text):
            found.append(label)

    st.subheader("Резултат")

    if found:

        for item in sorted(set(found)):
            st.error(f"⚠️ {item}")

    else:
        st.success("✅ Не са открити проблемни съставки")
