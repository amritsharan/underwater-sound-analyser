"""
Testing and Validation Script
Verify that the classifier is working correctly
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test that all required packages are installed."""
    print("\n" + "="*60)
    print("TEST 1: Checking Dependencies")
    print("="*60)
    
    packages = {
        'numpy': 'NumPy',
        'librosa': 'Librosa',
        'scipy': 'SciPy',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'soundfile': 'SoundFile'
    }
    
    all_installed = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:15s} - Installed")
        except ImportError:
            print(f"✗ {name:15s} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n❌ Some packages are missing!")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def test_classifier_import():
    """Test that classifier module can be imported."""
    print("\n" + "="*60)
    print("TEST 2: Classifier Module Import")
    print("="*60)
    
    try:
        from classifier import UnderwaterSoundClassifier
        print("✓ Successfully imported UnderwaterSoundClassifier")
        print(f"✓ Module version: 1.0")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_classifier_instantiation():
    """Test that classifier can be instantiated."""
    print("\n" + "="*60)
    print("TEST 3: Classifier Instantiation")
    print("="*60)
    
    try:
        from classifier import UnderwaterSoundClassifier
        
        # Test SVM
        clf_svm = UnderwaterSoundClassifier(model_type='svm')
        print("✓ SVM classifier created")
        
        # Test Random Forest
        clf_rf = UnderwaterSoundClassifier(model_type='random_forest')
        print("✓ Random Forest classifier created")
        
        # Test custom MFCC
        clf_custom = UnderwaterSoundClassifier(n_mfcc=20, sr=8000)
        print("✓ Custom configuration classifier created")
        
        return True
    except Exception as e:
        print(f"✗ Failed to instantiate: {e}")
        return False


def test_directory_structure():
    """Test that required directories exist."""
    print("\n" + "="*60)
    print("TEST 4: Directory Structure")
    print("="*60)
    
    required_dirs = [
        'data',
        'data/raw',
        'data/processed',
        'models'
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name:20s} - Exists")
        else:
            print(f"✗ {dir_name:20s} - NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some directories missing. Creating them...")
        for dir_name in required_dirs:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        print("✓ Directories created")
    
    return True


def test_required_files():
    """Test that all required Python files exist."""
    print("\n" + "="*60)
    print("TEST 5: Required Files")
    print("="*60)
    
    required_files = {
        'classifier.py': 'Main classifier module',
        'example.py': 'Basic example',
        'advanced_examples.py': 'Advanced examples',
        'requirements.txt': 'Dependencies list',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide'
    }
    
    all_exist = True
    for filename, description in required_files.items():
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            print(f"✓ {filename:25s} - {size:6d} bytes")
        else:
            print(f"✗ {filename:25s} - NOT FOUND")
            all_exist = False
    
    return all_exist


def test_audio_file_loading():
    """Test audio file loading functionality."""
    print("\n" + "="*60)
    print("TEST 6: Audio File Loading")
    print("="*60)
    
    try:
        from classifier import UnderwaterSoundClassifier
        import numpy as np
        
        clf = UnderwaterSoundClassifier()
        
        # Create a test audio file (1 second of silence)
        import soundfile as sf
        
        test_dir = Path('data/raw/test')
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / 'test_audio.wav'
        
        # Create synthetic audio
        duration = 2  # 2 seconds
        sample_rate = 16000
        t = np.linspace(0, duration, int(sample_rate * duration))
        # 440 Hz sine wave (A note)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # Save
        sf.write(test_file, audio, sample_rate)
        print(f"✓ Created test audio: {test_file}")
        
        # Load
        loaded_audio, sr = clf.load_audio_file(str(test_file))
        print(f"✓ Loaded audio: {len(loaded_audio)} samples at {sr} Hz")
        
        # Cleanup
        test_file.unlink()
        test_dir.rmdir()
        
        return True
    except Exception as e:
        print(f"✗ Audio loading failed: {e}")
        return False


def test_feature_extraction():
    """Test MFCC feature extraction."""
    print("\n" + "="*60)
    print("TEST 7: Feature Extraction")
    print("="*60)
    
    try:
        from classifier import UnderwaterSoundClassifier
        import numpy as np
        import soundfile as sf
        
        clf = UnderwaterSoundClassifier(n_mfcc=13)
        
        # Create test audio
        duration = 2
        sample_rate = 16000
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # Extract features
        features = clf.extract_mfcc_features(audio)
        
        if features is not None:
            print(f"✓ Extracted features: {len(features)} dimensions")
            print(f"✓ Feature range: [{features.min():.4f}, {features.max():.4f}]")
            print(f"✓ Feature mean: {features.mean():.4f}")
            return True
        else:
            print("✗ Feature extraction returned None")
            return False
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        return False


def test_model_creation():
    """Test model creation and training."""
    print("\n" + "="*60)
    print("TEST 8: Model Creation")
    print("="*60)
    
    try:
        from classifier import UnderwaterSoundClassifier
        import numpy as np
        import soundfile as sf
        from pathlib import Path
        
        # Create test data structure
        test_data_dir = Path('data/raw/test_classes')
        test_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create two test classes
        for class_name in ['class1', 'class2']:
            class_dir = test_data_dir / class_name
            class_dir.mkdir(exist_ok=True)
            
            # Create 3 test files per class
            for i in range(3):
                sample_rate = 16000
                duration = 1
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # Different frequencies for different classes
                freq = 440 if class_name == 'class1' else 880
                audio = 0.5 * np.sin(2 * np.pi * freq * t)
                
                file_path = class_dir / f'sample_{i}.wav'
                sf.write(file_path, audio, sample_rate)
        
        print("✓ Created test data structure")
        
        # Train
        clf = UnderwaterSoundClassifier(model_type='svm')
        clf.load_audio_files(str(test_data_dir))
        
        if len(clf.features) > 0:
            print(f"✓ Loaded {len(clf.features)} test samples")
            clf.train(test_size=0.33)
            print("✓ Model training completed")
            
            # Cleanup
            import shutil
            shutil.rmtree(test_data_dir)
            
            return True
        else:
            print("✗ No features loaded")
            return False
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("UNDERWATER SOUND CLASSIFIER - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Dependencies", test_imports),
        ("Classifier Import", test_classifier_import),
        ("Classifier Instantiation", test_classifier_instantiation),
        ("Directory Structure", test_directory_structure),
        ("Required Files", test_required_files),
        ("Audio Loading", test_audio_file_loading),
        ("Feature Extraction", test_feature_extraction),
        ("Model Creation", test_model_creation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour underwater sound classifier is ready to use!")
        print("\nNext steps:")
        print("1. Read QUICKSTART.md")
        print("2. Add audio files to data/raw/")
        print("3. Run: python example.py")
        return True
    else:
        print("\n" + "="*60)
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above and try again.")
        print("See SETUP.md for troubleshooting help.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
