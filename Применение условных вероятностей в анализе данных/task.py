import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Основная информация о данных
print("Размер данных:", df.shape)
print("\nПервые 5 строк:")
print(df.head())

print("\nИнформация о столбцах:")
print(df.info())

print("\nОсновные статистики:")
print(df.describe())

# Функция для вычисления условной вероятности
def conditional_probability(data, condition_col, condition_val, target_col, target_val=1):
    """
    Вычисляет P(target_col = target_val | condition_col = condition_val)
    """
    subset = data[data[condition_col] == condition_val]
    if len(subset) == 0:
        return 0
    return (subset[target_col] == target_val).mean()

# Анализ выживаемости по классу каюты
print("=" * 60)
print("АНАЛИЗ ВЫЖИВАЕМОСТИ ПО КЛАССУ КАЮТЫ")
print("=" * 60)

# Условные вероятности выживания по классам
for pclass in sorted(df['Pclass'].unique()):
    prob = conditional_probability(df, 'Pclass', pclass, 'Survived')
    count = len(df[df['Pclass'] == pclass])
    survived_count = len(df[(df['Pclass'] == pclass) & (df['Survived'] == 1)])
    print(f"P(Выжил | Класс {pclass}) = {prob:.3f} "
          f"({survived_count}/{count} пассажиров)")

# Анализ выживаемости по полу
print("\n" + "=" * 60)
print("АНАЛИЗ ВЫЖИВАЕМОСТИ ПО ПОЛУ")
print("=" * 60)

for sex in df['Sex'].unique():
    prob = conditional_probability(df, 'Sex', sex, 'Survived')
    count = len(df[df['Sex'] == sex])
    survived_count = len(df[(df['Sex'] == sex) & (df['Survived'] == 1)])
    print(f"P(Выжил | Пол {sex}) = {prob:.3f} "
          f"({survived_count}/{count} пассажиров)")

# ФОРМУЛА ПОЛНОЙ ВЕРОЯТНОСТИ
print("\n" + "=" * 60)
print("ФОРМУЛА ПОЛНОЙ ВЕРОЯТНОСТИ:")
print("P(Survived) = Σ P(Survived|Pclass=i) * P(Pclass=i)")
print("=" * 60)

total_prob = 0
prob_details = []

for pclass in sorted(df['Pclass'].unique()):
    # P(Pclass = i)
    P_class = (df['Pclass'] == pclass).mean()
    # P(Survived | Pclass = i)
    P_survived_given_class = conditional_probability(df, 'Pclass', pclass, 'Survived')
    
    # Вклад каждого класса
    contribution = P_survived_given_class * P_class
    total_prob += contribution
    
    prob_details.append({
        'Class': pclass,
        'P(Class)': round(P_class, 3),
        'P(Survived|Class)': round(P_survived_given_class, 3),
        'Вклад': round(contribution, 3)
    })

# Создаем DataFrame для наглядности
prob_df = pd.DataFrame(prob_details)
print(prob_df)

print(f"\nОбщая вероятность выживания, рассчитанная по формуле полной вероятности: {total_prob:.3f}")
print(f"Общая вероятность выживания, рассчитанная напрямую из данных: {df['Survived'].mean():.3f}")

# ТЕОРЕМА БАЙЕСА
print("\n" + "=" * 60)
print("ТЕОРЕМА БАЙЕСА:")
print("P(Pclass | Survived) = [P(Survived | Pclass) × P(Pclass)] / P(Survived)")
print("=" * 60)

# P(Survived) - знаменатель
P_S = df['Survived'].mean()

bayes_results = []

for pclass in sorted(df['Pclass'].unique()):
    # P(Pclass) - априорная вероятность
    P_A = (df['Pclass'] == pclass).mean()
    # P(Survived | Pclass) - правдоподобие
    P_B_given_A = conditional_probability(df, 'Pclass', pclass, 'Survived')
    
    # Применяем теорему Байеса
    P_A_given_B = (P_B_given_A * P_A) / P_S
    
    bayes_results.append({
        'Class': pclass,
        'P(Class)': round(P_A, 3),
        'P(Survived|Class)': round(P_B_given_A, 3),
        'P(Class|Survived)': round(P_A_given_B, 3)
    })

# Создаем DataFrame
bayes_df = pd.DataFrame(bayes_results)
print("Результаты применения теоремы Байеса:")
print(bayes_df)

# Визуализация
plt.figure(figsize=(15, 5))

# График 1: Условные вероятности выживания
plt.subplot(1, 3, 1)
sns.barplot(data=prob_df, x='Class', y='P(Survived|Class)')
plt.title('Условная вероятность выживания по классам')
plt.ylabel('P(Выжил | Класс)')

# График 2: Распределение классов среди всех пассажиров
plt.subplot(1, 3, 2)
sns.barplot(data=prob_df, x='Class', y='P(Class)')
plt.title('Распределение классов среди всех пассажиров')
plt.ylabel('Доля пассажиров')

# График 3: Распределение классов среди выживших (Байес)
plt.subplot(1, 3, 3)
sns.barplot(data=bayes_df, x='Class', y='P(Class|Survived)')
plt.title('Распределение классов среди выживших\n(теорема Байеса)')
plt.ylabel('P(Класс | Выжил)')

plt.tight_layout()
plt.show()

# Дополнительный анализ: выживаемость по полу и классу
print("\n" + "=" * 60)
print("ДЕТАЛИЗИРОВАННЫЙ АНАЛИЗ: ВЫЖИВАЕМОСТЬ ПО ПОЛУ И КЛАССУ")
print("=" * 60)

for sex in df['Sex'].unique():
    for pclass in sorted(df['Pclass'].unique()):
        subset = df[(df['Sex'] == sex) & (df['Pclass'] == pclass)]
        if len(subset) > 0:
            prob = subset['Survived'].mean()
            count = len(subset)
            survived_count = subset['Survived'].sum()
            print(f"P(Выжил | Пол {sex}, Класс {pclass}) = {prob:.3f} "
                  f"({survived_count}/{count} пассажиров)")

# Сводная таблица выживаемости
pivot_table = pd.pivot_table(df, 
                            values='Survived', 
                            index='Pclass', 
                            columns='Sex', 
                            aggfunc=['mean', 'count'])
print("\nСводная таблица выживаемости:")
print(pivot_table)