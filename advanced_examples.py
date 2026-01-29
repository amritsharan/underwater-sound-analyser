"""
Advanced Examples - Underwater Sound Classifier
Demonstrates advanced usage patterns and techniques
"""

from classifier import UnderwaterSoundClassifier
import numpy as np
from pathlib import Path


def example_1_basic_workflow():
    """Example 1: Basic Training and Prediction Workflow"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Training and Prediction")
    print("="*60)
    
    # Initialize
    classifier = UnderwaterSoundClassifier(model_type='svm')
    
    # Load data
    classifier.load_audio_files('data/raw/')
    
    # Train
    classifier.train(test_size=0.2)
    
    # Save
    classifier.save_model('models/basic_classifier.pkl')
    
    # Predict
    audio_files = list(Path('data/raw').rglob('*.wav'))
    if audio_files:
        prediction = classifier.predict(str(audio_files[0]))
        print(f"\nPrediction for {audio_files[0].name}: {prediction}")


def example_2_model_comparison():
    """Example 2: Compare Different Models"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Model Comparison")
    print("="*60)
    
    models_info = {
        'svm': {'accuracy': None, 'model': None},
        'random_forest': {'accuracy': None, 'model': None}
    }
    
    for model_type in ['svm', 'random_forest']:
        classifier = UnderwaterSoundClassifier(model_type=model_type)
        classifier.load_audio_files('data/raw/')
        classifier.train()
        
        # Store results
        from sklearn.metrics import accuracy_score
        if hasattr(classifier, 'y_test'):
            accuracy = accuracy_score(classifier.y_test, classifier.y_pred)
            models_info[model_type]['accuracy'] = accuracy
            models_info[model_type]['model'] = classifier
    
    # Print comparison
    print("\nModel Performance Summary:")
    print("-" * 40)
    for model_type, info in models_info.items():
        if info['accuracy'] is not None:
            print(f"{model_type:15s}: {info['accuracy']:.4f}")


def example_3_batch_prediction():
    """Example 3: Batch Prediction on Test Data"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Prediction")
    print("="*60)
    
    # Load model
    classifier = UnderwaterSoundClassifier()
    classifier.load_model('models/underwater_svm.pkl')
    
    # Batch predict
    test_dir = Path('data/raw')
    audio_files = list(test_dir.rglob('*.wav'))
    
    if audio_files:
        print(f"\nMaking predictions on {len(audio_files[:10])} files:")
        print("-" * 50)
        
        for audio_file in audio_files[:10]:
            prediction = classifier.predict(str(audio_file))
            print(f"{audio_file.name:30s} -> {prediction}")


def example_4_feature_analysis():
    """Example 4: Analyze Extracted Features"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Feature Analysis")
    print("="*60)
    
    classifier = UnderwaterSoundClassifier(n_mfcc=13)
    classifier.load_audio_files('data/raw/')
    
    if classifier.features is not None and len(classifier.features) > 0:
        print(f"\nFeature Statistics:")
        print("-" * 50)
        print(f"Number of samples: {len(classifier.features)}")
        print(f"Number of features per sample: {classifier.features.shape[1]}")
        print(f"Classes: {classifier.classes_}")
        
        print(f"\nFeature values (per class):")
        for class_name in classifier.classes_:
            class_mask = np.array(classifier.labels) == class_name
            class_features = classifier.features[class_mask]
            
            print(f"\n{class_name}:")
            print(f"  Samples: {len(class_features)}")
            print(f"  Mean (MFCC 0): {np.mean(class_features[:, 0]):.4f}")
            print(f"  Std (MFCC 0): {np.mean(class_features[:, 13]):.4f}")


def example_5_custom_mfcc():
    """Example 5: Use Different MFCC Coefficient Counts"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom MFCC Coefficients")
    print("="*60)
    
    for n_mfcc in [10, 13, 20]:
        print(f"\nTraining with n_mfcc={n_mfcc}")
        
        classifier = UnderwaterSoundClassifier(model_type='svm', n_mfcc=n_mfcc)
        classifier.load_audio_files('data/raw/')
        classifier.train(test_size=0.2)
        
        classifier.save_model(f'models/classifier_mfcc{n_mfcc}.pkl')


def example_6_visualization():
    """Example 6: Visualize Audio and Features"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Audio Visualization")
    print("="*60)
    
    classifier = UnderwaterSoundClassifier()
    
    audio_files = list(Path('data/raw').rglob('*.wav'))
    if audio_files:
        sample_file = str(audio_files[0])
        
        print(f"\nVisualizing: {sample_file}")
        
        try:
            # Plot spectrogram
            classifier.plot_spectrogram(sample_file, 
                                       title=f"Spectrogram: {Path(sample_file).name}")
            
            # Plot MFCC
            classifier.plot_mfcc(sample_file,
                               title=f"MFCC: {Path(sample_file).name}")
        except Exception as e:
            print(f"Could not display plots: {e}")


