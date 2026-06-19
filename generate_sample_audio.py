#!/usr/bin/env python3
"""
Generate sample audio files for the Underwater Sound Classifier project.
Creates synthetic whale calls, ship noise, and ambient underwater sounds.
"""

import sys
import numpy as np
import soundfile as sf
import os
from pathlib import Path

# Support UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def generate_whale_call(duration=2.0, sr=16000):
    """Generate a synthetic whale call (low frequency, melodic pattern)."""
    t = np.linspace(0, duration, int(sr * duration))
    
    # Whale calls are typically low frequency (20-500 Hz)
    # Create a frequency sweep pattern
    f1 = 100 + 50 * np.sin(2 * np.pi * 0.5 * t)  # 100-150 Hz sweep
    whale_call = np.sin(2 * np.pi * f1 * t)
    
    # Add amplitude modulation for realism
    envelope = np.sin(2 * np.pi * 0.3 * t) ** 2
    whale_call = whale_call * envelope
    
    # Add harmonic content
    whale_call += 0.3 * np.sin(2 * np.pi * (f1 * 2) * t) * envelope
    
    return whale_call.astype(np.float32)


def generate_ship_noise(duration=2.0, sr=16000):
    """Generate synthetic ship noise (mid-frequency, noisy pattern)."""
    t = np.linspace(0, duration, int(sr * duration))
    
    # Ship noise contains multiple frequencies (100-2000 Hz range)
    noise = np.random.randn(len(t))
    
    # Filter to mid-frequency range by adding harmonics
    ship_sound = (
        0.5 * np.sin(2 * np.pi * 200 * t) +  # Primary frequency
        0.3 * np.sin(2 * np.pi * 400 * t) +  # Harmonic
        0.2 * np.sin(2 * np.pi * 600 * t) +  # Harmonic
        0.5 * noise  # Broadband noise
    )
    
    # Apply envelope
    envelope = np.ones_like(t)
    envelope[:int(0.1 * sr)] = np.linspace(0, 1, int(0.1 * sr))  # fade in
    envelope[-int(0.1 * sr):] = np.linspace(1, 0, int(0.1 * sr))  # fade out
    
    ship_sound = ship_sound * envelope
    
    return (ship_sound / np.max(np.abs(ship_sound)) * 0.8).astype(np.float32)


def generate_ambient_sound(duration=2.0, sr=16000):
    """Generate synthetic ambient underwater sound (high frequency, continuous)."""
    t = np.linspace(0, duration, int(sr * duration))
    
    # Ambient ocean sound is typically higher frequency and noisy
    noise = np.random.randn(len(t))
    
    # Add some mid-to-high frequency components
    ambient = (
        0.3 * np.sin(2 * np.pi * 800 * t) +
        0.2 * np.sin(2 * np.pi * 1200 * t) +
        0.2 * np.sin(2 * np.pi * 1600 * t) +
        0.6 * noise
    )
    
    # Apply gentle envelope to avoid clicks
    envelope = 0.5 + 0.3 * np.sin(2 * np.pi * 0.2 * t)
    ambient = ambient * envelope
    
    return (ambient / np.max(np.abs(ambient)) * 0.7).astype(np.float32)


def main():
    """Generate sample audio files in the project structure."""
    
    # Sample rate
    sr = 16000
    
    # Base directory
    base_dir = Path(__file__).parent / "data" / "raw"
    
    # Create directories
    dirs = {
        "whale_calls": base_dir / "whale_calls",
        "ship_noise": base_dir / "ship_noise",
        "ambient_sound": base_dir / "ambient_sound"
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("🐋 Generating Sample Audio Files for Underwater Sound Classifier")
    print("=" * 60)
    
    # Generate whale call samples
    print("\n🐋 Generating whale calls...")
    for i in range(5):
        audio = generate_whale_call(duration=2.0, sr=sr)
        filename = dirs["whale_calls"] / f"whale_call_{i+1:02d}.wav"
        sf.write(filename, audio, sr)
        print(f"   ✓ Created: {filename.name}")
    
    # Generate ship noise samples
    print("\n🚢 Generating ship noise...")
    for i in range(5):
        audio = generate_ship_noise(duration=2.0, sr=sr)
        filename = dirs["ship_noise"] / f"ship_noise_{i+1:02d}.wav"
        sf.write(filename, audio, sr)
        print(f"   ✓ Created: {filename.name}")
    
    # Generate ambient sound samples
    print("\n🌊 Generating ambient underwater sounds...")
    for i in range(5):
        audio = generate_ambient_sound(duration=2.0, sr=sr)
        filename = dirs["ambient_sound"] / f"ambient_sound_{i+1:02d}.wav"
        sf.write(filename, audio, sr)
        print(f"   ✓ Created: {filename.name}")
    
    print("\n" + "=" * 60)
    print("✅ Successfully generated 15 sample audio files!")
    print("\nFiles created in:")
    for name, path in dirs.items():
        count = len(list(path.glob("*.wav")))
        print(f"   • {name}: {count} files in {path}")
    
    print("\n📁 Directory structure created:")
    print(f"   {base_dir}/")
    print(f"   ├── whale_calls/ (5 files)")
    print(f"   ├── ship_noise/ (5 files)")
    print(f"   └── ambient_sound/ (5 files)")
    
    print("\n✨ You can now use these files to train the classifier!")
    print("   Run: python run_desktop.py")
    print("   Then go to Training tab and select: data/raw/")


if __name__ == "__main__":
    main()
