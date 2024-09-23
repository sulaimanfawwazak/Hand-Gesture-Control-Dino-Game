import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui as auto

start_time = 0
current_time = 0

distance = 0
distance_x = 0
distance_y = 0
cx_thumb = 0
cy_thumb = 0
cx_index = 0
cy_index = 0

jump_cooldown = 1
last_jump_time = 0

distance_threshold = 30

# Get the feed from the camera
cap = cv2.VideoCapture(0)

# Frame size
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

print(f'frame_height: {frame_height}')
print(f'frame_width: {frame_width}')

# Instantiate mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

while True:
  ret, image = cap.read()

  if not ret:
    print(f"Can't read from camera")
    break

  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image_flip = cv2.flip(image, 1)

  results = hands.process(image_rgb)
  # print(results.multi_hand_landmarks)
  

  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      for idx, landmark in enumerate(hand_landmarks.landmark):
        cx, cy = int(landmark.x * frame_width), int(landmark.y * frame_height)
        if idx == 4:
          print(f'idx {idx}: {cx}, {cy}')

        if idx == 4:
          cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
          cx_thumb, cy_thumb = cx,cy
          # cv2.circle(image_flip, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        if idx == 8:
          cv2.circle(image, (cx, cy), 10, (255, 255, 0), cv2.FILLED)
          # cv2.circle(image_flip, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
          cx_index, cy_index = cx,cy

        distance = np.sqrt((cx_thumb - cx_index) + (cy_thumb - cy_index))
        distance_x = np.abs(cx_thumb - cx_index)
        distance_y = np.abs(cy_thumb - cy_index)
        # print(f'distance: {distance}')


        current_time = time.time()
        if distance_y < distance_threshold and cu:
          auto.press('up')
          # time.sleep(0.5)


      # Draw the landmark
      mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

  # Calculate the FPS
  current_time = time.time()
  fps = 1/(current_time - start_time)
  start_time = current_time

  cv2.putText(image, f'FPS: {fps:.2f} | dist: {distance:.2f} | dist_x: {distance_x} | dist_y: {distance_y}', (5, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
  # cv2.putText(image_flip, f'{fps:.2f}', (5, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)

  cv2.imshow("Camera", image)
  # cv2.imshow("Camera", image_flip)


  if cv2.waitKey(1) == ord(' '):
    break

cap.release()
cv2.destroyAllWindows()