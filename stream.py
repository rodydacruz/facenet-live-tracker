from facenet_pytorch import MTCNN
import torch
import numpy as np
import mmcv, cv2
from PIL import Image, ImageDraw
from IPython import display
import cv2

# Initialize MTCNN
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)

# YouTube video URL
youtube_url = 'https://www.youtube.com/watch?v=BpXsvIPvEIg&ab_channel=Newsmax'

# OpenCV video capture
cap = cv2.VideoCapture(youtube_url)

while True:
    # Read frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to RGB (facenet_pytorch MTCNN expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    boxes, _ = mtcnn.detect(frame_rgb)
    
    # Draw faces
    if boxes is not None:
        for box in boxes:
            box = box.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow('YouTube Live Stream', frame)
    
    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()