│
├── api/                   # Слой API
│   ├── auth.py            # Функциональность аутентификации
│   ├── billing.py         # Эндпоинты для работы с биллингом
│   ├── models.py          # API модели/схемы
│   ├── predictions.py     # Эндпоинты для предсказаний
│   ├── users.py           # Эндпоинты для управления пользователями
│   ├── schemas.py         # Схемы запросов/ответов
│   ├── user_controller.py # Обработчики запросов пользователей
│   └── dependencies.py    # Зависимости API и внедрение зависимостей
│
├── core/                  # Основная бизнес-логика
│   ├── entities/          # Доменные сущности/модели
│   │   ├── model.py       # Сущность модели
│   │   ├── prediction.py  # Сущность предсказания
│   │   ├── transaction.py # Сущность транзакции 
│   │   └── user.py        # Сущность пользователя
│   │
│   ├── repositories/      # Интерфейсы репозиториев
│   │   ├── model_repository.py      # Интерфейс доступа к данным моделей
│   │   ├── prediction_repository.py # Интерфейс доступа к данным предсказаний
│   │   ├── transaction_repository.py # Интерфейс доступа к данным транзакций
│   │   └── user_repository.py       # Интерфейс доступа к данным пользователей
│   │
│   └── use_cases/         # Бизнес сценарии использования
│       ├── billing_use_cases.py     # Операции биллинга
│       ├── model_use_cases.py       # Операции управления моделями
│       ├── prediction_use_cases.py  # Операции для предсказаний
│       └── user_use_cases.py        # Операции управления пользователями
│
├── infrastructure/        # Реализация инфраструктуры
│   ├── db/                # Реализации для работы с базой данных
│   │   └── repositories/  # Реализации репозиториев
│   │       ├── model_repository_impl.py      # Реализация репозитория моделей
│   │       ├── prediction_repository_impl.py # Реализация репозитория предсказаний
│   │       ├── transaction_repository_impl.py # Реализация репозитория транзакций
│   │       └── user_repository_impl.py       # Реализация репозитория пользователей
│   │
│   └── docker/            # Конфигурация Docker
│       ├── Dockerfile.api # Dockerfile для API сервиса
│       └── Dockerfile.ui  # Dockerfile для UI сервиса
│
├── models/                # ML модели
│   ├── lgbm.joblib        # Модель LightGBM
│   ├── logistic_regression.joblib # Модель логистической регрессии
│   └── random_forest.joblib # Модель случайного леса
│
├── ui/                    # Пользовательский интерфейс
│   └── app.py             # UI приложение
│
├── config/                # Конфигурация
│   └── settings.py        # Настройки приложения
│
├── docker-compose.yml     # Конфигурация Docker Compose
├── requirements.txt       # Зависимости Python
├── main.py                # Точка входа в приложение
└── README.md              # Документация проекта