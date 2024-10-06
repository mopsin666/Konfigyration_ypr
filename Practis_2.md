Практическая № 2

Задание 1

pip show matplotlib

![image](https://github.com/user-attachments/assets/95e71642-e462-4cb8-8d48-aa2d2082d135)


Задание 2

npm show express

![image](https://github.com/user-attachments/assets/6ffea599-f14b-4d81-9c53-ee1802d158bc)



Задание 3


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

Генерация графика для matplotlib

![image](https://github.com/user-attachments/assets/a280198b-660d-4dee-b47e-491336f2efef)


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



Генерация графика для express


![image](https://github.com/user-attachments/assets/4a23d185-2589-4b73-93dc-eb0af2b5a567)


Задание 4

include "globals.mzn";

include "alldifferent.mzn";

var 0..9: q1;

var 0..9: q2;

var 0..9: q3;

var 0..9: q4;

var 0..9: q5;

var 0..9: q6;

constraint alldifferent ([q1, q2, q3, q4, q5, q6]);

constraint q3+q2+q1 = q6+q5+q4;

output ["ticket: ","\(q1)","\(q2)", "\(q3)","\(q4)", "\(q5)", "\(q6)",];

![image](https://github.com/user-attachments/assets/984a8739-6769-4b6e-b133-fd8f1f23a148)


Задание 5

array [0..2] of var 0..5: menu;

array [0..2] of var 0..8: dropdown;

array [0..2] of var 0..2: icon;

constraint menu [0] == 1 /\ menu [2] == 0;

constraint dropdown [0] == 1 \/ dropdown [0] == 2;

constraint dropdown [2] == 0;

constraint icon [1] == 0 /\ icon [2] == 0;

constraint menu [1] == 0 /\ dropdown [1] == 8 /\ dropdown [0] == 1 \/ menu [1] != 0  /\ dropdown [0] == 2 /\ dropdown [1] <= 3;

constraint dropdown [0] == 2 /\ icon [0] == 2 \/ dropdown [0] == 1 /\ icon [0] ==1;

output [if (fix(icon[0] == 1)) then "root -> icons: \(icon)\n" endif];

output ["root -> "];

output [if (fix(icon[0] == 2)) then "Menu: \(menu) -> Dropdown:\(dropdown) -> " endif];

output [if (fix(dropdown[0] == 1)) then "Menu:\(menu)-> Dropdown:\(dropdown) -> " endif];

output [if (fix(dropdown [0] != 1)) then "Icons: \(icon)" endif];

![image](https://github.com/user-attachments/assets/5a2b410c-588f-45d0-a8ad-b0b7c08d0075)


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
