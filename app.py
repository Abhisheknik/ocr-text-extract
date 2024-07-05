import streamlit as st
import pandas as pd
from ocr_utils import extract_text_from_image, extract_text_from_pdf, convert_pdf_to_images
from PIL import Image
import tempfile
import os

EXCEL_FILE = "extracted_text.xlsx"

def save_to_excel(new_data, output_path):
    if os.path.exists(output_path):
        df_existing = pd.read_excel(output_path)
    else:
        df_existing = pd.DataFrame(columns=['Extracted Text'])

    new_paragraphs = new_data.split('\n\n')
    df_new = pd.DataFrame({'Extracted Text': new_paragraphs})

    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(output_path, index=False)
    
    return df_combined

def resize_image(image, max_width=600):
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        return image.resize((max_width, new_height))
    return image

def main():
    st.set_page_config(page_title="OCR Text Extractor", layout="wide")
    st.title("OCR Text Extractor")

    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        text = ""
        image = None

        col1, col2 = st.columns([2, 3])

        if file_details["FileType"] == "application/pdf":
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name
                    text = extract_text_from_pdf(temp_file_path)
                    images = convert_pdf_to_images(temp_file_path)
                    if images:
                        image = images[0]
            except Exception as e:
                st.error(f"Error processing PDF file: {e}")

        else:
            try:
                image = Image.open(uploaded_file)
                image = resize_image(image)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_file_path = temp_file.name
                    text = extract_text_from_image(temp_file_path)
            except Exception as e:
                st.error(f"Error processing image file: {e}")

        with col1:
            if image:
                st.image(image, caption=file_details["FileName"], use_column_width=True)

        with col2:
            st.subheader("Extracted Text:")
            st.text_area("Extracted Text", text, height=300)

        if st.button("Save Text to Excel", key="save_button"):
            try:
                if text:
                    df = save_to_excel(text, EXCEL_FILE)
                    st.success("Text has been extracted and saved to extracted_text.xlsx")

                    st.subheader("Extracted Text Table:")
                    st.dataframe(df, width=800, height=400)
            except Exception as e:
                st.error(f"Error saving to Excel: {e}")

if __name__ == '__main__':
    main()

# myenv\Scripts\activate
# streamlit run app.py