import os
import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model

model = load_model('gdrive/MyDrive/Fracture_Dataset/Vgg19TF.h5',compile=False)
lab = {0: 'Normal', 1: 'Fracture'}
def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = lab[y]
    print(res)
    return res

def run():
    img1 = Image.open('AccVal_acc.png')
    img1 = img1.resize((350,350))
    st.image(img1,use_column_width=False)
    st.title("Wrist Fracture Classification")
    #st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Data is based "500 Wrist X-ray images"</h4>''',
    #           unsafe_allow_html=True)

    img_file = st.file_uploader("Choose an Wrist Fracture x-ray", type=["jpg", "png"])
    if img_file is not None:
        st.image(img_file,use_column_width=False)
        save_image_path = './upload_images/'+img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        if st.button("Predict"):
            result = processed_img(save_image_path)
            st.success("Predicted Diagnosis is: "+result)
run()