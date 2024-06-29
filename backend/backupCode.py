import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
from firebase_config import storage, db
import concurrent.futures
import asyncio

async def detect_faces_and_encodings(img):
    loop = asyncio.get_running_loop()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    face_locations = await loop.run_in_executor(None, lambda: face_recognition.face_locations(imgS, model='hog'))
    face_encodings = await loop.run_in_executor(None, lambda: face_recognition.face_encodings(imgS, face_locations))
    return face_locations, face_encodings

async def process_frame(executor, img, frame_skip, frame_count, encondeListKnown, personIds):
    if frame_count % frame_skip == 0:
        face_locations, face_encodings = await detect_faces_and_encodings(img)
        return face_locations, face_encodings
    return [], []

async def main():
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

    # Carregando o enconding
    print("Carregando encoded file...")

    with open('encodeFile.p', 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)

    encondeListKnown, personIds = encodeListKnownWithIds
    print(personIds)
    print("Encoded carregado")
    modeType = 0
    counter = 0
    id = -1
    imgPerson = np.zeros((216, 216, 3), dtype=np.uint8)  # Placeholder para imgPerson

    frame_skip = 5  # Processar cada 5º frame
    frame_count = 0

    face_locations = []
    face_encodings = []

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    while True:
        success, img = cap.read()
        frame_count += 1

        if not success:
            print("Failed to capture image")
            break

        if frame_count % frame_skip == 0:
            face_locations, face_encodings = await process_frame(executor, img, frame_skip, frame_count, encondeListKnown, personIds)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if face_locations:
            print("Face locations detected:", face_locations)

        for encodeFace, faceLoc in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(encondeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encondeListKnown, encodeFace)
            print('matches', matches)
            print('faceDistance', faceDistance)

            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                print("Face conhecida detectada")
                print("id ", personIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1)

                id = personIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1

            if counter != 0:
                if counter == 1:
                    # get data
                    personInfo = db.reference(f'Person/{id}').get()
                    print(personInfo)

                    # get image
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgPerson = cv2.imdecode(array, cv2.IMREAD_COLOR)
                    imgPerson = cv2.resize(imgPerson, (216, 216))

                (w, h), _ = cv2.getTextSize(personInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 5)
                offset = (414 - w) // 2
                cvzone.putTextRect(imgBackground, str(personInfo['name']), (808 + offset, 445),
                                   scale=1, thickness=1, offset=2, colorR=(50, 50, 50))

            imgBackground[175:175 + 216, 909:909 + 216] = imgPerson

            counter += 1

        cv2.imshow('Face Attendance', imgBackground)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    executor.shutdown()

asyncio.run(main())
