import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Initial population distribution by age and sex
initial_population_male = np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 25])
initial_population_female = np.array([950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 25, 12.5])

# Fertility rates (births per woman by age group)
fertility_rates = np.array([0, 0, 0.05, 0.1, 0.15, 0.1, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Mortality rates (deaths per person by age group and sex)
mortality_rates_male = np.array([0.005, 0.002, 0.001, 0.001, 0.002, 0.002, 0.003, 0.004, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2])
mortality_rates_female = np.array([0.004, 0.002, 0.001, 0.001, 0.0015, 0.0015, 0.002, 0.0025, 0.003, 0.004, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03, 0.04, 0.06, 0.08, 0.12, 0.15])

# Migration rates (net migration per person by age group and sex)
migration_rates_male = np.zeros(21)  # Assuming no migration for simplicity
migration_rates_female = np.zeros(21)

# Project population for one time step (e.g., 5 years)
def project_population(population_male, population_female, fertility, mortality_male, mortality_female, migration_male, migration_female):
    # Births
    births = np.sum(population_female * fertility)
    
    # Age the population
    new_population_male = np.zeros_like(population_male)
    new_population_female = np.zeros_like(population_female)
    
    new_population_male[:-1] = population_male[1:] * (1 - mortality_male[1:])
    new_population_female[:-1] = population_female[1:] * (1 - mortality_female[1:])
    
    # Add births to the youngest age group
    new_population_male[0] = births * 0.51  # Assuming 51% of births are male
    new_population_female[0] = births * 0.49  # Assuming 49% of births are female
    
    # Apply migration
    new_population_male = new_population_male * (1 + migration_male)
    new_population_female = new_population_female * (1 + migration_female)
    
    return new_population_male, new_population_female

# Project population for 5 periods (e.g., 25 years)
n_periods = 5
population_male = initial_population_male
population_female = initial_population_female

# Store the population projections
projections_male = [population_male]
projections_female = [population_female]

for _ in range(n_periods):
    population_male, population_female = project_population(
        population_male, population_female, fertility_rates, mortality_rates_male, mortality_rates_female, migration_rates_male, migration_rates_female
    )
    projections_male.append(population_male)
    projections_female.append(population_female)

# Create a DataFrame to display the final population
age_groups = [f"{i*5}-{i*5+4}" for i in range(20)] + ["100+"]

# Visualize the population projections
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

for i, (population_male, population_female) in enumerate(zip(projections_male, projections_female)):
    axes[0].plot(age_groups, population_male, label=f"Period {i}")
    axes[1].plot(age_groups, population_female, label=f"Period {i}")

axes[0].set_title("Male Population Projection")
axes[0].set_xlabel("Age Group")
axes[0].set_ylabel("Population")
axes[0].legend()

axes[1].set_title("Female Population Projection")
axes[1].set_xlabel("Age Group")
axes[1].set_ylabel("Population")
axes[1].legend()

plt.tight_layout()
plt.show()
