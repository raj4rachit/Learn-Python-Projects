import cv2
import streamlit as st
from PIL import Image
import torch
import numpy as np


model_path = 'yolov5coco.pt'  # path ke weight
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path=model_path).to(device)


def main():
    st.title("Yolov5 Person Detection")

    uploaded_file = st.file_uploader(
        "Pilih gambar", type=["jpg", "png", 'webp'])

    button = st.button('Klik untuk deteksi')

    try:
        # menampilkan image yang diupload
        uploaded = st.image(uploaded_file, width=600)
        if button:
            uploaded.empty()
    except:
        st.write("Belum ada file dipuload")

    if button:
        try:
            img = Image.open(uploaded_file)

            results = model(img)

            predictions = results.pandas().xyxy[0]

            display_results(img, predictions)
        except:
            st.write("UPLOAD FOTONYA DULU WOY!")


def display_results(img, predictions):

    img = np.array(img)  # Convert PIL image to NumPy array

    for _, row in predictions.iterrows():
        x_min, y_min, x_max, y_max = int(row['xmin']), int(
            row['ymin']), int(row['xmax']), int(row['ymax'])
        confidence = row['confidence']
        label = f"{row['name']} ({confidence:.2f})"
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
        cv2.putText(img, label, (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    st.image(img, caption='Predicted', width=600)


if __name__ == "__main__":
    main()