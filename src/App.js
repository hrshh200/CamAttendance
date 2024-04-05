import React, { useRef, useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';

const WebcamCapture = () => {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [record, setRecorded] = useState("Not Recorded")
  const [iconData, setIconData] = useState(<FontAwesomeIcon icon={faTimesCircle} style={{ color: 'red' }} />);

  useEffect(() => {
    const initStream = new MediaStream();
    videoRef.current.srcObject = initStream;
    setStream(initStream);
  }, []);

  const startCapture = () => {
    const constraints = { video: true };

    navigator.mediaDevices.getUserMedia(constraints)
      .then(mediaStream => {
        videoRef.current.srcObject = mediaStream;
        setStream(mediaStream);
      })
      .catch(error => {
        console.error('Error accessing webcam:', error);
      });
  };


  const stopCapture = () => {
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      setStream(null);
    }
  };

  const takePicture = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    // Remove the prefix 'data:image/png;base64,' from the base64 string
    const base64Data = imageData.replace(/^data:image\/png;base64,/, '');

    // Convert the base64 data to a Blob object
    const blob = b64toBlob(base64Data, 'image/png');

    // Create a FormData object
    const formData = new FormData();
    formData.set('k1', blob); // Append the image data with key 'k1' to the FormData object

    try {
      // Make a POST request to your API endpoint
      const response = await axios.post('http://localhost:5000/predict', formData);
      console.log('Response from API:', response.data);
      if (response.data.Message === "Identified:Harsh") {
        setRecorded("Recorded");
        setIconData(<FontAwesomeIcon icon={faCheckCircle} style={{ color: 'green' }} />);
      }

      // You can handle the response from the API here
    } catch (error) {
      console.error('Error sending data to API:', error);
      // Handle errors here
    }
  };

  // Function to convert base64 data to a Blob object
  const b64toBlob = (b64Data, contentType = '', sliceSize = 512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      const slice = byteCharacters.slice(offset, offset + sliceSize);

      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }

    const blob = new Blob(byteArrays, { type: contentType });
    return blob;
  };


  return (
    <div>
      <center><h1>Cam Attendance</h1></center>
      <div className="videoframe-container">
        <div className="videoframe">
          <div className="container">
            <div className="video-container">
              <video ref={videoRef} autoPlay />
            </div>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Harsh</td>
                  <td>{iconData}{record}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="button-container">
            <button className="start-button" onClick={startCapture}>Start</button>
            <button className="stop-button" onClick={stopCapture}>Stop</button>
            <button className='record-button' onClick={takePicture}>Record</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebcamCapture;
