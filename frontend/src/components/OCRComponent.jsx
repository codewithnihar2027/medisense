import React, { useState } from 'react'
import { Camera, Upload, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import axios from 'axios'

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
    const file = e.dataTransfer.files[0]
    handleFileSelect(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    handleFileSelect(file)
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
      const response = await axios.post('/api/scan', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onResults(response.data)
    } catch (err) {
      console.error('OCR error:', err)
      setError('Failed to process image. Please try again.')
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
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Scan Prescription
        </h2>
        <p className="text-gray-600">
          Upload a prescription image to automatically detect medicines
        </p>
      </div>

      {/* Upload Area */}
      <div className="space-y-4">
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          {preview ? (
            <div className="space-y-4">
              <img
                src={preview}
                alt="Prescription preview"
                className="mx-auto max-h-64 rounded-lg shadow-md"
              />
              <div className="flex justify-center space-x-3">
                <button
                  onClick={handleUpload}
                  className="btn-primary flex items-center space-x-2"
                >
                  <Camera className="h-5 w-5" />
                  <span>Process Image</span>
                </button>
                <button
                  onClick={resetUpload}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <Upload className="h-5 w-5" />
                  <span>Choose Another</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <Camera className="mx-auto h-12 w-12 text-gray-400" />
              <div>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  Drop prescription image here
                </p>
                <p className="text-sm text-gray-600 mb-4">or</p>
                <label className="btn-secondary cursor-pointer inline-flex items-center space-x-2">
                  <Upload className="h-5 w-5" />
                  <span>Browse Files</span>
                  <input
                    type="file"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="hidden"
                  />
                </label>
              </div>
              <p className="text-xs text-gray-500">
                Supports: JPG, PNG, GIF (Max 10MB)
              </p>
            </div>
          )}
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
            <AlertCircle className="h-5 w-5" />
            <span className="text-sm">{error}</span>
          </div>
        )}
      </div>

      <div className="mt-6 space-y-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">📸 Tips for Best Results</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Ensure good lighting and clear focus</li>
            <li>• Place prescription on flat surface</li>
            <li>• Avoid shadows and glare</li>
            <li>• Crop to show only prescription text</li>
            <li>• Supported formats: JPG, PNG, GIF</li>
          </ul>
        </div>

        <div className="p-4 bg-yellow-50 rounded-lg">
          <h3 className="font-semibold text-yellow-900 mb-2">🔒 Privacy Notice</h3>
          <p className="text-sm text-yellow-800">
            Images are processed locally and not stored. Your prescription data remains private.
          </p>
        </div>
      </div>
    </div>
  )
}

export default OCRComponent
