import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle


def rhombus_mc(size):
    a = 10

    square = Rectangle((0, 0), a, a)

    rhombus = np.array([
        (a/2, 0),
        (a, a/2),
        (a/2, a),
        (0, a/2)
    ])

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(square)
    ax.add_patch(Polygon(rhombus, color='lightcoral'))

    X = np.random.uniform(0, a, size)
    Y = np.random.uniform(0, a, size)
    ax.scatter(X, Y, s=8, c='black')

    inside = np.sum(np.abs(X - a/2) + np.abs(Y - a/2) <= a/2)

    P_exp = inside / size
    P_theory = 0.5

    plt.axis('equal')
    plt.show()

    print(f"Экспериментальная вероятность: {P_exp:.4f}")
    print(f"Теоретическая вероятность:     {P_theory:.4f}")

rhombus_mc(5)