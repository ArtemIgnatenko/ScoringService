import joblib
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from category_encoders import LeaveOneOutEncoder
from config.settings import settings

import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

    
# Функция для кодирования бинарного столбца
def encode_binary_column(X):
    binary_feature = "cb_person_default_on_file"
    le = LabelEncoder()
    X_copy = X.copy()
    X_copy[binary_feature] = le.fit_transform(X_copy[binary_feature])
    return X_copy

def save_models():
    logger.info("Начинаю сохранение моделей...")
    """
    Сохраняет обученные модели в директорию MODEL_DIR.
    
    Этот код выполняется один раз при запуске сервиса или при обновлении моделей.
    """
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    
    # Загружаем данные
    # df = pd.read_csv('credit_risk_dataset.csv')
    df = pd.read_csv('/Users/artemignatenko/Documents/Учеба/ML-сервисы/ScoringService/infrastructure/ml/credit_risk_dataset.csv')
    
    # Предобработка данных
    df['person_home_ownership'] = df['person_home_ownership'].replace({'OTHER': 'RENT'})
    df["person_emp_length"] = df["person_emp_length"].fillna(df["person_emp_length"].mean())
    df["loan_int_rate"] = df["loan_int_rate"].fillna(df["loan_int_rate"].mean())
    
    # Разделение на признаки и целевую переменную
    X = df.drop(columns="loan_status")
    y = df["loan_status"]
    
    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # Определение числовых и категориальных признаков
    numerical_features = ["person_age", "person_income", "person_emp_length", 
                          "loan_amnt", "loan_int_rate", "loan_percent_income", 
                          "cb_person_cred_hist_length"]
    categorical_features = ["person_home_ownership", "loan_intent", "loan_grade"]
    binary_feature = "cb_person_default_on_file"
    
    # Модель логистической регрессии
    preprocessor_lr = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", LeaveOneOutEncoder(cols=categorical_features), categorical_features),
            ("bin", OneHotEncoder(drop="first", sparse_output=False), [binary_feature]),
        ],
        remainder="drop"
    )
    
    pipeline_lr = Pipeline(
        steps=[
            ("preprocessor", preprocessor_lr),
            ("classifier", LogisticRegression(random_state=42))
        ]
    )
    
    pipeline_lr.fit(X_train, y_train)
    joblib.dump(pipeline_lr, os.path.join(settings.MODEL_DIR, "logistic_regression.joblib"))
    # try:
    #     joblib.dump(pipeline_lr, os.path.join(settings.MODEL_DIR, "logistic_regression.joblib")) # ЧИСТО РАДИ ТЕСТА, ПОТОМ УДАЛИТЬ
    #     logger.info("Модель Logistic Regression сохранена.")
    # except Exception as e:
    #     print(f"Ошибка при сохранении модели logistic_regression: {e}")
    #     logger.error(f"Ошибка при сохранении модели Logistic Regression: {e}")

    
    # # Функция для кодирования бинарного столбца
    # def encode_binary_column(X):
    #     le = LabelEncoder()
    #     X_copy = X.copy()
    #     X_copy[binary_feature] = le.fit_transform(X_copy[binary_feature])
    #     return X_copy
    
    # Модель случайного леса
    preprocessor_rf = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="mean"), numerical_features),
            ("cat", LeaveOneOutEncoder(cols=categorical_features), categorical_features),
            ("bin", FunctionTransformer(encode_binary_column, validate=False), [binary_feature]),
        ],
        remainder="drop"
    )
    
    pipeline_rf = Pipeline(
        steps=[
            ("preprocessor", preprocessor_rf),
            ("classifier", RandomForestClassifier(n_estimators=898, max_depth=46, 
                                                 min_samples_split=13, min_samples_leaf=3, 
                                                 max_features='log2', bootstrap=False, 
                                                 criterion='gini', random_state=42))
        ]
    )
    
    pipeline_rf.fit(X_train, y_train)
    joblib.dump(pipeline_rf, os.path.join(settings.MODEL_DIR, "random_forest.joblib"))
    
    # Модель LightGBM
    pipeline_lgbm = Pipeline(
        steps=[
            ("preprocessor", preprocessor_rf),  # используем тот же препроцессор, что и для случайного леса
            ("classifier", LGBMClassifier(learning_rate=0.002116, n_estimators=453, 
                                         max_depth=142, num_leaves=424, min_child_samples=45, 
                                         subsample=0.8346, colsample_bytree=0.5666, 
                                         reg_alpha=0.0473, reg_lambda=0.00057, 
                                         random_state=42, verbose=-1))
        ]
    )
    
    pipeline_lgbm.fit(X_train, y_train)
    joblib.dump(pipeline_lgbm, os.path.join(settings.MODEL_DIR, "lgbm.joblib"))
    
    print("Модели успешно сохранены в директорию:", settings.MODEL_DIR)