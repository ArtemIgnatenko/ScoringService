import pandas as pd
from typing import Dict, Any

class DataPreprocessor:
    @staticmethod
    def validate_input_data(data: Dict[str, Any], expected_features: Dict[str, type]) -> bool:
        """Проверяет, что все необходимые поля присутствуют и имеют правильный тип."""
        for feature, feature_type in expected_features.items():
            if feature not in data:
                return False
            
            if not isinstance(data[feature], feature_type):
                return False
        
        return True
    
    @staticmethod
    def prepare_input_data(data: Dict[str, Any]) -> pd.DataFrame:
        """Преобразует словарь в DataFrame для модели."""
        return pd.DataFrame([data])
    
    @staticmethod
    def process_output(prediction, prediction_proba=None):
        """Обрабатывает выходные данные модели."""
        if prediction_proba is not None:
            if len(prediction_proba.shape) > 1 and prediction_proba.shape[1] > 1:
                # Для бинарной классификации берем вероятность класса 1
                probability = prediction_proba[0][1]
            else:
                probability = prediction_proba[0]
            
            return int(prediction[0]), float(probability)
        else:
            return int(prediction[0]), None
