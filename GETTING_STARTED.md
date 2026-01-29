# GETTING STARTED - Your First 30 Minutes

Follow this step-by-step guide to get your underwater sound classifier working.

## ⏱️ Timeline

- **Minutes 0-5**: Install dependencies
- **Minutes 5-10**: Verify installation  
- **Minutes 10-20**: Prepare sample data
- **Minutes 20-25**: Train your first model
- **Minutes 25-30**: Make predictions

## 🚀 Step 1: Install Dependencies (5 minutes)

### Windows (PowerShell)
```powershell
cd "c:\Users\User\OneDrive\Documents\GitHub\New folder"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux
```bash
cd "/path/to/project"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output**: Installing packages... (takes 2-3 minutes)

## ✅ Step 2: Verify Installation (5 minutes)

Run the test suite:
```bash
python test_classifier.py
```

You should see:
```
✓ NumPy              - Installed
✓ Librosa            - Installed
✓ SciPy              - Installed
✓ Scikit-learn       - Installed
✓ Matplotlib         - Installed
✓ SoundFile          - Installed

✅ ALL TESTS PASSED!
```

## 📊 Step 3: Prepare Sample Data (10 minutes)

The project includes an automatic data structure creator. Run:
```bash
python example.py
```

This will:
1. Create directory structure
2. Show you where to add audio files
3. Exit and wait for your data

You'll see:
```
Creating sample directory structure...
Created sample directory structure at data/raw

Next steps:
1. Add WAV audio files to the class subdirectories:
   - data/raw/whale_calls/sample1.wav, sample2.wav, ...
   - data/raw/ship_noise/sample1.wav, sample2.wav, ...
   - data/raw/ambient/sample1.wav, sample2.wav, ...

2. Run this script again to train the classifier
```

### Adding Your Audio Files

You can get sample underwater audio from:
- **Free sources**: Freesound.org, Zenodo, NOAA website
- **Dataset format**: Download WAV files
- **What you need**: 
  - At least 5-10 files per class
  - WAV format (not MP3)
  - 5-30 seconds duration each
  - 16,000 Hz sample rate or higher

**Quick test without data**: The code comes with a built-in test that creates synthetic audio

## 🤖 Step 4: Train Your Model (5 minutes)

After adding audio files (or to test with synthetic data), run:
```bash
python example.py
```

The script will:
1. Load all audio files from `data/raw/`
2. Extract MFCC features (takes a few seconds)
3. Train both SVM and Random Forest models
4. Show you the results
5. Save models to `models/`

You'll see output like:
```
Found 10 files in whale_calls
Found 10 files in ship_noise
Found 10 files in ambient

Loaded 30 audio files
Classes: ['ambient', 'ship_noise', 'whale_calls']
Feature shape: (30, 26)

Training SVM classifier...

==================================================
Model: SVM
Accuracy: 0.8667

Classification Report:
              precision    recall  f1-score   support

       ambient       0.86      0.86      0.86         7
  ship_noise       0.80      1.00      0.89         4
whale_calls       0.87      0.83      0.85         6

accuracy                           0.87        17
==================================================
```

## 🎯 Step 5: Make Your First Prediction (5 minutes)

Create a file called `my_prediction.py`:

```python
from classifier import UnderwaterSoundClassifier

# Load the trained model
classifier = UnderwaterSoundClassifier()
classifier.load_model('models/underwater_svm.pkl')

# Make a prediction
audio_file = 'data/raw/whale_calls/sample1.wav'
prediction = classifier.predict(audio_file)

print(f"Audio file: {audio_file}")
print(f"Predicted class: {prediction}")
```

Run it:
```bash
python my_prediction.py
```

Output:
```
Audio file: data/raw/whale_calls/sample1.wav
Predicted class: whale_calls
```

## 🎨 Bonus: Visualize Your Audio (5 minutes)

Create `my_visualization.py`:

```python
from classifier import UnderwaterSoundClassifier

classifier = UnderwaterSoundClassifier()

# Replace with your audio file
audio_file = 'data/raw/whale_calls/sample1.wav'

# Show spectrogram (frequency over time)
classifier.plot_spectrogram(audio_file, title="Spectrogram Analysis")

# Show MFCC features (what the model actually uses)
classifier.plot_mfcc(audio_file, title="MFCC Features")
```

