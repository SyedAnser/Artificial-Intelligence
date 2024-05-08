import numpy as np
import matplotlib.pyplot as plt

# Define membership functions
def membership_size(x):
    small = max(1 - x / 10, 0)
    large = min(x / 10, 1)
    return small, large

def membership_weight(x):
    small = max(1 - x / 100, 0)
    large = min(x / 100, 1)
    return small, large

def membership_quality(x):
    bad = max(1 - x / 0.5, 0)
    medium = max(min(2 * x, 2 * (1 - x)), 0)
    good = max((x - 0.5) / 0.5, 0)
    return bad, medium, good

# Fuzzify inputs
size_input = 5
weight_input = 50

small_size, large_size = membership_size(size_input)
small_weight, large_weight = membership_weight(weight_input)

print("Fuzzified Size:", "small:",small_size,"large:", large_size)
print("Fuzzified Weight:", "small:", small_weight,"large:", large_weight)

# Evaluate rules
rules = [
    ("Bad", min(small_size, small_weight)),
    ("Medium", min(small_size, large_weight)),
    ("Medium", min(large_size, small_weight)),
    ("Good", min(large_size, large_weight))
]

print("Firing Strength of Rules:")
for rule, strength in rules:
    print("Rule:", rule, "- Firing Strength:", strength)


# Plotting membership functions with areas cut at the firing strengths
plt.figure(figsize=(10, 6))

# Plot "Bad" membership function
x = np.linspace(0, 0.5, 100)
y_bad = np.maximum(1 - x / 0.5, 0)
y_bad_cut = np.minimum(y_bad, rules[0][1])
plt.plot(x, y_bad_cut, label='Bad', color='orange')

# Calculate centroid for "Bad" membership function
centroid_bad_x = np.trapz(y_bad_cut * x, x) / np.trapz(y_bad_cut, x)
area_bad = np.trapz(y_bad_cut, x)

# Plot "Medium" membership function
x = np.linspace(0, 1, 100)
y_medium = np.maximum(np.minimum(2 * x, 2 * (1 - x)), 0)
y_medium_cut = np.minimum(y_medium, rules[1][1])
plt.plot(x, y_medium_cut, label='Medium', color='blue')

# Calculate centroid for "Medium" membership function
centroid_medium_x = np.trapz(y_medium_cut * x, x) / np.trapz(y_medium_cut, x)
area_medium = np.trapz(y_medium_cut, x)

# Plot "Medium" membership function (second occurrence)
y_medium_cut2 = np.minimum(y_medium, rules[2][1])
plt.plot(x, y_medium_cut2, color='blue')

# Calculate centroid for the second "Medium" membership function
centroid_medium2_x = np.trapz(y_medium_cut2 * x, x) / np.trapz(y_medium_cut2, x)
area_medium2 = np.trapz(y_medium_cut2, x)

# Plot "Good" membership function
x = np.linspace(0.5, 1, 100)
y_good = (x - 0.5) / 0.5
y_good_cut = np.minimum(y_good, rules[3][1])
plt.plot(x, y_good_cut, label='Good', color='green')

# Calculate centroid for "Good" membership function
centroid_good_x = np.trapz(y_good_cut * x, x) / np.trapz(y_good_cut, x)
area_good = np.trapz(y_good_cut, x)

# Calculate center of gravity
cog = (centroid_bad_x * area_bad + centroid_medium_x * area_medium + centroid_medium2_x * area_medium2 + centroid_good_x * area_good) / (area_bad + area_medium + area_medium2 + area_good)

# Plot centroids
plt.scatter([centroid_bad_x, centroid_medium_x, centroid_medium2_x, centroid_good_x],
            [area_bad/2, area_medium/2, area_medium2/2, area_good/2],
            color='red', label='Centroid')

plt.xlabel('Quality')
plt.ylabel('Membership degree')
plt.title('Membership functions cut at the firing strengths')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.show()

print("Center of Gravity (COG):", cog)

# cog=0
# total_area=0

# plt.figure(figsize=(10, 6))

# # Plot "Bad" membership function
# x = np.linspace(0, 0.5, 100)
# y = np.maximum(1 - x / 0.5, 0)
# y_cut = np.minimum(y, rules[0][1])
# area = np.trapz(y_cut, x)
# cog += np.trapz(x * y_cut, x)
# total_area += area
# plt.plot(x, y_cut, label='Bad', color='orange')

# # Plot "Medium" membership function
# x = np.linspace(0, 1, 100)
# y = np.maximum(np.minimum(2 * x, 2 * (1 - x)), 0)
# y_cut = np.minimum(y, rules[1][1])
# area = np.trapz(y_cut, x)
# cog += np.trapz(x * y_cut, x)
# total_area += area
# plt.plot(x, y_cut, label='Medium', color='blue')

# # Plot "Medium" membership function (second occurrence)
# y_cut = np.minimum(y, rules[2][1])
# area = np.trapz(y_cut, x)
# cog += np.trapz(x * y_cut, x)
# total_area += area
# plt.plot(x, y_cut, color='blue')

# # Plot "Good" membership function
# x = np.linspace(0.5, 1, 100)
# y = (x - 0.5) / 0.5
# y_cut = np.minimum(y, rules[3][1])
# area = np.trapz(y_cut, x)
# cog += np.trapz(x * y_cut, x)
# total_area += area
# plt.plot(x, y_cut, label='Good', color='green')

# cog/=total_area
# print("CoG:", cog)

# # Plot CoG point
# plt.scatter(cog, 0, color='red', label='Center of Gravity (CoG)')

# plt.xlabel('Quality')
# plt.ylabel('Membership degree')
# plt.title('Membership functions cut at the firing strengths')
# plt.legend()
# plt.grid(True)
# plt.show()