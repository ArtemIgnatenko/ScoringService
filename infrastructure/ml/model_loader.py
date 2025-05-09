import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from config.settings import settings

class ModelLoader:
    _models = {}
    
    @classmethod
    def load_model(cls, model_name: str):
        """Загружает модель из файла, если она еще не загружена."""
        if model_name in cls._models:
            return cls._models[model_name]
        
        if model_name == 'Логистическая регрессия':
            model_name = 'logistic_regression'
        if model_name == 'Случайный лес':
            model_name = 'random_forest'
        if model_name == 'Градиентный бустинг':
            model_name = 'lgbm'
        model_path = os.path.join(settings.MODEL_DIR, f"{model_name}.joblib")
        # '/Users/artemignatenko/Documents/Учеба/ML-сервисы/ScoringService/models/logistic_regression.joblib'
        if not os.path.exists(model_path):
            raise ValueError(f"Модель {model_name} не найдена по пути {model_path}")
        
        model = joblib.load(model_path)
        cls._models[model_name] = model
        return model

    @classmethod
    def get_model_names(cls):
        """Возвращает список доступных моделей."""
        model_files = [f for f in os.listdir(settings.MODEL_DIR) if f.endswith('.joblib')]
        return [os.path.splitext(f)[0] for f in model_files]