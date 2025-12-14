from copy import deepcopy
a = [[44, -2, -5, 38, -91],
     [2, 0, 6, 3, 22],
     [13, 1, -4, 90, 11],
     [-3, -6, -98, -23, -24],
     [10, 34, 32, 31, 69]]
b = deepcopy(a)


def selection_sort(matrix):
    """Сортування вибором."""
    N = len(matrix)
    for line in matrix:
        for i in range(N-1):
            val = line[i]
            min_idx = i
            for j in range (i+1, N):
                if val > line[j]:
                    val = line[j]
                    min_idx = j
            if min_idx != i:
                temp = line[i]
                line[i] = line[min_idx]
                line[min_idx] = temp
    print("Відпрацювало сортування вибором:")
    for line in matrix:
        print(line)
    return matrix

def sum_el_upper_diagnal(matrix):
    """Рахує суми елементів стовпців, що знаходяться над побічною діагоналлю."""
    N = len(matrix)
    sum_column = []
    for j in range(N - 1):
        sum_temp = 0
        for i in range(N):
            if i + j < N - 1:
                sum_temp += matrix[i][j]
        sum_column.append(sum_temp)
    print(f"Суми стовпців (1-4):{sum_column}")
    geom_mean_of_sum = geom_mean_of_el(sum_column)
    return geom_mean_of_sum

def geom_mean_of_el(el):
    """Обчислює середнє геометричне модулів чисел у списку."""
    power = len(el)
    if power == 0:
        print("Помилка: передано порожній список!")
        return 0
    res = 1
    for x in el:
        res *= abs(x)

    result = res ** (1/power)
    print(f"Cереднє геометричне значення:{result:.4f}")
    return result


class ChatQueue:
    """Клас, що реалізує структуру даних Черга (FIFO) для повідомлень."""
    def __init__(self):
        self.queue = []

    def send_message(self, message):
        self.queue.append(message)

    def receive_message(self):
        if self.queue != []:
            return self.queue.pop(0)
        else:
            return("У вас немає вхідних сповіщень!")

    def show_all(self):
        return self.queue

    def ChatQueue_manager(self):
        """Запускає консольне меню для керування чатом."""
        while True:
            print("Напишіть що ви хочете зробити? Send/Receive/Show_all(messeage) or Exit")
            try:
                command = input().lower().strip()
            except KeyboardInterrupt:
                print("Ви виконали некоректне завершення програми!")
                break

            if command == "exit":
                break
            elif command == "send":
                print("Введіть повідомлення яке ви хочете залишити:")
                message = input()
                self.send_message(message)
                print("Повідомлення додано.")
            elif command == "receive":
                print("Ось яке повідомлення ви отрамали:")
                print(self.receive_message())
            elif command == "show_all":
                print("Всі повідомлення:")
                print(self.show_all())
            else:
                print("Ви ввели щось не коректне. Спробуйте ще раз")


selection_s = selection_sort(a)
sum_el_upper_d = sum_el_upper_diagnal(b)


my_chat = ChatQueue()
my_chat.ChatQueue_manager()