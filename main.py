import tkinter as tk
from tkinter import messagebox
import random


# Classe que define o algoritmo genético
class GeneticAlgorithm:
    def __init__(self, population_size, generations, crossover_rate, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = list(range(10))
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitness(self, individual):
        def decode(word, mapping):
            return int("".join(str(mapping[char]) for char in word))

        mapping = {char: digit for char, digit in zip("SENDMORY", individual)}
        send = decode("SEND", mapping)
        more = decode("MORE", mapping)
        money = decode("MONEY", mapping)

        return abs((send + more) - money)

    def select_parents(self, population, fitness_scores):
        total_fitness = sum(1 / (score + 1) for score in fitness_scores)
        probabilities = [(1 / (score + 1)) / total_fitness for score in fitness_scores]
        return random.choices(population, probabilities, k=2)

    def crossover(self, parent1, parent2):
        child1, child2 = parent1[:], parent2[:]
        for i in range(len(parent1)):
            if random.random() < self.crossover_rate:
                child1[i], child2[i] = child2[i], child1[i]
        return child1, child2

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]

    def run(self):
        population = self.initialize_population()
        best_solution = None
        best_fitness = float("inf")

        for generation in range(self.generations):
            fitness_scores = [self.fitness(ind) for ind in population]
            if min(fitness_scores) < best_fitness:
                best_fitness = min(fitness_scores)
                best_solution = population[fitness_scores.index(min(fitness_scores))]

            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])

            population = new_population

        return best_solution, best_fitness


# Interface gráfica com tkinter
def run_algorithm():
    try:
        population_size = int(entry_population.get())
        generations = int(entry_generations.get())
        crossover_rate = float(entry_crossover.get())
        mutation_rate = float(entry_mutation.get())

        ga = GeneticAlgorithm(
            population_size=population_size,
            generations=generations,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
        )
        solution, fitness = ga.run()

        mapping = {char: digit for char, digit in zip("SENDMORY", solution)}
        send = int("".join(str(mapping[char]) for char in "SEND"))
        more = int("".join(str(mapping[char]) for char in "MORE"))
        money = int("".join(str(mapping[char]) for char in "MONEY"))

        result_text.set(
            f"Solução encontrada:\n"
            f"Mapeamento: {mapping}\n"
            f"SEND = {send}, MORE = {more}, MONEY = {money}\n"
            f"Fitness = {fitness}"
        )
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")


# Configuração da interface tkinter
root = tk.Tk()
root.title("Algoritmo Genético - Criptoaritmética")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Tamanho da População:").grid(row=0, column=0, sticky="e")
entry_population = tk.Entry(frame)
entry_population.grid(row=0, column=1)

tk.Label(frame, text="Número de Gerações:").grid(row=1, column=0, sticky="e")
entry_generations = tk.Entry(frame)
entry_generations.grid(row=1, column=1)

tk.Label(frame, text="Taxa de Cruzamento (0 a 1):").grid(row=2, column=0, sticky="e")
entry_crossover = tk.Entry(frame)
entry_crossover.grid(row=2, column=1)

tk.Label(frame, text="Taxa de Mutação (0 a 1):").grid(row=3, column=0, sticky="e")
entry_mutation = tk.Entry(frame)
entry_mutation.grid(row=3, column=1)

tk.Button(frame, text="Executar", command=run_algorithm).grid(row=4, column=0, columnspan=2, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", padx=10, pady=10)
result_label.pack()

root.mainloop()
