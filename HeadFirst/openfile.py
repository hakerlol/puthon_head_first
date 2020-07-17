with open('todos.txt', 'a') as todos:
    print('Файл был открыт', file=todos)
    print('Написали второе предложение', file=todos)
    print('Перед закрытием', file=todos)

with open('todos.txt') as tasks:
    for sentens in tasks:
        print(sentens)
