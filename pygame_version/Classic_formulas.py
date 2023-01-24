import pygame
from pygame.color import THECOLORS
import math
from sys import exit


# Быстро считает до 7 знака, не багует, для более высоких точностей числа pi нужно просто подождать
# Программа зациклена while так, чтобы можно было после каждой симуляции нажимать 0,
# затем следующую цифру числа pi, которую хотите найти

class Block:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.vel_x = 0
        self.mass = 0
        self.x_min = 0
        self.x_max = 0

    def print_on_screen(self, screen, color: tuple):
        '''
        :param screen: Экран pygame
        :param color: Цвет выводимого прямоугольника
        :return: pygame.draw.rect(), рисующую прямоугольник в нужной позиции
        '''
        if self.x <= self.x_min:
            return pygame.draw.rect(screen, color, [self.x_min, self.y, self.width, self.width])
        elif self.x >= self.x_max:
            return pygame.draw.rect(screen, color, [self.x_max, self.y, self.width, self.width])
        else:
            return pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.width])

    def update_position(self) -> None:
        '''
        Прибавляет к координате скорость за единицу времени
        '''
        self.x += self.vel_x

    @staticmethod
    def collide(l_block, r_block) -> bool:
        '''
        :param l_block: Левый объект Block
        :param r_block: Правый объект Block
        :return: Выполнены условия столновения (один зашел за границы второго)
        '''
        return l_block.x + l_block.width >= r_block.x

    @staticmethod
    def bounce(l_block, r_block) -> None:
        '''
        Устанавливает объектам новые скорости после столкновения
        Используются формулы, выведенные из ЗСИ и ЗСЭ
        :param l_block: Левый объект Block
        :param r_block: Правый объект Block
        '''
        l_new_vel = (2 * r_block.vel_x * r_block.mass + l_block.mass * l_block.vel_x - r_block.mass * l_block.vel_x) / (l_block.mass + r_block.mass)
        r_new_vel = (2 * l_block.vel_x * l_block.mass + r_block.mass * r_block.vel_x - l_block.mass * r_block.vel_x) / (l_block.mass + r_block.mass)
        l_block.vel_x = l_new_vel
        r_block.vel_x = r_new_vel

    def wall_collide(self) -> bool:
        '''
        :return: Выполнено ли условие выхода за левый край экрана (стену)
        '''
        return self.x <= 0

    def reverse_vel(self) -> None:
        '''
        Изменяет скорость на противоположную
        '''
        self.vel_x *= -1


if __name__ == '__main__':
    pygame.init()

    # Параметры стартового окна
    HEIGHT = 1000
    WIDTH = 250
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Подсчет числа pi")
    font = pygame.font.SysFont('arial', 20)

    while True:
        stop_simulation = False

        # Некоторые переменные
        digits_pi = 0
        loops = 10000
        count_collisions = 0

        # Получение количества подсчитываемых цифр pi
        got_digits = False
        while not got_digits:
            pygame.time.delay(1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                     pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        digits_pi = (event.key - 48)
                        got_digits = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Объявление двух блоков
        block1 = Block()
        block1.width = 50
        block1.x = 300
        block1.y = WIDTH - block1.width
        block1.vel_x = 0
        block1.mass = 1
        block1.x_min = 0
        block1.x_max = 10000

        block2 = Block()
        block2.width = int(block1.width * math.log(digits_pi + 1, 2))
        block2.x = 500
        block2.y = WIDTH - block2.width
        block2.vel_x = -1 / loops
        block2.mass = pow(100, digits_pi - 1)
        block2.x_min = block1.width
        block2.x_max = block1.x_max

        while not stop_simulation:
            pygame.time.delay(1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        stop_simulation = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(THECOLORS['white'])

            text_left_1 = font.render(f"Отношение масс:  1 к 10^({2 * (digits_pi - 1)})", True, THECOLORS['black'])
            screen.blit(text_left_1, (20, 20))

            text_left_2 = font.render(f"Количество ударов: {count_collisions}", True, THECOLORS['black'])
            screen.blit(text_left_2, (20, 50))

            text_right_1 = font.render(f"Начальные скорости: v_1 = -1.0 м/с", True, THECOLORS['black'])
            screen.blit(text_right_1, (500, 20))

            text_right_2 = font.render(f"v_2 = 0.0 м/с", True, THECOLORS['black'])
            screen.blit(text_right_2, (698, 50))

            # Вывод итоговых значений
            if 0 <= block1.vel_x <= block2.vel_x:
                text_left_3 = font.render("Итог: pi = " + str(count_collisions / 10 ** (digits_pi - 1)), True, THECOLORS['black'])
                screen.blit(text_left_3, (20, 80))
                text_right_3 = font.render(f"Конечные скорости:", True, THECOLORS['black'])
                screen.blit(text_right_3, (500, 80))
                text_right_4 = font.render(f"v_1 = {round(block2.vel_x * loops, 8)} м/с", True, THECOLORS['black'])
                screen.blit(text_right_4, (698, 80))
                text_right_5 = font.render(f"v_2 = {round(block1.vel_x * loops, 8)} м/с", True, THECOLORS['black'])
                screen.blit(text_right_5, (698, 110))

            for i in range(loops):
                if Block.collide(block1, block2):
                    Block.bounce(block1, block2)
                    count_collisions += 1

                if block1.wall_collide():
                    count_collisions += 1
                    block1.reverse_vel()

                block1.update_position()
                block2.update_position()

            block1.print_on_screen(screen, THECOLORS['red'])
            block2.print_on_screen(screen, THECOLORS['orange'])

            pygame.display.update()
