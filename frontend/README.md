# MediSense Frontend

## Quick Start

### Prerequisites
- Node.js 16+ and npm
- Backend server running on http://localhost:8000

### Installation & Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

3. **Open browser:**
Navigate to http://localhost:5173

### Features

- 🔍 **Medicine Search** - Text-based search with dataset + internet fallback
- 📷 **OCR Scanner** - Upload prescription images for automatic detection
- 💰 **Price Comparison** - Compare medicine prices and find savings
- 🤖 **AI Analysis** - Enhanced medicine explanations
- 📊 **Affordability Score** - Visual savings indicators

### Components Structure

```
src/
├── components/
│   ├── SearchComponent.jsx    # Medicine search interface
│   ├── OCRComponent.jsx       # Image upload & OCR
│   └── ResultsComponent.jsx   # Results display
├── App.jsx                  # Main app with tabs
├── main.jsx                 # App entry point
└── index.css                # Tailwind styles
```

### API Integration

The frontend connects to these backend endpoints:
- `POST /api/search` - Search medicine
- `POST /api/scan` - OCR image processing

### Styling

- Built with **TailwindCSS** for modern, responsive design
- **Lucide React** icons for consistent UI
- Mobile-first responsive layout
- Accessibility-focused semantic HTML

### Development Notes

- Vite dev server with HMR
- Proxy configured for API calls to backend
- Error handling and loading states
- Form validation and user feedback
