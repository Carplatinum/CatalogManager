import datetime
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
from flask import Flask, jsonify, request

from .utils import get_data_from_api, process_dataframe, process_date

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/home', methods=['POST'])
def home() -> Any:
    """
    Обрабатывает запросы для страницы 'Главная'.
    """
    data: Dict[str, Any] = request.get_json()
    if 'date' in data:
        date_str: Any = data.get('date')
        date_obj: Optional[datetime.datetime] = process_date(date_str)
        if date_obj:
            # Пример использования API
            api_data: Optional[Dict[str, Any]] = get_data_from_api('https://example.com/api/data')
            if api_data:
                return jsonify({'date': date_str, 'api_data': api_data})
            else:
                return jsonify({'error': 'Failed to fetch API data'}), 500
        else:
            return jsonify({'error': 'Invalid date format'}), 400
    else:
        return jsonify({'error': 'Missing date parameter'}), 400


@app.route('/events', methods=['POST'])
def events() -> Any:
    """
    Обрабатывает запросы для страницы 'События'.
    """
    data: Dict[str, Any] = request.get_json()
    if 'df' in data:
        try:
            df: pd.DataFrame = pd.DataFrame(data['df'])
            processed_df: pd.DataFrame = process_dataframe(df)
            return jsonify(processed_df.to_dict(orient='records'))
        except Exception as e:
            logger.error(f"Ошибка при обработке DataFrame: {e}")
            return jsonify({'error': 'Failed to process DataFrame'}), 500
    else:
        return jsonify({'error': 'Missing DataFrame parameter'}), 400


if __name__ == '__main__':
    app.run(debug=True)


