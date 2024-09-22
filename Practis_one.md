Практическая №1

Задание 1

cut -d: -f1 /etc/passwd | sort

![image](https://github.com/user-attachments/assets/cf45745f-b120-4fb4-886d-390d5a09b832)

Задание 2

awk '{print $2, $1}' /etc/protocols | sort -rn | head -5

![image](https://github.com/user-attachments/assets/c5fcb850-6ece-411e-a5d9-58e61c794bf2)

Задание 3

line = input()

len = len(line)

print("+--", end='')

for i in range(0, len-1):

    print('-', end='')

print('--+')

print(f'|  {line}  |')

print("+--", end='')

for i in range(0, len-1):

    print('-', end='')

print('--+')

![image](https://github.com/user-attachments/assets/9baacef0-8722-46fa-bdf1-65ab097929af)

Задание 4

grep -o '\b[a-zA-Z_][a-zA-Z0-9_]*\b' main.cpp | sort | uniq

![image](https://github.com/user-attachments/assets/d5408d60-01f0-4350-9d24-1553cda4bccb)

Задание 5

./pract5.sh banner2.sh

chmod + x "$1"

cp "$1" /usr/local/bin/

![image](https://github.com/user-attachments/assets/0109bcd9-9d30-4c3c-adf1-0001124f18d8)


Задание 6

import os

def check_comment(file_path):
   
    with open(file_path, 'r') as file:
    
        first_line = file.readline().strip()
        
        if first_line.startswith(("//", "/*", "#")):
        
            return True
        
        else:
        
            return False

def main():
    
    for root, dirs, files in os.walk("."):
       
        for file in files:
        
            if file.endswith((".c", ".js", ".py")):
            
                file_path = os.path.join(root, file)
                
                if check_comment(file_path):
                
                    print(f"Comment found in {file_path}")
                
                else:
                
                    print(f"No comment found in {file_path}")

if __name__ == "__main__":
  
    main()

    ![image](https://github.com/user-attachments/assets/a52548b1-b24e-4d9b-ae98-a01d7e4c4785)

    Задание 7

    #!/bin/bash

find "$1" -type f -exec md5sum {} + | sort | uniq -w32 -dD

![image](https://github.com/user-attachments/assets/5a3acc2d-58f7-4c27-8ffd-a924544f30b3)

Задание 8    

#!/bin/bash

find . -name "*.$1" -print0 | tar -czvf archive.tar.gz --null -T -

![image](https://github.com/user-attachments/assets/911f5e0b-2df7-46cb-95d4-c18380c7e8c6)

Задание 9

#!/bin/bash

sed -e 's/    /\t/g' "$1" > "$2"

![image](https://github.com/user-attachments/assets/20acc056-b88c-4a72-9ef2-09609435d20b)

![image](https://github.com/user-attachments/assets/5784bf7c-d010-4add-b671-e78487e05d70)

Задание 10

#!/bin/bash

find "$1" -type f -empty -name "*.txt"

![image](https://github.com/user-attachments/assets/34b6b3c9-635a-44ff-90d5-3c58141be55d)


