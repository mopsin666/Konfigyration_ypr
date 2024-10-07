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

array [0..2] of var 0..2: sh;

array [0..2] of var 0..2: ta;

array [0..2] of var 0..2: fo;

array [0..2] of var 0..5: le;

array [0..2] of var 0..8: ro;

array [0..2] of var 0..2: ri;

constraint (fo[1]==0) \/ (fo[1]==1 /\ le[0]==1 /\ sh[0] >= 1) /\ (ri[0] == 1 /\ sh[0] < 2 /\ ta[0] == 1);

constraint ro[0] == 1 /\ ro[1] == 0 /\ ro[2] == 0 /\ fo[0] == 1 /\ fo[2] == 0 /\ le[0] == 1 /\ le[1] == 0 /\ le[2] == 0;

constraint ri[0] == 1 /\ ri[1] == 0 /\ ri[2] == 0 /\ sh[1] == 0 /\ sh[2]==0 /\ ta[1] == 0/\ ta[2] == 0;

output [

  if(fix(ta[0] == 2)) then "root \(ro) требует target \(ta)\n" endif,
  
  if (fix(fo[1] == 0/\ ta[0] == 2)) then "root \(ro) требует foo \(fo)\n" endif,
  
  if (fix(fo[1] ==1 /\ sh[0] == 1)) then "root \(ro) требует foo \(fo) требует left \(le) и требует right \(ri) требует shared \(sh) требует target \(ta)\n" endif

  ];

![image](https://github.com/user-attachments/assets/bd9b00db-80bb-4254-afc9-67f8dfdd3185)


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

![image](https://github.com/user-attachments/assets/8498d5ef-5939-45d9-befc-3872abdea283)

