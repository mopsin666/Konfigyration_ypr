# Эмулятор Shell для Unix-подобных ОС

## Описание
Этот проект представляет собой эмулятор оболочки, работающий в графическом режиме (GUI), который максимально приближен к реальной командной строке Unix-подобных операционных систем. Эмулятор использует виртуальную файловую систему, представляемую в виде zip-архива, не требуя его распаковки у пользователя. Логирование всех действий пользователя ведется в файл формата CSV.

Эмулятор поддерживает выполнение базовых команд, а также позволяет запускать стартовый скрипт для автоматического выполнения списка команд при инициализации.

## Основные функции и команды

- **`ls`** — вывод содержимого текущей директории.
- **`cd <директория>`** — смена текущей директории.
- **`pwd`** — вывод текущего пути.
- **`exit`** — завершение работы эмулятора.
- **`whoami`** — вывод имени текущего пользователя.
- **`chmod <права> <файл>`** — изменение прав доступа к файлу.

Эти команды работают в пределах виртуальной файловой системы, представленной zip-архивом.

## Аргументы командной строки

При запуске эмулятора из командной строки можно указать следующие параметры:

- **`--user`** — имя пользователя, которое будет отображаться в приглашении командной строки.
- **`--filesystem`** — путь к zip-архиву, содержащему виртуальную файловую систему.
- **`--logfile`** — путь к лог-файлу, в который будут записываться все действия пользователя в формате CSV.
- **`--script`** *(необязательно)* — путь к стартовому скрипту, который содержит команды для выполнения при запуске эмулятора.

### Пример запуска
```bash
python main.py --user dmitry --filesystem test.zip --logfile logfile.csv --script script.txt
```
## Тестирование
Для автоматического тестирования эмулятора использован модуль unittest. Тесты проверяют корректность работы команд и логирования.
### Запуск тестов:
```bash
python -m unittest tests.py
```
![image](https://github.com/user-attachments/assets/98bc1b97-9a41-41f3-93f4-97ddce064235)
