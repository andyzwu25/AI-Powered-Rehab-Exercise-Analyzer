# Machine Learning Training Guide

This guide explains how to train AI models for exercise form analysis using your own labeled videos.

## Overview

The app now supports **machine learning-based form analysis** that learns from labeled examples instead of using fixed rules. This provides much more accurate and adaptable analysis.

## How It Works

1. **Feature Extraction**: MediaPipe extracts pose landmarks and angles from videos
2. **Feature Engineering**: The system converts pose data into 49+ meaningful features (angles, velocities, alignment, etc.)
3. **Model Training**: Train a model (Random Forest or Gradient Boosting) on labeled examples
4. **Prediction**: The trained model predicts form scores (0-100) for new videos

## Training Workflow

### Step 1: Collect Training Data

You need **at least 10 labeled videos** per exercise type to train a model. More data = better accuracy.

**Option A: User Feedback Collection**
- Users analyze their videos
- They provide feedback scores (0-100) on the analysis
- This data is automatically collected via the `/api/feedback` endpoint

**Option B: Manual Data Collection**
- Upload videos and manually label them with scores
- Use the feedback API to store the labels

### Step 2: Train the Model

Once you have enough training data, train a model:

```bash
POST /api/train
Content-Type: application/json

{
  "exercise_type": "pull_up",
  "model_type": "random_forest"  // or "gradient_boosting"
}
```

**Response:**
```json
{
  "success": true,
  "exercise_type": "pull_up",
  "model_type": "random_forest",
  "training_samples": 80,
  "test_samples": 20,
  "test_r2": 0.85,
  "test_rmse": 8.5
}
```

### Step 3: Use the Trained Model

Once trained, the model is automatically used for analysis. The system:
1. Checks if a trained model exists
2. Uses ML model if available
3. Falls back to rule-based analysis if no model exists

## API Endpoints

### 1. Submit Feedback (Collect Training Data)

```bash
POST /api/feedback
Content-Type: application/json

{
  "exercise_type": "pull_up",
  "pose_data": [...],  // From analyze_exercise response
  "score": 85,  // User-provided score (0-100)
  "user_feedback": "Good form overall",
  "metadata": {
    "video_id": "abc123"
  }
}
```

### 2. Train Model

```bash
POST /api/train
Content-Type: application/json

{
  "exercise_type": "pull_up",
  "model_type": "random_forest"  // Optional, defaults to random_forest
}
```

### 3. Check Training Data Statistics

```bash
GET /api/training-data/pull_up
```

**Response:**
```json
{
  "exercise_type": "pull_up",
  "statistics": {
    "count": 100,
    "avg_score": 75.5,
    "min_score": 45,
    "max_score": 95,
    "std_score": 12.3
  }
}
```

### 4. Check Model Status

```bash
GET /api/model-status/pull_up
```

**Response:**
```json
{
  "exercise_type": "pull_up",
  "model_exists": true
}
```

## Model Types

### Random Forest (Recommended)
- **Pros**: Fast training, handles non-linear relationships, good default choice
- **Cons**: Can overfit with small datasets
- **Best for**: Most use cases

### Gradient Boosting
- **Pros**: Often more accurate, better for complex patterns
- **Cons**: Slower training, more prone to overfitting
- **Best for**: Large datasets (100+ examples)

## Improving Model Accuracy

1. **More Training Data**: Aim for 50+ examples per exercise
2. **Diverse Examples**: Include videos with:
   - Different body types
   - Different camera angles
   - Good and bad form examples
   - Various lighting conditions
3. **Quality Labels**: Accurate scores are crucial
4. **Retrain Periodically**: As you collect more data, retrain models

## File Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── ml/
│   │   │   ├── feature_extractor.py    # Extracts features from pose data
│   │   │   ├── model_trainer.py        # Trains and manages models
│   │   │   ├── data_collector.py        # Collects labeled training data
│   │   │   └── __init__.py
│   │   ├── exercises/
│   │   │   ├── base_analyzer.py         # Base class with ML integration
│   │   │   ├── pull_up_analyzer.py      # Exercise-specific analyzers
│   │   │   ├── push_up_analyzer.py
│   │   │   └── squat_analyzer.py
│   │   └── pose_analyzer.py
│   └── app.py
└── models/
    └── ml/
        ├── saved_models/                # Trained models stored here
        │   ├── pull_up_model.pkl
        │   ├── pull_up_scaler.pkl
        │   └── ...
        └── training_data/               # Collected training data
            ├── pull_up_data.jsonl
            └── ...
```

## Example: Training a Pull-Up Model

1. **Collect 20+ pull-up videos** with user feedback scores
2. **Check data**: `GET /api/training-data/pull_up`
3. **Train model**: `POST /api/train` with `{"exercise_type": "pull_up"}`
4. **Verify**: `GET /api/model-status/pull_up` should return `model_exists: true`
5. **Test**: Analyze a new pull-up video - it will use the ML model!

## Troubleshooting

**"Need at least 10 training examples"**
- Collect more labeled data via the feedback API

**Low accuracy (R² < 0.7)**
- Collect more diverse training examples
- Check label quality (are scores accurate?)
- Try gradient boosting instead of random forest

**Model not being used**
- Check model exists: `GET /api/model-status/<exercise>`
- Verify model files exist in `models/ml/saved_models/`
- Check logs for errors

## Next Steps

- **Collect initial training data**: Start with 10-20 labeled videos per exercise
- **Train your first model**: Use the `/api/train` endpoint
- **Iterate**: Collect more data, retrain, improve accuracy
- **Deploy**: Models are automatically used once trained

The system will automatically use ML models when available, falling back to rule-based analysis otherwise.

