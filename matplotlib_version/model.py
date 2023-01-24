import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.pyplot import *
from fractions import Fraction


# Ввод и вывод программы через консоль


# Волшебная команда для анимированных графиков
matplotlib.use("TkAgg")


def init_rectangles():
    l_rectangle.xy = (5, 5)
    r_rectangle.xy = (5, 5)
    ax.add_patch(l_rectangle)
    ax.add_patch(r_rectangle)
    return l_rectangle, r_rectangle


class Block:
    '''
    Класс прямоугольных блоков
    '''
    def __init__(self, position: Fraction, mass: int):
        '''
        :param position: начальная координата х
        :param mass: масса блока
        '''
        self.x = position  # Координата х
        self.m = mass  # Масса блока
        self.v = Fraction(0, 1)  # Скорость блока по х

    def wall_collide(self) -> None:
        """
        Упругое столкновение со стеной
        """
        self.v = -1 * self.v

    @staticmethod
    def block_collide(l_block, r_block) -> None:
        """
        Метод столкновения двух блоков, изменяет их скорости
        Использует формулы, выведенные из ЗСИ и ЗСЭ
        """
        v_a = l_block.v
        v_b = r_block.v
        m_a = l_block.m
        m_b = r_block.m
        v_a_new = (2 * v_b * m_b + m_a * v_a - m_b * v_a) / (m_a + m_b)
        v_b_new = (2 * v_a * m_a + m_b * v_b - m_a * v_b) / (m_a + m_b)
        l_block.v = v_a_new
        r_block.v = v_b_new

    @staticmethod
    def update(l_block, r_block) -> bool:
        """
        Обновляет координаты блоков, добавляя к ним (Скорость * time_to_collide)
        """
        t = Block.time_to_collide(l_block, r_block)
        if t == float("inf"):
            l_block.x = l_block.x + l_block.v
            r_block.x = r_block.x + r_block.v
            return False
        l_block.x = l_block.x + t * l_block.v
        r_block.x = r_block.x + t * r_block.v
        return True

    @staticmethod
    def time_to_collide(l_block, r_block) -> float | Fraction:
        """
        Считает время до ближайшего столкновения
        """
        # Оба блока движутся вправо, но правый быстрее (больше столкновения невозможны)
        if r_block.v >= l_block.v >= 0:
            return float("inf")

        # Блоки движутся навстречу друг другу
        elif l_block.v >= 0 >= r_block.v:
            return Fraction(r_block.x - l_block.x, l_block.v - r_block.v)

        # Левый блок ударяется о стену
        elif (r_block.v >= 0 and l_block.v < 0) or (l_block.v <= r_block.v < 0):
            return Fraction(-l_block.x, l_block.v)

        # Левый блок около стены
        elif l_block.x == 0:
            # Правый блок быстрее левого после соударения того со стеной
            if r_block.v >= abs(l_block.v):
                return float("inf")
            # Правый блок достижим для левого
            else:
                return Fraction(r_block.x, abs(l_block.v) - r_block.v)

        # Блоки движутся влево, но правый быстрее,
        # поэтому берем минимум из времени столкновения блоков и со стеной
        else:
            return min(Fraction(-l_block.x, l_block.v),
                       Fraction(r_block.x - l_block.x, l_block.v - r_block.v))


continue_process = True


def execute_collision() -> None:
    global blockA, blockB, counter
    # Столкновение не около стены
    if blockA.x == blockB.x != 0:
        Block.block_collide(blockA, blockB)
        counter += 1

    # Столкновение левого блока со стеной
    elif blockA.x == 0 != blockB.x:
        blockA.wall_collide()
        counter += 1

    # Левый блок зажат между стеной и правым
    elif blockA.x == blockB.x == 0:
        blockA.wall_collide()
        blockB.wall_collide()
        counter += 2


def process(_) -> tuple:
    global blockA, blockB, counter, l_rectangle, r_rectangle, continue_process, size, n, ax

    if continue_process:
        print(counter)

    prev = continue_process
    continue_process = Block.update(blockA, blockB)

    if prev != continue_process:
        print(f"pi = {counter / 10 ** n}\n")

    l_rectangle.xy = (blockA.x, 0)
    r_rectangle.xy = (blockB.x + size, 0)

    # Обрабатываем столкновение
    execute_collision()

    # Уменьшаем длину Fraction
    blockA.x = blockA.x.limit_denominator(2 ** 32)
    blockB.x = blockB.x.limit_denominator(2 ** 32)
    blockA.v = blockA.v.limit_denominator(2 ** 32)
    blockB.v = blockB.v.limit_denominator(2 ** 32)

    return l_rectangle, r_rectangle


# Объявляем блоки
# Масса левого блока 1 кг
blockA = Block(Fraction(2, 1), 1)
blockB = Block(Fraction(4, 1), 1)
blockB.v = Fraction(-1, 100)

# Масса блока B является 100^n кг, так как количество цифр pi - это (n + 1)
n = int(input("Print the number of pi you need: "))
blockB.m = 100 ** n

if n == 0:
    k = 300
    blockB.v = Fraction(-1, 5)
elif n == 1:
    k = 50
    blockB.v = Fraction(-1, 30)
elif n == 2:
    k = 20
    blockB.v = Fraction(-1, 800)
else:
    k = 1
    blockB.v = Fraction(-1, 1000)

# (Глобальная переменная) Счетчик ударов
counter = 0

# Создаем график
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

# Создаем прямоугольники на графике
size = 1.5
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
ax.set_title(f"Столкновение блоков. Отношение масс: 1 : 1" + "0" * 2 * n)
l_rectangle = plt.Rectangle((5, -5), size, size)
r_rectangle = plt.Rectangle((5, -5), 1.1 * size, 1.1 * size)

# Запуск анимированного графика
animation = animation.FuncAnimation(fig, process, init_func=init_rectangles, interval=k, blit=True)
plt.show()
