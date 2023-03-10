import streamlit as st
from PIL import Image
import pickle
import cv2
import numpy as np
import tensorflow
from tensorflow.keras.models import load_model
import os


# Load the pickled model
def get_model(file):
    cnn = None
    pickle_in = open(file, 'rb')
    cnn = load_model(file)
    if cnn is None:
        st.write('Loading the Model....')
    else:
        st.write('Model loaded successfully.')
    
    return cnn

# Preprocess input data
def preprocess(data):
    try:
        img = np.asarray(data)
        img = img.astype('uint8')
        img = cv2.resize(src=img, dsize=(28, 28))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        # img = (255-img)
        img = img/255
        img = img.reshape(-1, 28, 28, 1)
    
        return img
    
    except Exception as e:
        img = np.asarray(data)
        img = img.astype('uint8')
        img = cv2.resize(src=img, dsize=(28, 28))
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)
        img = (255-img)
        img = img/255
        img = img.reshape(-1, 28, 28, 1)
    
        return img

# Predict the digit for given input
def make_prediction(model, input):
    prediction = model.predict(input)
    prob_value = np.argmax(prediction)
    
    return prob_value
    
    
# Main funciton
def main():
    
    file = os.path.join('trained_model.h5')
    
    st.title('Hand Written Digit Recognition with CNN')
    activities = ['ML Model', 'About']
    choices = st.selectbox(label='-----------', options=['Choose an option','Deep Learning Model', 'Performance Summary', 'About'])

    if choices == 'Deep Learning Model':
        
        model = get_model(file)
        
        # Uploading image
        img = st.file_uploader('Upload image of a digit below:', type=['png', 'jpg', 'jpeg'])
        try:
            if img is not None:
                st.image(img, caption='Uploaded Image', width=300)
                img = Image.open(img)
        except:
            st.warning('Unsupported file')
            
        if st.button('Make Prediction'):
            input = None
            
            try:
                input = preprocess(img)
            except Exception as e:
                st.error('An Unknown error has occurred')
            
            if input is not None:
                prediction = None
                try:
                    output = None
                    prediction = make_prediction(model, input)
                    st.subheader('PREDICTION')
                    if prediction == 0:
                        output = 'ZERO'
                    elif prediction == 1:
                        output = 'ONE'
                    elif prediction == 2:
                        output = 'TWO'
                    elif prediction == 3:
                        output = 'THREE'
                    elif prediction == 4:
                        output = 'FOUR'
                    elif prediction == 5:
                        output = 'FIVE'
                    elif prediction == 6:
                        output = 'SIX'
                    elif prediction == 7:
                        output = 'SEVEN'
                    elif prediction == 8:
                        output = 'EIGHT'
                    elif prediction == 9:
                        output = 'NINE'
                        
                    st.success(f'You have uploaded an image of --------> "{prediction}".')
                    st.write('Have I got it right?')
                except Exception as e:
                    st.error('An Unknown error has occurred')
    
    elif choices == 'Performance Summary':
        st.write('Coming Soon')
    
    elif choices == 'About':
        st.subheader('About')
        st.markdown('''
                    This project implements a **convolutional neural network (CNN)** to recognize handwritten digits from the MNIST dataset.
                    The model is trained using Keras with TensorFlow as the backend.
                    
                    
                    ##### Created by **Mubarak Mayyeri**
                    ''')
                    

if __name__ == '__main__':
    main()       