import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for video processing
});

export interface Exercise {
  id: string;
  name: string;
  description: string;
  difficulty: string;
}

export interface AnalysisResult {
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

export interface ExerciseTips {
  exercise_id: string;
  tips: string[];
}

export const analyzeExercise = async (formData: FormData): Promise<AnalysisResult> => {
  try {
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to analyze exercise');
    }
    throw error;
  }
};

export const getSupportedExercises = async (): Promise<Exercise[]> => {
  try {
    const response = await api.get('/exercises');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch exercises:', error);
    return [];
  }
};

export const getExerciseTips = async (exerciseId: string): Promise<ExerciseTips> => {
  try {
    const response = await api.get(`/exercise/${exerciseId}/tips`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to fetch exercise tips');
    }
    throw error;
  }
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('API is not available');
  }
}; 