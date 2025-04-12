import os
import numpy as np
import librosa
import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

# Load models and scalers from pickle folder
models = {
    'SVM': pickle.load(open('pickle/svm_model.pkl', 'rb')),
    'KNN': pickle.load(open('pickle/knn_model.pkl', 'rb')),
    'Logistic Regression': pickle.load(open('pickle/logreg_model.pkl', 'rb')),
    'XGBoost': pickle.load(open('pickle/xgbc_model.pkl', 'rb'))
}
scaler = pickle.load(open('pickle/scaler.pkl', 'rb'))
label_encoder = pickle.load(open('pickle/label_encoder.pkl', 'rb'))

# Audio feature extraction
def getmetadata(filename):
    y, sr = librosa.load(filename)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo_arr = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    y_harmonic, y_percussive = librosa.effects.hpss(y)
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    beats = librosa.onset.onset_detect(y=y, sr=sr)

    metadata_list = [
        float(tempo),                              # 1
        len(beats),                                # 2
        np.mean(chroma_stft),                      # 3
        np.mean(rmse),                             
        np.mean(spec_centroid),
        np.mean(spec_bw),
        np.mean(spec_rolloff),
        np.mean(zero_crossing),                    # 8
    ]

    # Add MFCCs 1 to 20 → total: 28 features
    for i in range(20):
        metadata_list.append(np.mean(mfcc[i]))

    return metadata_list


# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    try:
        features = getmetadata(filepath)
        features = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features)

        predictions = {
            name: label_encoder.inverse_transform(model.predict(features_scaled))[0]
            for name, model in models.items()
        }

        return render_template('result.html', predictions=predictions, filename=file.filename)

    except Exception as e:
        return f"Error processing file: {e}"

# Run app
if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
