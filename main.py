

import streamlit as st
from pdf2image import convert_from_path
import os

# Create the PDF and image directories if they don't exist
if not os.path.exists("./pdf"):
    os.makedirs("./pdf")

if not os.path.exists("./image"):
    os.makedirs("./image")

# st.markdown("<h1 style='text-align: center;'>アンプゼー</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: lavender;'>アンプゼー</h1>", unsafe_allow_html=True)

# File uploader
file = st.file_uploader("Upload file", type=["pdf"])

if file is not None:
    # Save the uploaded file
    file_path = os.path.join("./pdf", file.name)
    
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    st.success(f"File saved successfully at {file_path}")

    # Convert PDF to images
    images = convert_from_path(file_path)
    image_paths = []
    
    for i, image in enumerate(images):
        image_path = f'./image/page{i}.jpg'
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    
    # Initialize session state
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0

    # Display current and next image
    current_page = st.session_state.page_number
    next_page = current_page + 1

    col1, col2 = st.columns(2)

    with col1:
        if current_page < len(image_paths):
            st.image(image_paths[current_page])
        else:
            st.write("No more pages on the left.")

    with col2:
        if next_page < len(image_paths):
            st.image(image_paths[next_page])
        else:
            st.write("No more pages on the right.")
    
    # Columns for navigation buttons
    col1, col2, col3 = st.columns([1, 1, 10])
    
    with col1:
        if st.button("⬅️"):
            if st.session_state.page_number > 0:
                st.session_state.page_number -= 2
                if st.session_state.page_number < 0:
                    st.session_state.page_number = 0
    
    with col2:
        if st.button("➡️"):
            if st.session_state.page_number < len(image_paths) - 2:
                st.session_state.page_number += 2
else:
    st.info("Please upload a PDF file")
