
## 📚 Лекции

# Задача 1: Бросание монеты на шахматную доску

### Постановка задачи

**Формулировка:** Монета радиуса \( R \) бросается на бесконечную шахматную доску с размером клетки \( S \). Нужно найти вероятность того, что монета полностью попадет внутрь одной клетки (не пересечет границы).

## 💻 Практика

### Код для Jupyter Notebook

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# Параметры эксперимента
N = 1000  # число бросков (можно менять)
S = 4.0   # размер клетки
R = 1.0   # радиус монеты

# Теоретическая вероятность
p_theor = ((S - 2*R) / S)**2 if 2*R <= S else .0

# Генерация случайных бросков
np.random.seed(42)  # для воспроизводимости результатов
x_center = np.random.uniform(0, S, N)
y_center = np.random.uniform(0, S, N)

# Проверка: полностью ли монета внутри клетки?
inside_cell = ((x_center > R) & (x_center < S - R) & 
               (y_center > R) & (y_center < S - R))

# Экспериментальная вероятность
p_exp = np.mean(inside_cell)

# Визуализация
plt.figure(figsize=(12, 10))

# Создаем шахматную доску
grid_size = max(3, min(10, int(np.sqrt(N) / 2) + 1))
total_size = grid_size * S

for i in range(grid_size):
    for j in range(grid_size):
        color = 'white' if (i + j) % 2 == 0 else 'lightgray'
        plt.gca().add_patch(Rectangle((i*S, j*S), S, S, 
                            facecolor=color, edgecolor='black', alpha=0.7))

# Распределяем броски по сетке
x_display = np.zeros(N)
y_display = np.zeros(N)

for i in range(N):
    cell_x = i % grid_size
    cell_y = i // grid_size
    x_display[i] = x_center[i] + cell_x * S
    y_display[i] = y_center[i] + cell_y * S

# Отображаем все броски
colors = ['green' if inside else 'red' for inside in inside_cell]
alphas = np.linspace(0.3, 0.8, N)

for i in range(N):
    circle = Circle((x_display[i], y_display[i]), R, 
                   fill=True, color=colors[i], alpha=alphas[i])
    plt.gca().add_patch(circle)
    plt.plot(x_display[i], y_display[i], 'ko', markersize=1, alpha=0.5)

# Статистика
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
plt.xlim(-1, total_size + 8)
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

# Вывод статистики
print("="*50)
print("СТАТИСТИКА ЭКСПЕРИМЕНТА")
print("="*50)
print(f"Теоретическая вероятность: {p_theor:.6f}")
print(f"Экспериментальная вероятность: {p_exp:.6f}")
print(f"Абсолютная ошибка: {abs(p_exp - p_theor):.6f}")
if p_theor > 0:
    print(f"Относительная ошибка: {abs(p_exp - p_theor)/p_theor*100:.2f}%")
    print(f"Успешных бросков: {np.sum(inside_cell)}/{N}")
```