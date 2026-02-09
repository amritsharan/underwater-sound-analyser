# Quick Start Guide - Underwater Sound Classifier

## 1. Setup (5 minutes)

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Prepare Your Data

### Directory Structure
Place your audio files in `data/raw/` organized by class:
```
data/raw/
├── whale_calls/
│   ├── whale1.wav
│   ├── whale2.wav
│   └── ...
├── ship_noise/
│   ├── ship1.wav
│   ├── ship2.wav
│   └── ...
└── ambient_ocean/
    ├── ambient1.wav
    ├── ambient2.wav
    └── ...
```

**Requirements:**
- Format: WAV files (16-bit PCM recommended)
- Sample rate: 16,000 Hz or higher
- Duration: 5-30 seconds per file
- Minimum: 10-15 files per class

## 3. Train Your Model

### Option A: Using the Example Script
```bash
python example.py
```

This will:
- Load all audio files from `data/raw/`
- Extract MFCC features from each file
- Train both SVM and Random Forest models
- Save trained models to `models/`
- Make predictions on sample audio

### Option B: Using the Classifier Directly

Create a file `train.py`:
```python
from classifier import UnderwaterSoundClassifier

# Create classifier
classifier = UnderwaterSoundClassifier(model_type='svm')

# Load audio files
classifier.load_audio_files('data/raw/')

# Train the model
classifier.train(test_size=0.2)

# Save for later use
classifier.save_model('models/my_classifier.pkl')
```

Then run:
```bash
python train.py
```

## 4. Make Predictions

Create a file `predict.py`:
```python
from classifier import UnderwaterSoundClassifier

# Load the trained model
classifier = UnderwaterSoundClassifier()
classifier.load_model('models/my_classifier.pkl')

# Predict on a single file
prediction = classifier.predict('path/to/audio.wav')
print(f"Predicted class: {prediction}")

# Predict on multiple files
results = classifier.predict_batch('data/raw/test_folder/')
for file, prediction in results.items():
    print(f"{file}: {prediction}")
```

Run:
```bash
python predict.py
```

## 5. Visualize Results

### Spectrogram
```python
classifier.plot_spectrogram('data/raw/whale_calls/sample.wav')
```
Shows frequency content over time.

### MFCC Features
```python
classifier.plot_mfcc('data/raw/whale_calls/sample.wav')
```
Shows extracted Mel-frequency Cepstral Coefficients.

### Confusion Matrix
```python
classifier.plot_confusion_matrix()
```
Shows how well the model performed on test data.

## 6. Model Comparison

Compare both models:
```python
from classifier import UnderwaterSoundClassifier

for model_type in ['svm', 'random_forest']:
    print(f"\nTraining {model_type}...")
    clf = UnderwaterSoundClassifier(model_type=model_type)
    clf.load_audio_files('data/raw/')
    clf.train()
    clf.save_model(f'models/{model_type}_model.pkl')
```

**Which model to choose?**
- **SVM**: Better for small datasets, clear boundaries between classes
- **Random Forest**: Better for larger datasets, captures complex patterns

## 7. Common Issues

**"No audio files found"**
- Check file format (must be .wav)
- Verify directory structure matches expected format
- Use absolute paths if relative paths don't work

**Poor accuracy?**
- Add more training data (at least 20-30 files per class)
- Ensure proper labeling (correct subdirectory names)
- Try different model types
- Visualize data to identify issues

**Out of memory?**
- Process fewer files at once
- Reduce sample rate (e.g., 8000 Hz instead of 16000)
- Use a machine with more RAM

## 8. Next Steps

1. **Add more data**: Better models need more diverse examples
2. **Experiment with hyperparameters**: Adjust n_mfcc, model parameters
3. **Implement cross-validation**: More robust accuracy estimates
4. **Add more features**: Combine MFCC with spectral centroid, zero crossing rate
5. **Try deep learning**: Use neural networks (CNN) for better performance
6. **Real-time classification**: Deploy model for live audio streams

## 9. Example Audio Sources

- **Whale sounds**: NOAA, Whale and Dolphin Conservation
- **Ship noise**: Underwater Acoustics Archive
- **Ocean ambient**: Freesound.org, Zenodo datasets

## 10. File Structure Overview

```
.
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── requirements.txt       # Python dependencies
├── classifier.py          # Main classifier class
├── example.py             # Example usage script
├── data/
│   ├── raw/              # Your training audio files
│   └── processed/        # Processed features (optional)
└── models/               # Saved trained models
```

---

**Need help?** Check the docstrings in `classifier.py` for detailed API documentation.
