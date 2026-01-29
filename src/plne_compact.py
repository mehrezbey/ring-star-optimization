import pulp
import time

# ============================================================
# PLNE COMPACTE — PROBLÈME ANNEAU-ÉTOILE
# ============================================================

def solve_ring_star_plne(points, d, p, alpha=1.0, time_limit=5):

    n = len(points)
    V = list(range(n))
    E = [(i, j) for i in V for j in V if i < j]

    model = pulp.LpProblem("RingStarCompact", pulp.LpMinimize)

    # =====================
    # VARIABLES
    # =====================
    y = pulp.LpVariable.dicts("y", V, 0, 1, cat="Binary")       # station
    a = pulp.LpVariable.dicts("a", (V, V), 0, 1, cat="Binary")  # affectation
    x = pulp.LpVariable.dicts("x", E, 0, 1, cat="Binary")      # cycle
    z = pulp.LpVariable.dicts("z", (V, V), 0, p-1)             # flot

    # =====================
    # OBJECTIF
    # =====================
    model += (
        alpha * pulp.lpSum(d[i][j] * x[(i, j)] for (i, j) in E)
        + pulp.lpSum(d[i][j] * a[i][j] for i in V for j in V)
    )

    # =====================
    # CONTRAINTES
    # =====================

    # (1) exactement p stations
    model += pulp.lpSum(y[i] for i in V) == p

    # (2) chaque sommet est affecté une fois
    for i in V:
        model += pulp.lpSum(a[i][j] for j in V) == 1

    # (3) affectation seulement vers station
    for i in V:
        for j in V:
            model += a[i][j] <= y[j]

    # (4) un sommet est affecté à lui-même ssi c’est une station
    for i in V:
        model += a[i][i] == y[i]

    # (5) degré = 2 pour les stations
    for i in V:
        model += pulp.lpSum(
            x[min(i, j), max(i, j)] for j in V if j != i
        ) == 2 * y[i]

    # (6) sommet 0 imposé station
    model += y[0] == 1

    # =====================
    # CONTRAINTES DE FLOT
    # =====================

    model += pulp.lpSum(z[0][j] for j in V if j != 0) == p - 1

    for i in V:
        if i != 0:
            model += (
                pulp.lpSum(z[j][i] for j in V if j != i)
                - pulp.lpSum(z[i][j] for j in V if j != i)
                == y[i]
            )

    for (i, j) in E:
        model += z[i][j] <= (p - 1) * x[(i, j)]
        model += z[j][i] <= (p - 1) * x[(i, j)]

    # =====================
    # RÉSOLUTION
    # =====================
    solver = pulp.PULP_CBC_CMD(msg=True, timeLimit=time_limit)
    t0 = time.time()
    model.solve(solver)
    t1 = time.time()

    # =====================
    # EXTRACTION SOLUTION
    # =====================
    stations = [i for i in V if pulp.value(y[i]) > 0.5]

    assignments = {}
    for i in V:
        for j in V:
            if pulp.value(a[i][j]) > 0.5:
                assignments[i] = j
                break

    cycle = [(i, j) for (i, j) in E if pulp.value(x[(i, j)]) > 0.5]

    return {
        "status": pulp.LpStatus[model.status],
        "cost": pulp.value(model.objective),
        "stations": stations,
        "assignments": assignments,
        "cycle": cycle,
        "solve_time": t1 - t0
    }


# ============================================================
# Reconstruction du cycle
# ============================================================

def build_cycle_from_edges(edges, start=0):
    adj = {}
    for i, j in edges:
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)

    cycle = [start]
    prev = None
    curr = start

    while True:
        nxt = adj[curr][0] if adj[curr][0] != prev else adj[curr][1]
        if nxt == start:
            cycle.append(start)
            break
        cycle.append(nxt)
        prev, curr = curr, nxt

    return cycle
