#!/usr/bin/env python
# coding: utf-8

# In[5]:


import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Open the webcam thing
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Get the screen size
screen_width, screen_height = pyautogui.size()

scroll_gate = True
right_click_gate = True
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # Convert the frame to RGB for processing by MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Run hand detection
    results = hands.process(rgb)
    
    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #This line Draws the whole skeleton of the hand but its not needed
            #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Coordinate objects of the improtant landmarks
            index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            palm = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            
            
            # Move the cursor to the finger position
            finger_x = int(index_finger_pip.x * screen_width)
            finger_y = int(index_finger_pip.y * screen_height)
            pyautogui.moveTo(finger_x, finger_y)
            
            # Gesture Logic
            left_click = abs(index_finger_tip.y - thumb_tip.y)
            middle_position = middle_finger_tip.y - thumb_tip.y
            scroll_y = (index_finger_tip.y - thumb_tip.y) + (middle_finger_tip.y - thumb_tip.y)
            right_click = pinky_tip.y - palm.y
            

            #This is so we can draw the dots.
            #This Red Dot that controles where the mouse is
            pip_x = int(index_finger_pip.x * frame.shape[1])
            pip_y = int(index_finger_pip.y * frame.shape[0])

            ind_x = int(index_finger_tip.x * frame.shape[1])
            ind_y = int(index_finger_tip.y * frame.shape[0])

            thumb_x = int(thumb_tip.x * frame.shape[1])
            thumb_y = int(thumb_tip.y * frame.shape[0])
            
            mid_x = int(middle_finger_tip.x * frame.shape[1])
            mid_y = int(middle_finger_tip.y * frame.shape[0])
            
            pink_x = int(pinky_tip.x * frame.shape[1])
            pink_y = int(pinky_tip.y * frame.shape[0])
            
                
            #Drag Logic
            if scroll_gate and right_click_gate:
                if ( -.01 < middle_position and middle_position < .05):
                    pyautogui.mouseDown(button="left")
                    ind_col = (255, 0, 0)
                    mid_col = (0, 255, 0)
                    thumb_col = (0, 255, 0)
                    pinky_col = (255,0,0)
                    cv2.putText(frame, "Drag", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # Release Drag
                else:
                    pyautogui.mouseUp(button="left")
                    ind_col = (255, 0, 0)
                    mid_col = (255, 0, 0)
                    thumb_col = (255, 0, 0)
                    pinky_col = (255,0,0)

                
            # Click Logic    
            # Left Click Logic
            if left_click < 0.05:
                pyautogui.click(button='left')
                ind_col = (0, 255, 0)
                mid_col = (255, 0, 0)
                thumb_col = (0, 255, 0)
                pinky_col = (255,0,0)
                cv2.putText(frame, "Left", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Right Click Logic
            elif right_click < -.2:
                if right_click_gate:
                    pyautogui.click(button='right')
                    right_click_gate = False
                    cv2.putText(frame, "Right", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    ind_col = (255, 0, 0)
                    mid_col = (255, 0, 0)
                    thumb_col = (255, 0, 0)
                    pinky_col = (0,255,0)
                #cv2.putText(frame, "Right", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                right_click_gate = True
                #cv2.putText(frame, "Right up", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                pinky_col = (255,0,0)
                
            #Scroll Logic
            # Start Scroll
            if scroll_y < -0.3:
                if scroll_gate:
                    pyautogui.mouseDown(button="middle")
                    scroll_gate = False
                ind_col = (0, 255, 0)
                mid_col = (0, 255, 0)
                thumb_col = (0, 255, 0)
                cv2.putText(frame, "Scroll", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Stop Scroll
            elif scroll_y > -0.1:
                pyautogui.mouseUp(button="middle")
                scroll_gate = True
                
                
            #This Renders the dots. Comment out these lines and it speeds up the program a bit.
            cv2.circle(frame, (pip_x, pip_y), 5, (0, 0, 255), -1) #Red dot, movement dot
            cv2.circle(frame, (ind_x, ind_y), 5, ind_col, -1)  #index finger tip dot
            cv2.circle(frame, (mid_x, mid_y), 5, mid_col, -1) # middle finger tip dot
            cv2.circle(frame, (thumb_x, thumb_y), 5, thumb_col, -1) # thumb tip dot
            cv2.circle(frame, (pink_x, pink_y), 5, pinky_col,-1) #pinky tip dot

            

    # Display the frame with detected hands
    cv2.imshow('Hand Recognition', frame)
    
    
    # Click on the camera screen and press 'q' key to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close program
cap.release()
cv2.destroyAllWindows()


# In[4]:





# In[11]:





# In[ ]:




