import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [responseFile, setResponseFile] = useState(null);

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
      const response = await axios.post('http://localhost:8080/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
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
    <div>
      <h1>Upload Excel File</h1>
      <input type="file" onChange={handleFileChange} accept=".xlsx,.xls" />
      <button onClick={handleUpload}>Upload and Download Processed File</button>
    </div>
  );
}


export default FileUpload;