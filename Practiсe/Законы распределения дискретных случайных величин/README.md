# Законы распределения дискретных случайных величин

**Формулировка:**

В службу поддержки приходит в среднем (\lambda=4) письма в час. (X) — число писем за 1 час.

Закон:
<img src="https://latex.codecogs.com/svg.image?P(X=k)=e^{-4}\frac{4^k}{k!}" />
(в расчётах взял
<img src="https://latex.codecogs.com/svg.image?k=0\dots14" /> для таблицы).

Результаты:

- <img src="https://latex.codecogs.com/svg.image?E(X)=\lambda=4" />
- <img src="https://latex.codecogs.com/svg.image?\mathrm{Var}(X)=\lambda=4" />
- <img src="https://latex.codecogs.com/svg.image?\sigma=2.0" />
- мод(ы): при целом <img src="https://latex.codecogs.com/svg.image?\lambda" />
  две моды: <img src="https://latex.codecogs.com/svg.image?\lambda-1=3" />
  и <img src="https://latex.codecogs.com/svg.image?\lambda=4" />  
  в общем для нецелого <img src="https://latex.codecogs.com/svg.image?\lfloor\lambda\rfloor" />.

Таблица и график распределения

![alt text](image.png)

### [Решение](task.py)
