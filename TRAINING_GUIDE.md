# Model Training Guide

## Overview

The framework now supports machine learning-based threat detection using a trained Random Forest model. The model is trained on the `cybersecurity_threat_detection_logs.csv` dataset.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `scikit-learn` - Machine learning library

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Load the cybersecurity threat detection logs
- Preprocess the data (feature engineering)
- Train a Random Forest classifier
- Evaluate the model performance
- Save the trained model to `output/threat_detection_model.pkl`

### 3. Use the Trained Model

The `LogAgent` will automatically use the trained ML model if available. Otherwise, it falls back to LLM-based analysis.

```python
from log_agent import LogAgent

# ML model will be used automatically if trained
log_agent = LogAgent()
result = log_agent.analyze()
```

## Training Details

### Features Used

The model uses the following features extracted from logs:

1. **Network Features**:
   - Source IP (last octet)
   - Destination IP (last octet)
   - Protocol (encoded)
   - Action (allowed/blocked, encoded)

2. **Temporal Features**:
   - Hour of day
   - Day of week

3. **Behavioral Features**:
   - Bytes transferred
   - User agent length
   - Suspicious user agent detection (Nmap, SQLMap, curl)
   - Request path length
   - Suspicious path detection (admin, backup, login, etc.)

4. **Log Type**:
   - Log type (firewall, application, ids, encoded)

### Model Architecture

- **Algorithm**: Random Forest Classifier
- **Trees**: 100 estimators
- **Max Depth**: 20
- **Class Weight**: Balanced (handles imbalanced classes)
- **Features**: 12 engineered features

### Threat Labels

The model predicts three threat levels:
- **benign**: Normal, safe activity
- **suspicious**: Potentially harmful activity
- **malicious**: Confirmed threat

## Training Options

### Full Dataset Training

```python
# In train_model.py, set:
sample_size=None  # Uses entire dataset
```

### Quick Training (for testing)

```python
# In train_model.py, set:
sample_size=50000  # Uses 50,000 samples
```

## Model Performance

After training, you'll see:
- **Accuracy**: Overall classification accuracy
- **Classification Report**: Precision, recall, F1-score per class
- **Confusion Matrix**: True vs predicted labels
- **Feature Importance**: Top features contributing to predictions

## Model Files

After training, these files are created in `output/`:

- `threat_detection_model.pkl` - Trained model
- `label_encoders.pkl` - Feature encoders
- `model_metadata.json` - Model metadata

## Using the Model

### Automatic Usage

The `LogAgent` automatically detects and uses the ML model:

```python
from main_orchestrator import CyberOrchestrator

orchestrator = CyberOrchestrator()
orchestrator.run_quick_scan()  # Uses ML model automatically
```

### Manual Usage

```python
from train_model import ThreatDetectionModel
import pandas as pd

# Load model
model = ThreatDetectionModel()
model.load_model()

# Load new data
df = pd.read_csv('new_logs.csv')

# Preprocess and predict
X, _ = model.preprocess_features(df, is_training=False)
predictions, probabilities = model.predict(X)

print(f"Predictions: {predictions}")
print(f"Probabilities: {probabilities}")
```

## Retraining

To retrain the model with new data:

1. Update `cybersecurity_threat_detection_logs.csv` with new logs
2. Run `python train_model.py` again
3. The old model will be overwritten

## Troubleshooting

### "Model not found" Error

**Solution**: Train the model first:
```bash
python train_model.py
```

### Memory Error During Training

**Solution**: Reduce sample size in `train_model.py`:
```python
sample_size=50000  # Instead of None
```

### Low Accuracy

**Solutions**:
1. Train on more data (increase `sample_size`)
2. Check data quality
3. Adjust model hyperparameters in `train_model.py`

## Performance Tips

1. **For Large Datasets**: Use `sample_size` parameter to limit training data
2. **For Faster Training**: Reduce `n_estimators` in RandomForestClassifier
3. **For Better Accuracy**: Increase `sample_size` and `n_estimators`

## Model Evaluation

The training script automatically:
- Splits data into train/test sets (80/20)
- Evaluates on test set
- Shows classification metrics
- Displays feature importance

## Next Steps

After training:
1. Review model performance metrics
2. Test on new log data
3. Integrate into your security workflow
4. Set up periodic retraining with new data



