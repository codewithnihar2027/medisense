import React from 'react'
import { 
  Pill, 
  Rupee, 
  TrendingDown, 
  CheckCircle, 
  AlertTriangle,
  Info,
  Loader2
} from 'lucide-react'

const ResultsComponent = ({ results, loading }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center justify-center space-x-3">
          <Loader2 className="h-6 w-6 animate-spin text-primary-600" />
          <span className="text-gray-600">Searching for alternatives...</span>
        </div>
      </div>
    )
  }

  if (!results) {
    return null
  }

  // Handle error case
  if (results.error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center space-x-3 text-red-600">
          <AlertTriangle className="h-6 w-6" />
          <div>
            <h3 className="font-semibold">Search Error</h3>
            <p className="text-sm mt-1">{results.error}</p>
          </div>
        </div>
      </div>
    )
  }

  // Handle no alternatives found case
  if (results.note && results.note.includes('No valid alternatives')) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center space-x-3 text-yellow-600">
          <AlertTriangle className="h-6 w-6" />
          <div>
            <h3 className="font-semibold">No Alternatives Found</h3>
            <p className="text-sm mt-1">{results.note}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Main Medicine Info */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center space-x-2">
              <Pill className="h-6 w-6 text-primary-600" />
              <span>{results.matched_medicine || results.medicine}</span>
            </h2>
            <p className="text-gray-600 mt-1">
              {results.generic_equivalent && `Generic: ${results.generic_equivalent}`}
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-gray-900 flex items-center space-x-1">
              <Rupee className="h-8 w-8" />
              <span>{results.price}</span>
            </div>
            <p className="text-sm text-gray-600">Current Price</p>
          </div>
        </div>

        {/* Affordability Score */}
        {results.affordability_score && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-green-900">Affordability Score</h3>
                <p className="text-sm text-green-700">Higher score = More savings available</p>
              </div>
              <div className="text-2xl font-bold text-green-600">
                {results.affordability_score}/10
              </div>
            </div>
          </div>
        )}

        {/* Status Note */}
        {results.note && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-2">
              <Info className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-semibold text-blue-900">Search Result</h4>
                <p className="text-sm text-blue-700 mt-1">{results.note}</p>
              </div>
            </div>
          </div>
        )}

        {/* AI Enhancement */}
        {results.ai_explanation && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-start space-x-2">
              <Info className="h-5 w-5 text-purple-600 mt-0.5" />
              <div>
                <h4 className="font-semibold text-purple-900">AI Analysis</h4>
                <p className="text-sm text-purple-700 mt-1">{results.ai_explanation}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Alternatives Section */}
      {results.alternatives && results.alternatives.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center space-x-2">
            <TrendingDown className="h-6 w-6 text-green-600" />
            <span>Cheaper Alternatives</span>
          </h3>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {results.alternatives.map((alternative, index) => (
              <div 
                key={index} 
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-gray-900">{alternative.brand_name}</h4>
                  <div className="text-lg font-bold text-green-600 flex items-center space-x-1">
                    <Rupee className="h-5 w-5" />
                    <span>{alternative.price}</span>
                  </div>
                </div>

                {alternative.manufacturer && (
                  <p className="text-sm text-gray-600 mb-2">
                    Manufacturer: {alternative.manufacturer}
                  </p>
                )}

                {alternative.savings_percent && (
                  <div className="flex items-center space-x-2 text-green-600 bg-green-50 px-2 py-1 rounded">
                    <TrendingDown className="h-4 w-4" />
                    <span className="text-sm font-medium">
                      Save {alternative.savings_percent}%
                    </span>
                  </div>
                )}

                {results.cheapest_option === alternative.brand_name && (
                  <div className="flex items-center space-x-2 text-green-600 mt-2">
                    <CheckCircle className="h-4 w-4" />
                    <span className="text-sm font-medium">Best Price!</span>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <h4 className="font-semibold text-yellow-900 mb-2">💰 Savings Summary</h4>
            <div className="text-sm text-yellow-800">
              <p>• Original: ₹{results.price}</p>
              <p>• Cheapest: ₹{results.cheapest_price}</p>
              <p>• You save: ₹{(results.price - results.cheapest_price).toFixed(2)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsComponent
