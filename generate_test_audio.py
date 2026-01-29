#!/usr/bin/env python3
"""
Generate test audio files for prediction in the processed folder.
Creates mixed audio files without categorization for testing the classifier.
"""

import numpy as np
import soundfile as sf
from pathlib import Path


def generate_whale_call(duration=2.0, sr=16000, variation=0):
    """Generate a synthetic whale call with variations."""
    t = np.linspace(0, duration, int(sr * duration))
    
    # Add variation to frequency
    base_freq = 100 + variation * 10
    f1 = base_freq + 50 * np.sin(2 * np.pi * (0.5 + variation * 0.1) * t)
    whale_call = np.sin(2 * np.pi * f1 * t)
    
    # Add amplitude modulation
    envelope = np.sin(2 * np.pi * (0.3 + variation * 0.05) * t) ** 2
    whale_call = whale_call * envelope
    
    # Add harmonic content
    whale_call += (0.3 + variation * 0.05) * np.sin(2 * np.pi * (f1 * 2) * t) * envelope
    
    return whale_call.astype(np.float32)


def generate_ship_noise(duration=2.0, sr=16000, variation=0):
    """Generate synthetic ship noise with variations."""
    t = np.linspace(0, duration, int(sr * duration))
    
    noise = np.random.randn(len(t))
    
    # Vary the primary frequency
    primary_freq = 200 + variation * 50
    ship_sound = (
        0.5 * np.sin(2 * np.pi * primary_freq * t) +
        0.3 * np.sin(2 * np.pi * (primary_freq * 2) * t) +
        0.2 * np.sin(2 * np.pi * (primary_freq * 3) * t) +
        (0.5 + variation * 0.1) * noise
    )
    
    # Apply envelope
    envelope = np.ones_like(t)
    envelope[:int(0.1 * sr)] = np.linspace(0, 1, int(0.1 * sr))
    envelope[-int(0.1 * sr):] = np.linspace(1, 0, int(0.1 * sr))
    
    ship_sound = ship_sound * envelope
    
    return (ship_sound / np.max(np.abs(ship_sound)) * 0.8).astype(np.float32)


def generate_ambient_sound(duration=2.0, sr=16000, variation=0):
    """Generate synthetic ambient underwater sound with variations."""
    t = np.linspace(0, duration, int(sr * duration))
    
    noise = np.random.randn(len(t))
    
    # Vary the frequency components
    base_freq = 800 + variation * 100
    ambient = (
        0.3 * np.sin(2 * np.pi * base_freq * t) +
        0.2 * np.sin(2 * np.pi * (base_freq * 1.5) * t) +
        0.2 * np.sin(2 * np.pi * (base_freq * 2) * t) +
        (0.6 + variation * 0.05) * noise
    )
    
    # Apply gentle envelope
    envelope = 0.5 + 0.3 * np.sin(2 * np.pi * (0.2 + variation * 0.05) * t)
    ambient = ambient * envelope
    
    return (ambient / np.max(np.abs(ambient)) * 0.7).astype(np.float32)


def main():
    """Generate test audio files in processed folder without categorization."""
    
    sr = 16000
    processed_dir = Path(__file__).parent / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎵 Generating Test Audio Files for Prediction")
    print("=" * 60)
    print(f"Output directory: {processed_dir}\n")
    
    # Generate mixed test files - 3 of each type with descriptive but not obvious names
    test_files = [
        # Whale calls with neutral names
        ("test_audio_001.wav", generate_whale_call, 0, "whale_calls"),
        ("test_audio_005.wav", generate_whale_call, 1, "whale_calls"),
        ("test_audio_009.wav", generate_whale_call, 2, "whale_calls"),
        
        # Ship noise with neutral names
        ("test_audio_002.wav", generate_ship_noise, 0, "ship_noise"),
        ("test_audio_006.wav", generate_ship_noise, 1, "ship_noise"),
        ("test_audio_010.wav", generate_ship_noise, 2, "ship_noise"),
        
        # Ambient sounds with neutral names
        ("test_audio_003.wav", generate_ambient_sound, 0, "ambient_sound"),
        ("test_audio_007.wav", generate_ambient_sound, 1, "ambient_sound"),
        ("test_audio_011.wav", generate_ambient_sound, 2, "ambient_sound"),
        
        # Additional mixed samples
        ("test_audio_004.wav", generate_whale_call, 3, "whale_calls"),
        ("test_audio_008.wav", generate_ship_noise, 3, "ship_noise"),
        ("test_audio_012.wav", generate_ambient_sound, 3, "ambient_sound"),
    ]
    
    print("Generating test files...")
    created_files = []
    
    for filename, generator_func, variation, actual_class in test_files:
        audio = generator_func(duration=2.0, sr=sr, variation=variation)
        filepath = processed_dir / filename
        sf.write(filepath, audio, sr)
        created_files.append((filename, actual_class))
        print(f"   ✓ Created: {filename}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully generated {len(created_files)} test audio files!")
    print(f"\n📁 Files created in: {processed_dir}")
    
    # Create answer key file
    answer_key_path = processed_dir / "ANSWER_KEY.txt"
    with open(answer_key_path, "w", encoding="utf-8") as f:
        f.write("TEST AUDIO FILES - ANSWER KEY\n")
        f.write("=" * 60 + "\n\n")
        f.write("Use these files to test your trained model's predictions.\n")
        f.write("The actual classes are:\n\n")
        for filename, actual_class in created_files:
            f.write(f"{filename:<25} -> {actual_class}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("Note: These files are generated synthetically for testing.\n")
        f.write("Train your model on data/raw/ first, then predict these files!\n")
    
    print(f"\n📝 Answer key created: {answer_key_path.name}")
    print("\n✨ Ready for testing!")
    print("\nNext steps:")
    print("   1. Train your model using data/raw/ directory")
    print("   2. Go to Prediction tab")
    print("   3. Test with files from data/processed/")
    print("   4. Check ANSWER_KEY.txt to verify predictions!")


if __name__ == "__main__":
    main()
