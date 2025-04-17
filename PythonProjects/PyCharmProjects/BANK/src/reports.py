import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def expenses_by_workday(df: pd.DataFrame, category: str, start_date_str: str) -> str:
    """
    Формирует отчет о тратах в рабочий/выходной день за трехмесячный период.
    """
    response_data: Dict[str, Any]

    try:
        # Преобразование даты в datetime-объект
        start_date: datetime = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date: datetime = start_date + timedelta(days=90)  # Трехмесячный период

        # Фильтрация данных по дате и категории
        filtered_df: pd.DataFrame = df[(df['date'] >= start_date) &
                                       (df['date'] <= end_date) & (df['category'] == category)].copy()

        if filtered_df.empty:
            response_data = {
                'status': 'success',
                'category': category,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'expenses_by_day_type': {}
            }
            return json.dumps(response_data, ensure_ascii=False)

        # Добавление столбца с типом дня (рабочий/выходной)
        filtered_df.loc[:, 'day_type'] = filtered_df['date'].apply(
            lambda x: 'рабочий' if x.weekday() < 5 else 'выходной'
        )

        # Группировка по типу дня и расчет суммы трат
        expenses_by_day_type: Dict[str, float] = filtered_df.groupby('day_type')['amount'].sum().to_dict()

        # Преобразование типов данных в JSON-сериализуемые
        expenses_by_day_type = {k: float(v) for k, v in expenses_by_day_type.items()}

        # Формирование JSON-ответа
        response_data = {
            'status': 'success',
            'category': category,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'expenses_by_day_type': expenses_by_day_type
        }
        return json.dumps(response_data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка формирования отчета: {e}")
        response_data = {'status': 'error', 'message': str(e)}
        return json.dumps(response_data, ensure_ascii=False)


def expenses_by_category(df: pd.DataFrame, category: str, start_date_str: str) -> str:
    """
    Формирует отчет об общей сумме трат по заданной категории за трехмесячный период.
    """
    response_data: Dict[str, Any]
    try:
        # Преобразование даты в datetime-объект
        start_date: pd.Timestamp = pd.to_datetime(start_date_str)
        end_date: pd.Timestamp = start_date + pd.Timedelta(days=90)  # Трехмесячный период

        # Фильтрация данных по дате и категории
        filtered_df: pd.DataFrame = df[
            (df['date'] >= start_date) &
            (df['date'] <= end_date) &
            (df['category'] == category)
            ]

        # Расчет общей суммы трат
        total_expenses: float = filtered_df['amount'].sum()

        # Формирование JSON-ответа
        response_data = {
            'status': 'success',
            'category': category,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'total_expenses': float(total_expenses) if not pd.isna(total_expenses) else 0.0
        }
        return json.dumps(response_data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка формирования отчета: {e}")
        response_data = {'status': 'error', 'message': str(e)}
        return json.dumps(response_data, ensure_ascii=False)


def expenses_by_day_of_week(df: pd.DataFrame, date_str: Optional[str] = None) -> str:
    """
    Формирует отчет о тратах по дням недели за трехмесячный период.
    """
    response_data: Dict[str, Any]
    date: datetime
    try:
        if date_str:
            # Преобразование даты в datetime-объект
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            # Использование текущей даты по умолчанию
            date = datetime.now()

        # Определение начала и конца трехмесячного периода
        start_date: datetime = date - timedelta(days=90)
        end_date: datetime = date

        # Фильтрация данных по дате
        filtered_df: pd.DataFrame = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()

        if filtered_df.empty:
            response_data = {
                'status': 'success',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'expenses_by_day': {}
            }
            return json.dumps(response_data, ensure_ascii=False)

        # Добавление столбца с днем недели
        filtered_df.loc[:, 'day_of_week'] = filtered_df['date'].dt.day_name()

        # Группировка по дню недели и расчет суммы трат
        expenses_by_day: Dict[str, float] = filtered_df.groupby('day_of_week')['amount'].sum().to_dict()

        # Преобразование типов данных в JSON-сериализуемые
        expenses_by_day = {k: float(v) for k, v in expenses_by_day.items()}

        # Формирование JSON-ответа
        response_data = {
            'status': 'success',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'expenses_by_day': expenses_by_day
        }
        return json.dumps(response_data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка формирования отчета: {e}")
        response_data = {'status': 'error', 'message': str(e)}
        return json.dumps(response_data, ensure_ascii=False)


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Вычисляет средние траты в каждый из дней недели за последние три месяца.
    """
    try:
        if date:
            end_date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            end_date = datetime.today().date()

        start_date = end_date - timedelta(days=90)

        filtered_transactions = transactions[(transactions['date'].dt.date >= start_date) &
                                             (transactions['date'].dt.date <= end_date)]

        if filtered_transactions.empty:
            logger.info("Нет транзакций за последние три месяца.")
            return pd.DataFrame(columns=['weekday', 'average_spending'])

        filtered_transactions = filtered_transactions.copy()
        filtered_transactions['weekday'] = filtered_transactions['date'].dt.strftime('%A')

        average_spending = filtered_transactions.groupby('weekday')['amount'].mean().reset_index()
        average_spending = average_spending.rename(columns={average_spending.columns[0]: 'weekday',
                                                            average_spending.columns[1]: 'average_spending'})

        return average_spending
    except Exception as e:
        logger.error(f"Ошибка при вычислении трат по дням недели: {e}")
        return pd.DataFrame(columns=['weekday', 'average_spending'])
