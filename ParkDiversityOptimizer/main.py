from park import Park
from solver import Solver

def main():
    configfile = './config.hjson'
    mypark = Park(configfile)
    #This has to be on nonclass level
    def myparkValue(individual):
        return mypark.getvalue_for_chosen(individual),  # tuple

    #Run solver
    gasolver = Solver()
    gasolver.registerfitness(myparkValue, len(mypark))
    gasolver.run()

    #Make a new park using results
    print("-- New Park Created --")
    newpark = mypark.make_child(gasolver.hof.items[0])
    newpark.print()


if __name__ == "__main__":
    main()