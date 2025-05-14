import random
from deap import base, creator, tools

def optimize_routes(drones, deliveries):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Teslimatları önceliğe göre sırala (önce yüksek öncelik)
    sorted_deliveries = sorted(deliveries, key=lambda x: -x.priority)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     lambda: random.choice(drones).id, n=len(sorted_deliveries))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_func(individual):
        total_energy = 0
        penalty = 0
        drone_states = {d.id: {"battery": d.battery, "pos": d.start_pos} for d in drones}

        for i, drone_id in enumerate(individual):
            drone_state = drone_states[drone_id]
            delivery = sorted_deliveries[i]
            dist = ((drone_state["pos"][0] - delivery.pos[0]) ** 2 +
                    (drone_state["pos"][1] - delivery.pos[1]) ** 2) ** 0.5
            energy_cost = dist * delivery.weight

            if delivery.weight > next(d.max_weight for d in drones if d.id == drone_id):
                penalty += 1000  # Ağırlık kapasitesi aşıldı
                continue

            if energy_cost > drone_state["battery"]:
                # Şarj gerekiyorsa simüle et
                penalty += 500
                drone_state["battery"] = 100  # Şarj ettik
            else:
                drone_state["battery"] -= energy_cost

            drone_state["pos"] = delivery.pos
            total_energy += energy_cost

        success_count = len(sorted_deliveries) - (penalty // 1000)
        return success_count - penalty / 10000,  # Maksimize edilecek

    toolbox.register("evaluate", eval_func)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=20)
    for _ in range(30):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.7:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fits = map(toolbox.evaluate, invalid)
        for ind, fit in zip(invalid, fits):
            ind.fitness.values = fit

        pop[:] = offspring

    best = tools.selBest(pop, 1)[0]
    return best
