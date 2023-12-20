import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def plot_with_mark(value):
    # Создание данных для графика
    x = np.linspace(0, 63, 100)
    y = np.zeros_like(x)

    # Создание градиента от зеленого до красного
    colors = mcolors.LinearSegmentedColormap.from_list('g_to_r', ['green', 'red'])

    # Построение графика
    plt.figure(figsize=(8, 2))
    plt.scatter(x, y,c=x, cmap=colors, s=100)

    tick_values = [0, 22, 36, 63]

    plt.xticks(tick_values)
    plt.yticks([])
    # Установка пределов оси X
    plt.xlim(0, 63)
    plt.title('Шкала тревожности Бекка')
    plt.axvline(x=value, color='black', linestyle='--')  # Размещение вертикальной полоски
    # Сохранение графика в виде изображения
    plt.savefig('your.png', bbox_inches='tight', pad_inches=0)

    # Показать график на экране (необязательно)
    plt.show()

plot_with_mark(42)