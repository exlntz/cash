import csv


def add_mechanic(text):
    processed_text=text.split()
    with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fm:
        csv.writer(fm).writerow(processed_text)


def add_car(text):
    with open('csvfiles/cars.csv', 'a', encoding='utf-8', newline='') as fc:
        csv.writer(fc).writerow(text)



print('''Введите данные механика через пробел в таком формате:

                Имя Возраст Пол''')
row_mechanic=input()#строку с машиной и с механиком нужно брать из админ панели
#row_car=[input()]    #желательно сделать кнопку добавить мех/машину и там уже сделать строку ввода


add_mechanic(row_mechanic)
#add_car(row_car)

#потом доделаю