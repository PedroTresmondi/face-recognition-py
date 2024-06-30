from flask import Flask, request, jsonify
from firebase_config import storage, db
import cv2
import face_recognition
import numpy as np
import pickle
import os

app = Flask(__name__)


# Carregar encodings conhecidos
def load_encodings():
    global encodeListKnown, personIds
    encode_file_path = os.path.join(os.path.dirname(__file__), 'encodeFile.p')
    with open(encode_file_path, 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, personIds = encodeListKnownWithIds



load_encodings()


def detect_faces_and_encodings(img):
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(imgS, model='hog')
    face_encodings = face_recognition.face_encodings(imgS, face_locations)
    return face_locations, face_encodings


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    face_locations, face_encodings = detect_faces_and_encodings(img)

    results = []
    for encodeFace, faceLoc in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDistance)
        if matches[matchIndex] and faceDistance[matchIndex] < 0.6:
            detected_id = personIds[matchIndex]
            personInfo = db.reference(f'Person/{detected_id}').get()
            results.append({
                'id': detected_id,
                'name': personInfo['name'] if personInfo else 'Unknown',
                'location': faceLoc
            })
        else:
            results.append({'id': None, 'name': 'Unknown', 'location': faceLoc})

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
