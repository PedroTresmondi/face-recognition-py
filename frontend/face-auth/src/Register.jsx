import React, { useState } from "react";
import Webcam from "react-webcam";
import { getDatabase, ref, set } from "firebase/database";
import {
  getStorage,
  ref as storageReference,
  uploadBytes,
} from "firebase/storage";
import { app } from "./firebase/firebaseConfig";

const generateUniqueId = () => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

const RegisterPage = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [imageSrc, setImageSrc] = useState(null);
  const [step, setStep] = useState(1);
  const webcamRef = React.useRef(null);
  const database = getDatabase(app);
  const storage = getStorage(app);

  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImageSrc(imageSrc);
  }, [webcamRef]);

  const handleSave = async () => {
    try {
      const userId = generateUniqueId();
      const newUserRef = ref(database, `Person/${userId}`);
      await set(newUserRef, {
        name: name,
        email: email,
        photoId: userId,
      });

      if (imageSrc) {
        await saveImageToStorage(userId, imageSrc);
      }

      alert("Usuário registrado com sucesso!");
      setName("");
      setEmail("");
      setImageSrc(null);
      setStep(1);
    } catch (error) {
      console.error("Erro ao registrar usuário:", error);
      alert(
        "Erro ao registrar usuário. Verifique o console para mais detalhes."
      );
    }
  };

  const saveImageToStorage = async (userId, imageSrc) => {
    try {
      const resizedImage = await resizeImage(imageSrc, 216, 216);
      const blobImage = await fetch(resizedImage).then((res) => res.blob());
      const imageRef = storageReference(storage, `Images/${userId}.png`);
      await uploadBytes(imageRef, blobImage);
    } catch (error) {
      console.error("Erro ao salvar imagem no Storage:", error);
      throw error;
    }
  };

  const resizeImage = async (imageSrc, maxWidth, maxHeight) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement("canvas");
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }

        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob((blob) => {
          resolve(URL.createObjectURL(blob));
        }, "image/jpeg");
      };
      img.src = imageSrc;
    });
  };

  const nextStep = () => {
    if (step === 1 && name && email) {
      setStep(2);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 className="text-2xl font-bold mb-4">Cadastro de Usuário</h2>
      {step === 1 && (
        <div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Nome:
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              E-mail:
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>
          <button
            onClick={nextStep}
            disabled={!name || !email}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
          >
            Próximo
          </button>
        </div>
      )}
      {step === 2 && (
        <div>
          <div className="relative mb-4">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/png"
              width={640}
              height={480}
              className="w-full h-full border border-gray-300 rounded"
            />

            <div className="absolute top-1/2 left-1/2 w-54 h-54 -mt-27 -ml-27 border-2 border-red-500 box-border" />
          </div>
          <button
            onClick={capture}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-4"
          >
            Capturar Foto
          </button>
          {imageSrc && <img src={imageSrc} alt="Captured" className="mb-4" />}
          {imageSrc && (
            <button
              onClick={handleSave}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Enviar
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default RegisterPage;