Run it:
```bash
python my_visualization.py
```

This will display two plots showing:
- **Spectrogram**: Frequency content changing over time
- **MFCC**: Perceptual features the model uses

## 📈 Next Steps After 30 Minutes

### Short-term (Next 1 hour)
- [ ] Read [README.md](README.md) - understand features
- [ ] Read [API_REFERENCE.md](API_REFERENCE.md) - understand all methods
- [ ] Collect more audio data (20-50 files per class)
- [ ] Improve accuracy by adding more training data

### Medium-term (Next 2-4 hours)
- [ ] Try different MFCC settings
- [ ] Compare SVM vs Random Forest
- [ ] Implement batch prediction
- [ ] Create a custom training script

### Long-term (Next 1-2 days)
- [ ] Add more sound classes
- [ ] Implement cross-validation
- [ ] Deploy as a web API
- [ ] Explore deep learning approaches

## 🔧 Troubleshooting in First 30 Minutes

### "Python command not found"
```bash
# Windows: Use full path
"C:\Python\python.exe" -m venv venv

# macOS: Try python3
python3 -m venv venv
```

### "pip install fails"
```bash
# Update pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

### "No audio files found" error
Make sure you have files in this structure:
```
data/raw/
├── whale_calls/
│   └── sample1.wav
├── ship_noise/
│   └── sample1.wav
└── ambient/
    └── sample1.wav
```

### "Module not found" error
Make sure virtual environment is activated:
```bash
# Should show (venv) at start of terminal line
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Out of memory error
```python
# In example.py or your script, use fewer files:
# Edit the directory to have fewer samples per class
```

## 📚 Key Files for First 30 Minutes

| File | Purpose | Status |
|------|---------|--------|
| requirements.txt | Dependencies | ✓ Ready |
| test_classifier.py | Verify setup | ✓ Ready |
| example.py | Run first training | ✓ Ready |
| classifier.py | Main code | ✓ Ready |
| data/raw/ | Your audio files | ⏳ Create |
| models/ | Saved models | ✓ Auto-created |

## 🎓 What You've Learned

After 30 minutes, you've learned:
- ✅ How to install the project
- ✅ How to structure audio data
- ✅ How to train a machine learning model
- ✅ How to make predictions
- ✅ How to visualize audio features

## 🚦 Status Check

**You're ready to proceed if:**
- [ ] Installation completed without errors
- [ ] test_classifier.py passed all tests
- [ ] example.py ran successfully
- [ ] You made a prediction successfully
- [ ] You understand the basic workflow

**If anything failed**: Check [SETUP.md](SETUP.md) troubleshooting section

## 💡 Pro Tips

1. **Start with synthetic data**: The code can create test data automatically
2. **Use quality audio**: Better input = better predictions
3. **More data = better accuracy**: Add 20+ files per class
4. **Compare models**: Try both SVM and Random Forest
5. **Check visualizations**: Use plots to understand your data

## 🎯 Your First Real Project

Once you complete this 30-minute guide, try a real project:

1. **Collect data**: Find 30+ audio files from 3 underwater sound categories
2. **Organize**: Put them in data/raw/class1/, data/raw/class2/, etc.
3. **Train**: Run example.py or write custom training
4. **Evaluate**: Check accuracy and confusion matrix
5. **Deploy**: Use the trained model for predictions

## 📞 Get Help

- **Installation issues**: See [SETUP.md](SETUP.md)
- **API questions**: See [API_REFERENCE.md](API_REFERENCE.md)
- **Usage examples**: See [example.py](example.py) and [advanced_examples.py](advanced_examples.py)
- **Project overview**: See [README.md](README.md)

## ✨ Congratulations!

You've successfully set up and tested your underwater sound classifier!

**Next**: Read [README.md](README.md) to understand all features
**Then**: Follow [QUICKSTART.md](QUICKSTART.md) for in-depth usage

Happy classifying! 🐋 🚢 🌊
