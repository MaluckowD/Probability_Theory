import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.colors as mcolors

# Параметры эксперимента
N = 100  # число бросков (можно менять)
S = 4.0  # размер клетки
R = 1.0  # радиус монеты

# Теоретическая вероятность
p_theor = ((S - 2*R) / S)**2 if 2*R <= S else 0.0

# Генерация случайных бросков
x_center = np.random.uniform(0, S, N)
y_center = np.random.uniform(0, S, N)

# Проверка: полностью ли монета внутри клетки?
inside_cell = ((x_center > R) & (x_center < S - R) & 
               (y_center > R) & (y_center < S - R))

# Экспериментальная вероятность
p_exp = np.mean(inside_cell)

# Создаем фигуру
plt.figure(figsize=(14, 10))

# Создаем шахматную доску (масштабируем количество клеток в зависимости от N)
grid_size = max(3, min(10, int(np.sqrt(N) / 2) + 1))  # адаптивный размер сетки
total_size = grid_size * S

# Рисуем шахматную доску
for i in range(grid_size):
    for j in range(grid_size):
        color = 'white' if (i + j) % 2 == 0 else 'lightgray'
        plt.gca().add_patch(Rectangle((i*S, j*S), S, S, 
                            facecolor=color, edgecolor='black', alpha=0.7))

# Распределяем все броски по сетке
x_display = np.zeros(N)
y_display = np.zeros(N)

for i in range(N):
    cell_x = i % grid_size
    cell_y = i // grid_size
    x_display[i] = x_center[i] + cell_x * S
    y_display[i] = y_center[i] + cell_y * S

# Отображаем все броски
colors = ['green' if inside else 'red' for inside in inside_cell]
alphas = np.linspace(0.3, 0.8, N)  # разная прозрачность для лучшей видимости

for i in range(N):
    circle = Circle((x_display[i], y_display[i]), R, 
                   fill=True, color=colors[i], alpha=alphas[i])
    plt.gca().add_patch(circle)
    # Центр монеты
    plt.plot(x_display[i], y_display[i], 'ko', markersize=1, alpha=0.5)

# Статистика на графике
stats_text = f'''Параметры:
Размер клетки: S = {S}
Радиус монеты: R = {R}
Всего бросков: N = {N}

Теоретическая вероятность: {p_theor:.4f}
Экспериментальная вероятность: {p_exp:.4f}
Относительная ошибка: {abs(p_exp - p_theor)/p_theor*100:.1f}%''' if p_theor > 0 else f'''Параметры:
Размер клетки: S = {S}
Радиус монеты: R = {R}
Всего бросков: N = {N}

Теоретическая вероятность: 0.0000
Экспериментальная вероятность: {p_exp:.4f}'''

plt.text(total_size + 1, total_size/2, stats_text, 
         bbox=dict(facecolor='white', alpha=0.8), fontsize=10,
         verticalalignment='center')

plt.title(f'Бросание монеты на шахматную доску (все {N} бросков)')
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(-1, total_size + 5)
plt.ylim(-1, total_size + 1)
plt.grid(True, alpha=0.3)
plt.gca().set_aspect('equal')

# Легенда
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
               markersize=10, label='Внутри клетки', alpha=0.7),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
               markersize=10, label='Пересекает границу', alpha=0.7)
]
plt.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.show()

# Дополнительная статистика в консоли
print("="*50)
print("СТАТИСТИКА ЭКСПЕРИМЕНТА")
print("="*50)
print(f"Размер клетки (S): {S}")
print(f"Радиус монеты (R): {R}")
print(f"Отношение R/S: {R/S:.3f}")
print(f"Количество бросков (N): {N}")
print(f"Теоретическая вероятность: {p_theor:.6f}")
print(f"Экспериментальная вероятность: {p_exp:.6f}")
print(f"Абсолютная ошибка: {abs(p_exp - p_theor):.6f}")

if p_theor > 0:
    print(f"Относительная ошибка: {abs(p_exp - p_theor)/p_theor*100:.2f}%")
    print(f"Количество успешных бросков: {np.sum(inside_cell)}")
    print(f"Количество неудачных бросков: {N - np.sum(inside_cell)}")
else:
    print("Теоретическая вероятность равна 0 (монета всегда пересекает границы)")