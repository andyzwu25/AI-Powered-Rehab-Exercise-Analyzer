import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Upload, Play, Image, FileVideo, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { analyzeExercise } from '../services/api';

interface AnalysisResult {
  success: boolean;
  exercise_type?: string;
  analysis?: {
    score: number;
    feedback: string[];
    exercise_type: string;
  };
  frame_count?: number;
  error?: string;
}

const AnalysisPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [exerciseType, setExerciseType] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const exercise = params.get('exercise');
    if (exercise) {
      setExerciseType(exercise);
    }
  }, [location]);

  const handleFileSelect = (selectedFile: File) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/avi', 'video/mov'];
    if (validTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
      setResult(null);
    } else {
      alert('Please select a valid video or image file (MP4, AVI, MOV, JPG, PNG, GIF)');
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file || !exerciseType) return;

    setIsAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('exercise_type', exerciseType);
      
      const analysisResult = await analyzeExercise(formData);
      setResult(analysisResult);
    } catch (error) {
      setResult({
        success: false,
        error: 'Failed to analyze exercise. Please try again.'
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'score-excellent';
    if (score >= 70) return 'score-good';
    return 'score-poor';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 90) return <CheckCircle className="h-6 w-6 text-green-500" />;
    if (score >= 70) return <CheckCircle className="h-6 w-6 text-yellow-500" />;
    return <XCircle className="h-6 w-6 text-red-500" />;
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Exercise Form Analysis</h1>
        <p className="text-gray-600">
          Upload a video or image of your exercise to get instant feedback on your form
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-xl shadow-sm p-8 mb-8">
        <div
          className={`upload-area rounded-lg border-2 border-dashed p-8 text-center ${
            dragActive ? 'dragover' : ''
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="space-y-4">
            <div className="flex justify-center">
              {file?.type.startsWith('video/') ? (
                <FileVideo className="h-12 w-12 text-blue-500" />
              ) : (
                <Image className="h-12 w-12 text-blue-500" />
              )}
            </div>
            
            {file ? (
              <div>
                <p className="text-lg font-medium text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            ) : (
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drop your file here or click to browse
                </p>
                <p className="text-sm text-gray-500">
                  Supports MP4, AVI, MOV, JPG, PNG, GIF (max 16MB)
                </p>
              </div>
            )}
            
            <button
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Choose File
            </button>
          </div>
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*,image/*"
          onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
          className="hidden"
        />
        
        {file && (
          <div className="mt-6 text-center">
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isAnalyzing ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-5 w-5" />
                  Analyze Exercise
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Results</h2>
          
          {result.success ? (
            <div className="space-y-6">
              {/* Exercise Type */}
              <div className="flex items-center space-x-3">
                <span className="text-lg font-medium text-gray-700">Exercise Type:</span>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {result.exercise_type?.replace('_', ' ').toUpperCase() || 'Unknown'}
                </span>
              </div>

              {/* Score */}
              {result.analysis && (
                <div className="flex items-center space-x-4">
                  <span className="text-lg font-medium text-gray-700">Form Score:</span>
                  <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${getScoreColor(result.analysis.score)}`}>
                    {getScoreIcon(result.analysis.score)}
                    <span className="text-white font-bold text-xl">
                      {result.analysis.score}/100
                    </span>
                  </div>
                </div>
              )}

              {/* Feedback */}
              {result.analysis?.feedback && result.analysis.feedback.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-3">Feedback & Suggestions:</h3>
                  <div className="space-y-2">
                    {result.analysis.feedback.map((feedback, index) => (
                      <div key={index} className="flex items-start space-x-2 p-3 bg-gray-50 rounded-lg">
                        <AlertCircle className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                        <p className="text-gray-700">{feedback}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Frame Count */}
              {result.frame_count && (
                <div className="text-sm text-gray-500">
                  Analyzed {result.frame_count} frame{result.frame_count !== 1 ? 's' : ''}
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center space-x-2 text-red-600">
              <XCircle className="h-5 w-5" />
              <span>{result.error || 'Analysis failed'}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalysisPage;
