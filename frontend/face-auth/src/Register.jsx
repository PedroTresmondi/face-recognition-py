import React, { useState } from 'react';
import Webcam from 'react-webcam';
import { getDatabase, ref, set } from 'firebase/database';
import { getStorage, ref as storageReference, uploadBytes } from 'firebase/storage';
import { app } from './firebase/firebaseConfig'; 

const generateUniqueId = () => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
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
        photoId: userId
      });

      if (imageSrc) {
        await saveImageToStorage(userId, imageSrc);
      }

      alert('Usuário registrado com sucesso!');
      setName('');
      setEmail('');
      setImageSrc(null);
    } catch (error) {
      console.error('Erro ao registrar usuário:', error);
      alert('Erro ao registrar usuário. Verifique o console para mais detalhes.');
    }
  };

  const saveImageToStorage = async (userId, imageSrc) => {
    try {
      const resizedImage = await resizeImage(imageSrc, 216, 216);
      const blobImage = await fetch(resizedImage).then(res => res.blob());
      const imageRef = storageReference(storage, `Images/${userId}.png`);
      await uploadBytes(imageRef, blobImage);
    } catch (error) {
      console.error('Erro ao salvar imagem no Storage:', error);
      throw error;
    }
  };

  const resizeImage = async (imageSrc, maxWidth, maxHeight) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
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

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(blob => {
          resolve(URL.createObjectURL(blob));
        }, 'image/jpeg');
      };
      img.src = imageSrc;
    });
  };

  return (
    <div>
      <h2>Cadastro de Usuário</h2>
      <div>
        <label>Nome:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <label>E-mail:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div style={{ position: 'relative', width: '612px', height: '480px' }}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/png"
          width={612}
          height={480}
        />
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: '216px',
          height: '216px',
          marginTop: '-108px',
          marginLeft: '-108px',
          border: '2px solid red',
          boxSizing: 'border-box',
        }} />
      </div>
      <button onClick={capture}>Capturar Foto</button>
      {imageSrc && <img src={imageSrc} alt="Captured" />}
      <button onClick={handleSave}>Salvar</button>
    </div>
  );
};

export default RegisterPage;
