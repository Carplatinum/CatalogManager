import datetime
import json
import logging
from typing import Any, Dict, Optional, cast

import pandas as pd
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data_from_api(url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())  # Явное приведение типа
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return None


def process_date(date_str: str) -> Optional[datetime.datetime]:
    """
    Преобразует строку с датой и временем в объект datetime.
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error(f"Ошибка при парсинге даты: {e}")
        return None


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает DataFrame, добавляя новый столбец 'new_column'.
    """
    # Пример обработки: добавление нового столбца
    df['new_column'] = 'example'
    return df


def to_json(data: Any) -> str:
    """
    Преобразует данные в JSON-строку.
    """
    return json.dumps(data, ensure_ascii=False)
