import React from 'react'
import { 
  Pill, 
  IndianRupee,   // ✅ FIXED
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
          <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
          <span className="text-gray-600">Searching for alternatives...</span>
        </div>
      </div>
    )
  }

  if (!results) return null

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

      {/* MAIN MEDICINE */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-start justify-between mb-4">

          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center space-x-2">
              <Pill className="h-6 w-6 text-blue-600" />
              <span>
                {results?.matched_medicine || results?.input_medicine}
              </span>
            </h2>

            {results?.generic_equivalent && (
              <p className="text-gray-600 mt-1">
                Generic: {results.generic_equivalent}
              </p>
            )}
          </div>

          <div className="text-right">
            <div className="text-3xl font-bold text-gray-900 flex items-center space-x-1">
              <IndianRupee className="h-8 w-8" /> {/* ✅ FIXED */}
              <span>{results?.price}</span>
            </div>
            <p className="text-sm text-gray-600">Current Price</p>
          </div>

        </div>

        {/* AFFORDABILITY */}
        {results?.affordability_score && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <div className="flex justify-between">
              <div>
                <h3 className="font-semibold text-green-900">Affordability Score</h3>
                <p className="text-sm text-green-700">Higher = More savings</p>
              </div>
              <div className="text-2xl font-bold text-green-600">
                {results.affordability_score}/10
              </div>
            </div>
          </div>
        )}

        {results?.note && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-700">{results.note}</p>
          </div>
        )}

        {results?.ai_explanation && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mt-3">
            <p className="text-sm text-purple-700">{results.ai_explanation}</p>
          </div>
        )}
      </div>

      {/* ALTERNATIVES */}
      {results?.alternatives?.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">

          <h3 className="text-xl font-bold mb-4 flex items-center space-x-2">
            <TrendingDown className="h-6 w-6 text-green-600" />
            <span>Cheaper Alternatives</span>
          </h3>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

            {results.alternatives.map((alt, index) => (
              <div key={index} className="border rounded-lg p-4">

                <h4 className="font-semibold">{alt.brand_name}</h4>

                <p className="text-green-600 font-bold flex items-center">
                  <IndianRupee className="h-4 w-4" /> {/* ✅ FIXED */}
                  {alt.price}
                </p>

                {alt.manufacturer && (
                  <p className="text-sm text-gray-500">{alt.manufacturer}</p>
                )}

                {alt.savings_percent && (
                  <p className="text-green-600 text-sm">
                    Save {alt.savings_percent}%
                  </p>
                )}

                {results.cheapest_option === alt.brand_name && (
                  <div className="text-green-600 text-sm flex items-center mt-2">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    Best Price
                  </div>
                )}

              </div>
            ))}

          </div>

          <div className="mt-4 bg-yellow-50 p-4 rounded-lg text-sm">
            <p>Original: ₹{results.price}</p>
            <p>Cheapest: ₹{results.cheapest_price}</p>
            <p>
              Save: ₹{(results.price - results.cheapest_price).toFixed(2)}
            </p>
          </div>

        </div>
      )}

    </div>
  )
}

export default ResultsComponent