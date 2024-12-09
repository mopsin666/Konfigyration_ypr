import sys
import yaml
import re

# Словарь для хранения определённых констант
constants = {}


# Функция для обработки чисел, массивов и словарей
def process_value(value):
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, list):
        return f"list({', '.join(process_value(v) for v in value)})"
    elif isinstance(value, dict):
        return f"([{', '.join(f'{k} : {process_value(v)}' for k, v in value.items())}])"
    elif isinstance(value, str):
        # Проверяем, если это константа, то возвращаем её имя
        if value in constants:
            return str(constants[value])
        return value
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")


# Функция для обработки выражений
def process_expression(expression):
    # Мы просто возвращаем выражение как есть, без выполнения вычислений
    return expression


# Функция для обработки констант и выражений
def handle_constants(data):
    result = {}

    # Обрабатываем константы, но не вычисляем их
    for key, value in data.get('constants', {}).items():
        if isinstance(value, str) and value.startswith("@{") and value.endswith("}"):
            # Оставляем выражение как есть
            constants[key] = value
        elif isinstance(value, str) and re.match(r'^def\s+\w+\s*=\s*.+;$', value):
            # Это определение константы
            constants[key] = value
        else:
            result[key] = value

    # Вернем результат без вычислений
    return result


# Функция для загрузки и обработки YAML
def load_yaml(file_path):
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return handle_constants(data)
        except yaml.YAMLError as e:
            print("Error parsing YAML:", e)
            sys.exit(1)


# Главная функция для преобразования
def convert_yaml_to_config(data):
    result = []
    for key, value in data.items():
        # Для каждого ключа создаем строку в формате "key : value"
        result.append(f"{key} : {process_value(value)}")

    # Возвращаем итоговый формат как текст
    return f"([{', '.join(result)}])"


# Основная функция
def main():
    if len(sys.argv) != 2:
        print("Usage: python config_converter.py <path_to_yaml_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not file_path.endswith('.yaml'):
        print("Error: The provided file must be a YAML file.")
        sys.exit(1)

    try:
        data = load_yaml(file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        config_text = convert_yaml_to_config(data)
    except Exception as e:
        print(f"Error while converting YAML to config: {e}")
        sys.exit(1)

    # Записываем результат в файл output.txt
    try:
        with open('output.txt', 'w') as file:
            file.write(config_text)
        print("Output written to output.txt")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
