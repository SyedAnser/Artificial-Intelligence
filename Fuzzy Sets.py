import numpy as np
import matplotlib.pyplot as plt

class FuzzySet:
    def __init__(self, name, membership_func):
        self.name = name
        self.membership_func = membership_func

class FuzzyVariable:
    def __init__(self, name, range_start, range_end, granularity):
        self.name = name
        self.range_start = range_start
        self.range_end = range_end
        self.granularity = granularity
        self.values = np.arange(range_start, range_end + granularity, granularity)

    def plot(self, fuzzy_sets, operations=None, plot_title=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))
        else:
            fig = ax.get_figure()

        # Plot fuzzy sets without any operations
        if not operations:
            for fuzzy_set in fuzzy_sets:
                ax.plot(self.values, [fuzzy_set.membership_func(x) for x in self.values], label=fuzzy_set.name)
        
        # Plot unions, intersections, and complements if provided
        if operations:
            for op_name, op_func, fs1, fs2 in operations:
                if op_name == "Complement":
                    ax.plot(self.values, [op_func(fs1, x) for x in self.values], label=f'{op_name}({fs1.name})')
                else:
                    ax.plot(self.values, [op_func(fs1, fs2, x) for x in self.values], label=f'{op_name}({fs1.name}, {fs2.name})')

        ax.set_title(plot_title if plot_title else f"Fuzzy Sets for {self.name}")
        ax.set_xlabel(self.name)
        ax.set_ylabel("Membership Degree")
        ax.legend()
        ax.grid(True)

        if not ax:
            plt.show()

            ax.set_title(plot_title if plot_title else f"Fuzzy Sets for {self.name}")
            ax.set_xlabel(self.name)
            ax.set_ylabel("Membership Degree")
            ax.legend()
            ax.grid(True)
            plt.show()

def union(fuzzy_set1, fuzzy_set2, x):
    return max(fuzzy_set1.membership_func(x), fuzzy_set2.membership_func(x))

def intersection(fuzzy_set1, fuzzy_set2, x):
    return min(fuzzy_set1.membership_func(x), fuzzy_set2.membership_func(x))

def complement(fuzzy_set, x):
    return 1 - fuzzy_set.membership_func(x)



def membership_function(func):
    def wrapper(x):
        return func(x)
    return wrapper


@membership_function
def very_short(x):
    if x <= 150:
        return 1
    elif x > 150 and x < 160:
        return (160 - x) / 10
    else:
        return 0

@membership_function
def short(x):
    if x >= 140 and x <= 170:
        return min((x - 140) / 30, (180 - x) / 10)
    else:
        return 0

@membership_function
def medium(x):
    if x >= 160 and x <= 190:
        return min((x - 160) / 30, (200 - x) / 10)
    else:
        return 0

@membership_function
def tall(x):
    if x >= 180 and x <= 210:
        return min((x - 180) / 30, (220 - x) / 10)
    else:
        return 0

@membership_function
def very_tall(x):
    if x >= 220:
        return 1
    elif x > 200 and x < 220:
        return (x - 200) / 20
    else:
        return 0

# Create fuzzy sets
very_short_set = FuzzySet("Very Short", very_short)
short_set = FuzzySet("Short", short)
medium_set = FuzzySet("Medium", medium)
tall_set = FuzzySet("Tall", tall)
very_tall_set = FuzzySet("Very Tall", very_tall)

# Create a fuzzy variable
height_variable = FuzzyVariable("Height", 130, 230, 1)

# Define all fuzzy sets in a list
fuzzy_sets = [very_short_set, short_set, medium_set, tall_set, very_tall_set]

# Create a figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Fuzzy Sets Analysis', fontsize=16)

# Plot fuzzy sets without any operations
height_variable.plot(fuzzy_sets, plot_title="Fuzzy Sets", ax=axes[0, 0])

# Calculate union for each pair of sets
operations = []
for i in range(len(fuzzy_sets)):
    for j in range(i+1, len(fuzzy_sets)):
        operations.append(("Union", union, fuzzy_sets[i], fuzzy_sets[j]))

# Plot unions
height_variable.plot(fuzzy_sets, operations=operations, plot_title="Unions", ax=axes[0, 1])

# Calculate intersection for each pair of sets
operations = []
for i in range(len(fuzzy_sets)):
    for j in range(i+1, len(fuzzy_sets)):
        operations.append(("Intersection", intersection, fuzzy_sets[i], fuzzy_sets[j]))

# Plot intersections
height_variable.plot(fuzzy_sets, operations=operations, plot_title="Intersections", ax=axes[1, 0])

# Calculate complement for each set
operations = []
for fuzzy_set in fuzzy_sets:
    operations.append(("Complement", complement, fuzzy_set, None))

# Plot complements
height_variable.plot(fuzzy_sets, operations=operations, plot_title="Complements", ax=axes[1, 1])

plt.tight_layout()
plt.show()
