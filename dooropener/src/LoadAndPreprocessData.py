import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from collections import deque
import time
import datetime as dt
import os

CODE_PATH = "/home/imdavid/workplace/dooropener/src/"
# Load the trained model
MODEL = load_model(f'{CODE_PATH}dog_detection_model.keras')

def log(message: str):
    # Setup a log file
    with open(f"{CODE_PATH}log.txt", "a") as logfile:
        ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f"""{ts} - {message}\n"""
        logfile.write(text)

def preprocess_image(img, target_size):
    img = cv2.resize(img, target_size)
    img_array = np.expand_dims(img, axis=0)
    img_array = img_array / 255.0
    return img_array

def logging(log_message: str):
    with open(f"{CODE_PATH}log.txt", "a") as myfile:
        myfile.write(log_message)

def openDoor():
    ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{ts} Door opened!")
    log(f"Door opened!\n")
    
def closeDoor():
    ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{ts} Door closed!")
    log(f"Door closed!\n")

def test():
    # Parameters
    img_height = 480
    img_width = 640
    target_size = (img_height, img_width)  # Replace with your model's input size
    
    # Path to directory containing test images
    test_images_path = f'{CODE_PATH}Dataset/Loki/'
    
    with open(f"{CODE_PATH}testlog.txt", "a") as logfile:
        for filename in os.listdir(test_images_path):
            if filename.endswith(".jpg"):
                img_path = os.path.join(test_images_path, filename)
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Error: Could not read image {img_path}")
                    continue
                
                # Preprocess the image
                processed_img = preprocess_image(img, target_size)
                
                # Make a prediction
                prediction = MODEL.predict(processed_img)
                print(prediction)
                
                # Assume it's a binary classification: 0 - No Loki, 1 - Loki, 2 - Door Open
                predicted_class = np.argmax(prediction, axis=1)
                print(predicted_class)
                
                ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if predicted_class == 1:
                    openDoor()
                    print(f"Loki detected! Image: {filename}")
                    logfile.write(f"{ts} - Loki detected!\n")
                elif predicted_class == 2:
                    closeDoor()
                    print(f"Door open detected! Image: {filename}")
                    logfile.write(f"{ts} - Door open detected!\n")
                else:
                    print(f"No Loki detected in image: {filename}")
                    logfile.write(f"{ts} - No Loki detected!\n")

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream from webcam")
        return

    # Parameters
    img_height = 300
    img_width = 300
    buffer_size = 10
    target_size = (img_height, img_width)  # Replace with your model's input size

    # Rolling buffer to store images
    buffer = deque(maxlen=buffer_size)
    door_is_open = 0    

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Add the captured frame to the buffer
        buffer.append(frame)

        # Preprocess the latest frame
        processed_img = preprocess_image(buffer[-1], target_size)

        # Make a prediction
        prediction = MODEL.predict(processed_img)
        print(prediction)

        # Assume it's a binary classification: 0 - No Loki, 1 - Loki, 2 - Door Open
        predicted_class = np.argmax(prediction, axis=1)
        print(predicted_class)

        if predicted_class == 1:
            openDoor()
            ts = dt.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            filename = f"images/inside_motion_{ts}.jpg"  # Unique filename with timestamp
            cv2.imwrite(filename, frame)
            print(f"Loki detected! Image saved: {filename}")
            log(f"Loki detected! Image saved: {filename}")
        elif predicted_class == 2:
            door_is_open += 1
            if door_is_open > 6:
                closeDoor()
                door_is_open = 0
            log(f"Door open detected!")
        else:
            door_is_open = 0
            log(f"No Loki detected!")
            
        # Wait for 1 second before capturing the next frame
        time.sleep(1)

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test()

