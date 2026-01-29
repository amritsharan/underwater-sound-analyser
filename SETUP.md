# Setup Instructions - Underwater Sound Classifier

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- ~500 MB disk space for dependencies

## Step-by-Step Setup

### 1. Open Terminal in Project Directory

Navigate to the project folder in your terminal:
```bash
cd "c:\Users\User\OneDrive\Documents\GitHub\New folder"
```

### 2. Create Virtual Environment

A virtual environment isolates project dependencies:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- **librosa**: Audio processing and feature extraction
- **numpy**: Numerical computations
- **scipy**: Scientific computing
- **scikit-learn**: Machine learning models
- **matplotlib**: Data visualization
- **soundfile**: Audio file I/O

Installation takes ~2-3 minutes depending on internet speed.

### 4. Verify Installation

```bash
python -c "import librosa; import sklearn; print('All packages installed successfully!')"
```

## Project Structure

After setup, your project should look like:

```
Underwater Sound Classifier/
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick start guide
├── SETUP.md                   # This file
├── requirements.txt           # Dependencies
├── classifier.py              # Main classifier module
├── example.py                 # Basic example
├── advanced_examples.py       # Advanced examples
├── data/
│   ├── raw/                   # Place your audio files here
│   └── processed/             # Processed features
├── models/                    # Trained models (auto-created)
└── venv/                      # Virtual environment (created by setup)
```

## Next Steps

### 1. Prepare Your Audio Data

Create subdirectories in `data/raw/` for each class:

```bash
mkdir data/raw/whale_calls
mkdir data/raw/ship_noise
mkdir data/raw/ambient_ocean
```

Copy your WAV audio files into these directories.

### 2. Train a Model

Run the example script:
```bash
python example.py
```

Or use the quick training script:
```python
from classifier import UnderwaterSoundClassifier

clf = UnderwaterSoundClassifier(model_type='svm')
clf.load_audio_files('data/raw/')
clf.train()
clf.save_model('models/my_model.pkl')
```

### 3. Make Predictions

```python
clf = UnderwaterSoundClassifier()
clf.load_model('models/my_model.pkl')
prediction = clf.predict('data/raw/whale_calls/sample.wav')
print(f"Prediction: {prediction}")
```

## Troubleshooting

### Issue: "python: command not found" or "python not in PATH"

**Solution**: Install Python from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installation

### Issue: "ModuleNotFoundError: No module named 'librosa'"

**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
# Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Issue: "No module named 'venv'"

**Solution**: Install venv module
```bash
# On Debian/Ubuntu
sudo apt-get install python3-venv

# On macOS
brew install python3
```

### Issue: Audio files not found

**Check**:
1. Files are in `.wav` format (not `.mp3` or other formats)
2. Directory structure matches: `data/raw/class_name/file.wav`
3. File permissions allow reading

### Issue: Out of memory error

**Solutions**:
1. Use fewer files for training
2. Reduce sample rate: `librosa.load(file, sr=8000)`
3. Use a machine with more RAM

### Issue: ModuleNotFoundError on import

**Solution**: Make sure virtual environment is activated:
```bash
# Check if activated (should show (venv) prefix)
python --version

# If not activated:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

## Deactivating Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```

To reactivate later:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

## System Requirements

### Minimum
- CPU: Intel i5 or equivalent (2-3 GHz)
- RAM: 4 GB
- Disk: 1 GB free space
- Internet: For installation only

### Recommended
- CPU: Intel i7 or equivalent
- RAM: 8 GB+
- Disk: 2+ GB free space
- SSD for faster processing

## Performance Tips

1. **Use SVM for small datasets** (< 100 samples): Faster training
2. **Use Random Forest for larger datasets** (> 100 samples): Better accuracy
3. **Reduce MFCC coefficients** if slow: `n_mfcc=10` instead of 13
4. **Batch process files** instead of individual predictions
5. **Use GPU** (optional): Requires CUDA for faster computation

## File Format Requirements

**Supported Audio Formats**: WAV (primary), OGG, MP3 (with ffmpeg)

**Optimal Settings**:
- Channels: Mono or Stereo (will be converted to mono)
- Sample Rate: 16,000 Hz - 44,100 Hz
- Bit Depth: 16-bit or 24-bit
- Duration: 5-30 seconds
- Size: < 5 MB per file

## Getting Help

1. Check QUICKSTART.md for common usage patterns
2. Read docstrings in classifier.py: `python -c "from classifier import UnderwaterSoundClassifier; help(UnderwaterSoundClassifier)"`
3. Run examples: `python example.py` and `python advanced_examples.py`
4. Check error messages carefully - they often indicate the solution

## Environment Variables (Optional)

To use specific audio library versions or GPU:

```bash
# On macOS (use system-installed ffmpeg)
export LIBROSA_AUDIO_BACKEND=soundfile

# For TensorFlow GPU (advanced)
export CUDA_VISIBLE_DEVICES=0
```

## Next Learning Steps

After mastering the basics:

1. **Explore features**: Try different MFCC settings, add spectral features
2. **Improve accuracy**: Implement data augmentation, try hyperparameter tuning
3. **Deploy model**: Create a web API using Flask or FastAPI
4. **Deep learning**: Transition to neural networks (CNN) for better performance
5. **Real-time processing**: Implement streaming audio classification

---

**Setup complete!** Proceed to QUICKSTART.md for your first training.
