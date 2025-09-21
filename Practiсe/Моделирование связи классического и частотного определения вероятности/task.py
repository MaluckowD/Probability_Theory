from itertools import product
from random import choices
import pandas as pd
import matplotlib.pyplot as plt

# Классическая вероятность для 5 монеток
ls = list(product(['О', 'Р'], repeat=5))
prob = {}
for combo in ls:
    count_o = combo.count('О')  # количество орлов
    prob[count_o] = prob.get(count_o, 0) + 1

N_all = len(ls)
for count in prob:
    prob[count] /= N_all

# Частотная вероятность
def coin_toss():
    return choices(['О', 'Р'], k=5)

N = 1_000_000
freq = {}
for _ in range(N):
    result = coin_toss()
    count_o = result.count('О')
    freq[count_o] = freq.get(count_o, 0) + 1

for count in freq:
    freq[count] /= N

# Сравнение
df = pd.DataFrame({
    "Вероятность": [prob.get(i, 0) for i in range(6)],
    "Частота": [freq.get(i, 0) for i in range(6)]
}, index=range(6))

df["Отклонение"] = abs(df["Вероятность"] - df["Частота"])

print("Количество орлов в 5 бросках:")
print(df)
df[['Вероятность', 'Частота']].plot(kind='bar', rot=0, figsize=(10, 6))
plt.title("Распределение количества орлов (5 бросков)")
plt.show()