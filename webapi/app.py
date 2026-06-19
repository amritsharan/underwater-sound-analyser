from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import sys
import tempfile
import glob
import traceback

from pathlib import Path
import pickle

# Ensure project root is on sys.path so `from classifier import ...` works
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import project classifier
from classifier import UnderwaterSoundClassifier

app = Flask(__name__, static_folder='../website', static_url_path='')
CORS(app)


def find_model_path():
    models_dir = Path(PROJECT_ROOT) / 'models'
    if not models_dir.exists():
        return None
    pkl_files = list(models_dir.glob('*.pkl'))
    return str(pkl_files[0]) if pkl_files else None


@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, 'index.html'))


@app.route('/<path:filename>')
def static_files(filename):
    # Serve any other static file from website folder
    return send_from_directory(app.static_folder, filename)


@app.route('/predict', methods=['POST'])
def predict():
    # Accept uploaded audio file under 'file'
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Save to temp file
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, f.filename)
    f.save(tmp_path)

    try:
        model_path = find_model_path()
        clf = UnderwaterSoundClassifier()
        if model_path:
            try:
                # Try to load with classifier.load_model (expects dict format)
                clf.load_model(model_path)
            except Exception:
                # Fallback: try to load raw sklearn model
                with open(model_path, 'rb') as fh:
                    loaded = pickle.load(fh)
                clf.model = loaded
                # scaler may not be present; attempts to predict without scaling may fail
        else:
            return jsonify({'error': 'No trained model found in /models. Train and save a model first.'}), 400

        # Predict
        pred = clf.predict(tmp_path)
        if pred is None:
            return jsonify({'error': 'Prediction failed. Ensure model and scaler are available.'}), 500

        return jsonify({'prediction': str(pred)})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
