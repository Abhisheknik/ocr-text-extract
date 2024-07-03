import streamlit as st # type: ignore
import pandas as pd
from ocr_utils import extract_text_from_image, extract_text_from_pdf, convert_pdf_to_images
from PIL import Image
import tempfile
import os

EXCEL_FILE = "extracted_text.xlsx"

def save_to_excel(new_data, output_path):
    # Read existing data if the file exists
    if os.path.exists(output_path):
        df_existing = pd.read_excel(output_path)
    else:
        df_existing = pd.DataFrame(columns=['Extracted Text'])

    # Split the new text into paragraphs based on double line breaks
    new_paragraphs = new_data.split('\n\n')
    df_new = pd.DataFrame({'Extracted Text': new_paragraphs})

    # Append new data to existing data
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(output_path, index=False)
    
    return df_combined

def resize_image(image, height):
    # Resize the image while maintaining the aspect ratio
    aspect_ratio = image.width / image.height
    new_width = int(height * aspect_ratio)
    return image.resize((new_width, height))

def main():
    st.title("OCR (Text Extractor)")

    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        text = ""
        image = None

        # Set columns with equal width
        col1, col2 = st.columns(2)

        # Process PDF files
        if file_details["FileType"] == "application/pdf":
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name
                    text = extract_text_from_pdf(temp_file_path)
                    # Convert first page of PDF to image for display
                    images = convert_pdf_to_images(temp_file_path)
                    if images:
                        image = images[0]
            except Exception as e:
                st.error(f"Error processing PDF file: {e}")

        # Process image files
        else:
            try:
                image = Image.open(uploaded_file)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_file_path = temp_file.name
                    text = extract_text_from_image(temp_file_path)
            except Exception as e:
                st.error(f"Error processing image file: {e}")

        with col1:
            if image:
                resized_image = resize_image(image, 400)  # Resize the image to height 400
                st.image(resized_image, caption=file_details["FileName"], use_column_width=True)

        with col2:
            st.subheader("Extracted Text:")
            st.text_area("Extracted Text", text, height=400)

        # Save extracted text to Excel and display as table
        if text:
            try:
                df = save_to_excel(text, EXCEL_FILE)
                st.success("Text has been extracted and saved to extracted_text.xlsx")

                st.subheader("Extracted Text Table:")
                st.dataframe(df, width=800, height=400)
            except Exception as e:
                st.error(f"Error saving to Excel: {e}")

if __name__ == '__main__':
    main()
