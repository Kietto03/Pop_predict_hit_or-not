import os
import librosa
import numpy as np
import pandas as pd

def extract_features(file_path):
    try:
        print(f"Processing: {file_path}")
        y, sr = librosa.load(file_path, sr=None)

        if len(y) == 0:
            raise ValueError(f"File {file_path} is empty or unreadable.")

        features = {
            'tempo': librosa.beat.tempo(y=y, sr=sr)[0],
            'beats': len(librosa.onset.onset_detect(y=y, sr=sr)),
            'chroma_stft': np.mean(librosa.feature.chroma_stft(y=y, sr=sr)),
            'rmse': np.mean(librosa.feature.rms(y=y)),
            'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            'spectral_bandwidth': np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
            'rolloff': np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y))
        }

        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(20):
            features[f'mfcc{i+1}'] = np.mean(mfccs[i])

        return features

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_all_wav_files(base_folders):
    wav_files = []
    for label, folder in base_folders.items():
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.wav'):
                    wav_files.append((os.path.join(root, file), label))
    return wav_files

def create_dataset(folders, output_csv):
    all_data = []
    labeled_files = get_all_wav_files(folders)

    for file_path, label in labeled_files:
        features = extract_features(file_path)
        if features:
            features['file_name'] = os.path.basename(file_path)
            features['label'] = label
            all_data.append(features)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"\n✅ Dataset saved to: {output_csv}")
    else:
        print("⚠️ No valid data to save.")

if __name__ == "__main__":
    folders = {
        'Trendy': 'Trendy',
        'Mid': 'Mid',
        'Flop': 'Flop'
    }

    create_dataset(folders, "output_dataset.csv")
