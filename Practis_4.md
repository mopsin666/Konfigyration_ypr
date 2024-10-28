Практическая работа №4

Задание 1

![image](https://github.com/user-attachments/assets/f602d920-1545-489f-925d-cc5fdb4c3eda)

Задание 2

![image](https://github.com/user-attachments/assets/8cbbf263-1a21-42c5-b613-e9fe634bddca)

Задание 3

![image](https://github.com/user-attachments/assets/1941c6e1-4040-4d0c-bbfe-7f0634d8674d)
![image](https://github.com/user-attachments/assets/6c244f36-50f2-4853-8609-3b78a3c60521)
![image](https://github.com/user-attachments/assets/c70c08dd-9fd1-46c4-83d3-5fb99146d208)

Задание 4

Код на Python

import os

import subprocess

def list_git_objects():

    # Получить список всех объектов в репозитории
    
    objects = subprocess.check_output(['git', 'rev-list', '--objects', '--all']).decode('utf-8').splitlines()

    for obj in objects:
    
        # Разделить строку на объект и его путь
        
        obj_hash, obj_path = obj.split(' ', 1)
        
        print(f"Объект: {obj_hash}")
        
        # Вывести содержимое объекта
        
        try:
        
            obj_content = subprocess.check_output(['git', 'cat-file', '-p', obj_hash]).decode('utf-8')
            
            print(f"Содержимое {obj_path}:\n{obj_content}")
            
        except subprocess.CalledProcessError as e:
        
            print(f"Не удалось получить содержимое объекта: {e}")
            
        print("-" * 50)

if __name__ == "__main__":

    list_git_objects()

Скриншот выполнения

![image](https://github.com/user-attachments/assets/019cb546-7d36-4546-8131-d79146e94ce0)

