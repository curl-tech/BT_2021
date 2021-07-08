from deap import base, creator, tools, algorithms
import random
import numpy


class Solver:
    def __init__(self):
        #Basic toolbox setup 
        random.seed(88)        
        self.toolbox = base.Toolbox()
        self.toolbox.register("zeroOrOne", random.randint, 0, 1)
        
        #Make ga creator know fitness
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        #Setup toolbox params
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.hof = tools.HallOfFame(1)
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("max", numpy.max)
        self.stats.register("avg", numpy.mean)

    def gettoolbox(self):
        return (self.toolbox)
    
    def registerfitness(self,callbackfn,fitnesslength):
        self.toolbox.register("evaluate", callbackfn)
        self.toolbox.register("individualCreator", tools.initRepeat, creator.Individual, self.toolbox.zeroOrOne, fitnesslength)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/fitnesslength)
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)
        # This is the generation 0 and a must be preserved to initiate any run
        self.population = self.toolbox.populationCreator(n=50)

    def run(self):
        # perform simple ga with all the setup already done
        algorithms.eaSimple(self.population, self.toolbox, cxpb=0.9, mutpb=0.1,
                        ngen=50, verbose=False, stats=self.stats, halloffame=self.hof)
