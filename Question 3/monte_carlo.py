import numpy as np

P_Sunny = 0.6
P_Sprinkler_given_Sunny = {True: 0.7, False: 0.3}
P_Rainy_given_Sunny = {True: 0.2, False: 0.5}
P_WetGarden_given_Sprinkler_Rainy = {
    (True, True): 0.95,
    (True, False): 0.85,
    (False, True): 0.75,
    (False, False): 0.05,
}

def simulate_bayesian_network(num_samples=10000):
    count_wet_garden_given_rainy = 0
    count_rainy = 0

    for _ in range(num_samples):
        sunny = np.random.rand() < P_Sunny
        sprinkler = np.random.rand() < P_Sprinkler_given_Sunny[sunny]
        rainy = np.random.rand() < P_Rainy_given_Sunny[sunny]
        wet_garden = np.random.rand() < P_WetGarden_given_Sprinkler_Rainy[(sprinkler, rainy)]

        if rainy:
            count_rainy += 1
        if wet_garden and rainy:
            count_wet_garden_given_rainy += 1

    return count_wet_garden_given_rainy / count_rainy if count_rainy > 0 else 0

estimated_probability = simulate_bayesian_network()
print(f"Estimated Probability: {estimated_probability}")