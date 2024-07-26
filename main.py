import numpy as np
from scipy.optimize import minimize
import random

"""
Worth mentioning that (due to generating random data) sometimes the optimization may fail to find a solution. I'm sure there are ways 
to fix this (e.g. maybe constraints/bounds??) but I can't figure it out :(
"""

def generate_randomdata(num_warehouses, num_outlets, supply_range, demand_range, a_range, b_range):
    warehouses = [f"W{i+1}" for i in range(num_warehouses)]
    outlets = [f"O{i+1}" for i in range(num_outlets)]

    supply = {w: random.randint(*supply_range) for w in warehouses}
    demand = {o: random.randint(*demand_range) for o in outlets}
    # I generate cost coefficients here (randomized of course)
    a = {(w, o): random.uniform(*a_range) for w in warehouses for o in outlets}
    b = {(w, o): random.uniform(*b_range) for w in warehouses for o in outlets}
    # Uncomment to print generated data
    # print("Warehouses:", warehouses)
    # print("Outlets:", outlets)
    # print("Supply:", supply)
    # print("Demand:", demand)
    # print("Quadratic cost coefficients (a):", a)
    # print("Linear cost coefficients (b):", b)
    return warehouses, outlets, supply, demand, a, b

def initial_guess(warehouses, outlets):
    return [1 for _ in range(len(warehouses) * len(outlets))] # init guess is set to 1 just as a baseline
def cost_function(x, warehouses, outlets, a, b):
    total_cost = 0
    index = 0
    for w in warehouses:
        for o in outlets:
            total_cost += a[(w, o)] * x[index]**2 + b[(w, o)] * x[index]
            index += 1
    return total_cost

def supply_constraint(w, indices, supply):
    return lambda x: supply[w] - sum(x[i] for i in indices)
def demand_constraint(o, indices, demand):
    return lambda x: sum(x[i] for i in indices) - demand[o]

def create_constraints(warehouses, outlets, supply, demand):
    # print(warhouses)
    constraints = []
    
    for w in warehouses:
        indices = [i for i, wh in enumerate(warehouses * len(outlets)) if wh == w]
        constraints.append({
            'type': 'ineq',
            'fun': supply_constraint(w, indices, supply)
        })
    
    for o in outlets:
        indices = [i for i, ot in enumerate(outlets * len(warehouses)) if ot == o]
        constraints.append({
            'type': 'ineq',
            'fun': demand_constraint(o, indices, demand)
        })
    # print(constraints)
    return constraints

def create_bounds(warehouses, outlets):
    # print(warehouses)
    return [(0, None) for _ in range(len(warehouses) * len(outlets))]

def optimize_supply_chain(warehouses, outlets, supply, demand, a, b):
    x = initial_guess(warehouses, outlets)
    constraints = create_constraints(warehouses, outlets, supply, demand)
    bounds = create_bounds(warehouses, outlets) 
    result = minimize(
        cost_function, x, args=(warehouses, outlets, a, b), 
        method='SLSQP', bounds=bounds, constraints=constraints
    )
    print(result, "hello world")
    return result

def print_results(result, warehouses, outlets):
    if result.success:
        print("We did it!")
        print("Total Cost:", result.fun)
        quantities = result.x.reshape((len(warehouses), len(outlets)))
        for i, w in enumerate(warehouses):
            for j, o in enumerate(outlets):
                print(f"Route {w} to {o}: {quantities[i][j]:.2f} units")
    else:
        print("We did not do it.")
        print(result)

def main():
    num_warehouses = 2
    num_outlets = 3
    supply_range = (10, 30)
    demand_range = (5, 20)
    a_range = (0.01, 0.1) # a_range is for the quadratic (non-linear) term
    b_range = (1, 5) # b_range is for the linear term

    warehouses, outlets, supply, demand, a, b = generate_randomdata(num_warehouses, num_outlets, supply_range, demand_range, a_range, b_range)

    result = optimize_supply_chain(warehouses, outlets, supply, demand, a, b)
    print_results(result, warehouses, outlets)

if __name__ == "__main__":
    main()
