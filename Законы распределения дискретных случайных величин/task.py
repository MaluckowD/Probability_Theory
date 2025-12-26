# Poisson(λ=4): корректный вывод таблицы и график с линиями
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

lam = 4

# k = 0..14
k_max = 14
k = np.arange(0, k_max + 1)
pmf = [math.exp(-lam) * lam**i / math.factorial(i) for i in k]
pmf_tail = 1.0 - sum(pmf)

# Построим аккуратную таблицу (один раз)
df = pd.DataFrame({
    "k": list(k) + [f">{k_max}"],
    "P(X=k)": pmf + [pmf_tail]
})
pd.set_option("display.float_format", "{:.6f}".format)
print("Теоретическое распределение Пуассона (λ=4):")
print(df.to_string(index=False))

# Теоретические характеристики
E = lam
Var = lam
sigma = math.sqrt(Var)
modes = [int(lam)-1, int(lam)] if lam == int(lam) else [math.floor(lam)]
print(f"\nE(X) = {E}, Var(X) = {Var}, sigma = {sigma:.6f}, моды = {modes}")

# Многоугольник распределения (точки, соединённые линией)
plt.figure(figsize=(8,4))
plt.plot(k, pmf, marker='o')       # линия + точки
plt.title("Многоугольник распределения Пуассона (λ=4)")
plt.xlabel("k")
plt.ylabel("P(X=k)")
plt.xticks(k)
plt.grid(False)
plt.tight_layout()
plt.show()

# --- Моделирование ---
n_sim = 200_000
rng = np.random.default_rng(42)
samples = rng.poisson(lam, size=n_sim)

# Эмпирическая таблица (k=0..14 и хвост)
emp_freqs = [np.mean(samples == i) for i in k]
emp_tail = np.mean(samples > k_max)

df_compare = pd.DataFrame({
    "k": list(k) + [f">{k_max}"],
    "Empirical P(X=k)": emp_freqs + [emp_tail],
    "Theoretical P(X=k)": pmf + [pmf_tail]
})
print("\nСравнение эмпирического и теоретического распределений:")
print(df_compare.to_string(index=False, float_format="{:.6f}".format))

# Выборочные моменты
E_emp = samples.mean()
Var_emp = samples.var()
sigma_emp = math.sqrt(Var_emp)
print(f"\nМоделирование (n={n_sim}): Выборочное E = {E_emp:.6f}, Var = {Var_emp:.6f}, sigma = {sigma_emp:.6f}")

# Гистограмма + теоретическая линия (соединённые точки)
plt.figure(figsize=(8,4))
plt.hist(samples, bins=np.arange(-0.5, k_max+1.5, 1), density=True, alpha=0.6, label="Эмпирические")
plt.plot(k, pmf, marker='o', label="Теоретические P(X=k)")
plt.title("Гистограмма выборки и теоретический PMF (λ=4)")
plt.xlabel("k")
plt.ylabel("Относительная частота / вероятность")
plt.legend()
plt.tight_layout()
plt.show()
