# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        weight = None
        score= 0
        w = self.weights
        # Go over each value within the constant C
        for c in Cgrid:
            for iter in range(self.max_iterations):
                print "Starting iteration: ", iter
                for i in range(len(trainingData)):
                    update = util.Counter()
                    for iterlabel in self.legalLabels:
                        update[iterlabel] = w[iterlabel] * trainingData[i]
                    nextLabel = update.argMax()
                    if trainingLabels[i] == nextLabel:
                        continue
                    # determine tau for the minimum update
                    t = (w[nextLabel] - w[trainingLabels[i]]) * trainingData[i] + 1.0
                    t = t / ((trainingData[i] * trainingData[i]) * 2)
                    t = min(c, t)
                    # update Wy and Wy*
                    for feature in self.features:
                        w[trainingLabels[i]][feature] = w[trainingLabels[i]][feature] + t * trainingData[i][feature]
                        w[nextLabel][feature] = w[nextLabel][feature] - t * trainingData[i][feature]
            # classify data and count correct labels
            tempCorrect = self.count_temps(self.classify(validationData), validationLabels)
            if tempCorrect < score:
                continue
            score = tempCorrect
            weight = w
        if weight == None:
            return
        w = weight

    def count_temps(self, guesses, validationLabels):
        temps = 0
        for i in range(len(guesses)):
            if(guesses[i] != validationLabels[i]):
                continue
            temps += 1;
        return temps

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


