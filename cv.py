import random
import cv2
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

# Set up Streamlit UI
st.title("Hand Tracking Game")

# Webcam
width = 1920
height = 1080
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)  # Adjust maxHands to the desired number of hands to detect

# Find Function
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

# Game Variables
cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
timeStart = time.time()
totalTime = 20

# Game Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if time.time() - timeStart < totalTime:
        hands, img = detector.findHands(img, draw=False)

        if hands:
            for hand in hands:
                lmList = hand['lmList']
                x1, y1, h = lmList[5]
                x2, y2, h = lmList[17]
                x, y, w, h = hand['bbox']
                distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                A, B, C = coff
                distanceCM = A * distance ** 2 + B * distance + C

                if distanceCM < 40:
                    if x < cx < x + w and y < cy < y + h:
                        counter = 1

                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

            if counter:
                counter += 1
                color = (0, 255, 0)
                if counter == 3:
                    cx = random.randint(100, 1100)
                    cy = random.randint(100, 600)
                    color = (255, 0, 255)
                    score += 1
                    counter = 0

        # Draw Button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # Game HUD
        st.image(img, use_column_width=True)
        st.write(f'Time: {int(totalTime - (time.time() - timeStart))} seconds')
        st.write(f'Score: {str(score).zfill(2)}')

    else:
        st.write('Game Over')
        st.write(f'Your Score: {score}')
        st.write('Press R to restart')

    # Break the loop when 'r' is pressed
    button_count = 0  # Initialize a counter for unique keys

    if st.button('Restart (Press R)', key=f'restart_button_{button_count}'):
        # Your button code here
        button_count += 1  # Increment the counter for the next button

        timeStart = time.time()
        score = 0

    # Ensure the app updates frequently to show the webcam feed
    time.sleep(0.03)
