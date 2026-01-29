# API Reference - UnderwaterSoundClassifier

Complete documentation for all methods and parameters.

## Class: UnderwaterSoundClassifier

Main class for underwater sound classification.

### Constructor

```python
UnderwaterSoundClassifier(model_type='svm', n_mfcc=13, sr=16000)
```

**Parameters:**
- `model_type` (str): Type of ML model
  - `'svm'`: Support Vector Machine (default)
  - `'random_forest'`: Random Forest Classifier
  
- `n_mfcc` (int): Number of MFCC coefficients to extract
  - Default: `13`
  - Range: 10-40 (higher = more detail but slower)
  
- `sr` (int): Sample rate for audio loading
  - Default: `16000` Hz
  - Common values: 8000, 16000, 22050, 44100

**Example:**
```python
# Standard classifier with SVM
clf = UnderwaterSoundClassifier()

# Random Forest with 20 MFCC coefficients
clf = UnderwaterSoundClassifier(model_type='random_forest', n_mfcc=20)

# Lower sample rate for faster processing
clf = UnderwaterSoundClassifier(sr=8000)
```

---

## Methods

### load_audio_file(file_path)

Load a single audio file.

**Parameters:**
- `file_path` (str): Path to WAV audio file

**Returns:**
- `tuple`: (audio_array, sample_rate)
  - `audio_array` (np.array): Audio time series
  - `sample_rate` (int): Sample rate in Hz

**Raises:**
- `Exception`: If file cannot be loaded

**Example:**
```python
audio, sr = clf.load_audio_file('data/raw/whale_calls/sample.wav')
print(f"Loaded {len(audio)} samples at {sr} Hz")
```

---

### extract_mfcc_features(audio)

Extract MFCC features from audio data.

**Parameters:**
- `audio` (np.array): Audio time series

**Returns:**
- `np.array`: Feature vector of shape (n_mfcc * 2,)
  - First n_mfcc values: mean of each MFCC coefficient
  - Last n_mfcc values: standard deviation of each MFCC coefficient

**Example:**
```python
audio, sr = clf.load_audio_file('sample.wav')
features = clf.extract_mfcc_features(audio)
print(f"Extracted {len(features)} features")
```

---

### load_audio_files(data_dir, file_extension='.wav')

Load all audio files from organized directory structure.

**Directory Structure Required:**
```
data_dir/
├── class1/
│   ├── file1.wav
│   ├── file2.wav
│   └── ...
├── class2/
│   ├── file1.wav
│   └── ...
```

**Parameters:**
- `data_dir` (str): Root directory containing class subdirectories
- `file_extension` (str): File extension to search for (default: '.wav')

**Attributes Set:**
- `self.features` (np.array): Shape (n_samples, n_features)
- `self.labels` (list): Class labels for each sample
- `self.file_paths` (list): Paths to each audio file
- `self.classes_` (list): Unique class names

**Example:**
```python
clf.load_audio_files('data/raw/')
print(f"Loaded {len(clf.features)} samples")
print(f"Classes: {clf.classes_}")
```

---

### extract_features()

Process loaded audio files (validation step).

**Parameters:** None

**Returns:** None

**Side Effects:**
- Prints feature extraction summary

**Example:**
```python
clf.load_audio_files('data/raw/')
clf.extract_features()
```

---

### train(test_size=0.2)

Train the ML model on loaded data.

**Parameters:**
- `test_size` (float): Proportion of data for testing (default: 0.2)
  - 0.2 = 80% train, 20% test

**Side Effects:**
- Trains `self.model`
- Fits `self.scaler` for feature normalization
- Sets attributes: `self.y_test`, `self.y_pred`, `self.X_test_scaled`
- Prints accuracy metrics and classification report

**Raises:**
- Prints warning if no features loaded

**Example:**
```python
clf.load_audio_files('data/raw/')
clf.train(test_size=0.25)  # 75% train, 25% test
```

---

### predict(audio_file)

Predict class for a single audio file.

**Parameters:**
- `audio_file` (str): Path to audio file

**Returns:**
- `str`: Predicted class name
- `None`: If file cannot be loaded or processed

**Requires:**
- Model must be trained or loaded before calling

**Example:**
```python
clf.load_model('models/my_model.pkl')
prediction = clf.predict('new_sample.wav')
print(f"Prediction: {prediction}")
```

---

### predict_batch(audio_directory)

Predict classes for multiple files in a directory.

**Parameters:**
- `audio_directory` (str): Directory containing WAV files

**Returns:**
- `dict`: {file_path: predicted_class, ...}

**Example:**
```python
results = clf.predict_batch('data/raw/test_audio/')
for file, prediction in results.items():
    print(f"{file}: {prediction}")
```

---

### save_model(model_path)

Save trained model to disk.

**Parameters:**
- `model_path` (str): Path to save model (e.g., 'models/my_model.pkl')

**Side Effects:**
- Creates directory if it doesn't exist
- Saves model, scaler, and metadata

**Example:**
```python
clf.train()
clf.save_model('models/underwater_classifier.pkl')
```

---

### load_model(model_path)

Load a previously trained model from disk.

**Parameters:**
- `model_path` (str): Path to saved model file

**Side Effects:**
- Restores: model, scaler, classes, n_mfcc, sr
- Prints loaded classes

