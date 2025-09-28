import random
import matplotlib.pyplot as plt
import numpy as np

def monty_hall_simulation(num_trials=10000, change_choice=True):
    """
    Моделирование парадокса Монти Холла
    
    Parameters:
    num_trials - количество испытаний
    change_choice - менять ли выбор после открытия двери
    """
    wins = 0
    win_history = []
    
    for i in range(num_trials):
        # Создаем двери: 0 - коза, 1 - автомобиль
        doors = [0, 0, 1]
        random.shuffle(doors)
        
        # Игрок выбирает случайную дверь
        player_choice = random.randint(0, 2)
        
        # Ведущий открывает дверь с козой (не выбранную игроком)
        doors_to_open = [i for i in range(3) if i != player_choice and doors[i] == 0]
        host_opens = random.choice(doors_to_open)
        
        if change_choice:
            # Игрок меняет выбор на оставшуюся дверь
            new_choice = [i for i in range(3) if i != player_choice and i != host_opens][0]
            final_choice = new_choice
        else:
            # Игрок не меняет выбор
            final_choice = player_choice
        
        # Проверяем результат
        if doors[final_choice] == 1:
            wins += 1
        
        # Сохраняем историю побед для графика
        win_history.append(wins / (i + 1))
    
    return wins / num_trials, win_history

np.random.seed(42)
random.seed(42)

trials = 10000
prob_change, history_change = monty_hall_simulation(trials, change_choice=True)
prob_no_change, history_no_change = monty_hall_simulation(trials, change_choice=False)

print(f"Вероятность выигрыша при смене выбора: {prob_change:.4f}")
print(f"Вероятность выигрыша без смены выбора: {prob_no_change:.4f}")
print(f"Теоретическая вероятность при смене: 2/3 = {2/3:.4f}")
print(f"Теоретическая вероятность без смены: 1/3 = {1/3:.4f}")

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(history_change, 'b-', alpha=0.7, label='Со сменой выбора')
plt.plot(history_no_change, 'r-', alpha=0.7, label='Без смены выбора')
plt.axhline(y=2/3, color='blue', linestyle='--', alpha=0.5, label='Теор. 2/3')
plt.axhline(y=1/3, color='red', linestyle='--', alpha=0.5, label='Теор. 1/3')
plt.xlabel('Количество испытаний')
plt.ylabel('Вероятность выигрыша')
plt.title('Сходимость вероятностей выигрыша')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
strategies = ['Со сменой', 'Без смены']
probabilities = [prob_change, prob_no_change]
theoretical = [2/3, 1/3]

x = np.arange(len(strategies))
width = 0.35

plt.bar(x - width/2, probabilities, width, label='Экспериментальные', alpha=0.7)
plt.bar(x + width/2, theoretical, width, label='Теоретические', alpha=0.7)

plt.xlabel('Стратегия')
plt.ylabel('Вероятность')
plt.title('Сравнение экспериментальных и теоретических вероятностей')
plt.xticks(x, strategies)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Дополнительная статистика
print("\nДополнительная статистика:")
print(f"Улучшение при смене выбора: {prob_change/prob_no_change:.2f} раз")
print(f"Абсолютное улучшение: {(prob_change - prob_no_change)*100:.1f}%")

def extended_monty_hall(num_doors=3, num_trials=10000):
    """
    Расширенная версия для разного количества дверей
    """
    results_change = []
    results_no_change = []
    
    for doors_count in range(3, num_doors + 1):
        wins_change = 0
        wins_no_change = 0
        
        for _ in range(num_trials):
            doors = [0] * doors_count
            car_position = random.randint(0, doors_count - 1)
            doors[car_position] = 1
            
            # Игрок выбирает дверь
            player_choice = random.randint(0, doors_count - 1)
            
            # Ведущий открывает все двери с козами кроме одной
            doors_available_to_open = [i for i in range(doors_count) 
                                     if i != player_choice and doors[i] == 0]
            # Оставляем одну дверь закрытой (кроме выбранной игроком)
            host_opens = random.sample(doors_available_to_open, len(doors_available_to_open) - 1)
            
            remaining_doors = [i for i in range(doors_count) 
                             if i != player_choice and i not in host_opens]
            new_choice = remaining_doors[0]
            
            if doors[new_choice] == 1:
                wins_change += 1
            if doors[player_choice] == 1:
                wins_no_change += 1
        
        results_change.append(wins_change / num_trials)
        results_no_change.append(wins_no_change / num_trials)
    
    return results_change, results_no_change


max_doors = 10
change_probs, no_change_probs = extended_monty_hall(max_doors, 5000)

plt.figure(figsize=(10, 6))
doors_range = range(3, max_doors + 1)

plt.plot(doors_range, change_probs, 'bo-', label='Со сменой выбора')
plt.plot(doors_range, no_change_probs, 'ro-', label='Без смены выбора')

theoretical_change = [1 - 1/n for n in doors_range]  # P(win) = 1 - 1/n
theoretical_no_change = [1/n for n in doors_range]   # P(win) = 1/n

plt.plot(doors_range, theoretical_change, 'b--', alpha=0.5, label='Теор. со сменой')
plt.plot(doors_range, theoretical_no_change, 'r--', alpha=0.5, label='Теор. без смены')

plt.xlabel('Количество дверей')
plt.ylabel('Вероятность выигрыша')
plt.title('Парадокс Монти Холла для разного количества дверей')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()