import { useState, useRef, useEffect } from "react";
import axios from "axios";

function AuthPage() {
  const [result, setResult] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const getUserMedia = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        videoRef.current.srcObject = stream;
      } catch (error) {
        console.error("Error accessing webcam:", error);
      }
    };

    getUserMedia();

    const intervalId = setInterval(handleCapture, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL("image/png");
  };

  const handleCapture = async () => {
    const imageData = captureImage();
    const blob = await fetch(imageData).then((res) => res.blob());
    const formData = new FormData();
    formData.append("image", blob);

    try {
      const response = await axios.post(
        // api do fly.io https://face-recognition-py-snowy-dream-6989.fly.dev/detect
        '/api/detect',  //api local
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResult(response.data);
    } catch (error) {
      console.error("Error detecting faces:", error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen overflow-y-hidden">
      <div className="flex flex-col items-center text-center p-8 rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4">Face Recognition</h1>
        <video
          ref={videoRef}
          width="640"
          height="480"
          autoPlay
          className="mb-4 border border-gray-300 rounded"
        ></video>
        <canvas
          ref={canvasRef}
          width="640"
          height="480"
          style={{ display: "none" }}
        ></canvas>

        {result && result.length > 0 ? (
          <div className="w-full">
            {result.map((person, index) => (
              <div
                key={index}
                className="mb-4 border border-gray-300 p-4 rounded"
              >
                <h2 className="text-xl font-semibold mb-2">
                  Identified Person:
                </h2>

                <p className="text-lg font-bold">Name: {person.name}</p>
                <p>Email: {person.email}</p>
                <p>ID: {person.id}</p>
                <p>Autenticado em: {person.autenticado_em}</p>  {/* Atualizado para exibir autenticado_em */}
              </div>
            ))}
          </div>
        ) : null}
        {/* Exibe mensagem quando não há resultados */}
        {result && result.length === 0 && (
          <div className="w-full">
            <h2 className="text-xl font-semibold mb-2">No Results</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default AuthPage;
