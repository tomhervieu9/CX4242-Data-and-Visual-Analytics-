import csv
import numpy as np
import ast
import random
from collections import Counter
import random
import copy
import csv


class RandomForest(object):
	class __DecisionTree():

		def learn(self,X,y):
			attributes = range(0,(len(X[0])))
			nextAttribute = len(X[0])
			self.default = 1
			self.tree = self.createDecisionTree(X, attributes, y, len(X))

		def createDecisionTree(self, data, attributeList, targetAttributes, trainSetSize):
			completed = []
			keyVals = []
			checked = {}
			labels = targetAttributes
			if (((len(data)*1.0)/trainSetSize) < 0.01): 			# Modification: pruning if data is less than 3% in size of the training data
				return Counter([attr for attr in targetAttributes]).most_common(1)[0][0]
			if (labels.count(labels[0]) == len(labels)): 			#this is where the next attribute index to split on is decided - without replacement
				return labels[0]
			if (len(attributeList) > -1): 
				nextNum = random.randint(0, len(attributeList)-1)		
				while nextNum in completed:
					nextNum = random.randint(0, len(attributeList)-1)
					completed.append(nextNum)
			else:
				nextNum = attributeList[-1]
				del attributeList[-1]
			tree = {nextNum : {}}
			print tree
			for i in range(0, len(data)):
				if data[i][nextNum] not in checked:
					checked[data[i][nextNum]] = 1
					keyVals.append(data[i][nextNum])
			for val in keyVals:
				subData = []
				for i in range(0, len(data)):
					if (data[i][nextNum] == val):
						subData.append(data[i])
				branch = self.createDecisionTree(subData, attributeList, targetAttributes, trainSetSize)
				tree[nextNum][val] = branch
			return tree		

		def classify(self, record):
			quality = self.classifyHelper(self.tree, record, [0])	
			if quality is None:
				quality = self.default		
			return quality

		def classifyHelper(self, tree, obj, count):
			if (tree is None):
				return None 
			if (not isinstance (tree, dict)):
				return tree
			rootAttribute = tree.keys()[0]
			subTrees = tree.values()[0]			 
			branchCount = len(tree.values()[0])
			if (branchCount > count[0]):
				count[0] = branchCount
			rootAttributeValue = obj[rootAttribute]
			if rootAttributeValue not in subTrees:
				return None
			return self.classifyHelper(subTrees[rootAttributeValue], obj, count)

		def __init__(self):
			self.tree = {}
		
		default = 0
               
	num_trees = 0
	decision_trees = []
	bootstraps_datasets = [] # the bootstrapping dataset for trees
	bootstraps_labels = []   # the true class labels,
                             # corresponding to records in the bootstrapping dataset 
	def __init__(self, num_trees):
		self.num_trees = num_trees
		self.decision_trees = [self.__DecisionTree() for i in range(num_trees)]
	
	def _bootstrapping(self, XX, n):
		# TODO: create a sample dataset with replacement of size n
		#
		# Note that you will also need to record the corresponding
		#           class labels for the sampled records for training purpose.
		#
		# Referece: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
		X = []
		y = []
		for i in range(n):
			r = random.randint(0,len(XX)-1)
			X.append(XX[r][:-1])
			y.append(XX[r][-1])
		return X, y

	def bootstrapping(self, XX):
		for i in range(self.num_trees):
			sample, label = self._bootstrapping(XX, len(XX))
			self.bootstraps_datasets.append(sample)
			self.bootstraps_labels.append(label)

	def fitting(self):
		# TODO: train `num_trees` decision trees using the bootstraps datasets and labels
		for i in range(self.num_trees):
			self.decision_trees[i].learn(self.bootstraps_datasets[i], self.bootstraps_labels[i])

	def voting(self, X):
		y = np.array([], dtype = int)
		for record in X:
			# TODO: find the sets of proper trees that consider the record
			#       as an out-of-bag sample, and predict the label(class) for the record.
			#       The majority vote serves as the final label for this record.
			votes = []
			for i in range(len(self.bootstraps_datasets)):
				dataset = self.bootstraps_datasets[i]
				if not any((record == x).all() for x in dataset):
					oobTree = self.decision_trees[i]
					effective_vote = oobTree.classify(record)
					votes.append(effective_vote)
			counts = np.bincount(votes)
			if len(counts) == 0:
				pass
			else:
				y = np.append(y, np.argmax(counts))
		return y

def main():
	X = list()
	y = list()
	XX = list() # Contains data features and data labels

	# Note: you must NOT change the general steps taken in this main() function.

	# Load data set
	with open("hw4-data.csv") as f:
		next(f, None)
		for line in csv.reader(f, delimiter = ","):
			X.append(line[:-1])
			y.append(line[-1])
			xline = [ast.literal_eval(i) for i in line]
			XX.append(xline[:])
	# Initialize according to your implementation
	forest_size = 10
	# Initialize a random forest
	randomForest = RandomForest(forest_size)
	# Create the bootstrapping datasets
	randomForest.bootstrapping(XX)
	# Build trees in the forest
	randomForest.fitting()
	y_truth = np.array(y, dtype = int)
	X = np.array(X, dtype = float)
	y_predicted = randomForest.voting(X)
	#results = [prediction == truth for prediction, truth in zip(y_predicted, y_test)]
	results = [prediction == truth for prediction, truth in zip(y_predicted, y_truth)]
	accuracy = float(results.count(True)) / float(len(results))
	print "accuracy: %.4f" % accuracy

main()