import React, { useState } from 'react'
import { Search, AlertCircle } from 'lucide-react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL

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
      const response = await axios.post(`${API}/api/search`, {
        medicine_name: medicineName.trim()
      })

      onResults(response.data)

    } catch (err) {
      console.error('Search error:', err)

      setError(err.response?.data?.error || 'Search failed')
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

      <h2 className="text-2xl font-bold mb-4">
        Search Medicine
      </h2>

      <form onSubmit={handleSearch} className="space-y-4">

        <input
          type="text"
          value={medicineName}
          onChange={handleInputChange}
          placeholder="e.g. Dolo 650, Crocin"
          className="w-full border p-3 rounded-lg"
        />

        {error && (
          <div className="text-red-600 flex items-center gap-2">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        <button className="btn-primary w-full flex justify-center items-center gap-2">
          <Search size={18} />
          Search
        </button>

      </form>

    </div>
  )
}

export default SearchComponent