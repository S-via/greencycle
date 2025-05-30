
import React, { useState } from 'react';


export default function UploadForm() {
  const [fileSelect, setFileSelect] = useState(null);
  const [previewFile, setPreviewFile] = useState(null);
  const [upload, setUpload] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFileSelect(file);
    setPreviewFile(URL.createObjectURL(file));
    setMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!fileSelect) {
      setMessage('Please select a file');
      return;
    }

    setUpload(true);

    const formData = new FormData();
    formData.append('image', fileSelect);

    try {
      const response = await fetch(process.env.REACT_APP_API_URL + '/uploaded', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setMessage(data.message || 'Upload successful');
    } catch (error) {
      console.error(error);
      setMessage('Upload failed. Please try again.');
    } finally {
      setUpload(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='upload-form'>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {previewFile && (
        <img
          src={previewFile}
          alt="preview"
          style={{ maxWidth: '300px', marginTop: '10px' }}
        />
      )}
      <button type="submit" disabled={upload} className='upload-button'>
        {upload ? 'Uploading...' : 'Upload'}
      </button>
      {message && <p>{message}</p>}
    </form>
  );
}














