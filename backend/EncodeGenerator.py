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
            print(f'Imagem carregada: {user_id}')
    return images

def find_encoding(imagesList, personIds):
    encodeList = []
    validPersonIds = []
    for img, person_id in zip(imagesList, personIds):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode = encodings[0]
            encodeList.append(encode)
            validPersonIds.append(person_id)
        else:
            print(f"Nenhuma face encontrada para o ID: {person_id}")
    return encodeList, validPersonIds

def update_encodings():
    images_from_storage = get_images_from_storage()
    personIds = list(images_from_storage.keys())
    imgList = list(images_from_storage.values())
    
    print(f"Person IDs from storage: {personIds}")
    print("Encoding iniciado...")

    if not imgList:
        print("No images found in storage.")
        return

    encodeListKnown, validPersonIds = find_encoding(imgList, personIds)
    encodeListKnownWithIds = [encodeListKnown, validPersonIds]
    
    print("Encoding completo!")
    with open("encodeFile.p", 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)
    
    print("Arquivo salvo")

if __name__ == "__main__":
    update_encodings()
