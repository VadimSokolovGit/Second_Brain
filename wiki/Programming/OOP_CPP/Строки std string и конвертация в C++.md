# Строки std::string и конвертация типов в C++

> [!info] Что такое `std::string`
> В C++ тип `std::string` — это не самостоятельный класс, а псевдоним (typedef), созданный на основе шаблонного класса:
> ```cpp
> typedef std::basic_string<char> string;
> ```
> Этот шаблон инкапсулирует управление динамическим массивом символов в куче (подобно `std::vector`). 
> - `std::string` — работает с типом `char` (1-байтовые символы ASCII).
> - `std::wstring` — работает с типом `wchar_t` (для Юникода и кириллицы на некоторых платформах).

## Конвертация строки в число и обратно

Начиная с C++11, появились простые и удобные функции для конвертации, заменяющие старые Си-функции (`atoi`) и потоки (`stringstream`).

> [!success] Из числа в строку
> Используется универсальная перегруженная функция **`std::to_string(value)`**.
> Она принимает любые базовые числа (`int`, `float`, `double`, `long`) и возвращает объект `std::string`.

> [!success] Из строки в число
> Функции разделяются в зависимости от желаемого типа данных:
> - **`std::stoi()`** — String to Integer (`int`)
> - **`std::stod()`** — String to Double (`double`)
> - **`std::stof()`** — String to Float (`float`)
> - **`std::stol()`** — String to Long (`long`)

> [!warning] Ловушка для экзамена (Исключения)
> Если передать в `std::stoi()` строку, которую невозможно превратить в число (например, `"привет"`), программа не просто вернёт ошибку, а выбросит исключение **`std::invalid_argument`**.
> *Защита:* Обязательно оборачивайте такой код в блок `try-catch`.

## Пример кода

> [!example] Код
> ```cpp
> #include <iostream>
> #include <string> // Заголовочный файл для работы со строками и конвертации
> 
> int main() {
>     setlocale(LC_ALL, "Russian");
> 
>     std::cout << "--- 1. Конвертация ЧИСЛА В СТРОКУ ---\n";
>     int age = 20;
>     double pi = 3.14159;
> 
>     std::string strAge = std::to_string(age);
>     std::string strPi = std::to_string(pi);
> 
>     std::cout << "Строка с возрастом: " << strAge << "\n";
>     std::cout << "Строка с Пи: " << strPi << "\n\n";
> 
> 
>     std::cout << "--- 2. Конвертация СТРОКИ В ЧИСЛО ---\n";
>     std::string strPrice = "1250";
>     std::string strWeight = "45.75";
> 
>     // Конвертируем в соответствующие типы
>     int price = std::stoi(strPrice);
>     double weight = std::stod(strWeight);
> 
>     // Проверяем, что это теперь числа (проводим математические операции)
>     int doublePrice = price * 2; 
>     double halfWeight = weight / 2;
> 
>     std::cout << "Удвоенная цена (int): " << doublePrice << "\n";
>     std::cout << "Половина веса (double): " << halfWeight << "\n\n";
> 
> 
>     std::cout << "--- 3. Защита от некорректного ввода (try-catch) ---\n";
>     std::string badString = "Текст123";
> 
>     try {
>         int badNumber = std::stoi(badString); // Здесь код сломается
>         std::cout << "Успешно прочитано число: " << badNumber << "\n";
>     } 
>     catch (const std::invalid_argument& e) {
>         std::cout << "[Ошибка]: Строку '" << badString << "' невозможно преобразовать в число!\n";
>     }
> 
>     return 0;
> }
> ```

## Источники
- [OOP C++](file:///c:/Users/USER/Desktop/Second%20Brain/raw/OOP%20C++)
