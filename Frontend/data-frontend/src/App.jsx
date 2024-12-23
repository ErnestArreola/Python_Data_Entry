import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [responseFile, setResponseFile] = useState(null);
  const [message, setMessage] = useState('');

  //https://python-data-entry.onrender.com/upload

  useEffect(() => {
    // Axios GET request to the Flask backend
    axios.get('https://python-data-entry.onrender.com', {headers: {"Access-Control-Allow-Origin": "*"}}) 
      .then(response => {
        // Extracting the 'message' field from the JSON response
        setMessage(response.data.message);
        console.log(response);
      })
      .catch(error => {
        console.error("There was an error fetching the message:", error);
      });
  }, []); // Empty dependency array means this will run only once (on component mount)



  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Sending the file to the Flask server
      const response = await axios.post('https://python-data-entry.onrender.com/upload', formData, {
        headers: {
          'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        },
        responseType: 'blob' // Ensure that the response is a binary file (Excel file)
      });

      // Handle the received file (Excel file)
      const receivedBlob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(receivedBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'processed_file.xlsx'; // Name of the file when downloaded
      link.click();
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <>
    <div>
      <h1>Upload Excel File</h1>
      <input type="file" onChange={handleFileChange} accept=".xlsx,.xls" />
      <button onClick={handleUpload}>Upload and Download Processed File</button>
    </div>
    <div>
      <h1>{message}</h1>
    </div>
    </>
  );
}


export default FileUpload;