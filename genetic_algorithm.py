import random
from datetime import datetime

class Population():
    def __init__(self):
        self.Individual = list()
        self.popSize = 0

    def randomPop(self, numGenes, popSize):
        self.popSize = popSize
        for i in range(popSize):
            random.seed(datetime.now())
            self.Individual_Class = Individual()
            self.Individual.append(self.Individual_Class.new_Individual(numGenes))

    def null_population(self, popSize):
        self.popSize = popSize
        for i in range(self.popSize):
            self.Individual.append(None)

    def setIndividual(self, individual, position):
        self.Individual[position] = individual

    def setNextIndividual(self, individual):
        for i in range(self.popSize):
            if self.Individual[i] == None:
                self.Individual[i] = individual
                return

    def hasSolution(self, solution):
        found = None
        for j in range(len(self.Individual)):
            if self.Individual[j].genes == solution:
                found = self.Individual[j]
                break
        if found == None:
            return False
        return found

    def sortPopulation(self):
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(self.Individual)-1):
                if self.Individual[i].fitness < self.Individual[i + 1].fitness:
                    temp = self.Individual[i]
                    self.Individual[i] = self.Individual[i + 1]
                    self.Individual[i + 1] = temp
                    swapped = True

    def getNumIndividuals(self):
        return len(self.Individual)

class Individual():
    def __init__(self):
        self.genes = ''
        self.fitness = 0
        self.Data = Data()
        self.numGenes = len(self.Data.phrase)

    def new_Individual(self, numGenes):
        self.genes = ''
        characters = self.Data.characters
        for i in range(self.numGenes):
            self.genes += characters[random.randint(0, (len(characters)-1))]
        self.calculateFitness()
        return self

    def mutateIndividual(self, genes):
        self.genes = genes
        if random.uniform(0,1) <= self.Data.mutationRate:
            characters = self.Data.characters
            newGene = ''
            randomPos = random.randint(0, len(genes))
            for i in range(len(genes)):
                if i == randomPos:
                    newGene += characters[random.randint(0, len(characters)-1)]
                else:
                    newGene += genes[i]
            self.genes = newGene
        self.calculateFitness()
        return

    def calculateFitness(self):
        solution = self.Data.phrase
        for i in range(len(solution)):
            if solution[i] == self.genes[i]:
                self.fitness += 1
        return

class Data():
    def __init__(self):
        self.phrase = 'Encoinfo'  # The target phrase for the GA to find
        self.characters = "!,.:;?áÁãÃâÂõÕôÔóÓéêÉÊíQWERTYUIOPASDFGHJKLÇZXCVBNMqwertyuiopasdfghjklçzxcvbnm1234567890 "
        self.mutationRate = 0.43

    def newGeneration(self, population, elitism):
        newPopulation = Population()
        if elitism:
            newPopulation.Individual.append(population.Individual[0])

        while newPopulation.getNumIndividuals() < len(population.Individual):
            parents = self.tournamentSelection(population)
            children = self.crossover(parents[0], parents[1])
            newPopulation.Individual.append(children[0])
            newPopulation.Individual.append(children[1])

        newPopulation.sortPopulation()
        return newPopulation

    def crossover(self, ind1, ind2):
        cutPoint = random.randint(0, (len(ind1.genes)))
        while cutPoint == 0 or cutPoint == len(ind1.genes):
            cutPoint = random.randint(0, (len(ind1.genes)))

        children = [Individual(), Individual()]
        parent1Genes = ind1.genes
        parent2Genes = ind2.genes

        child1Genes = parent1Genes[:cutPoint] + parent2Genes[cutPoint:]
        child2Genes = parent2Genes[:cutPoint] + parent1Genes[cutPoint:]

        children[0].mutateIndividual(child1Genes)
        children[1].mutateIndividual(child2Genes)

        return children

    def tournamentSelection(self, population):
        intermediatePopulation = Population()
        intermediatePopulation.null_population(3)

        intermediatePopulation.setNextIndividual(population.Individual[random.randint(0, len(population.Individual)-1)])
        intermediatePopulation.setNextIndividual(population.Individual[random.randint(0, len(population.Individual)-1)])
        intermediatePopulation.setNextIndividual(population.Individual[random.randint(0, len(population.Individual)-1)])

        intermediatePopulation.sortPopulation()

        parents = [intermediatePopulation.Individual[0], intermediatePopulation.Individual[1]]

        return parents

def main():
    print('Starting Genetic Algorithm')
    data = Data()

    popSize = 6
    numGenes = len(data.phrase)
    print('Creating initial population')
    population = Population()
    population.randomPop(numGenes, popSize)
    solutionFound = False
    generation = 0

    while not solutionFound:
        print('Generation: %d' % generation)
        generation += 1
        print('Creating new generation from the fittest individuals...')
        population = data.newGeneration(population, True)
        print('Fittest individual generated: %s' % (population.Individual[0].genes))
        print('Checking for solution')
        solutionFound = population.hasSolution(data.phrase)
        if solutionFound:
            print('Solution: %s' % solutionFound.genes)
            print('Solution found in generation %d' % generation)
            break
        print('Solution not found\n')

main()
