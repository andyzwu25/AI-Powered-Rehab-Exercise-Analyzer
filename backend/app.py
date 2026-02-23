from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import sys
from werkzeug.utils import secure_filename

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

try:
    from models.pose_analyzer import PoseAnalyzer
    from utils.file_utils import allowed_file, create_upload_folder
    from models.ml.model_trainer import ModelTrainer
    from models.ml.data_collector import DataCollector
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure the __init__.py files are in the app, models, and utils directories")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Create upload folder if it doesn't exist
create_upload_folder(app.config['UPLOAD_FOLDER'])

# Initialize pose analyzer
pose_analyzer = PoseAnalyzer()

# Initialize ML components
model_trainer = ModelTrainer()
data_collector = DataCollector()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Exercise Form Analyzer API is running'})

@app.route('/api/analyze', methods=['POST'])
def analyze_exercise():
    """Analyze uploaded video or image for exercise form"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        if 'exercise_type' not in request.form:
            return jsonify({'error': 'No exercise type specified'}), 400

        file = request.files['file']
        exercise_type = request.form['exercise_type']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        analysis_result = pose_analyzer.analyze_exercise(file_path, exercise_type)
        
        # Include pose_data in response for potential feedback collection
        # (pose_data is stored internally and can be retrieved if needed)
        
        os.remove(file_path)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises', methods=['GET'])
def get_supported_exercises():
    """Get list of supported exercises"""
    exercises = [
        {
            'id': 'pull_up',
            'name': 'Pull Up',
            'description': 'Upper body strength exercise targeting back and biceps',
            'difficulty': 'Intermediate'
        },
        {
            'id': 'push_up',
            'name': 'Push Up',
            'description': 'Bodyweight exercise targeting chest, shoulders, and triceps',
            'difficulty': 'Beginner'
        },
        {
            'id': 'squat',
            'name': 'Squat',
            'description': 'Lower body exercise targeting quadriceps, hamstrings, and glutes',
            'difficulty': 'Beginner'
        },
        {
            'id': 'deadlift',
            'name': 'Deadlift',
            'description': 'Compound exercise targeting posterior chain',
            'difficulty': 'Advanced'
        },
        {
            'id': 'plank',
            'name': 'Plank',
            'description': 'Core stability exercise',
            'difficulty': 'Beginner'
        }
    ]
    return jsonify(exercises)

@app.route('/api/exercise/<exercise_id>/tips', methods=['GET'])
def get_exercise_tips(exercise_id):
    """Get form tips for a specific exercise"""
    tips = {
        'pull_up': [
            'Keep your core engaged throughout the movement',
            'Pull your shoulder blades down and back',
            'Avoid swinging or using momentum',
            'Lower yourself with control'
        ],
        'push_up': [
            'Maintain a straight line from head to heels',
            'Keep your core tight',
            'Lower your body as a single unit',
            'Keep your elbows close to your body'
        ],
        'squat': [
            'Keep your chest up and core engaged',
            'Push your knees out in line with your toes',
            'Keep your weight in your heels',
            'Go as deep as you can while maintaining good form'
        ],
        'deadlift': [
            'Keep your back straight and core engaged',
            'Push through your heels',
            'Keep the bar close to your body',
            'Stand up straight at the top'
        ],
        'plank': [
            'Keep your body in a straight line',
            'Engage your core muscles',
            'Don\'t let your hips sag',
            'Breathe steadily'
        ]
    }
    
    exercise_tips = tips.get(exercise_id, ['No specific tips available for this exercise'])
    return jsonify({'exercise_id': exercise_id, 'tips': exercise_tips})

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train an ML model for a specific exercise type"""
    try:
        data = request.get_json()
        
        if 'exercise_type' not in data:
            return jsonify({'error': 'exercise_type is required'}), 400
        
        exercise_type = data['exercise_type']
        
        # Get training data from data collector
        training_examples = data_collector.load_training_data(exercise_type)
        
        if len(training_examples) < 10:
            return jsonify({
                'error': f'Need at least 10 training examples, got {len(training_examples)}',
                'current_count': len(training_examples)
            }), 400
        
        # Extract pose data and labels
        training_data = [ex['pose_data'] for ex in training_examples]
        labels = [ex['score'] for ex in training_examples]
        
        # Train model
        model_type = data.get('model_type', 'random_forest')
        results = model_trainer.train_model(
            exercise_type=exercise_type,
            training_data=training_data,
            labels=labels,
            model_type=model_type
        )
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for training data collection"""
    try:
        data = request.get_json()
        
        required_fields = ['exercise_type', 'pose_data', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        exercise_type = data['exercise_type']
        pose_data = data['pose_data']
        score = float(data['score'])
        user_feedback = data.get('user_feedback')
        metadata = data.get('metadata', {})
        
        # Validate score range
        if not (0 <= score <= 100):
            return jsonify({'error': 'Score must be between 0 and 100'}), 400
        
        # Save training example
        example_id = data_collector.save_training_example(
            exercise_type=exercise_type,
            pose_data=pose_data,
            score=score,
            user_feedback=user_feedback,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'example_id': example_id,
            'message': 'Feedback saved successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/training-data/<exercise_type>', methods=['GET'])
def get_training_data_stats(exercise_type):
    """Get statistics about collected training data for an exercise"""
    try:
        stats = data_collector.get_training_statistics(exercise_type)
        return jsonify({
            'exercise_type': exercise_type,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-status/<exercise_type>', methods=['GET'])
def get_model_status(exercise_type):
    """Check if a trained model exists for an exercise type"""
    try:
        model_exists = model_trainer.model_exists(exercise_type)
        return jsonify({
            'exercise_type': exercise_type,
            'model_exists': model_exists
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
