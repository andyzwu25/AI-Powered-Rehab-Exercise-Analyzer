import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, Camera, TrendingUp, Users } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* New Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Analyze Your Form, Perfect Your Lifts
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Select an exercise below, upload your video, and get instant, AI-powered feedback.
        </p>
      </div>

      {/* Choose Your Exercise Section */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
          Choose Your Exercise
        </h2>
        <div className="grid md:grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Pull-up Card */}
          <div className="bg-white p-6 rounded-xl shadow-lg exercise-card">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Pull-up</h3>
            <div className="mb-4">
              <h4 className="font-semibold mb-2">Video Requirements:</h4>
              <ul className="list-disc list-inside text-gray-600 text-sm">
                <li>Ensure your entire body is visible from the side.</li>
                <li>Make sure your face is in view for nose detection.</li>
                <li>Use a stable camera with good lighting.</li>
              </ul>
            </div>
            <Link
              to="/analysis?exercise=pull_up"
              className="w-full inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Upload className="mr-2 h-5 w-5" />
              Analyze Pull-up
            </Link>
          </div>

          {/* Push-up Card */}
          <div className="bg-white p-6 rounded-xl shadow-lg exercise-card">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Push-up</h3>
            <div className="mb-4">
              <h4 className="font-semibold mb-2">Video Requirements:</h4>
              <ul className="list-disc list-inside text-gray-600 text-sm">
                <li>Ensure your entire body is visible from the side.</li>
                <li>Place the camera at a height level with your body.</li>
                <li>Use a stable camera with good lighting.</li>
              </ul>
            </div>
            <Link
              to="/analysis?exercise=push_up"
              className="w-full inline-flex items-center justify-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors"
            >
              <Upload className="mr-2 h-5 w-5" />
              Analyze Push-up
            </Link>
          </div>

          {/* Squat Card */}
          <div className="bg-white p-6 rounded-xl shadow-lg exercise-card">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Squat</h3>
            <div className="mb-4">
              <h4 className="font-semibold mb-2">Video Requirements:</h4>
              <ul className="list-disc list-inside text-gray-600 text-sm">
                <li>Ensure your entire body is visible from the side.</li>
                <li>Capture your full range of motion.</li>
                <li>Use a stable camera with good lighting.</li>
              </ul>
            </div>
            <Link
              to="/analysis?exercise=squat"
              className="w-full inline-flex items-center justify-center px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors"
            >
              <Upload className="mr-2 h-5 w-5" />
              Analyze Squat
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 py-12">
        <div className="text-center p-6 bg-white rounded-xl shadow-sm">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Camera className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Video & Image Support</h3>
          <p className="text-gray-600">
            Upload videos or images of your exercises. We support MP4, AVI, MOV, JPG, PNG, and more.
          </p>
        </div>

        <div className="text-center p-6 bg-white rounded-xl shadow-sm">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="h-8 w-8 text-green-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-time Analysis</h3>
          <p className="text-gray-600">
            Get instant feedback on your form with detailed analysis of joint angles and body positioning.
          </p>
        </div>

        <div className="text-center p-6 bg-white rounded-xl shadow-sm">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="h-8 w-8 text-purple-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Personalized Tips</h3>
          <p className="text-gray-600">
            Receive specific suggestions to improve your form and prevent injuries.
          </p>
        </div>
      </div>

      {/* Supported Exercises */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
          Supported Exercises
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { name: 'Pull-ups', difficulty: 'Intermediate', description: 'Upper body strength' },
            { name: 'Push-ups', difficulty: 'Beginner', description: 'Chest and triceps' },
            { name: 'Squats', difficulty: 'Beginner', description: 'Lower body strength' },
            { name: 'Deadlifts', difficulty: 'Advanced', description: 'Posterior chain' },
            { name: 'Planks', difficulty: 'Beginner', description: 'Core stability' },
            { name: 'More coming...', difficulty: 'All levels', description: 'Stay tuned' }
          ].map((exercise, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-sm exercise-card">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{exercise.name}</h3>
              <p className="text-sm text-gray-500 mb-2">{exercise.description}</p>
              <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                exercise.difficulty === 'Beginner' ? 'bg-green-100 text-green-800' :
                exercise.difficulty === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {exercise.difficulty}
              </span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default HomePage;
