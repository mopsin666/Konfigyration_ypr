import os
import re
import config_converter

# Функция для приведения результата к единому стилю
def normalize_output(output):
    # Приводим True/False к нижнему регистру для соответствия формату
    output = re.sub(r'\bTrue\b', 'true', output)
    output = re.sub(r'\bFalse\b', 'false', output)

    # Добавляем пробелы после запятых, если их нет
    output = re.sub(r',(\S)', r', \1', output)

    # Удаляем лишние пробелы перед закрывающими скобками
    output = re.sub(r'\s+\)', ')', output)

    # Удаляем лишние пробелы перед закрывающими скобками списков и словарей
    output = re.sub(r'\s+\]', ']', output)
    
    return output.strip()

# Функция для выполнения теста
def run_test(file_path, expected_output):
    # Загружаем данные из YAML и конвертируем их
    data = config_converter.load_yaml(file_path)
    result = config_converter.convert_yaml_to_config(data)
    
    # Нормализуем результат и ожидаемый вывод для точного сравнения
    normalized_result = normalize_output(result)
    normalized_expected = normalize_output(expected_output)

    # Проверяем соответствие результата ожидаемому значению
    if normalized_result == normalized_expected:
        print(f"Test passed for {file_path}")
    else:
        print(f"Test failed for {file_path}")
        print("Expected:")
        print(normalized_expected)
        print("Got:")
        print(normalized_result)

# Примеры тестов
def test_all():
    # Путь к папке с тестовыми файлами
    base_path = "C:\\Users\\mopsi\\Desktop\\ann\\"

    # Пример 1
    example_1_path = os.path.join(base_path, "network_config.yaml")
    expected_output_1 = "([network : ([name : corporate_network, hosts : list(([name : host1, ip : 192.168.1.10]), ([name : host2, ip : 192.168.1.20])), subnets : list(([subnet_name : office, range : 192.168.1.0/24]))])])"
    run_test(example_1_path, expected_output_1)

    # Пример 2
    example_2_path = os.path.join(base_path, "server_config.yaml")
    expected_output_2 = "([server : ([hostname : my-server, port : 8080, max_connections : 100, logging : true, timeout : 30, health_check : ([interval : 5, retries : 3 ])])])"
    run_test(example_2_path, expected_output_2)

    # Пример 3
    example_3_path = os.path.join(base_path, "user_prefs.yaml")
    expected_output_3 = "([preferences : ([theme : dark, notifications : ([email : true, sms : false]), recent_files : list(report1.docx, summary.pdf, budget.xlsx), max_recent_files : 10, font_size : 12, advanced : ([dev_mode : false, cache_size : 256])])])"
    run_test(example_3_path, expected_output_3)

# Запуск всех тестов
if __name__ == "__main__":
    test_all()