**Example:**
```python
clf = UnderwaterSoundClassifier()
clf.load_model('models/my_model.pkl')
prediction = clf.predict('sample.wav')
```

---

### plot_spectrogram(audio_file, title='Spectrogram')

Display mel-spectrogram of audio file.

**Parameters:**
- `audio_file` (str): Path to audio file
- `title` (str): Plot title (default: 'Spectrogram')

**Returns:** None

**Side Effects:**
- Displays matplotlib figure

**Notes:**
- Requires display capability (GUI environment)
- Shows frequency content over time
- Useful for understanding audio characteristics

**Example:**
```python
clf.plot_spectrogram('data/raw/whale_calls/sample.wav', 
                     title='Whale Call Spectrogram')
```

---

### plot_mfcc(audio_file, title='MFCC')

Display MFCC features of audio file.

**Parameters:**
- `audio_file` (str): Path to audio file
- `title` (str): Plot title (default: 'MFCC')

**Returns:** None

**Side Effects:**
- Displays matplotlib figure

**Notes:**
- Shows extracted MFCC coefficients
- Perceptually relevant frequency representation
- Used by the classifier for feature extraction

**Example:**
```python
clf.plot_mfcc('data/raw/whale_calls/sample.wav')
```

---

### plot_confusion_matrix()

Display confusion matrix from last training.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Displays matplotlib figure

**Requires:**
- Model must be trained before calling
- Attributes `y_test` and `y_pred` must exist

**Example:**
```python
clf.train()
clf.plot_confusion_matrix()
```

---

## Attributes

### Read-Only After Training

- `clf.classes_` (list): Unique class names
- `clf.features` (np.array): Extracted features, shape (n_samples, n_features)
- `clf.labels` (list): Class label for each sample
- `clf.file_paths` (list): File path for each sample
- `clf.model`: Trained ML model instance
- `clf.scaler`: Fitted StandardScaler for feature normalization

### After Training

- `clf.y_test` (list): True labels on test set
- `clf.y_pred` (list): Predicted labels on test set
- `clf.X_test_scaled` (np.array): Scaled test features

---

## Usage Patterns

### Pattern 1: Basic Training and Prediction

```python
from classifier import UnderwaterSoundClassifier

# Train
clf = UnderwaterSoundClassifier(model_type='svm')
clf.load_audio_files('data/raw/')
clf.train()
clf.save_model('models/classifier.pkl')

# Predict
clf_loaded = UnderwaterSoundClassifier()
clf_loaded.load_model('models/classifier.pkl')
prediction = clf_loaded.predict('new_audio.wav')
```

### Pattern 2: Model Comparison

```python
for model_type in ['svm', 'random_forest']:
    clf = UnderwaterSoundClassifier(model_type=model_type)
    clf.load_audio_files('data/raw/')
    clf.train()
    clf.save_model(f'models/{model_type}.pkl')
```

### Pattern 3: Feature Analysis

```python
clf = UnderwaterSoundClassifier()
clf.load_audio_files('data/raw/')

# Access features before training
for i, label in enumerate(clf.classes_):
    class_features = clf.features[np.array(clf.labels) == label]
    print(f"{label}: {len(class_features)} samples, {class_features.shape[1]} features")
```

### Pattern 4: Batch Processing

```python
clf = UnderwaterSoundClassifier()
clf.load_model('models/classifier.pkl')

# Process entire directory
results = clf.predict_batch('data/raw/test_audio/')
for file, pred in results.items():
    print(f"{file}: {pred}")
```

---

## Error Messages and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: librosa` | Dependencies not installed | `pip install -r requirements.txt` |
| `FileNotFoundError` | Audio file not found | Check file path and format |
| `ValueError: model_type must be...` | Invalid model type | Use 'svm' or 'random_forest' |
| `No audio files loaded` | No files in directory | Check directory structure |
| `Model not trained` | Predict before training | Call `train()` first |

---

## Performance Considerations

### Speed
- **SVM**: ~50-500 ms per prediction (depends on data size)
- **Random Forest**: ~10-100 ms per prediction
- **Feature extraction**: ~100-500 ms per file

### Memory
- ~1 MB per 10 seconds of audio at 16 kHz
- Features: ~1 KB per sample
- Trained model: ~1-5 MB

### Accuracy Factors
- Number of training samples (minimum 20 per class)
- Quality of audio recordings
- Clarity of audio classes
- Model hyperparameters

---

## Constants

### Feature Size
- `n_features = n_mfcc * 2`
- Default: 26 features per sample (13 MFCC coefficients)

### Sample Duration
- Typical: 5-30 seconds
- Recommended: 10-20 seconds
- Minimum: 1 second

### Class Balance
- Recommended: Equal samples per class
- Acceptable: ≤ 3:1 ratio between classes

---

## Dependencies

- **librosa**: Audio processing and MFCC extraction
- **numpy**: Numerical arrays and operations
- **scipy**: Signal processing utilities
- **scikit-learn**: SVM, Random Forest, scaling, metrics
- **matplotlib**: Visualization (optional for headless systems)
- **soundfile**: WAV file I/O (optional, fallback to scipy)

---

**Last Updated**: 2024
**Version**: 1.0
