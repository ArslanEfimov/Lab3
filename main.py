stuffdict = {"rifle": ("в", 3, 25),
             "pistol": ("п", 2, 15),
             "ammunition": ("б", 2, 15),
             "med": ("а", 2, 20),
             "inhaler": ("и", 1, 5),
             "knife": ("н", 1, 15),
             "axe": ("т", 3, 20),
             "obereg": ("о", 1, 25),
             "flyazhka": ("ф", 1, 15),
             "antidot": ("д", 1, 10),
             "food": ("к", 2, 20),
             "arbalet": ("р", 2, 20),
             }
# Для моего варианта - 9 ячеек
print("Введите вместимость инвентаря Тома:")
stock = int(input())
# Условие для дополнительного задания с случаем в 7 ячеек
if stock == 7:
    print("Случай с инвентарем в 7 ячеек:")


def get_area_and_value(stuffdict):
    symbol = [stuffdict[item][0] for item in stuffdict]
    area = [stuffdict[item][1] for item in stuffdict]
    value = [stuffdict[item][2] for item in stuffdict]
    return symbol, area, value


def get_memtable(stuffdict, S=stock - 1):
    symbol, area, value = get_area_and_value(stuffdict)
    n = len(value)  # находим размеры таблицы

    # создаём таблицу из нулевых значений
    V = [[0 for a in range(S + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for a in range(S + 1):
            # базовый случай, для моего варианта с астмой

            if i == 0 or a == 0:
                V[i][a] = 5

            # максимизируем значение суммарной ценности
            elif area[i - 1] <= a:
                V[i][a] = max(value[i - 1] + V[i - 1][a - area[i - 1]], V[i - 1][a])

            # если площадь предмета больше площади столбца,
            # забираем значение ячейки из предыдущей строки
            else:
                V[i][a] = V[i - 1][a]

    return V, symbol, area, value


def get_selected_items_list(stuffdict, S=stock - 1):
    V, symbol, area, value = get_memtable(stuffdict)
    n = len(value)
    res = V[n][S]  # начинаем с последнего элемента таблицы
    a = S  # начальная площадь - максимальная
    items_list = [("и", 1, 5)]  # список площадей и ценностей, добавляем услове астмы

    for i in range(n, 0, -1):  # идём в обратном порядке
        if res <= 0:  # условие прерывания - собрали "рюкзак"
            break
        if res == V[i - 1][a]:  # ничего не делаем, двигаемся дальше
            continue
        else:
            # "забираем" предмет
            items_list.append((symbol[i - 1], area[i - 1], value[i - 1]))
            res -= value[i - 1]  # отнимаем значение ценности от общей
            a -= area[i - 1]  # отнимаем площадь от общей

    selected_stuff = []

    # находим ключи исходного словаря - названия предметов
    for search in items_list:
        for key, value in stuffdict.items():
            if value == search and value[1] > 1:
                for n in range(value[1]):
                    selected_stuff.append(value[0])
            if value == search and value[1] == 1:
                selected_stuff.append(value[0])
    return selected_stuff


stuff = get_selected_items_list(stuffdict)
print("Вещи, которые Тому будут самыми выгодными:")
s_count = 0
matrix_stuff = []
for i in range(3):
    matrix_stuff.append(["/"] * 3)
    for j in range(3):
        if s_count < stock:
            matrix_stuff[i][j] = stuff[s_count]
            s_count += 1
        print(list(matrix_stuff[i][j]), end="  ")
    print()
    print()
sum_all = sum([stuffdict[item][2] for item in stuffdict])
sum_stuff = 0
new_stuff = []
for i in range(stock - 1):
    if stuff[i] != stuff[i + 1] and i != stock - 2:
        new_stuff.append(stuff[i])
    if i == stock - 2:
        new_stuff.append(stuff[i])
for search in new_stuff:
    for key, value in stuffdict.items():
        if value[0] == search:
            sum_stuff += value[2]
print("Итоговые очки выживания Тома:", 10 + sum_stuff - (sum_all - sum_stuff))
if 10 + sum_stuff - (sum_all - sum_stuff) < 0:
    print("Тома съедят Зомбииииии!!!")
