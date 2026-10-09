from collections import deque

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

P = 0.5          # вероятность каждого ребра
START = 4        # откуда ищем путь
TARGET = 5       # куда ищем путь

def has_path(edges, start, target):
    """
    Проверяет, существует ли путь из start в target
    Используется BFS.
    """
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


def full_enumeration_probability(edges, p):
    """
    Для каждого подмножества проверяем, есть ли путь START -> TARGET.
    Складываем вероятности тех подмножеств, где путь есть.
    """
    n = len(edges)
    total_prob = 0.0

    for mask in range(1 << n):
        subset = []
        k = 0  # число рёбер в подмножестве

        for i, e in enumerate(edges):
            if mask & (1 << i):
                subset.append(e)
                k += 1

        if has_path(subset, START, TARGET):
            total_prob += (p ** k) * ((1 - p) ** (n - k))

    return total_prob


def formula_probability(p):
    """
    P45(p) = p + p^3 + p^4 - 2p^5 - 4p^6 + 6p^7 - 2p^8
    """
    return (
        p
        + p ** 3
        + p ** 4
        - 2 * p ** 5
        - 4 * p ** 6
        + 6 * p ** 7
        - 2 * p ** 8
    )

def main():
    global EDGES, P

    prob_enum = full_enumeration_probability(EDGES, P)
    prob_form = formula_probability(P)

    print(f"Полный перебор: {prob_enum:.10f}")
    print(f"Формула:        {prob_form:.10f}")

    print(f"Разность:       {abs(prob_enum - prob_form):.3e}")

    print("0 - график зависимости от p [0, 1]")
    
    import numpy as np
    import matplotlib.pyplot as plt

    p_values = np.arange(0, 1.01, 0.1)
    y_values = [formula_probability(x) for x in p_values]

    plt.plot(p_values, y_values, 'o-')

    plt.xlabel('p')
    plt.ylabel('P45(p)')
    plt.title('Зависимость вероятности существования пути 4–5 от p')
    plt.grid()
    plt.show()
    

if __name__ == "__main__":
    main()