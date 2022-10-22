from dataclasses import dataclass
import csv
from functools import reduce
import itertools
from operator import add
from copy import deepcopy
from typing import Dict, List
from itertools import combinations_with_replacement

@dataclass
class Ingredient:
    name: str
    magimins: List[int]
    traits: List[int]
    cost: int
    available: int

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name) + 1

class Mix:
    def __init__(self):
        self.ingredients = {}

    def append(self, ingredient):
        if not ingredient in self.ingredients.keys():
            self.ingredients[ingredient] = 1
        else:
            self.ingredients[ingredient] += 1
    
    def __len__(self):
        return sum([pcs for pcs in self.ingredients.values()])
    
    def magimins(self):
        total = [0, 0, 0, 0, 0]
        for ingredient, pcs in self.ingredients.items():
            total = [a + pcs*b for a,b in zip(total, ingredient.magimins)]
        return total

    def total_magimins(self):
        return sum(self.magimins())

    def test_recipe(self, recipe):
        ratio = [a / b for a,b in zip(self.magimins(), recipe) if b > 0]
        ratio = max(round(sum(ratio) / len(ratio)), 1)
        ideal = [ratio * a for a in recipe]
        diff = [abs(a - b) / ratio for a,b in zip(ideal, self.magimins())]
        return sum(diff)

    def total_cost(self):
        cost = 0
        for ingredient, pcs in self.ingredients.items():
            cost += pcs*ingredient.cost
        return cost

    def __eq__(self, other):
        return self.ingredients == other.ingredients
    
    def __hash__(self):
        return hash(self.ingredients) + 1
    
    def traits(self):
        good_traits = [False, False, False, False, False]
        bad_traits = [False, False, False, False, False]

        for ingredient in self.ingredients.keys():
            good_traits = [a or (b == 1) for a,b in zip(good_traits, ingredient.traits)]
            bad_traits = [a or (b == -1) for a,b in zip(bad_traits, ingredient.traits)]
        
        return [1 if good else -1 if bad else 0 for good, bad in zip(good_traits, bad_traits)]

    def str_ingredients(self):
        return reduce(lambda x,y: f"{x} {y}", [f"{pcs}x {ing.name}" for ing, pcs in self.ingredients.items()])

    def __str__(self):
        if len(self) > 0:
            return f"{self.total_cost():4d}g {self.total_magimins():4d}m {['+' if t == 1 else '-' if t == -1 else ' ' for t in self.traits()]} {self.str_ingredients()}"
        else:
            return "[]"
    
    def __repr__(self):
        return str(self)

@dataclass
class Cauldron:
    max_ingredients: int
    max_magimins: int

def get_unique(list):
    unique = []

    for i in range(len(list)):
        found = False
        element = list[i]
        for j in range(i+1, len(list)):
            if element == list[j]:
                found = True
                break
        
        if not found:
            unique.append(element)

    return unique

def optimize(ingredients, cauldron, recipe):
    solutions = []
    for num_ingredients in range(1, cauldron.max_ingredients):
        for combination in itertools.combinations_with_replacement(ingredients, num_ingredients):
            viable = True
            for ingredient in combination:
                if combination.count(ingredient) > ingredient.available:
                    viable = False
                    break
            if not viable:
                continue
            
            mix = Mix()
            for ingredient in combination:
                mix.append(ingredient)
            
            if mix.total_magimins() > cauldron.max_magimins:
                continue

            if mix.test_recipe(recipe) == 0:
                solutions.append(mix)
    return solutions

def main():
    cauldron = Cauldron(4, 120)
    recipe = [1, 2, 0, 0, 0]

    with open('Potionomics Ingredients - List.csv') as f:
        csv_ingredients = csv.DictReader(f)
        ingredients = [
            Ingredient(
                ing['Ingredients'], 
                [int(ing['A']), int(ing['B']), int(ing['C']), int(ing['D']), int(ing['E'])],
                [
                    1 if ing['Taste'] == 'Good' else -1 if ing['Taste'] == 'Bad' else 0,
                    1 if ing['Touch'] == 'Good' else -1 if ing['Touch'] == 'Bad' else 0,
                    1 if ing['Smell'] == 'Good' else -1 if ing['Smell'] == 'Bad' else 0,
                    1 if ing['Sight'] == 'Good' else -1 if ing['Sight'] == 'Bad' else 0,
                    1 if ing['Sound'] == 'Good' else -1 if ing['Sound'] == 'Bad' else 0
                ],
                int(ing['Price (Quinn)']),
                int(ing['Availability'])
                )
            for ing in csv_ingredients]
    
    solution = optimize(ingredients, cauldron, recipe)
    
    with open('output.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['cost', 'magimins', 'taste', 'touch', 'smell', 'sight', 'sound', 'ingredients'])
        writer.writeheader()
        for s in solution:
            t = s.traits()
            writer.writerow({
                'cost': s.total_cost(),
                'magimins': s.total_magimins(),
                'taste': 'Good' if t[0] == 1 else 'Bad' if t[0] == -1 else '',
                'touch': 'Good' if t[1] == 1 else 'Bad' if t[1] == -1 else '',
                'smell': 'Good' if t[2] == 1 else 'Bad' if t[2] == -1 else '',
                'sight': 'Good' if t[3] == 1 else 'Bad' if t[3] == -1 else '',
                'sound': 'Good' if t[4] == 1 else 'Bad' if t[4] == -1 else '',
                'ingredients': s.str_ingredients()
            })


if __name__ == "__main__":
    main()