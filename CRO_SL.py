import time
import pdb

import numpy as np
from CoralPopulation import CoralPopulation
from matplotlib import pyplot as plt

import cro_dt.TensorflowTree as tft
import tensorflow as tf

"""
Coral reef optimization with substrate layers

Parameters:
    popSize: maximum number of corals in the reef        [Integer,          100  recomended]
    rho: percentage of initial ocupation of the reef     [Real from 0 to 1, 0.6  recomended]
    Fb: broadcast spawning proportion                    [Real from 0 to 1, 0.98 recomended]
    Fd: depredation proportion                           [Real from 0 to 1, 0.2  recomended]
    Pd: depredation probability                          [Real from 0 to 1, 0.9  recomended]
    k: maximum attempts for larva setting                [Integer,          4    recomended]
    K: maximum amount of corals with duplicate solutions [Integer,          20   recomended]

    group_subs: evolve only within the same substrate or with the whole population

    dynamic: change the size of each substrate
    dyn_method: which value to use for the evaluation of the substrates
    dyn_metric: how to process the data from the substrate for the evaluation
    dyn_steps: number of times the substrates will be evaluated
    prob_amp: parameter that makes probabilities more or less extreme with the same data

"""


class CRO_SL:
    """
    Constructor of the CRO algorithm
    """

    def __init__(self, objfunc, substrates, params):
        self.params = params

        # Dynamic parameters
        self.dynamic = params["dynamic"]
        self.dyn_method = params["dyn_method"]

        # Verbose parameters
        self.verbose = params["verbose"]
        self.v_timer = params["v_timer"]

        # Stopping conditions
        self.stop_cond = params["stop_cond"]
        self.Ngen = params["Ngen"]
        self.Neval = params["Neval"]
        self.time_limit = params["time_limit"]
        self.fit_target = params["fit_target"]

        # Data structures of the algorithm
        self.objfunc = objfunc
        self.substrates = substrates
        self.population = CoralPopulation(objfunc, substrates, params)

        # Metrics
        self.history = []
        self.pop_size = []
        self.best_fitness = 0
        self.time_spent = 0
        self.real_time_spent = 0

    def restart(self):
        self.population = CoralPopulation(self.objfunc, self.substrates, self.params)
        self.history = []
        self.pop_size = []
        self.best_fitness = 0
        self.time_spent = 0
        self.real_time_spent = 0
        self.objfunc.counter = 0

    """
    One step of the algorithm
    """

    def step(self, progress, depredate=True, classic=False):
        if not classic:
            self.population.generate_substrates(progress)

        larvae = self.population.evolve_with_substrates()

        if self.evaluation_scheme.startswith("tf_batch"):
            self.calculate_fitness_tf_batch(larvae)

        self.population.larvae_setting(larvae)

        if depredate:
            self.population.extreme_depredation()
            self.population.depredation()

        _, best_fitness = self.population.best_solution()
        self.history.append(best_fitness)

    """
    Stopping conditions given by a parameter
    """

    def stopping_condition(self, gen, time_start):
        stop = True
        if self.stop_cond == "neval":
            stop = self.objfunc.counter >= self.Neval
        elif self.stop_cond == "ngen":
            stop = gen >= self.Ngen
        elif self.stop_cond == "time":
            stop = time.time() - time_start >= self.time_limit
        elif self.stop_cond == "fit_target":
            if self.objfunc.opt == "max":
                stop = self.population.best_solution()[1] >= self.fit_target
            else:
                stop = self.population.best_solution()[1] <= self.fit_target

        return stop

    """
    Progress of the algorithm as a number between 0 and 1, 0 at the begining, 1 at the end
    """

    def progress(self, gen, time_start):
        prog = 0
        if self.stop_cond == "neval":
            prog = self.objfunc.counter / self.Neval
        elif self.stop_cond == "ngen":
            prog = gen / self.Ngen
        elif self.stop_cond == "time":
            prog = (time.time() - time_start) / self.time_limit
        elif self.stop_cond == "fit_target":
            if self.objfunc.opt == "max":
                prog = self.population.best_solution()[1] / self.fit_target
            else:
                prog = self.fit_target / self.population.best_solution()[1]

        return prog

    """
    Execute the algorithm to get the best solution possible along with it's evaluation
    """

    def optimize(self):
        gen = 0
        time_start = time.process_time()
        real_time_start = time.time()
        display_timer = time.time()

        self.population.generate_random()
        
        if self.evaluation_scheme.startswith("tf_batch"):
            self.calculate_fitness_tf_batch(self.population.population)
            
        self.step(0, depredate=False)
        while not self.stopping_condition(gen, real_time_start):
            prog = self.progress(gen, real_time_start)
            self.step(prog, depredate=True)
            gen += 1
            if self.verbose and time.time() - display_timer > self.v_timer:
                self.step_info(gen, real_time_start)
                display_timer = time.time()

        self.real_time_spent = time.time() - real_time_start
        self.time_spent = time.process_time() - time_start
        return self.population.best_solution()

    """
    Execute the classic version of the algorithm
    """

    def optimize_classic(self):
        gen = 0
        time_start = time.process_time()
        real_time_start = time.time()
        display_timer = time.time()

        self.population.generate_random()
        self.step(0, depredate=False)
        while not self.stopping_condition(gen, real_time_start):
            prog = self.progress(gen, real_time_start)
            self.step(prog, depredate=True, classic=True)
            gen += 1
            if self.verbose and time.time() - display_timer > self.v_timer:
                self.step_info(gen, real_time_start)
                display_timer = time.time()

        self.real_time_spent = time.time() - real_time_start
        self.time_spent = time.process_time() - time_start
        return self.population.best_solution()

    """
    Save the result of an execution to a csv file in disk
    """

    def save_solution(self, file_name="solution.csv"):
        ind, fit = self.population.best_solution()
        np.savetxt(file_name, ind.reshape([1, -1]), delimiter=',')
        with open(file_name, "a") as file:
            file.write(str(fit))

    """
    Displays information about the current state of the algotithm
    """

    def step_info(self, gen, start_time):
        print(f"Time Spent {round(time.time() - start_time, 2)}s:")
        print(f"\tGeneration: {gen}")
        best_fitness = self.population.best_solution()[1]
        print(f"\tBest fitness: {best_fitness}")
        print(f"\tEvaluations of fitness: {self.objfunc.counter}")

        if self.dynamic:
            print(f"\tSubstrate probability:")
            subs_names = [i.evolution_method for i in self.substrates]
            weights = [round(i, 6) for i in self.population.substrate_weight]
            adjust = max([len(i) for i in subs_names])
            for idx, val in enumerate(subs_names):
                print(f"\t\t{val}:".ljust(adjust + 3, " ") + f"{weights[idx]}")
        print()

    """
    Shows a summary of the execution of the algorithm
    """

    def display_report(self, show_plots=True, filename=None):
        if self.dynamic:
            self.display_report_dyn(show_plots, filename)
        else:
            self.display_report_nodyn(show_plots, filename)

    """
    Version of the summary for the dynamic variant
    """

    def display_report_dyn(self, show_plots=True, filename=None):
        factor = 1
        if self.objfunc.opt == "min" and self.dyn_method != "success":
            factor = -1

        # Print Info
        print("Number of generations:", len(self.history))
        print("Real time spent: ", round(self.real_time_spent, 5), "s", sep="")
        print("CPU time spent: ", round(self.time_spent, 5), "s", sep="")
        print("Number of fitness evaluations:", self.objfunc.counter)
        print(f"\tSubstrate probability:")
        subs_names = [i.evolution_method for i in self.substrates]
        weights = [round(i, 6) for i in self.population.substrate_weight]
        adjust = max([len(i) for i in subs_names])
        for idx, val in enumerate(subs_names):
            print(f"\t\t{val}:".ljust(adjust + 3, " ") + f"{weights[idx]}")

        best_fitness = self.population.best_solution()[1]
        print("Best fitness:", best_fitness)

        # Plot fitness history
        fig, (ax1, ax2) = plt.subplots(2, 2, figsize=(10, 10))
        fig.suptitle("CRO_SL")
        plt.subplot(2, 2, 1)

        plt.plot(self.history, "blue")
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("CRO_SL fitness")

        plt.subplot(2, 2, 2)
        m = np.array(self.population.substrate_history)[1:].T
        for i in m:
            plt.plot(factor * i)
        plt.legend([i.evolution_method for i in self.substrates])
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("Fitness of each substrate")

        plt.subplot(2, 1, 2)
        prob_data = np.array(self.population.substrate_w_history).T
        plt.stackplot(range(prob_data.shape[1]), prob_data, labels=[i.evolution_method for i in self.substrates])
        plt.legend()
        plt.xlabel("generations")
        plt.ylabel("probability")
        plt.title("Probability of each substrate")

        if show_plots:
            plt.show()

        if filename is not None:
            plt.savefig(filename)

    """
    Version of the summary for the dynamic variant
    """

    def display_report_nodyn(self, show_plots=True, filename=None):
        factor = 1
        if self.objfunc.opt == "min":
            factor = -1

        # Print Info
        print("Number of generations:", len(self.history))
        print("Real time spent: ", round(self.real_time_spent, 5), "s", sep="")
        print("CPU time spent: ", round(self.time_spent, 5), "s", sep="")
        print("Number of fitness evaluations:", self.objfunc.counter)
        print(f"\tSubstrate probability:")
        subs_names = [i.evolution_method for i in self.substrates]
        weights = [round(i, 6) for i in self.population.substrate_weight]
        adjust = max([len(i) for i in subs_names])
        for idx, val in enumerate(subs_names):
            print(f"\t\t{val}:".ljust(adjust + 3, " ") + f"{weights[idx]}")

        best_fitness = self.population.best_solution()[1]
        print("Best fitness:", best_fitness)

        # Plot fitness history
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle("CRO_SL")
        plt.subplot(1, 2, 1)

        plt.plot(self.history, "blue")
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("CRO_SL fitness")

        plt.subplot(1, 2, 2)
        m = np.array(self.population.substrate_history)[1:].T
        for i in m:
            plt.plot(factor * i)
        plt.legend([i.evolution_method for i in self.substrates])
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("Fitness of each substrate")

        if show_plots:
            plt.show()

        if filename is not None:
            plt.savefig(filename)

    def calculate_fitness_tf_batch(self, corals):
        X_train_, Y_train_, M, depth, n_attributes, n_classes = self.data

        solutions = [i.solution for i in corals]
        if self.is_univariate:
            accuracies = tft.dt_matrix_fit_batch_univariate_nb(solutions, X_train_, Y_train_, depth,
                                                               n_classes, M, len(X_train_), len(corals)).numpy()
        else:
            accuracies = tft.dt_matrix_fit_batch_multivariate_nb(solutions, X_train_, Y_train_, depth,
                                                                 n_classes, M, len(X_train_), len(corals)).numpy()

        for coral, accuracy in zip(corals, accuracies):
            coral.fitness_calculated = True
            coral.fitness = accuracy
        self.objfunc.counter += len(corals)