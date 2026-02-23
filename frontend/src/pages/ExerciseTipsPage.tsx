import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Lightbulb, CheckCircle, ArrowLeft } from 'lucide-react';
import { getExerciseTips, getSupportedExercises, Exercise } from '../services/api';

const ExerciseTipsPage: React.FC = () => {
  const { exerciseId } = useParams<{ exerciseId: string }>();
  const [tips, setTips] = useState<string[]>([]);
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!exerciseId) return;
      
      setLoading(true);
      try {
        // Fetch exercise details
        const exercises = await getSupportedExercises();
        const currentExercise = exercises.find(ex => ex.id === exerciseId);
        setExercise(currentExercise || null);

        // Fetch tips
        const tipsData = await getExerciseTips(exerciseId);
        setTips(tipsData.tips);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load exercise tips');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [exerciseId]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading exercise tips...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <button
          onClick={() => window.history.back()}
          className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 transition-colors mb-4"
        >
          <ArrowLeft className="h-5 w-5" />
          <span>Back</span>
        </button>
        
        <div className="flex items-center space-x-3 mb-6">
          <Lightbulb className="h-8 w-8 text-yellow-500" />
          <h1 className="text-3xl font-bold text-gray-900">
            {exercise?.name || 'Exercise'} Form Tips
          </h1>
        </div>
        
        {exercise && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-blue-800">
              <span className="font-semibold">Difficulty:</span> {exercise.difficulty}
            </p>
            <p className="text-blue-700 mt-1">{exercise.description}</p>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Form Tips & Best Practices</h2>
        
        {tips.length > 0 ? (
          <div className="space-y-4">
            {tips.map((tip, index) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                <CheckCircle className="h-6 w-6 text-green-500 mt-0.5 flex-shrink-0" />
                <p className="text-gray-700">{tip}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Lightbulb className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No specific tips available for this exercise.</p>
          </div>
        )}
      </div>

      {/* Additional Resources */}
      <div className="mt-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white">
        <h3 className="text-xl font-bold mb-4">Want to Improve Your Form?</h3>
        <p className="mb-6 opacity-90">
          Upload a video or image of your exercise to get personalized feedback and analysis.
        </p>
        <button
          onClick={() => window.location.href = '/analysis'}
          className="inline-flex items-center px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
        >
          Analyze Your Form
        </button>
      </div>
    </div>
  );
};

export default ExerciseTipsPage; 