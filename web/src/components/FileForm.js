import { useState } from 'react';
import './FileForm.css'

function FileForm() {
  const [file, setFile] = useState(null);
  const [classValue, setClassValue] = useState(null);
  const [confidenceValue, setConfidenceValue] = useState(null);

  const handleFileInputChange = (event) => {
    console.log(event.target.files);
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = "http://localhost:8000/predict";
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const resultData = await response.json();
        console.log("File uploaded successfully!", resultData);

        // Update state with class and confidence values
        if (resultData && resultData.class && resultData.confidence) {
          setClassValue(resultData.class);
          setConfidenceValue(resultData.confidence);
        } else {
          console.error("Class or confidence values not found in the response.");
        }
      } else {
        console.error("Failed to upload file.");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className='wrapper'>
      <h1>PROTEGER</h1>
      <form onSubmit={handleSubmit}>
        <div className='inputImg'>
          <input type="file" onChange={handleFileInputChange}  />
        </div>
        <div>
          <button className="uploadBtn" type="submit">Upload</button>
        </div>

      </form>

      {classValue !== null && confidenceValue !== null && (
        <div className='result'> 
          <p>Diesese type: {classValue}</p>
        
          <p> Accuracy: {confidenceValue * 100}</p>
        </div>
      )} 




        
      
     


    </div>
  );
}

export default FileForm;
