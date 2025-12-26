import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rv_continuous
from scipy import integrate

class CustomDistribution(rv_continuous):
    def __init__(self, a, b):
        super().__init__(a=a, b=b, name='custom_dist')
    
    def _pdf(self, x):
        """Плотность распределения"""
        result = np.zeros_like(x)
        result[(x >= self.a) & (x <= self.b)] = -2 * x / 9 + 8/9
        return result
    
    def _cdf(self, x):
        "Функция распределения"
        result = np.zeros_like(x)
        result[x < 1] = 0
        result[(x >= self.a) & (x <= self.b)] = - x ** 2 / 9 +  8 * x / 9 - 7/9
        result[x > 4] = 1
        return result
    
    # def _ppf(self, q):
    #     """Обратная функция распределения (квантильная функция)"""
    #     return (15 * q + 1) ** 0.25
    
a, b = 1.0, 4.0
custom_dist = CustomDistribution(a, b) # создаем экземпляр распределения

# np.random.seed(42)
sample = custom_dist.rvs(size=10000) # генерация выборки

print(f"Размер выборки: {len(sample)}")
print(f"Первые 10 значений: {sample[:10]}")

x_test = np.linspace(a - 0.5, b + 0.5, 100)
pdf_values = custom_dist.pdf(x_test)
cdf_values = custom_dist.cdf(x_test)

print("Проверка нормировки плотности:")
integral, error = integrate.quad(custom_dist.pdf, a, b)
print(f"f(x)dx на [{a}, {b}] = {integral:.6f} (ошибка: {error:.2e})")

print("\nПроверка в граничных точках:")
print(f"F({a}) = {custom_dist.cdf(a):.6f}")
print(f"F({b}) = {custom_dist.cdf(b):.6f}")

# Вычисление числовых характеристик
print("ЧИСЛОВЫЕ ХАРАКТЕРИСТИКИ".center(50, '*'))
print(f"Математическое ожидание: {custom_dist.mean():.4f}")
print(f"Медиана: {custom_dist.median():4f}")
print(f"Дисперсия: {custom_dist.var():.4f}")
print(f"Стандартное отклонение: {custom_dist.std():.4f}")
print("Статистики (среднее, дисперсия, асимметрия, эксцесс):",
      *custom_dist.stats(moments='mvsk'), sep='\n\t')

# Квантили
print(f"25%-квантиль: {custom_dist.ppf(0.8):.4f}")
print(f"75%-квантиль: {custom_dist.ppf(0.75):.4f}")
