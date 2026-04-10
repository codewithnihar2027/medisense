import React, { useState } from 'react'
import SearchComponent from './components/SearchComponent'
import ResultsComponent from './components/ResultsComponent'
import OCRComponent from './components/OCRComponent'
import { Search, Camera, Pill } from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('search')
  const [searchResults, setSearchResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearchResults = (results) => {
    setSearchResults(results)
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Pill className="h-8 w-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">MediSense</h1>
            </div>
            <p className="text-sm text-gray-600">Affordable Medicine Intelligence</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-8 bg-white rounded-lg shadow-sm p-1 w-fit">
          <button
            onClick={() => setActiveTab('search')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'search'
                ? 'bg-primary-600 text-white'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            <Search className="h-4 w-4" />
            <span>Search Medicine</span>
          </button>
          <button
            onClick={() => setActiveTab('ocr')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'ocr'
                ? 'bg-primary-600 text-white'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            <Camera className="h-4 w-4" />
            <span>Scan Prescription</span>
          </button>
        </div>

        {/* Tab Content */}
        <div className="space-y-8">
          {activeTab === 'search' && (
            <SearchComponent 
              onResults={handleSearchResults} 
              onLoading={handleLoading}
            />
          )}
          
          {activeTab === 'ocr' && (
            <OCRComponent 
              onResults={handleSearchResults} 
              onLoading={handleLoading}
            />
          )}

          {/* Results Display */}
          {searchResults && (
            <ResultsComponent 
              results={searchResults} 
              loading={loading}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-sm text-gray-600">
            <p>© 2024 MediSense. Built during hackathon for affordable healthcare.</p>
            <p className="mt-2">⚠️ Medical decisions should always be verified by professionals.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
