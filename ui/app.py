import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import os


API_URL = os.environ.get("API_URL", "http://localhost:8000/api")


# Инициализация состояния сессии
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.username = None

# Дополнительные состояния для отслеживания действий
if 'deposit_submitted' not in st.session_state:
    st.session_state.deposit_submitted = False
    
if 'prediction_submitted' not in st.session_state:
    st.session_state.prediction_submitted = False

# Функции для взаимодействия с API
def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.authenticated = True
            st.session_state.token = data["access_token"]
            st.session_state.username = username
            return True
        else:
            error_message = "Неверные учетные данные"
            if response.status_code != 401:
                try:
                    error_message = response.json().get("detail", error_message)
                except:
                    pass
            st.error(error_message)
            return False
    except Exception as e:
        st.error(f"Ошибка при подключении к API: {str(e)}")
        return False

def register(username, email, password):
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 200:
            st.success("Регистрация успешна! Теперь вы можете войти.")
            return True
        else:
            error_message = "Ошибка при регистрации"
            try:
                error_message = response.json().get("detail", error_message)
            except:
                pass
            st.error(error_message)
            return False
    except Exception as e:
        st.error(f"Ошибка при подключении к API: {str(e)}")
        return False

def get_user_info():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/users/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Ошибка при получении данных пользователя: {str(e)}")
        return None

def get_models():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/models", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Ошибка при получении списка моделей: {str(e)}")
        return []

def get_predictions():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/predictions", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Ошибка при получении истории предсказаний: {str(e)}")
        return []

def get_transactions():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/billing/transactions", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Ошибка при получении истории транзакций: {str(e)}")
        return []

def deposit(amount, description="Пополнение баланса"):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_URL}/billing/deposit",
            json={"amount": amount, "description": description},
            headers=headers
        )
        if response.status_code == 200:
            st.success(f"Баланс успешно пополнен на {amount} кредитов")
            # Устанавливаем флаг, что депозит был выполнен
            st.session_state.deposit_submitted = False
            st.rerun()  # Используем st.rerun() вместо устаревшего st.experimental_rerun
            return True
        else:
            error_message = "Ошибка при пополнении баланса"
            try:
                error_message = response.json().get("detail", error_message)
            except:
                pass
            st.error(error_message)
            return False
    except Exception as e:
        st.error(f"Ошибка при подключении к API: {str(e)}")
        return False

def create_prediction(model_id, input_data):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_URL}/predictions",
            json={"model_id": model_id, "input_data": input_data},
            headers=headers
        )
        if response.status_code == 200:
            # Устанавливаем флаг, что предсказание было создано
            st.session_state.prediction_submitted = False
            return response.json()
        else:
            error_message = "Ошибка при создании предсказания"
            try:
                error_message = response.json().get("detail", error_message)
            except:
                pass
            st.error(error_message)
            return None
    except Exception as e:
        st.error(f"Ошибка при подключении к API: {str(e)}")
        return None

def logout():
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.username = None
    # Сбрасываем флаги
    st.session_state.deposit_submitted = False
    st.session_state.prediction_submitted = False

# Обработчики форм
def handle_deposit_submit():
    st.session_state.deposit_submitted = True

def handle_prediction_submit():
    st.session_state.prediction_submitted = True

# Интерфейс для страницы входа
def login_page():
    st.title("Сервис машинного обучения с биллингом")
    
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Имя пользователя")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти")
            
            if submit:
                if login(username, password):
                    st.rerun()  # Используем st.rerun() вместо устаревшего st.experimental_rerun
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Имя пользователя")
            new_email = st.text_input("Email")
            new_password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Зарегистрироваться")
            
            if submit:
                register(new_username, new_email, new_password)

