import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()
    
    # Convert the BGR image to RGB and process it with Mediapipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Check if hands are detected in the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of index finger and thumb landmarks
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            # Calculate the distance between index finger and thumb landmarks
            distance = abs(index_finger.x - thumb.x) + abs(index_finger.y - thumb.y)
            
            # Control PowerPoint based on hand gesture distance
            if distance < 0.1:
                pyautogui.press('right')  # Move to next slide when fingers are close together
            elif distance > 0.3:
                pyautogui.press('left')  # Move to previous slide when fingers are apart
    
    # Display the frame with hand landmarks (optional)
    annotated_frame = frame.copy()
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.drawing.draw_landmarks(annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('Hand Gestures', annotated_frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()