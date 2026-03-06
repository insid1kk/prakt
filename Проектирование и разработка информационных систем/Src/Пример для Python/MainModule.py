#Модуль запуска приложения

from SampleModule import *

#Отображение данных
def show(*results):
    for result in results:
        print(result)

#Запуск приложения
if __name__ == "__main__":

    result_1 = sum_numbers(1, 2, 3, 4, 5)
    result_2 = sum_numbers(55, 66, 77, 88, 99)
    
    show(result_1, result_2)