num1 = input("введите первое число:")
num2 = input("введите второе число: ")
num3 = input("введите операцию(-, +, *, /): ")

if num3 == "+":
   result = (int(num1) + int(num2))
elif num3 == "-":
    result = (int(num1) - int(num2))
elif num3 == "*":
    result = (int(num1) * int(num2))
elif num3 == "/":
    result = (int(num1) / int(num2))
else:
    result = None
print("выбранное первое число: ", num1)
print("выбранное второе число: ", num2)
print("выбранная операция: ", num3)
if result is not None:
    print("Итог:", result)
else:
    print("Итог: неизвестная операция") 