def get_greeting(date_time: datetime.datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.
    """
    hour: int = date_time.hour
    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_card_info(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Извлекает информацию по картам из списка транзакций.
    """
    cards: Dict[str, Dict[str, Any]] = {}
    for transaction in transactions:
        card_number: Optional[str] = transaction.get('card_number')
        if card_number:
            last_digits: str = card_number[-4:]
            if last_digits in cards:
                cards[last_digits]['total_spent'] += transaction.get('amount', 0)
            else:
                cards[last_digits] = {
                    'last_digits': last_digits,
                    'total_spent': transaction.get('amount', 0),
                    'cashback': 0
                }

    for card in cards.values():
        card['cashback'] = card['total_spent'] / 100

    return list(cards.values())


def get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает топ-5 транзакций по сумме.
    """
    sorted_transactions: List[Dict[str, Any]] = sorted(
        transactions,
        key=lambda x: abs(x.get('amount', 0)),
        reverse=True
    )
    top_transactions: List[Dict[str, Any]] = []
    for transaction in sorted_transactions[:5]:
        top_transaction: Dict[str, Any] = {
            'date': transaction.get('date'),
            'amount': transaction.get('amount'),
            'category': transaction.get('category'),
            'description': transaction.get('description')
        }
        top_transactions.append(top_transaction)

    return top_transactions


def get_currency_rates(user_settings: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют из API.
    """
    # api_key: str = "YOUR_EXCHANGE_RATE_API_KEY"
    url: str = "https://api.exchangerate-api.com/v4/latest/RUB"
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data: Dict[str, Any] = response.json()
        rates: List[Dict[str, Any]] = []
        for currency in user_settings['user_currencies']:
            rate: Optional[float] = data.get('rates', {}).get(currency)
            if rate:
                rates.append({
                    'currency': currency,
                    'rate': rate
                })
        return rates
    except requests.exceptions.RequestException as e:
        logger.error(f"Не удалось получить курсы валют: {e}")
        return []


def get_stock_prices(user_settings: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Получает цены на акции из API.
    """
    api_key: str = "YOUR_ALPHA_VANTAGE_API_KEY"
    stock_prices: List[Dict[str, Any]] = []
    for stock in user_settings['user_stocks']:
        url: str = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data: Dict[str, Any] = response.json()
            global_quote: Dict[str, Any] = data.get('Global Quote', {})  # Add this line
            price: Optional[float] = global_quote.get('05. price')  # Change this line
            if price:
                stock_prices.append({
                    'stock': stock,
                    'price': float(price)
                })
        except requests.exceptions.RequestException as e:
            logger.error(f"Не удалось получить цену акции для {stock}: {e}")
        except KeyError as e:
            logger.error(f"Не удалось распарсить цену акции для {stock}: {e}")

    return stock_prices


def get_expenses(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Анализирует список транзакций и формирует структуру расходов.
    """
    expenses: Dict[str, float] = {}
    transfers_and_cash: Dict[str, float] = {}

    for transaction in transactions:
        if transaction.get('type') == 'expense':
            category: Optional[str] = transaction.get('category')
            amount: float = transaction.get('amount', 0)

            if category is not None:
                if category in expenses:
                    expenses[category] += amount
                else:
                    expenses[category] = amount

                if category in ['Наличные', 'Переводы']:
                    if category in transfers_and_cash:
                        transfers_and_cash[category] += amount
                    else:
                        transfers_and_cash[category] = amount

    return {
        'expenses': expenses,
        'transfers_and_cash': transfers_and_cash,
    }

    # Сортировка и группировка расходов
    sorted_expenses: List[Tuple[str, float]] = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    main_expenses: List[Tuple[str, float]] = sorted_expenses[:7]
    other_amount: float = sum(amount for category, amount in sorted_expenses[7:])

    if other_amount > 0:
        main_expenses.append(('Остальное', other_amount))

    sorted_transfers_and_cash: List[Tuple[str, float]] = sorted(
        transfers_and_cash.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    result: Dict[str, Any] = {
        'total_amount': sum(expenses.values()),
        'main': [{'category': category, 'amount': round(amount)} for category, amount in main_expenses],
        'transfers_and_cash': [{'category': category, 'amount': round(amount)} for category, amount in
                               sorted_transfers_and_cash]
    }
    return result


def get_income(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Анализирует список транзакций и возвращает информацию о доходах.
    """
    income: Dict[str, float] = {}

    for transaction in transactions:
        if transaction.get('type') == 'income':
            category: Optional[str] = transaction.get('category')
            amount: float = transaction.get('amount', 0)

            if category is not None:  # Проверка на None
                if category in income:
                    income[category] += amount
                else:
                    income[category] = amount

    # Сортировка поступлений
    sorted_income: List[Tuple[str, float]] = sorted(income.items(), key=lambda x: x[1], reverse=True)

    result: Dict[str, Any] = {
        'total_amount': sum(income.values()),
        'main': [{'category': category, 'amount': round(amount)} for category, amount in sorted_income]
    }
    return result


def get_transactions(date_time: datetime.datetime, data_range: str = 'M') -> List[Dict[str, Any]]:
    """
    Получает список транзакций за определенный период, исходя из заданной даты и диапазона.
    """
    transactions: List[Dict[str, Any]] = [
        {'date': '2024-04-01', 'type': 'expense', 'category': 'Супермаркеты', 'amount': 100},
        {'date': '2024-04-05', 'type': 'income', 'category': 'Пополнение', 'amount': 500},
        {'date': '2024-04-10', 'type': 'expense', 'category': 'Топливо', 'amount': 200}
    ]

    if data_range == 'W':
        start_date = date_time - datetime.timedelta(days=date_time.weekday())
    elif data_range == 'M':
        start_date = date_time.replace(day=1)
    elif data_range == 'Y':
        start_date = date_time.replace(month=1, day=1)
    elif data_range == 'ALL':
        start_date = datetime.datetime(1970, 1, 1)
    else:
        start_date = date_time.replace(day=1)  # default to month start

    filtered_transactions = [
        transaction for transaction in transactions
        if start_date <= datetime.datetime.strptime(transaction['date'], '%Y-%m-%d') <= date_time
    ]

    return filtered_transactions


def main(date_time_str: str, data_range: str = 'M') -> str:
    """
    Главная функция, которая обрабатывает запрос и возвращает
    JSON с данными о доходах, расходах, курсах валют и ценах на акции.
    """
    try:
        date_time: datetime.datetime = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # Загрузка пользовательских настроек
        with open('user_settings.json') as f:
            user_settings: Dict[str, List[str]] = json.load(f)

        transactions: List[Dict[str, Any]] = get_transactions(date_time, data_range)

        expenses: Dict[str, Any] = get_expenses(transactions)
        income: Dict[str, Any] = get_income(transactions)
        currency_rates: List[Dict[str, Any]] = get_currency_rates(user_settings)
        stock_prices: List[Dict[str, Any]] = get_stock_prices(user_settings)

        result: Dict[str, Any] = {
            'expenses': expenses,
            'income': income,
            'currency_rates': currency_rates,
            'stock_prices': stock_prices
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}")
        return json.dumps({'error': 'Failed to process request'}, ensure_ascii=False)
