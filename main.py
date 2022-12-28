import numpy as np
import math
import time
from enum import Enum

class Vehicle:
    def __init__(self, position, speed, angle):
        self.position = position
        self.speed = speed
        self.angle = angle
    def update_position(self, tick_time):
        # Рассчитываем изменение позиции по осям X и Y
        dx = self.speed * math.cos(self.angle) * tick_time
        dy = self.speed * math.sin(self.angle) * tick_time
        # Обновляем позицию
        self.position = (self.position[0] + dx, self.position[1] + dy)
     

class Autopilot:
    def __init__(self, leader_distance):
        self.leader_distance = leader_distance

    def follow_leader(self, leader, follower):
        # Рассчитываем расстояние до лидера по осям X и Y
        dx = leader.position[0] - follower.position[0]
        dy = leader.position[1] - follower.position[1]
        # Рассчитываем текущее расстояние до лидера
        current_distance = math.sqrt(dx * dx + dy * dy)

        # Рассчитываем требуемое изменение скорости
        speed_diff = current_distance- self.leader_distance  
        # Увеличиваем/уменьшаем скорость преследователя
        follower.speed += speed_diff
        
        # Рассчитываем требуемое изменение угла
        angle_diff = math.atan2(dy, dx) - follower.angle
        # Увеличиваем/уменьшаем угол преследователя
        follower.angle += angle_diff

    # Метод следования с применеием нечеткой логики
    # Вначале известно точное расстояние до лидера,
    # но намеренно уменьшается для добавления нечеткости
    def follow_leader_fuzzy(self, leader, follower):
        # Рассчитываем расстояние до лидера по осям X и Y
        dx = leader.position[0] - follower.position[0]
        dy = leader.position[1] - follower.position[1]
        # Рассчитываем текущее расстояние до лидера
        current_distance = math.sqrt(dx * dx + dy * dy)

        current_distance = decrease_distance_accuracy(current_distance)
        # Рассчитываем требуемое изменение скорости
        speed_diff = current_distance- self.leader_distance  
        # Увеличиваем/уменьшаем скорость преследователя
        follower.speed += speed_diff
        
        # Рассчитываем требуемое изменение угла
        angle_diff = math.atan2(dy, dx) - follower.angle
        # Увеличиваем/уменьшаем угол преследователя
        follower.angle += angle_diff

def decrease_distance_accuracy(distance):
    if (distance <= Distance.CLOSE):
        return Distance.CLOSE / 2
    if (distance <= Distance.NOT_FAR):
        return Distance.NOT_FAR / 2
    if (distance <= Distance.FAR):
        return Distance.FAR / 2
    if (distance <= Distance.TOO_FAR):
        return Distance.TOO_FAR
        
        
        

class Distance(Enum):
    CLOSE = 10
    NOT_FAR = 50
    FAR = 100
    TOO_FAR = 200
Distance = Enum("Distance", ["CLOSE", "NOT_FAR", "FAR"])
        
def update_distance(autopilot, leader, follower):
    # Рассчитываем расстояние до лидера по осям X и Y
    dx = leader.position[0] - follower.position[0]
    dy = leader.position[1] - follower.position[1]
    # Рассчитываем текущее расстояние до лидера
    current_distance = math.sqrt(dx * dx + dy * dy)
    autopilot.leader_distance = current_distance

def update_leader_parameters(leader):
    # Запрашиваем у пользователя новые параметры
    leader.speed = float(input("Введите новую скорость лидера: "))
    leader.angle = float(input("Введите новый угол управления лидера: "))
def tick():
    update_distance(autopilot, leader, follower)
    leader.update_position(1)
    follower.update_position(1)
    save_logs(filename, leader ,follower,log_number)



def save_logs(filename, leader, follower, age):
    # Открываем файл для дозаписи
    with open(filename, 'a') as f:
        # Записываем позиции автомобилей
        f.write(f"{leader.position[0]}\t{leader.position[1]}\t{follower.position[0]}\t{follower.position[1]}\t{age}\n")



import matplotlib.pyplot as plt

def show_positions(filename):
    # Открываем файл с данными
    with open(filename, 'r') as f:
        # Читаем строки из файла
        lines = f.readlines()

    # Список для хранения позиций автомобилей
    positions = []
    # Список для хранения "возраста" логов
    ages = []

    # Перебираем строки из файла
    for line in lines:
        # Разбиваем строку на части, разделенные табуляцией
        parts = line.strip().split('\t')
        # Извлекаем позиции автомобилей
        leader_pos = (float(parts[0]), float(parts[1]))
        follower_pos = (float(parts[2]), float(parts[3]))
        # Добавляем позиции в список
        positions.append((leader_pos, follower_pos))
        # Извлекаем "возраст" лога
        age = int(parts[4])
        # Добавляем "возраст" в список
        ages.append(age)
    # Максимальный "возраст" лога
    max_age = max(ages)
    if(max_age == 0):
        max_age = 50

    # Перебираем позиции автомобилей
    for pos, age in zip(positions, ages):
        # Рассчитываем размер точки
        size = (max_age - age) / max_age * 50
        # Рисуем точку для позиции "лидера"
        plt.scatter(pos[0][0], pos[0][1], c='r', s=size)
        # Рисуем точку для позиции "следующего"
        plt.scatter(pos[1][0], pos[1][1], c='b', s=size)

    # Отображаем график
    plt.show()


# Инициализация объектов "лидер" и автопилот
leader = Vehicle((0, 0), 10, math.pi / 2  )
follower = Vehicle((0, 10), 0, 0)
autopilot = Autopilot(10)
filename = "positions.txt"
log_number = 0

with open(filename, 'w') as f:
        f.write('')
# Следование за "лидером"
autopilot.follow_leader_fuzzy(leader, follower)

# Выполняем итерации следования
while True:
    # Обновляем параметры лидера 
    update_leader_parameters(leader)
    # Выполняем следование
    autopilot.follow_leader_fuzzy(leader, follower)
    tick()
    # Лидер едет по спирали
    # leader.angle += math.pi / 180 * 15
    # leader.speed += 1
    print(leader.position)
    print(follower.position)
    show_positions(filename)
    time.sleep(0.1)

