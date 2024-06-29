import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import subprocess
from firebase_config import storage, db
import concurrent.futures
from firebase_admin import db as realtime_db
import sys

def detect_faces_and_encodings(img):
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(imgS, model='hog')
    face_encodings = face_recognition.face_encodings(imgS, face_locations)
    return face_locations, face_encodings

def run_encode_generator():
    try:
        python_path = sys.executable
        print(f"Executando encodeGenerator.py com {python_path}...")
        subprocess.run([python_path, "encodeGenerator.py"], check=True)
        print("encodeGenerator.py executado.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar encodeGenerator.py: {e}")

def on_person_changed(event):
    print(f"Alteração detectada. Dados do evento: {event.data}")
    run_encode_generator()
    reload_encodings()

def reload_encodings():
    global encodeListKnown, personIds
    print("Recarregando encodings...")
    try:
        with open('encodeFile.p', 'rb') as file:
            encodeListKnownWithIds = pickle.load(file)
        encodeListKnown, personIds = encodeListKnownWithIds
        print("Encodings recarregados!")
    except Exception as e:
        print(f"Erro ao recarregar encodings: {e}")

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)


imgBackground = cv2.imread('Resources/background.png')

# Importando os images mode na lista
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
bucket = storage.bucket()

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Carregando o encoding
print("Carregando encoded file...")

reload_encodings()

modeType = 0
counter = 0
current_id = -1
imgPerson = np.zeros((216, 216, 3), dtype=np.uint8)  # Placeholder para imgPerson

frame_skip = 24  # Processar cada 5º frame
frame_count = 0

face_locations = []
face_encodings = []

# Utilizando ThreadPoolExecutor para gerenciar threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# listener para monitorar alterações no Firebase Realtime Database
person_ref = realtime_db.reference('Person')
person_ref.listen(on_person_changed)

while True:
    success, img = cap.read()
    frame_count += 1

    if not success:
        print("Failed to capture image")
        break

    if frame_count % frame_skip == 0:
        future = executor.submit(detect_faces_and_encodings, img)
        face_locations, face_encodings = future.result()

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        print('matches', matches)
        print('faceDistance', faceDistance)

        matchIndex = np.argmin(faceDistance)
        if matches[matchIndex] and faceDistance[matchIndex] < 0.6:  # Threshold for face recognition confidence
            print("Face conhecida detectada")
            print("id ", personIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1)

            detected_id = personIds[matchIndex]
            if counter == 0 or current_id != detected_id:
                counter = 0
                current_id = detected_id
                cvzone.putTextRect(imgBackground, "Autenticando", (275, 400))
                cv2.imshow('Face Auth', imgBackground)
                cv2.waitKey(1)
                counter = 1
                modeType = 1

                # get data
                personInfo = db.reference(f'Person/{detected_id}').get()
                print(personInfo)

                # get image
                blob = bucket.blob(f'Images/{detected_id}.png')
                if blob.exists():
                    img_array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgPerson = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    imgPerson = cv2.resize(imgPerson, (216, 216))
                else:
                    print(f'Imagem não encontrada para o ID {detected_id}')

            if personInfo:
                (w, h), _ = cv2.getTextSize(personInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 5)
                offset = (414 - w) // 2
                cvzone.putTextRect(imgBackground, str(personInfo['name']), (808 + offset, 510),
                                   scale=2, thickness=2, offset=2, colorR=(50, 50, 50))

            imgBackground[175:175 + 216, 909:909 + 216] = imgPerson
        else:
            print("Rosto não conhecido detectado")
            modeType = 0  # Set modeType to 0 when face is not recognized

        counter += 1

    cv2.imshow('Face Auth', imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()