def example_7_cross_validation():
    """Example 7: Cross-Validation for Better Estimates"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Cross-Validation")
    print("="*60)
    
    from sklearn.model_selection import cross_val_score
    
    classifier = UnderwaterSoundClassifier(model_type='svm')
    classifier.load_audio_files('data/raw/')
    
    if len(classifier.features) >= 10:
        # Scale features
        X_scaled = classifier.scaler.fit_transform(classifier.features)
        
        # Cross-validation (5-fold)
        scores = cross_val_score(classifier.model, X_scaled, 
                               classifier.labels, cv=5)
        
        print(f"\n5-Fold Cross-Validation Scores:")
        print(f"  Scores: {scores}")
        print(f"  Mean: {scores.mean():.4f} (+/- {scores.std():.4f})")


def example_8_save_features():
    """Example 8: Save Extracted Features for Later Use"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Save Extracted Features")
    print("="*60)
    
    import pickle
    
    classifier = UnderwaterSoundClassifier()
    classifier.load_audio_files('data/raw/')
    
    # Save features
    features_data = {
        'features': classifier.features,
        'labels': classifier.labels,
        'file_paths': classifier.file_paths,
        'classes': classifier.classes_
    }
    
    features_path = 'data/processed/features.pkl'
    
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    with open(features_path, 'wb') as f:
        pickle.dump(features_data, f)
    
    print(f"\nFeatures saved to {features_path}")
    print(f"Total samples: {len(features_data['features'])}")


def example_9_new_classes():
    """Example 9: Train with Custom Classes"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Custom Sound Classes")
    print("="*60)
    
    print("\nExample custom underwater sound categories:")
    print("  - Biological: whale_calls, dolphin_clicks, fish_sounds")
    print("  - Anthropogenic: ship_noise, sonar, drilling")
    print("  - Environmental: waves, rain, earthquakes")
    
    print("\nTo use custom classes:")
    print("1. Create subdirectories in data/raw/ with your class names")
    print("2. Add WAV files to each subdirectory")
    print("3. Run classifier.load_audio_files('data/raw/')")
    print("4. Classes will be auto-detected from directory names")


def example_10_performance_metrics():
    """Example 10: Detailed Performance Metrics"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Performance Metrics")
    print("="*60)
    
    from sklearn.metrics import precision_recall_fscore_support
    
    classifier = UnderwaterSoundClassifier(model_type='svm')
    classifier.load_audio_files('data/raw/')
    classifier.train(test_size=0.2)
    
    if hasattr(classifier, 'y_test'):
        precision, recall, f1, _ = precision_recall_fscore_support(
            classifier.y_test, classifier.y_pred
        )
        
        print(f"\nDetailed Performance Metrics:")
        print("-" * 50)
        for i, class_name in enumerate(classifier.classes_):
            print(f"\n{class_name}:")
            print(f"  Precision: {precision[i]:.4f}")
            print(f"  Recall: {recall[i]:.4f}")
            print(f"  F1-Score: {f1[i]:.4f}")


# Run all examples
if __name__ == '__main__':
    print("\n" + "="*60)
    print("UNDERWATER SOUND CLASSIFIER - ADVANCED EXAMPLES")
    print("="*60)
    
    examples = [
        ("Basic Workflow", example_1_basic_workflow),
        ("Model Comparison", example_2_model_comparison),
        ("Batch Prediction", example_3_batch_prediction),
        ("Feature Analysis", example_4_feature_analysis),
        ("Custom MFCC", example_5_custom_mfcc),
        ("Visualization", example_6_visualization),
        ("Cross-Validation", example_7_cross_validation),
        ("Save Features", example_8_save_features),
        ("Custom Classes", example_9_new_classes),
        ("Performance Metrics", example_10_performance_metrics),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nNote: Check data/raw/ for audio files first!")
    print("Run: python example.py  (to create sample structure)")
    
    # Uncomment to run a specific example:
    # example_1_basic_workflow()
    # example_2_model_comparison()
    # ... etc
