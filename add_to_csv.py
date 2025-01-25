import csv


def add_mechanic(text):
    with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fm:
        csv.writer(fm).writerow(text)


def add_car(text):
    with open('csvfiles/cars.csv', 'a', encoding='utf-8', newline='') as fc:
        csv.writer(fc).writerow(text)

#строку с машиной и с механиком нужно брать из админ панели
#желательно сделать кнопку добавить мех/машину и там уже сделать строку ввода
row_car=[input()]
row_mechanic=[input()]


add_mechanic(row_mechanic)
add_car(row_car)

