# -*- coding: utf-8 -*-
"""Differential Evolution (DE).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BJdDmLeOpTJP7_24N6-RDfXFryBW_2dG
"""

# Implement two variants of DE. First of them is the original rand/1/bin and the second is the more modern adaptive variant - jDE.

# ______________________________________
# Recommended parameter values for Rand/1/bin CR = 0.3; F = 0.5
# for jDE: tau1 = tau2 = 0.1; CR = init to 0.3 (range 0 to 1); F = init to 0.5 (range 0.1 to 0.9)

# ______________________________________
# Mutation
# Rand/1:
# v_i = x_r1 + F(x_r2 - x_r3)

# ______________________________________
# Crossover
# j_rand = randInt(1, D)
# u_i,j = v_i,j, if rand(0,1) <= CR or j = j_rand
#        = x_i,j
# ______________________________________

# Tasks
# 1) Implement DE versions: Rand/1/bin and jDE
# 2) Test both versions on test functions

import numpy as np

def sphere(x):
    """Sphere function."""
    return np.sum(x**2)

def schwefel(x):
    """Schwefel function."""
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))

def rastrigin(x):
    """Rastrigin function."""
    return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

def rand_1_bin_de(pop_size, dim, bounds, max_iter, obj_func, CR=0.3, F=0.5):
    """Implementation of Rand/1/bin Differential Evolution."""
    # Initialization
    population = np.random.uniform(bounds[0], bounds[1], size=(pop_size, dim))
    best_solution = population[np.argmin([obj_func(ind) for ind in population])]

    for _ in range(max_iter):
        for i in range(pop_size):
            # Mutation
            r1, r2, r3 = np.random.choice(pop_size, 3, replace=False)
            v = population[r1] + F * (population[r2] - population[r3])

            # Crossover
            j_rand = np.random.randint(dim)
            mask = np.random.rand(dim) <= CR
            u = np.where(mask | (np.arange(dim) == j_rand), v, population[i])

            # Selection
            if obj_func(u) < obj_func(population[i]):
                population[i] = u

        # Update best solution
        current_best = population[np.argmin([obj_func(ind) for ind in population])]
        if obj_func(current_best) < obj_func(best_solution):
            best_solution = current_best

    return best_solution, obj_func(best_solution)

def jde(pop_size, dim, bounds, max_iter, obj_func, tau1=0.1, tau2=0.1, CR_range=(0, 1), F_range=(0.1, 0.9)):
    """Implementation of jDE (self-adaptive) Differential Evolution."""
    # Initialization
    population = np.random.uniform(bounds[0], bounds[1], size=(pop_size, dim))
    CR = np.random.uniform(*CR_range, size=pop_size)
    F = np.random.uniform(*F_range, size=pop_size)
    best_solution = population[np.argmin([obj_func(ind) for ind in population])]

    for _ in range(max_iter):
        for i in range(pop_size):
            # Mutation
            r1, r2, r3 = np.random.choice(pop_size, 3, replace=False)
            v = population[r1] + F[i] * (population[r2] - population[r3])

            # Crossover
            j_rand = np.random.randint(dim)
            mask = np.random.rand(dim) <= CR[i]
            u = np.where(mask | (np.arange(dim) == j_rand), v, population[i])

            # Selection
            if obj_func(u) < obj_func(population[i]):
                population[i] = u

                # Adaptation of CR and F
                CR[i] = max(0, min(1, CR[i] * np.exp(tau1 * np.random.normal(0, 1))))
                F[i] = max(0.1, min(0.9, F[i] * np.exp(tau2 * np.random.normal(0, 1))))

        # Update best solution
        current_best = population[np.argmin([obj_func(ind) for ind in population])]
        if obj_func(current_best) < obj_func(best_solution):
            best_solution = current_best

    return best_solution, obj_func(best_solution)

# Test on Sphere, Schwefel, and Rastrigin functions
pop_size = 50
dim = 10
bounds = (-5.12, 5.12)  # Assuming the same bounds for all functions
max_iter = 100

# Test Rand/1/bin DE
print("Rand/1/bin DE:")
for obj_func in [sphere, schwefel, rastrigin]:
    best_solution, best_value = rand_1_bin_de(pop_size, dim, bounds, max_iter, obj_func)
    print(f"{obj_func.__name__}: Best Value = {best_value}, Best Solution = {best_solution}")

# Test jDE
print("\njDE:")
for obj_func in [sphere, schwefel, rastrigin]:
    best_solution, best_value = jde(pop_size, dim, bounds, max_iter, obj_func)
    print(f"{obj_func.__name__}: Best Value = {best_value}, Best Solution = {best_solution}")

