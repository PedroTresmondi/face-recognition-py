from flask import Flask, request, jsonify
from firebase_config import storage, db
import cv2
import face_recognition
from flask_cors import CORS
import numpy as np
import pickle
import os
import threading
import subprocess
from datetime import datetime  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Carregar encodings conhecidos
def load_encodings():
    global encodeListKnown, personIds
    with open('encodeFile.p', 'rb') as file:
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
    load_encodings() 
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
                'email': personInfo['email'] if personInfo else 'Unknown',
                'name': personInfo['name'] if personInfo else 'Unknown',
                'location': faceLoc,
                'autenticado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            })
        else:
            results.append({'id': None, 'name': 'Unknown', 'location': faceLoc, 'autenticado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    return jsonify(results)

def person_listener(event):
    print('Novo registro adicionado à coleção Person')
    print('Evento recebido:', event.event_type, event.path, event.data)
    subprocess.call(["python", os.path.join(os.path.dirname(__file__), "EncodeGenerator.py")])
    load_encodings() 

def start_listener():
    person_ref = db.reference('Person')
    person_ref.listen(person_listener)

if __name__ == '__main__':
    threading.Thread(target=start_listener).start()
    app.run(host="0.0.0.0", port=5000)
