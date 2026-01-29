"""
Underwater Sound Classifier
Main module for audio classification using MFCC features and machine learning.
"""

import os
import numpy as np
import librosa
import soundfile as sf
import pickle
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import warnings

warnings.filterwarnings('ignore')


class UnderwaterSoundClassifier:
    """
    A classifier for underwater sounds using MFCC features and ML models.
    
    Parameters:
    -----------
    model_type : str, default='svm'
        Type of model to use: 'svm' or 'random_forest'
    n_mfcc : int, default=13
        Number of MFCC coefficients to extract
    sr : int, default=16000
        Sample rate for audio loading
    """
    
    def __init__(self, model_type='svm', n_mfcc=13, sr=16000):
        """Initialize the classifier."""
        self.model_type = model_type
        self.n_mfcc = n_mfcc
        self.sr = sr
        
        # Initialize model
        if model_type == 'svm':
            self.model = SVC(kernel='rbf', C=1.0, gamma='scale')
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError("model_type must be 'svm' or 'random_forest'")
        
        self.scaler = StandardScaler()
        self.classes_ = None
        self.features = None
        self.labels = None
        self.file_paths = None
        
    def load_audio_file(self, file_path):
        """
        Load a single audio file.
        
        Parameters:
        -----------
        file_path : str
            Path to the audio file (WAV format)
            
        Returns:
        --------
        np.array
            Audio time series, sample rate
        """
        try:
            audio, sr = librosa.load(file_path, sr=self.sr)
            return audio, sr
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None, None
    
    def extract_mfcc_features(self, audio):
        """
        Extract MFCC features from audio.
        
        Parameters:
        -----------
        audio : np.array
            Audio time series
            
        Returns:
        --------
        np.array
            Feature vector (mean and std of MFCC coefficients)
        """
        if audio is None:
            return None
            
        # Compute MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=self.sr, n_mfcc=self.n_mfcc)
        
        # Compute mean and standard deviation for each MFCC coefficient
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)
        
        # Concatenate mean and std (total 26 features)
        features = np.concatenate([mfcc_mean, mfcc_std])
        
        return features
    
    def load_audio_files(self, data_dir, file_extension='.wav'):
        """
        Load audio files from directory structure: data_dir/class_name/*.wav
        
        Parameters:
        -----------
        data_dir : str
            Root directory containing subdirectories with audio files
        file_extension : str, default='.wav'
            Audio file extension to look for
        """
        self.features = []
        self.labels = []
        self.file_paths = []
        self.classes_ = []
        
        data_path = Path(data_dir)
        
        # Iterate through class directories
        for class_dir in data_path.iterdir():
            if class_dir.is_dir():
                class_name = class_dir.name
                self.classes_.append(class_name)
                
                # Iterate through audio files in class directory
                audio_files = list(class_dir.glob(f'*{file_extension}'))
                print(f"Found {len(audio_files)} files in {class_name}")
                
                for audio_file in audio_files:
                    audio, sr = self.load_audio_file(str(audio_file))
                    
                    if audio is not None:
                        features = self.extract_mfcc_features(audio)
                        
                        if features is not None:
                            self.features.append(features)
                            self.labels.append(class_name)
                            self.file_paths.append(str(audio_file))
        
        self.features = np.array(self.features)
        self.classes_ = sorted(list(set(self.labels)))
        
        print(f"\nLoaded {len(self.features)} audio files")
        print(f"Classes: {self.classes_}")
        print(f"Feature shape: {self.features.shape}")
    
    def extract_features(self):
        """Extract features from loaded audio (placeholder for additional processing)."""
        if self.features is None:
            print("No audio files loaded. Please call load_audio_files() first.")
            return
        print(f"Features extracted. Shape: {self.features.shape}")
    
    def train(self, test_size=0.2):
        """
        Train the classifier on loaded audio data.
        
        Parameters:
        -----------
        test_size : float, default=0.2
            Proportion of data to use for testing
        """
        if self.features is None or len(self.features) == 0:
            print("No features to train on. Load audio files first.")
            return
        
        # Split data
        from sklearn.model_selection import train_test_split
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.labels, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print(f"Training {self.model_type} classifier...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*50}")
        print(f"Model: {self.model_type.upper()}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print(f"{'='*50}\n")
        
        # Store test results and accuracy for later use
        self.y_test = y_test
        self.y_pred = y_pred
        self.X_test_scaled = X_test_scaled
        self.accuracy = accuracy
    
    def predict(self, audio_file):
        """
        Predict class for a new audio file.
        
        Parameters:
        -----------
        audio_file : str
            Path to the audio file
            
        Returns:
        --------
        str
            Predicted class name
        """
        audio, sr = self.load_audio_file(audio_file)
        
        if audio is None:
            return None
        
        features = self.extract_mfcc_features(audio)
        
        if features is None:
            return None
        
        # Scale features using the scaler from training
        features_scaled = self.scaler.transform([features])
        
        prediction = self.model.predict(features_scaled)[0]
        return prediction
    
    def predict_batch(self, audio_directory):
        """
        Predict classes for multiple audio files in a directory.
        
        Parameters:
        -----------
        audio_directory : str
            Directory containing audio files
            
        Returns:
        --------
        dict
            Dictionary with file paths and predictions
        """
        results = {}
        audio_path = Path(audio_directory)
        
        for audio_file in audio_path.glob('*.wav'):
            prediction = self.predict(str(audio_file))
            results[str(audio_file)] = prediction
        
        return results
    
    def save_model(self, model_path):
        """
        Save the trained model to disk.
        
        Parameters:
        -----------
        model_path : str
            Path to save the model
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'classes': self.classes_,
            'n_mfcc': self.n_mfcc,
            'sr': self.sr
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """
        Load a trained model from disk.
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model
        """
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.classes_ = model_data['classes']
        self.n_mfcc = model_data['n_mfcc']
        self.sr = model_data['sr']
        
        print(f"Model loaded from {model_path}")
        print(f"Classes: {self.classes_}")
    
    def plot_spectrogram(self, audio_file, title="Spectrogram"):
        """
        Plot the spectrogram of an audio file.
        
        Parameters:
        -----------
        audio_file : str
            Path to the audio file
        title : str
            Title for the plot
        """
        audio, sr = self.load_audio_file(audio_file)
        
        if audio is None:
            return
        
        # Compute spectrogram
        S = librosa.feature.melspectrogram(y=audio, sr=sr)
        S_db = librosa.power_to_db(S, ref=np.max)
        
        # Plot
        plt.figure(figsize=(10, 4))
        img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(img, format='%+2.0f dB')
        plt.title(title)
        plt.tight_layout()
        plt.show()
    
    def plot_mfcc(self, audio_file, title="MFCC"):
        """
        Plot the MFCC features of an audio file.
        
        Parameters:
        -----------
        audio_file : str
            Path to the audio file
        title : str
            Title for the plot
        """
        audio, sr = self.load_audio_file(audio_file)
        
        if audio is None:
            return
        
        # Compute MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc)
        
        # Plot
        plt.figure(figsize=(10, 4))
        img = librosa.display.specshow(mfcc, sr=sr, x_axis='time')
        plt.colorbar(img, format='%+2.0f')
        plt.title(title)
        plt.ylabel('MFCC')
        plt.tight_layout()
        plt.show()
    
    def plot_confusion_matrix(self):
        """Plot confusion matrix from last training."""
        if not hasattr(self, 'y_test'):
            print("No test data available. Train the model first.")
            return
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.colorbar()
        
        tick_marks = np.arange(len(self.classes_))
        plt.xticks(tick_marks, self.classes_, rotation=45)
        plt.yticks(tick_marks, self.classes_)
        
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    print("Underwater Sound Classifier")
    print("=" * 50)
    print("\nUsage Example:")
    print("-" * 50)
    print("""
# Create classifier
classifier = UnderwaterSoundClassifier(model_type='svm')

# Load audio files from directory structure
# data/raw/
#   ├── class1/
#   │   ├── sample1.wav
#   │   └── sample2.wav
#   └── class2/
#       ├── sample1.wav
#       └── sample2.wav

classifier.load_audio_files('data/raw/')
classifier.train()
classifier.save_model('models/classifier.pkl')

# Make predictions
prediction = classifier.predict('data/raw/class1/sample.wav')
print(f"Predicted class: {prediction}")

# Visualize
classifier.plot_spectrogram('data/raw/class1/sample.wav')
classifier.plot_mfcc('data/raw/class1/sample.wav')
    """)
