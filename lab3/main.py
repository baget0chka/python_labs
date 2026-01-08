import csv
import json
from kafka import KafkaProducer

#validation and load
def check_row(row):
    for i in range (len(row)):
        if row[i] == "":
            row.remove(row[i])
        elif len(row[i]) > 255:
            row.remove(row[i])
        elif row[i][0] == "-":
            if row[i][1:].isdigit():
                row[i] = int(row[i])
        elif row[i].isdigit():
            row[i] = int(row[i])
        else:
            try:
                row[i] = float(row[i])
            except ValueError:
                continue
    return row

def manual_input():
    columns = []
    rows = []
    columns_cnt = input("Введите количество столбцов в таблице: ").strip()
    while (not columns_cnt.isdigit() or columns_cnt == ""): 
        columns_cnt = input("Введите количество столбцов в таблице: ").strip()
    while (int(columns_cnt) <= 0):
        columns_cnt = input("Введите количество столбцов в таблице: ").strip()
    
    for i in range(int(columns_cnt)):
        column = input(f"Введите название {i+1} столбца: ").strip()
        while column == "":
            column = input(f"Введите название {i+1} столбца: ").strip()
        while not column.isalnum():
            column = input(f"Введите название {i+1} столбца: ").strip()
        columns.append(column)
    
    rows_cnt = input("Введите количество строк в таблице: ").strip()
    while (not rows_cnt.isdigit() or rows_cnt == ""): 
        rows_cnt = input("Введите количество строк в таблице: ").strip()
    while (int(rows_cnt) <= 0):
        rows_cnt = input("Введите количество строк в таблице: ").strip()
    
    print("Введите данные строк, используя в качестве разделителя |")
    for i in range(int(rows_cnt)):
        row = input(f"Введите данные {i+1} строки: ").strip()
        while row == "":
            row = input(f"Введите данные {i+1} строки: ").strip()
        while len(row.split("|")) > int(columns_cnt):
            row = input("Количество ячеек должно быть равно количеству столбцов: ").strip()

        row = [r.strip() for r in row.split('|')]
        row = check_row(row)
        
        if len(row) == int(columns_cnt):
            rows.append(row)

    return columns, rows

def csv_input():
    columns = []
    rows = []
    csv_path = input("Введите путь к файлу: ").strip()
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            columns = next(reader)
            columns = [c.strip() for c in columns]
            for col in columns:
                if not col.isalnum():
                    columns.remove(col)
            id = 1
            for row in reader:
                row = [r.strip() for r in row]
                row = check_row(row)
                
                if len(row) == len(columns):
                    rows.append(row)

    except FileNotFoundError:
        print("Файл не найден")

    return columns, rows

def json_input():
    columns, rows = [], []
    table_name = ""
    json_path = input("Введите путь к файлу: ").strip()
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if "columns" not in data or "rows" not in data:
            print("Файл имеет неправильную структуру.")
            return table_name, columns, rows

        if "table_name" not in data:
            table_name = load_table_name()
        else:
            table_name = data["table_name"]

        for col in data["columns"]:
            if col.strip().isalnum():
                columns.append(col.strip())

        for row in data["rows"]:
            row = [r.strip() for r in row]
            row = check_row(row)

            if len(row) == len(columns):
                rows.append(row)

        return table_name, columns, rows
    
    except FileNotFoundError:
        print("Файл не найден")

    return table_name, columns, rows

def load_table_name():
    table_name = input("Введите название таблицы: ").strip()
    while table_name == "":
        table_name = input("Введите название таблицы: ").strip()
    return table_name

def load_data():
    print("Выберите способ загрузки данных:")
    print("1. ручной ввод")
    print("2. загрузить файл CSV")
    print("3. загрузить файл JSON")

    choice = input().strip()
    match choice:
        case "1":
            table_name = load_table_name()
            columns, rows = manual_input()
            if len(rows) > 0:
                message = {"table_name": table_name,
                        "columns": columns,
                        "rows": rows}
                send(message)
                return 
            else:
                print("Нет корректных строк.")
                return
        case "2":
            table_name = load_table_name()
            columns, rows = csv_input()
            if len(rows) > 0 and len(columns) > 0:
                message = {"table_name": table_name,
                        "columns": columns,
                        "rows": rows}
                send(message)
                return 
            else:
                print("Нет корректных данных.")
                return
        case "3":
            table_name, columns, rows = json_input()
            if len(rows) > 0 and len(columns) > 0:
                message = {"table_name": table_name,
                        "columns": columns,
                        "rows": rows}
                send(message)
                return 
            else:
                print("Нет корректных данных.")
                return
        case _:
            print("Неверный формат ввода")
            return

#send to kafka
def send(message):
    producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # вставить нужный адрес
    value_serializer=lambda v: json.dumps(v).encode('utf-8') # Сериализатор
    )

    topic_name = 'test_topic'

    future = producer.send(topic_name, value=message)
    try:
        record_metadata = future.get(timeout=30)
        print(f"Сообщение отправлено: Топик={record_metadata.topic}, Партиция={record_metadata.partition}, Смещение={record_metadata.offset}")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

    producer.close()

#colsole app      
def app():
    print("="*20 + " Отправка сообщений в Kafka " + "="*20)
    while True:
        load_data()
        new_table = input("Желаете отправить еще одну таблицу? (y/n): ").lower()
        if new_table != "y":
            break
    print("Работа окончена")

if __name__ == "__main__":
    app()

