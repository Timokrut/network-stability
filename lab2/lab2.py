from collections import deque
from math import ceil, comb
from random import random, sample, seed

import matplotlib.pyplot as plt


VERTICES = [1, 2, 3, 4, 5, 6]
EDGES = [
    (1, 5),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (2, 6),
    (3, 6),
    (5, 6),
]

START = 4
TARGET = 5
EPS = 0.01

L_MIN = 1  # Есть прямое ребро 4-5.
L_MAX = 6  # 8 - 2 = 6 // Чтобы разорвать связь, нужно убрать хотя бы два ребра.


def has_path(edges, start, target):
    adj = {v: [] for v in VERTICES}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = {start}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        if v == target:
            return True
        for nb in adj[v]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return False


def formula_probability(p):
    return p + p**3 + p**4 - 2*p**5 - 4*p**6 + 6*p**7 - 2*p**8


def simulate(p, n, fast=False):
    # Этапы 1 и 2. Каждое ребро независимо появляется с вероятностью p.
    successes = 0
    for _ in range(n):
        edges = [edge for edge in EDGES if random() < p]
        if fast and len(edges) < L_MIN:
            continue
        if fast and len(edges) > L_MAX:
            successes += 1
        elif has_path(edges, START, TARGET):
            successes += 1

    probability = successes / n
    variance = probability * (1 - probability) / (n - 1)
    return probability, variance


def sim3(p, n):
    m = len(EDGES)
    probability = variance = 0

    for j in range(m + 1):
        weight = comb(m, j) * p**j * (1 - p)**(m - j)
        if weight == 0:
            continue

        n_j = max(2, round(weight * n))
        successes = 0

        for _ in range(n_j):
            edges = sample(EDGES, j)
            if has_path(edges, START, TARGET):
                successes += 1

        p_j = successes / n_j
        probability += weight * p_j
        variance += weight**2 * p_j * (1 - p_j) / (n_j - 1)

    return probability, variance


def main():
    seed(15)
    n = ceil(2.25 / EPS**2)
    p_values = [i / 10 for i in range(11)]
    exact_values = [formula_probability(p) for p in p_values]
    estimates = [[], [], []]
    variance_sums = [0, 0, 0]

    print(f'Вариант 15. N = {n}, l_min = {L_MIN}, l_max = {L_MAX}')
    print(' p    Точно    Этап 1   Этап 2   Этап 3     Дисп. 1    Дисп. 2    Дисп. 3')
    for p, exact in zip(p_values, exact_values):
        p1, v1 = simulate(p, n)
        p2, v2 = simulate(p, n, fast=True)
        p3, v3 = sim3(p, n)
        for i, (value, variance) in enumerate([(p1, v1), (p2, v2), (p3, v3)]):
            estimates[i].append(value)
            variance_sums[i] += variance
        print(f'{p:.1f}   {exact:.5f}  {p1:.5f}  {p2:.5f}  {p3:.5f}'
              f'    {v1:.2e}   {v2:.2e}   {v3:.2e}')

    fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    titles = ['Простое моделирование', 'Пропуск проверок', 'Расслоенная выборка']
    for i, ax in enumerate(axes):
        error = max(abs(value - exact) for value, exact in zip(estimates[i], exact_values))
        mean_variance = variance_sums[i] / len(p_values)
        print(f'Этап {i + 1}. Макс. ошибка: {error:.5f}. Средняя дисперсия: {mean_variance:.2e}')

        ax.plot(p_values, exact_values, '--', label='Точно')
        ax.plot(p_values, estimates[i], 'o', markersize=4, label='Моделирование')
        ax.set(title=titles[i], xlabel='p')
        ax.grid()
    axes[0].set_ylabel('P45(p)')
    axes[0].legend()
    fig.tight_layout()
    plt.savefig('lab2_graph.png', dpi=160)
    plt.show()

    #При p = 0 или p = 1 проверок BFS нет, поэтому N / N' не определено.
    speedup_p = [i / 100 for i in range(1, 100)]
    speedup = []
    m = len(EDGES)
    for p in speedup_p:
        check_probability = sum(
            comb(m, j) * p**j * (1 - p)**(m - j)
            for j in range(L_MIN, L_MAX + 1)
        )
        speedup.append(1 / check_probability)

    plt.figure(figsize=(7, 4))
    plt.plot(speedup_p, speedup)
    plt.xlabel('p')
    plt.ylabel("N / N'")
    plt.title('Этап 2. Выигрыш по числу проверок BFS')
    plt.xticks(p_values)
    plt.ylim(0, 15)
    plt.grid()
    plt.tight_layout()
    plt.savefig('lab2_speedup.png', dpi=160)
    plt.show()

if __name__ == '__main__':
    main()
