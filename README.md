Слои проекта:
```
├── README.md
├── config
│   └── settings.py
├── core
│   ├── entities
│   │   ├── model.py
│   │   ├── prediction.py
│   │   ├── transaction.py
│   │   └── user.py
│   ├── repositories
│   │   ├── model_repository.py
│   │   ├── prediction_repository.py
│   │   ├── transaction_repository.py
│   │   └── user_repository.py
│   └── use_cases
│       ├── billing_use_cases.py
│       ├── model_use_cases.py
│       ├── prediction_use_cases.py
│       └── user_use_cases.py
├── docker
│   ├── Dockerfile.api
│   └── Dockerfile.ui
├── docker-compose.yml
├── infrastructure
│   ├── db
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repositories
│   │       ├── model_repository_impl.py
│   │       ├── prediction_repository_impl.py
│   │       ├── transaction_repository_impl.py
│   │       └── user_repository_impl.py
│   ├── ml
│   │   ├── credit_risk_dataset.csv
│   │   ├── model_loader.py
│   │   ├── model_service.py
│   │   ├── preprocessor.py
│   │   └── save_models.py
│   └── web
│       ├── api
│       │   ├── auth.py
│       │   ├── billing.py
│       │   ├── models.py
│       │   ├── predictions.py
│       │   └── users.py
│       ├── dependencies.py
│       ├── schemas.py
│       └── user_controller.py
├── main.py
├── ml_billing.db
├── models
│   ├── lgbm.joblib
│   ├── logistic_regression.joblib
│   └── random_forest.joblib
├── requirements.txt
└── ui
    └── app.py

```