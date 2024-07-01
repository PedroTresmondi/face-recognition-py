import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

function AuthPage() {
  const [result, setResult] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const getUserMedia = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;
      } catch (error) {
        console.error('Error accessing webcam:', error);
      }
    };
    getUserMedia();

    const intervalId = setInterval(handleCapture, 1000); 

    return () => clearInterval(intervalId);
  }, []);

  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/png');
  };

  const handleCapture = async () => {
    const imageData = captureImage();
    const blob = await fetch(imageData).then(res => res.blob());
    const formData = new FormData();
    formData.append('image', blob);

    try {
      const response = await axios.post('http://localhost:5000/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error detecting faces:', error);
    }
  };

  return (
    <div>
      <h1>Face Recognition</h1>
      <video ref={videoRef} width="640" height="480" autoPlay></video>
      <canvas ref={canvasRef} width="640" height="480" style={{ display: 'none' }}></canvas>
      {result && result.length > 0 ? (
        <div>
          <h2>Identified Person:</h2>
          {result.map((person, index) => (
            <div key={index} style={{ marginBottom: '20px', border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
              <p style={{ fontSize: '1.5em', fontWeight: 'bold' }}>Name: {person.name}</p>
              <p>Email: {person.email}</p>
              <p>ID: {person.id}</p>
              <p>Authentication Time: {person.time}</p>
            </div>
          ))}
        </div>
      ) : (
        <div>
          <h2>Results:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default AuthPage;
