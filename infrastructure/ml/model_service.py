from typing import Dict, Any, Tuple
import pandas as pd
from infrastructure.ml.model_loader import ModelLoader
from infrastructure.ml.preprocessor import DataPreprocessor

class ModelService:
    def __init__(self):
        self.expected_features = {
            "person_age": int,
            "person_income": int,
            "person_home_ownership": str,
            "person_emp_length": float,
            "loan_intent": str,
            "loan_grade": str,
            "loan_amnt": int,
            "loan_int_rate": float,
            "loan_percent_income": float,
            "cb_person_default_on_file": str,
            "cb_person_cred_hist_length": int
        }
    
    async def predict(self, model_name: str, input_data: Dict[str, Any]) -> Tuple[int, float]:
        """
        Выполняет предсказание с использованием указанной модели.
        
        Args:
            model_name: Название модели (logistic_regression, random_forest, lgbm)
            input_data: Словарь с входными данными
            
        Returns:
            Tuple[int, float]: Предсказание (0 или 1) и вероятность класса 1
        """
        # Проверяем входные данные
        if not DataPreprocessor.validate_input_data(input_data, self.expected_features):
            raise ValueError("Неверный формат входных данных")
        
        # Загружаем модель
        model = ModelLoader.load_model(model_name)
        
        # Готовим данные для предсказания
        df = DataPreprocessor.prepare_input_data(input_data)
        
        # Выполняем предсказание
        prediction = model.predict(df)
        prediction_proba = model.predict_proba(df)
        
        # Обрабатываем результат
        result, probability = DataPreprocessor.process_output(prediction, prediction_proba)
        
        return result, probability
    
    async def get_available_models(self):
        """Возвращает список доступных моделей."""
        return ModelLoader.get_model_names()
# При запуске сервиса нужно предварительно сохранить модели в директорию MODEL_DIR
# Вот пример сохранения моделей: