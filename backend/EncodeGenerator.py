import cv2
import face_recognition
import pickle
import os
import numpy as np
from firebase_config import storage

def get_images_from_storage():
    blobs = storage.bucket().list_blobs(prefix='Images/')
    images = {}
    for blob in blobs:
        if blob.name.endswith('.png'):
            user_id = os.path.splitext(os.path.basename(blob.name))[0]
            img_array = np.frombuffer(blob.download_as_string(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            images[user_id] = img
    return images

def find_encoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Carregar imagens do Firebase Storage
images_from_storage = get_images_from_storage()

# Separar IDs e imagens
personIds = list(images_from_storage.keys())
imgList = list(images_from_storage.values())

print(personIds)

print("Encoding iniciado...")
encodeListKnown = find_encoding(imgList)
encodeListKnownWithIds = [encodeListKnown, personIds]

print("Encoding completo!")

# Salvar os encodings
with open("encodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("Arquivo salvo")
