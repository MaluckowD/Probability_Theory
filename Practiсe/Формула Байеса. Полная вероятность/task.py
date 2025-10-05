import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb
import random

total_ways = comb(20, 3, exact=True)

P_H = [
    comb(15, 0, exact=True) * comb(5, 3, exact=True) / total_ways,
    comb(15, 1, exact=True) * comb(5, 2, exact=True) / total_ways,
    comb(15, 2, exact=True) * comb(5, 1, exact=True) / total_ways,
    comb(15, 3, exact=True) * comb(5, 0, exact=True) / total_ways
]

P_B_given_H = [(6 + k) / 10 for k in range(4)]

P_B_total = sum(P_H[k] * P_B_given_H[k] for k in range(4))

def simulate():
    urn1 = [0] * 15 + [1] * 5
    urn2 = [0] * 6 + [1] * 1
    random.shuffle(urn1)
    transferred = urn1[:3]
    urn2.extend(transferred)
    chosen = random.choice(urn2)
    return 1 if chosen == 0 else 0

np.random.seed(42)
num_trials = 100000
results = [simulate() for _ in range(num_trials)]
simulated_prob = np.mean(results)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

k_values = np.arange(4)
ax1.bar(k_values, P_H, color='skyblue', edgecolor='navy', alpha=0.7)
ax1.set_xlabel('Число белых шаров, переложенных из 1-й урны (k)')
ax1.set_ylabel('Вероятность P(H_k)')
ax1.set_title('Распределение гипотез о переложенных шарах')
ax1.set_xticks(k_values)
for i, v in enumerate(P_H):
    ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')

ax2.bar(k_values, P_B_given_H, color='lightgreen', edgecolor='green', alpha=0.7)
ax2.set_xlabel('Число белых шаров, переложенных из 1-й урны (k)')
ax2.set_ylabel('P(Белый | H_k)')
ax2.set_title('Условная вероятность вынуть белый шар\nиз 2-й урны после перекладывания')
ax2.set_xticks(k_values)
for i, v in enumerate(P_B_given_H):
    ax2.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom')

contributions = [P_H[k] * P_B_given_H[k] for k in range(4)]
ax3.bar(k_values, contributions, color='orange', edgecolor='darkorange', alpha=0.7)
ax3.set_xlabel('Число белых шаров, переложенных из 1-й урны (k)')
ax3.set_ylabel('Вклад в P(Белый)')
ax3.set_title('Вклад каждой гипотезы в общую вероятность')
ax3.set_xticks(k_values)
for i, v in enumerate(contributions):
    ax3.text(i, v + 0.005, f'{v:.3f}', ha='center', va='bottom')

methods = ['Теоретическая', 'Смоделированная']
probabilities = [P_B_total, simulated_prob]
colors = ['red', 'blue']

bars = ax4.bar(methods, probabilities, color=colors, alpha=0.7, edgecolor='black')
ax4.set_ylabel('Вероятность')
ax4.set_title('Сравнение теоретической и смоделированной вероятности')
ax4.set_ylim(0, 1)

for bar, prob in zip(bars, probabilities):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{prob:.6f}', ha='center', va='bottom')

fig.suptitle('Вероятность вынуть белый шар из 2-й урны после перекладывания 3-х шаров из 1-й урны', 
             fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

print(f"Теоретическая вероятность: {P_B_total:.6f} ({P_B_total*100:.2f}%)")
print(f"Смоделированная вероятность: {simulated_prob:.6f} ({simulated_prob*100:.2f}%)")
print(f"Абсолютная ошибка: {abs(P_B_total - simulated_prob):.6f}")