import pygame
from pygame.color import THECOLORS
import math
import sys


# Быстро считает до 4 знака, далее возникает бага из-за недостаточной точности дробей в python
# Программа зациклена while так, чтобы можно было после каждой симуляции нажимать 0,
# затем следующую цифру числа pi, которую хотите найти


class Block:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.beta_x = 0
        self.mass = 0
        self.x_min = 0
        self.x_max = 0

        self.beta_koef = 1

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
        self.x += self.beta_x

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
        Высчитывает beta СО, в которой импульсы сталкивающихся тел равны и для каждого тела
        вызывает функцию, которая меняет его импульс
        :param l_block: Левый объект Block
        :param r_block: Правый объект Block
        '''
        a = (l_block.mass * r_block.beta_x + r_block.mass * l_block.beta_x)
        b = (l_block.mass + r_block.mass) * (1 + l_block.beta_x * r_block.beta_x)
        c = (l_block.mass * l_block.beta_x + r_block.mass * r_block.beta_x)
        beta_in_system = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        STO.bounce_in_inerc_sys(l_block, beta_in_system)
        STO.bounce_in_inerc_sys(r_block, beta_in_system)


    def wall_collide(self) -> bool:
        '''
        :return: Выполнено ли условие выхода за левый край экрана (стену)
        '''
        return self.x <= 0

    def reverse_beta(self) -> None:
        '''
        Изменяет скорость на противоположную
        '''
        self.beta_x *= -1


class STO:

    @staticmethod
    def bounce_in_inerc_sys(block: Block, beta_in_system: float) -> None:
        '''
        Переходит в инерционную СО, меняет импульс(скорость) тела на противоположный и переходит обратно
        '''
        block.beta_x = -(block.beta_x + beta_in_system) / (1 + block.beta_x * beta_in_system)
        block.beta_x = (block.beta_x - beta_in_system) / (1 - block.beta_x * beta_in_system)


if __name__ == '__main__':
    pygame.init()

    # Параметры стартового окна
    HEIGHT = 1000
    WIDTH = 250
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Подсчет числа pi в СТО")
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
                    sys.exit()

        if digits_pi >= 4: # увеличиваем частоту кадров для больших значений
            loops *= 10

        # Объявление двух блоков
        block1 = Block()
        block1.width = 50
        block1.x = 150
        block1.y = WIDTH - block1.width
        block1.beta_x = 0
        block1.mass = 1
        block1.x_min = 0
        block1.x_max = 10000

        block2 = Block()
        block2.width = int(block1.width * math.log(digits_pi + 1, 2))
        block2.x = 400
        block2.y = WIDTH - block2.width
        block2.beta_x = -1 / loops
        block2.mass = pow(100, digits_pi - 1)
        block2.x_min = block1.width
        block2.x_max = block1.x_max

        if digits_pi >= 4:
            block2.x = 220

        if digits_pi > 4:
            block1.beta_koef /= 100
            block2.beta_koef /= 100

        while not stop_simulation:
            pygame.time.delay(1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        stop_simulation = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(THECOLORS['white'])

            text_left_1 = font.render(f"Отношение масс:  1 к 10^({2 * (digits_pi - 1)})", True, THECOLORS['black'])
            screen.blit(text_left_1, (20, 20))

            text_left_2 = font.render(f"Количество ударов: {count_collisions}", True, THECOLORS['black'])
            screen.blit(text_left_2, (20, 50))

            text_right_1 = font.render(f"Начальные скорости: beta_1 = {-1 / loops}", True, THECOLORS['black'])
            screen.blit(text_right_1, (500, 20))

            text_right_2 = font.render(f"beta_2 = 0.0", True, THECOLORS['black'])
            screen.blit(text_right_2, (698, 50))

            # Вывод итоговых значений
            if 0 - 1e-7 <= block1.beta_x <= block2.beta_x:
                text_left_3 = font.render("Итог: pi = " + str(count_collisions / 10 ** (digits_pi - 1)), True,
                                          THECOLORS['black'])
                screen.blit(text_left_3, (20, 80))
                text_right_3 = font.render(f"Конечные скорости:", True, THECOLORS['black'])
                screen.blit(text_right_3, (500, 80))
                text_right_4 = font.render(f"beta_1 = {round(block2.beta_x, 8)} м/с", True, THECOLORS['black'])
                screen.blit(text_right_4, (698, 80))
                beta_2 = round(block1.beta_x, 8)
                text_right_5 = font.render(f"beta_2 = {abs(beta_2) if beta_2 > -1e-6 else beta_2} м/с", True, THECOLORS['black'])
                screen.blit(text_right_5, (698, 110))

            for i in range(loops):
                if Block.collide(block1, block2):
                    Block.bounce(block1, block2)
                    count_collisions += 1

                if block1.wall_collide():
                    count_collisions += 1
                    block1.reverse_beta()

                block1.update_position()
                block2.update_position()

            block1.print_on_screen(screen, THECOLORS['red'])
            block2.print_on_screen(screen, THECOLORS['orange'])

            pygame.display.update()
