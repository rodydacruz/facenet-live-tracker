from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
import mmcv
import cv2
import requests
from PIL import Image, ImageDraw
from IPython import display
from lib.people_service import PersonRepository
from lib.log_service import LogRepository
from io import BytesIO

# Initialize MTCNN and InceptionResnetV1
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

videoSrc = 'video_1.mov'

# Load video frames
video = mmcv.VideoReader(videoSrc)
frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]

# Initialize the PersonCRUD object
people = PersonRepository('persons.db')
# Initialize the LogCRUD object
logs = LogRepository('persons.db')
# Get all persons from the database
persons = people.get_all_persons()

# Function to detect faces and compare with person photos
def detect_and_compare(frame, person):
    # Retrieve person's photo URL
    photo_url = person[4]  # Assuming person schema: id, name, age, email, photo_url
    
    # Download or access the photo
    response = requests.get(photo_url)
    person_photo = Image.open(BytesIO(response.content))

    # Convert person_photo to PyTorch tensor
    person_photo_tensor = mtcnn(person_photo).to(device)

    # Detect faces in the frame
    boxes, _ = mtcnn.detect(frame)

    # Compare each detected face with the person's photo
    if boxes is not None:
        for box in boxes:
            # Extract the coordinates of the face bounding box
            x1, y1, x2, y2 = box
                
            # Crop the face from the frame
            face = frame.crop((int(x1), int(y1), int(x2), int(y2)))

            # Convert face to PyTorch tensor
            face_tensor = mtcnn(face)
            
            # Check if a face is detected
            if face_tensor is not None:
                # Convert face tensor to device
                face_tensor = face_tensor.to(device)
                
                # Get embeddings
                face_embedding = resnet(face_tensor)
                person_embedding = resnet(person_photo_tensor)
            
                # Calculate similarity score
                similarity = torch.cosine_similarity(face_embedding, person_embedding, dim=1).item()
            
                # If similarity score is above a certain threshold, consider it a match
                if similarity > 0.7:  # You can adjust this threshold according to your requirement
                    log = logs.log_last_seen(person[0],videoSrc )
                    print(f"Face detected for {person[1]}:")
                    print(log)
            else:
                print("No face detected in the cropped image")
    else:
        print("No faces detected in the frame")

# Detect and compare faces for each frame and person
for i, frame in enumerate(frames):
    print(f'\rProcessing frame {i+1}/{len(frames)}', end='')
    for person in persons:
        try:
            detect_and_compare(frame, person)
        except Exception as e:
            print("Error In Processing Frame")
        finally:
            pass

print('\nDone')