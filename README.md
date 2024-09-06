# Implement two variants of DE. First of them is the original rand/1/bin and the second is the more modern adaptive variant - jDE.
## Recommended parameter values for Rand/1/bin CR = 0.3; F = 0.5
- for jDE: tau1 = tau2 = 0.1; CR = init to 0.3 (range 0 to 1); F = init to 0.5 (range 0.1 to 0.9)

- Mutation
Rand/1:
v_i = x_r1 + F(x_r2 - x_r3)

- Crossover
j_rand = randInt(1, D)
u_i,j = v_i,j, if rand(0,1) <= CR or j = j_rand
       = x_i,j

## Tasks
- Implement DE versions: Rand/1/bin and jDE
- Test both versions on test functions
