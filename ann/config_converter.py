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
        if value in constants:
            return str(constants[value])
        return value
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

# Функция для обработки выражений с вычислением
def evaluate_expression(expression):
    try:
        parts = expression.split()
        op = parts[0]
        if op == '+':
            return int(parts[1]) + int(parts[2])
        elif op == '-':
            return int(parts[1]) - int(parts[2])
        elif op == '*':
            return int(parts[1]) * int(parts[2])
        elif op == '/':
            return int(parts[1]) / int(parts[2])
        elif op == 'abs':
            return abs(int(parts[1]))
        else:
            raise ValueError("Unsupported operation")
    except Exception as e:
        print(f"Error evaluating expression: {expression}")
        raise e

# Функция для обработки констант и выражений
def handle_constants(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, str) and value.startswith("@{") and value.endswith("}"):
            # Вычисляем выражение
            expression = value[2:-1]
            result[key] = evaluate_expression(expression)
        elif isinstance(value, dict):
            result[key] = handle_constants(value)
        elif isinstance(value, str) and re.match(r'^def\s+\w+\s*=\s*.+;$', value):
            # Обработка объявления константы в формате def имя = значение;
            name, expr = value[4:-1].split("=")
            name, expr = name.strip(), expr.strip()
            constants[name] = evaluate_expression(expr) if expr.startswith("@{") else process_value(expr)
            result[key] = f"def {name} = {constants[name]};"
        else:
            result[key] = value
    return result

# Главная функция для преобразования
def convert_yaml_to_config(data):
    result = []
    for key, value in data.items():
        result.append(f"{key} : {process_value(value)}")
    return f"([{', '.join(result)}])"

# Функция для загрузки и обработки YAML
def load_yaml(file_path):
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return handle_constants(data)
        except yaml.YAMLError as e:
            print("Error parsing YAML:", e)
            sys.exit(1)

# Основная функция
def main():
    if len(sys.argv) != 2:
        print("Usage: python config_converter.py <path_to_yaml_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    data = load_yaml(file_path)
    config_text = convert_yaml_to_config(data)
    print(config_text)

if __name__ == "__main__":
    main()
