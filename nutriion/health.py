import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set your Google API Key here
api_key = "AIzaSyATxC68T5dgaFYBz1D1h7TKch7UvyfCEuM"

# Set page configuration
st.set_page_config(page_title="NutriFy ")

# Inject custom CSS
st.markdown(
    """
    <link rel="stylesheet" type="text/css" href="./style.css">
    """,
    unsafe_allow_html=True,
)


# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Initialize Streamlit app
st.title("NutriFy 🍎")
st.write(
    "NutriFy is an innovative application designed to simplify the process of analyzing the nutritional content of food items captured in images.")


# Input fields
input_text = st.text_input("Input Prompt:")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
Your input prompt...
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake
in the following format:
- Total fat
- Saturated fat
- Trans fat
- Cholesterol
- Sodium
- Total carbohydrate
- Dietary fiber
- Total sugars
- Added sugars
- Protein
- Vitamins and minerals
"""

# If submit button is clicked
if submit:
    genai.configure(api_key=api_key)  # Configuring with API key

    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please upload an image.")
