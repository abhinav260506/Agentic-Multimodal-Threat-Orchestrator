"""
Train Machine Learning Model for Cybersecurity Threat Detection
Uses the cybersecurity_threat_detection_logs.csv dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')
import config


class ThreatDetectionModel:
    """Machine Learning model for cybersecurity threat detection"""
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.model_path = config.OUTPUT_DIR / "threat_detection_model.pkl"
        self.encoders_path = config.OUTPUT_DIR / "label_encoders.pkl"
        self.metadata_path = config.OUTPUT_DIR / "model_metadata.json"
    
    def load_data(self, csv_path: Path, sample_size: int = None):
        """Load and prepare the dataset"""
        print(f"Loading data from {csv_path}...")
        
        # Load data in chunks if it's large
        if sample_size:
            df = pd.read_csv(csv_path, nrows=sample_size)
        else:
            # Try to load all, but limit if too large
            try:
                df = pd.read_csv(csv_path)
                if len(df) > 100000:
                    print(f"Dataset is large ({len(df)} rows). Sampling 100,000 rows for training...")
                    df = df.sample(n=100000, random_state=42)
            except MemoryError:
                print("Dataset too large. Loading 50,000 rows...")
                df = pd.read_csv(csv_path, nrows=50000)
        
        print(f"Loaded {len(df)} rows")
        print(f"Threat label distribution:\n{df['threat_label'].value_counts()}")
        
        return df
    
    def preprocess_features(self, df: pd.DataFrame, is_training: bool = True):
        """Preprocess features for ML model"""
        print("\nPreprocessing features...")
        
        # Create a copy
        data = df.copy()
        
        # Extract features from IP addresses (simplified - just use last octet)
        data['source_ip_last'] = data['source_ip'].apply(lambda x: int(x.split('.')[-1]) if pd.notna(x) else 0)
        data['dest_ip_last'] = data['dest_ip'].apply(lambda x: int(x.split('.')[-1]) if pd.notna(x) else 0)
        
        # Extract hour from timestamp
        data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
        data['hour'] = data['timestamp'].dt.hour.fillna(0)
        data['day_of_week'] = data['timestamp'].dt.dayofweek.fillna(0)
        
        # Encode categorical features
        categorical_features = ['protocol', 'action', 'log_type']
        
        if is_training:
            # Fit label encoders
            for feature in categorical_features:
                le = LabelEncoder()
                data[feature + '_encoded'] = le.fit_transform(data[feature].astype(str))
                self.label_encoders[feature] = le
        else:
            # Transform using existing encoders
            for feature in categorical_features:
                if feature in self.label_encoders:
                    le = self.label_encoders[feature]
                    # Handle unseen categories
                    data[feature + '_encoded'] = data[feature].astype(str).apply(
                        lambda x: le.transform([x])[0] if x in le.classes_ else -1
                    )
                else:
                    data[feature + '_encoded'] = 0
        
        # Extract features from user_agent (simplified)
        data['user_agent_length'] = data['user_agent'].astype(str).str.len()
        data['is_suspicious_ua'] = data['user_agent'].astype(str).str.contains(
            'Nmap|SQLMap|curl', case=False, na=False
        ).astype(int)
        
        # Extract features from request_path
        data['request_path_length'] = data['request_path'].astype(str).str.len()
        data['is_suspicious_path'] = data['request_path'].astype(str).str.contains(
            'admin|backup|login|upload|phpmyadmin|wp-login', case=False, na=False
        ).astype(int)
        
        # Select features for training
        feature_columns = [
            'source_ip_last', 'dest_ip_last', 'hour', 'day_of_week',
            'protocol_encoded', 'action_encoded', 'log_type_encoded',
            'bytes_transferred', 'user_agent_length', 'is_suspicious_ua',
            'request_path_length', 'is_suspicious_path'
        ]
        
        if is_training:
            self.feature_columns = feature_columns
        
        X = data[feature_columns].fillna(0)
        
        return X, data['threat_label'] if 'threat_label' in data.columns else None
    
    def train(self, csv_path: Path, sample_size: int = None, test_size: float = 0.2):
        """Train the threat detection model"""
        print("="*60)
        print("TRAINING CYBERSECURITY THREAT DETECTION MODEL")
        print("="*60)
        
        # Load data
        df = self.load_data(csv_path, sample_size)
        
        # Preprocess
        X, y = self.preprocess_features(df, is_training=True)
        
        # Encode target variable
        label_encoder_y = LabelEncoder()
        y_encoded = label_encoder_y.fit_transform(y)
        self.label_encoders['threat_label'] = label_encoder_y
        
        print(f"\nEncoded threat labels: {dict(zip(label_encoder_y.classes_, label_encoder_y.transform(label_encoder_y.classes_)))}")
        
        # Split data
        print(f"\nSplitting data (test_size={test_size})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Train model
        print("\nTraining Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',  # Handle imbalanced classes
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print("MODEL PERFORMANCE")
        print(f"{'='*60}")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=label_encoder_y.classes_))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        print("\nTop 10 Most Important Features:")
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(feature_importance.head(10).to_string(index=False))
        
        # Save model
        self.save_model()
        
        return accuracy
    
    def predict(self, X):
        """Make predictions on new data"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first or load_model()")
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        # Decode predictions
        if 'threat_label' in self.label_encoders:
            decoded_predictions = self.label_encoders['threat_label'].inverse_transform(predictions)
        else:
            decoded_predictions = predictions
        
        return decoded_predictions, probabilities
    
    def save_model(self):
        """Save the trained model and encoders"""
        print(f"\nSaving model to {self.model_path}...")
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save encoders
        with open(self.encoders_path, 'wb') as f:
            pickle.dump(self.label_encoders, f)
        
        # Save metadata
        metadata = {
            'feature_columns': self.feature_columns,
            'model_type': 'RandomForestClassifier',
            'n_features': len(self.feature_columns)
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Model saved successfully!")
    
    def load_model(self):
        """Load the trained model and encoders"""
        print(f"Loading model from {self.model_path}...")
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}. Train the model first.")
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(self.encoders_path, 'rb') as f:
            self.label_encoders = pickle.load(f)
        
        with open(self.metadata_path, 'r') as f:
            metadata = json.load(f)
            self.feature_columns = metadata['feature_columns']
        
        print("Model loaded successfully!")


def main():
    """Main training function"""
    log_file = config.LOG_DIR / "cybersecurity_threat_detection_logs.csv"
    
    if not log_file.exists():
        print(f"Error: Log file not found at {log_file}")
        return
    
    # Create model instance
    model = ThreatDetectionModel()
    
    # Train model (use sample_size=None to train on full dataset, or specify a number)
    # For faster training, you can use sample_size=50000
    print("\nStarting training...")
    print("Note: For large datasets, this may take several minutes.")
    
    accuracy = model.train(
        csv_path=log_file,
        sample_size=None,  # Set to None for full dataset, or a number like 50000 for faster training
        test_size=0.2
    )
    
    print(f"\n{'='*60}")
    print("TRAINING COMPLETE!")
    print(f"{'='*60}")
    print(f"Model saved to: {model.model_path}")
    print(f"Final Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()



