import React, { useState } from 'react'
import { Camera, Upload, AlertCircle } from 'lucide-react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL

const OCRComponent = ({ onResults, onLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState('')
  const [error, setError] = useState('')
  const [isDragging, setIsDragging] = useState(false)

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setPreview(URL.createObjectURL(file))
      setError('')
    } else {
      setError('Please select a valid image file')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    handleFileSelect(e.dataTransfer.files[0])
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleFileChange = (e) => {
    handleFileSelect(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    setError('')
    onLoading(true)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await axios.post(`${API}/api/scan`, formData)

      onResults(response.data)

    } catch (err) {
      console.error('OCR error:', err)
      setError(err.response?.data?.error || 'Scan failed')
    } finally {
      onLoading(false)
    }
  }

  const resetUpload = () => {
    setSelectedFile(null)
    setPreview('')
    setError('')
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-4">Scan Prescription</h2>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`border-2 border-dashed p-6 rounded-lg text-center ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
      >

        {preview ? (
          <>
            <img src={preview} className="mx-auto max-h-60 mb-4" />

            <button onClick={handleUpload} className="btn-primary mr-2">
              Scan
            </button>

            <button onClick={resetUpload} className="btn-secondary">
              Reset
            </button>
          </>
        ) : (
          <>
            <p className="mb-3">Upload or drag image</p>

            <input type="file" onChange={handleFileChange} />
          </>
        )}
      </div>

      {error && (
        <div className="text-red-600 mt-4 flex items-center gap-2">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

    </div>
  )
}

export default OCRComponent