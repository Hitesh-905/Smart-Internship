import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  // 1. Handle File Selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setResult(null) // Reset previous results
  }

  // 2. Handle Upload Button Click
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF first!")
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      // We will define the URL in the next phase, 
      // for now, we point to where our backend LIVES.
      const response = await axios.post("http://127.0.0.1:8000/upload_resume/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResult(response.data)
    } catch (error) {
      console.error("Error uploading file:", error)
      alert("Error connecting to the AI Brain. (We will fix this in Phase 5!)")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1>🚀 Smart Internship Engine</h1>
      <p>Upload your resume to see if you match the job!</p>

      <div className="upload-box">
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>

      {result && (
        <div className="result-box">
          <h2>Analysis Result</h2>
          <div className="score-card">
            <span className="score-label">Match Score:</span>
            <span className="score-value">{result.match_score}%</span>
          </div>
          <p><strong>Matched Against:</strong> {result.matched_against}</p>
          <div className="snippet">
            <strong>Resume Snippet:</strong>
            <p>"{result.extracted_text_snippet}"</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App