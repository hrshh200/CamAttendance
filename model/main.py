
from flask import Flask , jsonify , request
from flask_cors import CORS
import pathlib
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import random
import pandas as pd
import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, MaxPooling2D, Flatten, Conv2D
from keras.models import load_model

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello World"

@app.route('/predict', methods=['POST'])
def predict_model():
    file = request.files['k1']
    print(file)
    file_data = file.read()
    nparr = np.frombuffer(file_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img_resize = cv2.resize(img, (300,300))
    # img_gray = cv2.cvtColor(img_resize , cv2.COLOR_BGR2GRAY)
    # img = img_gray.reshape(1,300,300,1)
    data = predict(img)
    if data == 1:
        return jsonify({'Message':'Identified:Harsh'})
    else:
        return jsonify({'Message':'Not identified'})


#CONVERTING IMAGES TO CSV FILES
# import os
# import numpy as np
# import pandas as pd
# from PIL import Image
#
# root = 'Images'
# fnames = os.listdir(root)
#
# # List to store flattened image data and filenames
# image_data = []
# image_filenames = []
#
# # Iterate over each image file in the folder
# for i in range(len(fnames)):
#     filepath = os.path.join(root, fnames[i])
#     img = Image.open(filepath)
#     img = img.resize((300,300))
#     print(img)
#     # Convert image to grayscale and flatten it into a 1D array
#     img_array = np.array(img.convert('L')).flatten()
#     # Append the flattened image data to image_data
#     image_data.append(img_array)
#     # Append the filename to image_filenames list
#     image_filenames.append(fnames[i])
#
# # Convert the lists to NumPy arrays
# image_data = np.array(image_data)
# image_filenames = np.array(image_filenames)
#
# # Concatenate image data with filenames along the column axis
# data_with_filenames = np.column_stack((image_data, image_filenames))
#
# # Convert NumPy array to DataFrame
# df = pd.DataFrame(data_with_filenames)
#
# # Save the DataFrame to a CSV file
# csv_file_path = 'output.csv'
# df.to_csv(csv_file_path, index=False, header=False)  # Exclude row and column labels
#
# print("CSV file saved successfully.")


#SHOWING IMAGES FROM CSV FILES AND TRAINING THE MODEL

# Load the CSV file into a DataFrame


def predict(img):

    model = load_model('keras_model.h5')
    #model = pickle.load(open('C:/Users/User/PycharmProjects/CamAttendance/model_saved', 'rb'))
    pred = model.predict(img)
    # pred = (pred > 0.5)
    if pred == 1:
        return 1
    else:
        return 0



# # Extract image data and filenames
# image_data = df.iloc[:, :-1].values  # Extract all columns except the last one
# image_filenames = df.iloc[:, -1].values  # Extract the last column
#
# # Display the images
# for i in range(len(image_filenames)):
#     # Reshape the flattened image data into its original shape
#     img_array = image_data[i].reshape((300, 300))  # Assuming each image is 100x100 pixels
#
#     # Display the image
#     plt.imshow(img_array, cmap='gray')  # Assuming grayscale images
#     plt.title(image_filenames[i])  # Set title as the filename
#     plt.show()
#













# TAKING FRAMES FROM OPENCV

# def camerashot():
#     i = 1
#     cascadepath = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
#
#     clf = cv2.CascadeClassifier(str(cascadepath))
#
#     nameid = str(input("Enter the name")).lower()
#     path = 'Images/' + nameid
#
#     isExists = os.path.exists(path)
#
#     if isExists:
#         print("Name already exists")
#         print("Try for another name....")
#
#     else:
#         os.makedirs(path)
#
#     camera = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
# #
#     while True:
#         res , frame = camera.read()
#         faces = clf.detectMultiScale(
#             frame,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#             flags=cv2.CASCADE_SCALE_IMAGE
#         )
#         for (x,y,w,h) in faces:
#             i = i + 1
#             cv2.imwrite(path + f'image_{i}.jpg', frame[y:y + h, x:x + w])
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,255))
#
#
#             cv2.imshow("Window" ,frame)
#             cv2.waitKey(1)
#             if i>=500:
#                  break
#
#     camera.release()
#     cv2.destroyAllWindows()
# # #
if __name__ == '__main__':
    predict_model()

