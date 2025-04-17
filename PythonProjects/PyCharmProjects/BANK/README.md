# Finance Analyzer

## Описание

Этот проект представляет собой систему для анализа финансовых данных, включающую в себя:

-   Обработку и анализ транзакций.
-   Формирование отчетов о расходах и доходах.
-   Получение информации о курсах валют и ценах на акции.
-   Предоставление API для доступа к данным.

## Структура проекта

Проект состоит из нескольких основных модулей:

-   `reports.py`: Модуль для формирования финансовых отчетов.
-   `services.py`: Модуль, содержащий бизнес-логику приложения.
-   `utils.py`: Модуль с вспомогательными функциями.
-   `views.py`: Модуль, реализующий API endpoints с использованием Flask.
-   `test_*.py`: Модули с тестами для соответствующих модулей.

## Модули

### `reports.py`

Содержит функции для формирования отчетов:

-   `expenses_by_workday(df: pd.DataFrame, category: str, start_date_str: str) -> str`: Формирует отчет о тратах в рабочий/выходной день за трехмесячный период.
-   `expenses_by_category(df: pd.DataFrame, category: str, start_date_str: str) -> str`: Формирует отчет об общей сумме трат по заданной категории за трехмесячный период.
-   `expenses_by_day_of_week(df: pd.DataFrame, date_str: Optional[str] = None) -> str`: Формирует отчет о тратах по дням недели за трехмесячный период.
-   `spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame`: Вычисляет средние траты в каждый из дней недели за последние три месяца.

### `services.py`

Содержит функции, реализующие бизнес-логику:

-   `calculate_cashback_categories(year: int, month: int, transactions: List[Dict[str, Any]]) -> str`: Вычисляет наиболее выгодные категории для повышенного кэшбэка.
-   `invest_piggy_bank(month: int, transactions: List[Dict[str, Any]], rounding_limit: int) -> str`: Рассчитывает сумму для инвестиционной копилки на основе округления общей суммы транзакций за месяц.
-   `simple_search(query: str, transactions: List[Dict[str, Any]]) -> str`: Выполняет простой поиск транзакций по запросу.
-   `search_by_phone(transactions: List[Dict[str, Any]]) -> str`: Ищет телефонные номера в данных транзакций.
-   `search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> str`: Ищет переводы физическим лицам в данных транзакций.
-   `invest_piggy_bank_monthly(month: int, transactions: List[Dict[str, Any]], rounding_step: int) -> str`: Рассчитывает сумму для инвестиционной копилки за указанный месяц с округлением.
-   `invest_piggy_bank_rounding(spent_amount: float, rounding_step: int, current_balance: float) -> str`: Функция для автоматического копления в инвесткопилку через округление одной транзакции.

### `utils.py`

Содержит вспомогательные функции:

-   `get_data_from_api(url: str) -> Optional[Dict[str, Any]]`: Получает данные из API.
-   `process_date(date_str: str) -> Optional[datetime.datetime]`: Преобразует строку с датой и временем в объект datetime.
-   `process_dataframe(df: pd.DataFrame) -> pd.DataFrame`: Обрабатывает DataFrame, добавляя новый столбец 'new_column'.
-   `to_json(data: Any) -> str`: Преобразует данные в JSON-строку.

### `views.py`

Реализует API endpoints с использованием Flask:

-   `/home` (POST): Обрабатывает запросы для страницы 'Главная'.
-   `/events` (POST): Обрабатывает запросы для страницы 'События'.

Также содержит функции для обработки данных и формирования ответов:

-   `get_greeting(date_time: datetime.datetime) -> str`: Возвращает приветствие в зависимости от времени суток.
-   `get_card_info(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]`: Извлекает информацию по картам из списка транзакций.
-   `get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]`: Возвращает топ-5 транзакций по сумме.
-   `get_currency_rates(user_settings: Dict[str, List[str]]) -> List[Dict[str, Any]]`: Получает курсы валют из API.
-   `get_stock_prices(user_settings: Dict[str, List[str]]) -> List[Dict[str, Any]]`: Получает цены на акции из API.
-   `get_expenses(transactions: List[Dict[str, Any]]) -> Dict[str, Any]`: Анализирует список транзакций и формирует структуру расходов.
-   `get_income(transactions: List[Dict[str, Any]]) -> Dict[str, Any]`: Анализирует список транзакций и возвращает информацию о доходах.
-   `get_transactions(date_time: datetime.datetime, data_range: str = 'M') -> List[Dict[str, Any]]`: Получает список транзакций за определенный период, исходя из заданной даты и диапазона.
-   `main(date_time_str: str, data_range: str = 'M') -> str`: Главная функция, которая обрабатывает запрос и возвращает JSON с данными о доходах, расходах, курсах валют и ценах на акции.

## Тестирование

Для запуска тестов необходимо установить pytest:

pip install pytest

Запуск тестов:

pytest

## Зависимости

-   pandas
-   Flask
-   requests
-   typing
-   datetime
-   json
-   logging
-   re
-   pytest

Установка зависимостей:

pip install -r requirements.txt

## Настройка

Необходимо создать файл `user_settings.json` с настройками пользователя (валюты, акции):

{
"user_currencies": ["USD", "EUR"],
"user_stocks": ["AAPL", "GOOG"]
}

## Запуск

python src/views.py

## API Endpoints

-   `POST /home`:
    -   Принимает: JSON с параметром `date` (дата в формате `YYYY-MM-DD HH:MM:SS`).
    -   Возвращает: JSON с данными о доходах, расходах, курсах валют и ценах на акции.
-   `POST /events`:
    -   Принимает: JSON с параметром `df` (DataFrame в формате JSON).
    -   Возвращает: JSON с обработанным DataFrame.

## Логирование

Для логирования используется модуль `logging`. Настройки логирования заданы в каждом модуле:

import logging

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(name)

## Примеры

### Формирование отчета о тратах по категориям

import pandas as pd  
from src.reports import expenses_by_category

data = {'date': ['2024-04-01', '2024-04-02'], 'category': ['Food', 'Food'], 'amount':}  
df = pd.DataFrame(data)
result = expenses_by_category(df, 'Food', '2024-04-01')
print(result)

### Получение данных через API

import requests  
import json

url = 'http://localhost:5000/home'
headers = {'Content-type': 'application/json'}
data = {'date': '2024-04-17 10:00:00'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())

## Лицензия
Этот проект распространяется под лицензией [MIT License](LICENSE)

## Авторы 
[ANTAQ](https://github.com/Carplatinum)