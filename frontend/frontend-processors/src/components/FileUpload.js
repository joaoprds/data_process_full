import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

function FileUpload() {
  const [bills, setBills] = useState(null);
  const [legislators, setLegislators] = useState(null);
  const [votes, setVotes] = useState(null);
  const [voteResults, setVoteResults] = useState(null);

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (name === 'bills') setBills(files[0]);
    if (name === 'legislators') setLegislators(files[0]);
    if (name === 'votes') setVotes(files[0]);
    if (name === 'voteResults') setVoteResults(files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('bills', bills);
    formData.append('legislators', legislators);
    formData.append('votes', votes);
    formData.append('vote_results', voteResults);

    try {
      const response = await axios.post('http://localhost:5000/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">Upload Legislative Data</h1>
      <form onSubmit={handleSubmit}>
        <div className="upload-section">
          <h2>Bills</h2>
          <input type="file" name="bills" onChange={handleFileChange} required />
        </div>
        <div className="upload-section">
          <h2>Legislators</h2>
          <input type="file" name="legislators" onChange={handleFileChange} required />
        </div>
        <div className="upload-section">
          <h2>Votes</h2>
          <input type="file" name="votes" onChange={handleFileChange} required />
        </div>
        <div className="upload-section">
          <h2>Vote Results</h2>
          <input type="file" name="voteResults" onChange={handleFileChange} required />
        </div>
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default FileUpload;
