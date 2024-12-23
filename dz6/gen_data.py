import pandas as pd
import random
import numpy as np

# Define the size of the file in rows (estimate for ~300MB file)
# Each row of ~100 bytes would require ~3 million rows for 300MB
estimated_rows = 6000000

# Generate data for used cars
brands = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes", "Volkswagen", "Hyundai", "Kia"]
models = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
    "Ford": ["F-150", "Escape", "Mustang", "Explorer"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Traverse"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Pathfinder"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Mercedes": ["C-Class", "E-Class", "GLC", "GLE"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Jetta"],
    "Hyundai": ["Elantra", "Santa Fe", "Tucson", "Sonata"],
    "Kia": ["Optima", "Sorento", "Sportage", "Soul"],
}
years = range(1986, 2024)
conditions = ["Excellent", "Good", "Fair", "Poor"]
transmissions = ["Automatic", "Manual"]
fuel_types = ["Gasoline", "Diesel", "Electric", "Hybrid"]
colors = ["Black", "White", "Silver", "Blue", "Red", "Green", "Gray"]

# Parameters for normal distribution
price_mean = 20000
price_std = 10000
mileage_mean = 75000
mileage_std = 50000

# Generate the data
data = []
for _ in range(estimated_rows):
    brand = random.choice(brands)
    model = random.choice(models[brand])
    year = random.choice(years)
    condition = random.choice(conditions)
    transmission = random.choice(transmissions)
    fuel_type = random.choice(fuel_types)
    color = random.choice(colors)
    price = max(1000, int(np.random.normal(price_mean, price_std)))
    mileage = max(0, int(np.random.normal(mileage_mean, mileage_std)))

    data.append([brand, model, year, condition, transmission, fuel_type, color, price, mileage])

# Create DataFrame
columns = ["Brand", "Model", "Year", "Condition", "Transmission", "Fuel Type", "Color", "Price", "Mileage"]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
file_path = './data/used_cars_300mb.csv'
df.to_csv(file_path, index=False)

file_path