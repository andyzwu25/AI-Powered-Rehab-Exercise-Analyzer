# Exercise Form Analyzer - Setup Guide

This guide will help you set up and run the Exercise Form Analyzer web application.

## Prerequisites

### For Backend (Python)
- Python 3.8 or higher
- pip (Python package manager)

### For Frontend (React)
- Node.js 18 or higher
- npm (Node package manager)

## Installation Steps

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

The backend will be running at `http://localhost:5000`

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will be running at `http://localhost:3000`

## Usage

1. Open your browser and go to `http://localhost:3000`
2. You'll see the home page with information about the app
3. Click "Start Analyzing" or navigate to the Analysis page
4. Upload a video or image of your exercise
5. Click "Analyze Exercise" to get form feedback
6. View the results with score and suggestions

## Supported File Types

### Videos
- MP4
- AVI
- MOV

### Images
- JPG/JPEG
- PNG
- GIF

## Supported Exercises

Currently, the app supports analysis for:
- Pull-ups
- Push-ups
- Squats
- Deadlifts
- Planks

## Features

- **Real-time Analysis**: Upload videos or images for instant form analysis
- **AI-Powered Detection**: Uses MediaPipe for accurate pose detection
- **Form Scoring**: Get a numerical score (0-100) for your form
- **Personalized Feedback**: Receive specific suggestions for improvement
- **Exercise Tips**: Access detailed form tips for each exercise
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## Troubleshooting

### Backend Issues
- Make sure Python 3.8+ is installed
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is available
- For MediaPipe issues, try: `pip install mediapipe --upgrade`

### Frontend Issues
- Make sure Node.js 18+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that port 3000 is available

### Analysis Issues
- Ensure the uploaded file is a supported format
- Make sure the person is clearly visible in the video/image
- Try different lighting conditions if pose detection fails
- Keep the file size under 16MB

## Development

### Backend Development
- The main Flask app is in `backend/app.py`
- Pose analysis logic is in `backend/app/models/pose_analyzer.py`
- Utility functions are in `backend/app/utils/`

### Frontend Development
- Main app component is in `frontend/src/App.tsx`
- Pages are in `frontend/src/pages/`
- Components are in `frontend/src/components/`
- API services are in `frontend/src/services/`

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze` - Analyze uploaded exercise file
- `GET /api/exercises` - Get list of supported exercises
- `GET /api/exercise/<id>/tips` - Get tips for specific exercise

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details 