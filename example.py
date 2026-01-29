"""
Example script demonstrating the Underwater Sound Classifier.
Shows how to train and use the classifier with sample data.
"""

from classifier import UnderwaterSoundClassifier
import os
from pathlib import Path


def create_sample_data():
    """Create sample directory structure for demo."""
    data_dir = Path('data/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create class subdirectories
    for class_name in ['whale_calls', 'ship_noise', 'ambient']:
        class_dir = data_dir / class_name
        class_dir.mkdir(exist_ok=True)
        
    print(f"Created sample directory structure at {data_dir}")
    print("\nNext steps:")
    print("1. Add WAV audio files to the class subdirectories:")
    print("   - data/raw/whale_calls/sample1.wav, sample2.wav, ...")
    print("   - data/raw/ship_noise/sample1.wav, sample2.wav, ...")
    print("   - data/raw/ambient/sample1.wav, sample2.wav, ...")
    print("\n2. Run this script again to train the classifier")


def main():
    """Main demonstration function."""
    
    # Check if data directory exists with audio files
    data_dir = Path('data/raw')
    
    if not data_dir.exists():
        print("Creating sample directory structure...")
        create_sample_data()
        return
    
    # Check if any audio files exist
    audio_files = list(data_dir.rglob('*.wav'))
    
    if not audio_files:
        print("No audio files found in data/raw/")
        print("\nPlease add WAV audio files to:")
        for class_name in ['whale_calls', 'ship_noise', 'ambient']:
            print(f"  - data/raw/{class_name}/")
        return
    
    print(f"Found {len(audio_files)} audio files\n")
    
    # Initialize classifier - try both models
    for model_type in ['svm', 'random_forest']:
        print(f"\n{'='*60}")
        print(f"Training with {model_type.upper()}")
        print(f"{'='*60}\n")
        
        classifier = UnderwaterSoundClassifier(model_type=model_type)
        
        # Load audio files
        print("Loading audio files...")
        classifier.load_audio_files('data/raw/')
        
        # Extract features
        print("\nExtracting features...")
        classifier.extract_features()
        
        # Train model
        print("\nTraining model...")
        classifier.train(test_size=0.2)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        classifier.save_model(f'models/underwater_{model_type}.pkl')
        
        # Make sample predictions
        print("\nMaking predictions on training data:")
        print("-" * 40)
        sample_files = list(data_dir.rglob('*.wav'))[:3]
        
        for audio_file in sample_files:
            prediction = classifier.predict(str(audio_file))
            print(f"File: {audio_file.name}")
            print(f"Predicted class: {prediction}\n")
        
        # Try to visualize (if GUI available)
        try:
            print("\nGenerating visualizations...")
            if sample_files:
                classifier.plot_spectrogram(str(sample_files[0]), 
                                          title=f"Spectrogram - {sample_files[0].parent.name}")
                classifier.plot_mfcc(str(sample_files[0]), 
                                   title=f"MFCC - {sample_files[0].parent.name}")
                classifier.plot_confusion_matrix()
        except Exception as e:
            print(f"Could not display plots (running in non-GUI environment): {e}")


if __name__ == '__main__':
    main()
