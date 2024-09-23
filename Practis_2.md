Практическая № 2

Задание 1

pip show matplotlib

![image](https://github.com/user-attachments/assets/f7d47b68-bce5-4434-a340-afd75529f38f)

Задание 2

npm show express

![image](https://github.com/user-attachments/assets/0e270f8f-ca37-4304-ac8e-ab2a3e9f7e2d)

Задание 3

Создаем 2 файла md.dot и ed.not

digraph G {

    rankdir=LR;

    node [shape=ellipse, style=filled, color=lightblue];

    "matplotlib" -> "numpy";
    
    "matplotlib" -> "pillow";
    
    "matplotlib" -> "cycler";
    
    "matplotlib" -> "kiwisolver";
    
    "matplotlib" -> "pyparsing";
    
    "matplotlib" -> "python-dateutil";

}


digraph G {

    rankdir=LR;
    
    node [shape=ellipse, style=filled, color=lightgreen];

    "express" -> "accepts";
    
    "express" -> "array-flatten";
    
    "express" -> "body-parser";
    
    "express" -> "content-disposition";
    
    "express" -> "cookie";
    
    "express" -> "cookie-signature";
    
    "express" -> "debug";
    
    "express" -> "depd";
    
    "express" -> "encodeurl";
    
    "express" -> "escape-html";
    
    "express" -> "etag";
    
    "express" -> "finalhandler";
    
    "express" -> "fresh";
    
    "express" -> "merge-descriptors";
    
    "express" -> "methods";
    
    "express" -> "on-finished";
    
    "express" -> "parseurl";
    
    "express" -> "path-to-regexp";
    
    "express" -> "proxy-addr";
    
    "express" -> "qs";
    
    "express" -> "range-parser";
    
    "express" -> "safe-buffer";
    
    "express" -> "send";
    
    "express" -> "serve-static";
    
    "express" -> "setprototypeof";
    
    "express" -> "statuses";
    
    "express" -> "type-is";
    
    "express" -> "utils-merge";
    
    "express" -> "vary";

}

$ dot -Tpng md.dot -o matplotlib_dependencies.png

Генерация графика для matplotlib

![image](https://github.com/user-attachments/assets/2cf3dc74-60f6-4dd8-897d-614bc0af0046)


Генерация графика для express

$ dot -Tpng ed.dot -o express_dependencies.png

![image](https://github.com/user-attachments/assets/7ea8b2d0-5904-4f60-b4ff-8320d1761279)
![image](https://github.com/user-attachments/assets/067b62ea-f609-4326-b80d-39e1f3cd5bd0)
![image](https://github.com/user-attachments/assets/b075583b-1300-4a3d-9121-95645b44c425)

Задание 4

include "alldifferent.mzn";

var 1..9: d1;  

var 0..9: d2; 

var 0..9: d3; 

var 0..9: d4; 

var 0..9: d5;  

var 0..9: d6; 

constraint alldifferent([d1, d2, d3, d4, d5, d6]);

constraint d1 + d2 + d3 = d4 + d5 + d6;

solve minimize d1 + d2 + d3; 

![image](https://github.com/user-attachments/assets/6827304b-b224-48eb-8c58-be62207894f8)

Задание 5

% Use this editor as a MiniZinc scratch book

set of int: MenuVersions = 1..6;

set of int: DropdownVersions = 1..5;

set of int: IconVersions = 1..2;

array[MenuVersions] of int: menu = [150, 140, 130, 120, 110, 100];

array[DropdownVersions] of int: dropdown = [230, 220, 210, 200, 180];

array[IconVersions] of int: icons = [200, 100];

var MenuVersions: selected_menu;

var DropdownVersions: selected_dropdown;

var IconVersions: selected_icons;

constraint

    (selected_menu = 1 -> selected_dropdown in 1..3) /\
    
    (selected_menu = 2 -> selected_dropdown in 2..4) /\
    
    (selected_menu = 3 -> selected_dropdown in 3..5) /\
    
    (selected_menu = 4 -> selected_dropdown in 4..5) /\
    
    (selected_menu = 5 -> selected_dropdown = 5) /\
    
    (selected_dropdown = 1 -> selected_icons = 1) /\
    
    (selected_dropdown = 2 -> selected_icons in 1..2) /\
    
    (selected_dropdown = 3 -> selected_icons in 1..2) /\
    
    (selected_dropdown = 4 -> selected_icons in 1..2) /\
    
    (selected_dropdown = 5 -> selected_icons in 1..2);

solve satisfy;

output [
    
    "Selected menu version: \(menu[selected_menu])\n",
    
    "Selected dropdown version: \(dropdown[selected_dropdown])\n",
    
    "Selected icon version: \(icons[selected_icons])\n"

];

![image](https://github.com/user-attachments/assets/7d68b950-b525-46f0-bc41-e43b66236112)

Задание 6

include "alldifferent.mzn";

% Пакеты и их версии

var 1..1: root_version;  % версия пакета root

var 1..2: foo_version;  % версия пакета foo

var 1..2: left_version;  % версия пакета left

var 1..2: right_version;  % версия пакета right

var 1..2: shared_version;  % версия пакета shared

var 1..2: target_version;  % версия пакета target

% Зависимости между пакетами

constraint (root_version == 1) -> (foo_version == 1 \/ foo_version == 2);

constraint (root_version == 1) -> (target_version == 2);

constraint (foo_version == 2) -> (left_version == 1);

constraint (foo_version == 2) -> (right_version == 1);

constraint (left_version == 1) -> (shared_version == 1 \/ shared_version == 2);

constraint (right_version == 1) -> (shared_version == 1);

constraint (shared_version == 1) -> (target_version == 1 \/ target_version == 2);

% Решение

solve satisfy;

![image](https://github.com/user-attachments/assets/9c000b77-65ea-4e0e-8b17-e1b670726be3)

Задание 7

int: num_packages;

set of int: Packages = 1..num_packages;

array[Packages] of set of int: Versions;

array[Packages] of var int: selected_version;

array[Packages] of set of int: dependencies;

array[Packages, Packages] of int: min_version;

array[Packages, Packages] of int: max_version;

constraint
  
  forall(i in Packages) (
  
    forall(dep in dependencies[i]) (
    
      selected_version[dep] >= min_version[i, dep] /\
      
      selected_version[dep] <= max_version[i, dep]
    
    )
  
  );

solve satisfy;
