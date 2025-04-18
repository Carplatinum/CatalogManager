# CatalogManager  
CatalogManager — простой и удобный Python-проект для управления каталогами товаров и их загрузки из JSON-файлов. Проект демонстрирует основные принципы объектно-ориентированного программирования, работу с файлами и тестирование с помощью pytest.
# Описание
Проект содержит две основные модели:

Product — товар с атрибутами: название, описание, цена и количество.

Category — категория товаров с атрибутами: название, описание и список товаров.

Также реализована функция загрузки категорий и товаров из JSON-файла, что позволяет удобно импортировать данные.

Для контроля количества созданных категорий и общего количества товаров используются статические счётчики.

# Установка
Клонируйте репозиторий:  
* git clone https://github.com/Carplatinum/CatalogManager  
cd catalogmanager  

Установите зависимости:  
* pip install -r requirements.txt  

# Использование
Запуск основного скрипта.  
В main.py показано, как создавать объекты Product и Category, а также как работать с их атрибутами и статическими счётчиками.  
* python -m src.main
# Загрузка данных из JSON
Функция позволяет загрузить категории и товары из JSON-файла:  
* load_categories_from_json(file_path: str) -> List[Category]  
# Тестирование
Для запуска тестов используется pytest  
Тесты покрывают:
* Инициализацию классов
* Корректность подсчёта количества категорий и товаров
* Загрузку данных из JSON  
# Лицензия
Проект открыт и доступен для использования и модификации.