# Интерфейс для основной страницы
def main_page():
    user_info = get_user_info()
    
    # Боковая панель с информацией о пользователе
    with st.sidebar:
        st.subheader(f"Привет, {st.session_state.username}!")
        st.write(f"Баланс: {user_info['balance']} кредитов")
        
        st.divider()
        
        # Пополнение баланса
        with st.form("deposit_form"):
            st.subheader("Пополнение баланса")
            amount = st.number_input("Сумма", min_value=1.0, value=50.0, step=10.0)
            description = st.text_input("Описание", value="Пополнение баланса")
            submit_deposit = st.form_submit_button("Пополнить", on_click=handle_deposit_submit)
        
        # Проверяем, был ли отправлен запрос на депозит
        if st.session_state.deposit_submitted:
            deposit(amount, description)

        st.divider()
        
        # Кнопка выхода
        if st.button("Выйти"):
            logout()
            st.rerun()  # Используем st.rerun() вместо устаревшего st.experimental_rerun
    
    # Основной контент
    st.title("Сервис машинного обучения с биллингом")
    
    # Вкладки для разных функций
    tab1, tab2, tab3, tab4 = st.tabs(["Создать предсказание", "История предсказаний", "Транзакции", "Статистика"])
    
    # Вкладка создания предсказания
    with tab1:
        st.header("Создать новое предсказание")
        
        # Получение списка моделей
        models = get_models()

        if not models:
            st.error("Не удалось загрузить список моделей. Пожалуйста, попробуйте позже или обратитесь к администратору.")
            st.info("Ваш текущий баланс: " + str(user_info['balance']) + " кредитов")
            return  # Завершаем выполнение функции

        model_names = {model["id"]: f"{model['name']} ({model['price']} кредитов)" for model in models}
        model_prices = {model["id"]: model["price"] for model in models}

        # Выбор модели
        selected_model_id = st.selectbox(
            "Выберите модель",
            options=list(model_names.keys()),
            format_func=lambda x: model_names[x]
        )

        # Проверяем, что выбранная модель существует в словаре цен
        if selected_model_id is not None and selected_model_id in model_prices:
            st.info(f"Стоимость предсказания: {model_prices[selected_model_id]} кредитов")
        else:
            st.warning("Выберите модель из списка")

        st.info(f"Ваш текущий баланс: {user_info['balance']} кредитов")
        # Форма для ввода данных
        with st.form("prediction_form"):
            st.subheader("Входные данные для предсказания")
            
            col1, col2 = st.columns(2)
            
            with col1:
                person_age = st.number_input("Возраст", min_value=18, max_value=100, value=30)
                person_income = st.number_input("Годовой доход ($)", min_value=0, value=50000, step=1000)
                person_home_ownership = st.selectbox(
                    "Тип собственности",
                    options=["RENT", "OWN", "MORTGAGE"],
                    index=0
                )
                person_emp_length = st.number_input("Стаж работы (лет)", min_value=0.0, value=5.0, step=0.5)
                loan_intent = st.selectbox(
                    "Цель займа",
                    options=["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
                    index=0
                )
            
            with col2:
                loan_grade = st.selectbox(
                    "Грейд займа",
                    options=["A", "B", "C", "D", "E", "F", "G"],
                    index=0
                )
                loan_amnt = st.number_input("Сумма займа ($)", min_value=500, value=10000, step=500)
                loan_int_rate = st.number_input("Процентная ставка (%)", min_value=1.0, max_value=30.0, value=12.5, step=0.5)
                loan_percent_income = st.number_input("Соотношение займа к доходу", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
                cb_person_default_on_file = st.selectbox(
                    "Дефолт в кредитной истории",
                    options=["N", "Y"],
                    index=0
                )
                cb_person_cred_hist_length = st.number_input("Длина кредитной истории (лет)", min_value=0, value=3)
            
            submit_button = st.form_submit_button("Создать предсказание", on_click=handle_prediction_submit)
        
        # Проверяем, был ли отправлен запрос на создание предсказания
        if st.session_state.prediction_submitted:
            if user_info["balance"] < model_prices[selected_model_id]:
                st.error(f"Недостаточно средств на балансе. Требуется: {model_prices[selected_model_id]}, Доступно: {user_info['balance']}")
                st.session_state.prediction_submitted = False
            else:
                input_data = {
                    "person_age": person_age,
                    "person_income": person_income,
                    "person_home_ownership": person_home_ownership,
                    "person_emp_length": person_emp_length,
                    "loan_intent": loan_intent,
                    "loan_grade": loan_grade,
                    "loan_amnt": loan_amnt,
                    "loan_int_rate": loan_int_rate,
                    "loan_percent_income": loan_percent_income,
                    "cb_person_default_on_file": cb_person_default_on_file,
                    "cb_person_cred_hist_length": cb_person_cred_hist_length
                }
                
                prediction = create_prediction(selected_model_id, input_data)
                if prediction:
                    st.success("Предсказание успешно создано!")
                    st.write("Результат предсказания:")
                    
                    result_text = "Низкий риск дефолта" if prediction["result"] == 0 else "Высокий риск дефолта"
                    probability = prediction["probability"] * 100
                    
                    st.metric("Решение", result_text)
                    st.metric("Вероятность выплаты кредита", f"{probability:.2f}%")
                    
                    # Обновляем страницу, чтобы отобразить новые данные
                    st.rerun()  # Используем st.rerun() вместо устаревшего st.experimental_rerun
    
    # Вкладка истории предсказаний
    with tab2:
        st.header("История предсказаний")
        
        predictions = get_predictions()
        if predictions:
            df_predictions = pd.DataFrame(predictions)
            df_predictions["created_at"] = pd.to_datetime(df_predictions["created_at"])
            df_predictions = df_predictions.sort_values("created_at", ascending=False)
            
            for idx, pred in df_predictions.iterrows():
                with st.expander(f"Предсказание #{pred['id']} ({pred['created_at']})"):
                    result_text = "Низкий риск дефолта" if pred["result"] == 0 else "Высокий риск дефолта"
                    probability = pred["probability"] * 100
                    
                    st.write(f"**Результат:** {result_text}")
                    st.write(f"**Вероятность выплаты кредита:** {probability:.2f}%")
                    st.write("**Входные данные:**")
                    st.json(pred["input_data"])
        else:
            st.info("У вас пока нет истории предсказаний")
    
    # Вкладка транзакций
    with tab3:
        st.header("История транзакций")
        
        transactions = get_transactions()
        if transactions:
            df_transactions = pd.DataFrame(transactions)
            df_transactions["created_at"] = pd.to_datetime(df_transactions["created_at"])
            df_transactions = df_transactions.sort_values("created_at", ascending=False)
            
            st.dataframe(
                df_transactions[["created_at", "amount", "transaction_type", "description"]],
                column_config={
                    "created_at": "Дата",
                    "amount": "Сумма",
                    "transaction_type": "Тип",
                    "description": "Описание"
                },
                hide_index=True
            )
        else:
            st.info("У вас пока нет истории транзакций")
    
    # Вкладка статистики
    with tab4:
        st.header("Статистика использования")
        
        predictions = get_predictions()
        transactions = get_transactions()
        
        if predictions:
            df_predictions = pd.DataFrame(predictions)
            df_predictions["created_at"] = pd.to_datetime(df_predictions["created_at"])
            
            # График использования моделей
            model_counts = df_predictions["model_id"].value_counts().reset_index()
            model_counts.columns = ["Модель", "Количество"]
            
            # Отображаем названия моделей вместо ID
            models_dict = {model["id"]: model["name"] for model in models}
            model_counts["Модель"] = model_counts["Модель"].map(models_dict)
            
            st.subheader("Использование моделей")
            fig = px.bar(model_counts, x="Модель", y="Количество")
            st.plotly_chart(fig)
            
            # График результатов предсказаний
            result_counts = df_predictions["result"].value_counts().reset_index()
            result_counts.columns = ["Результат", "Количество"]
            result_counts["Результат"] = result_counts["Результат"].map({0: "Высокий риск", 1: "Низкий риск"})
            
            st.subheader("Распределение результатов")
            fig = px.pie(result_counts, values="Количество", names="Результат")
            st.plotly_chart(fig)
        else:
            st.info("Недостаточно данных для статистики")

# Основной код приложения
def main():
    if st.session_state.authenticated:
        main_page()
    else:
        login_page()

if __name__ == "__main__":
    main()