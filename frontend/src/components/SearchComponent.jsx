import React, { useState } from 'react'
import { Search, Loader2, AlertCircle } from 'lucide-react'
import axios from 'axios'

const SearchComponent = ({ onResults, onLoading }) => {
  const [medicineName, setMedicineName] = useState('')
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    
    if (!medicineName.trim()) {
      setError('Please enter a medicine name')
      return
    }

    setError('')
    onLoading(true)

    try {
      const response = await axios.post('/api/search', {
        medicine_name: medicineName.trim()
      })

      onResults(response.data)
    } catch (err) {
      console.error('Search error:', err)
      setError('Failed to search medicine. Please try again.')
    } finally {
      onLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setMedicineName(e.target.value)
    if (error) setError('')
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Search for Medicine
        </h2>
        <p className="text-gray-600">
          Enter a medicine name to find alternatives and compare prices
        </p>
      </div>

      <form onSubmit={handleSearch} className="space-y-4">
        <div>
          <label htmlFor="medicine-search" className="block text-sm font-medium text-gray-700 mb-2">
            Medicine Name
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              id="medicine-search"
              type="text"
              value={medicineName}
              onChange={handleInputChange}
              placeholder="e.g., Dolo 650, Paracetamol, Crocin..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 placeholder-gray-500"
            />
          </div>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
            <AlertCircle className="h-5 w-5" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        <button
          type="submit"
          className="w-full btn-primary flex items-center justify-center space-x-2"
        >
          <Search className="h-5 w-5" />
          <span>Search Medicine</span>
        </button>
      </form>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Pro Tips</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Try both brand names (Dolo 650) and generic names (Paracetamol)</li>
          <li>• Include dosage information for better matches</li>
          <li>• Check spelling for accurate results</li>
          <li>• Use scan feature for prescription images</li>
        </ul>
      </div>
    </div>
  )
}

export default SearchComponent
