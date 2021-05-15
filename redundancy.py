
from deap import base
from deap import gp

from primitives import KilobotsPrimitiveSetTyped
from nodes import KilobotNodes



class Redundancy():
	
	chromosomes = []
	results = []

	sequenceNodes = ["seqm2", "seqm3", "seqm4"]
	fallbackNodes = ["selm2", "selm3", "selm4"]
	probabilityNodes = ["probm2", "probm3", "probm4"]
	conditionNodes = ["ifgevar", "ifltvar", "ifgecon", "ifltcon"]
	compositeNodes = ["ifgevar", "ifltvar", "ifgecon", "ifltcon", "set"]
	decoratorNodes = ["successd", "failured", "repeat"]
	actionNodes = ["ml", "mr", "mf", "set"]
	actuationNodes = ["ml", "mr", "mf"]
	successNodes = ["successl", "successd", "ml", "mr", "mf", "set"]
	failureNodes = ["failurel", "failured"]

	
	blackboard = ['0.0', '0.0', '0.0', '0.0']

	active = [True]
	output = []
	trailingNodesList = []
	repeatNodes = []
	composites = []


	def __init__(self):
		self.primitivetree = gp.PrimitiveTree([])
		self.pset = KilobotsPrimitiveSetTyped("MAIN", [], str)
		nodes = KilobotNodes(self.pset)
		# self.addChromosomes()
		self.addTests()

	def resetLists(self):
		self.output[:] = []
		self.composites[:] = []
		self.trailingNodesList[:] = []
		self.active = [True]
		self.blackboard = ['0.0', '0.0', '0.0', '0.0']
		self.repeatNodes = []

	def addTests(self):
		self.tests = []
		self.tests.append({"chromosome": "repeat(seqm2(selm4(probm3(mr, mr, mr), probm2(ifgecon(5, 0.707), ifltcon(2, 0.775)), ifgevar(5, 5), failurel), selm3(seqm4(mf, successl, mf, ifgevar(4, 6)), seqm4(mf, ifgevar(5, 2), failurel, mr), selm4(ifltvar(6, 3), mf, ifgecon(3, 0.405), ml))), 2)",
								 "capitalised": "repeat(seqm2(selm4(probm3(mr, mr, mr), PROBM2(IFGECON(5, 0.707), IFLTCON(2, 0.775)), IFGEVAR(5, 5), FAILUREL), selm3(seqm4(mf, successl, mf, ifgevar(4, 6)), seqm4(mf, ifgevar(5, 2), failurel, MR), selm4(ifltvar(6, 3), mf, IFGECON(3, 0.405), ML))), 2)",
								 "trimmed": ['repeat', 'seqm2', 'selm4', 'probm3', 'mr', 'mr', 'mr', 'selm3', 'seqm4', 'mf', 'successl', 'mf', 'ifgevar', 'seqm4', 'mf', 'ifgevar', 'failurel', 'selm4', 'ifltvar', 'mf'],
								 "ratio": 0.714285714286})
		self.tests.append({"chromosome": "seqm4(successd(selm3(ifltvar(4, 8), mr, mf)), selm3(ifltvar(4, 8), mr, mr), seqm4(mf, failurel, ifltvar(2, 4), ifltvar(1, 4)), probm3(mf, failurel, mr))",
								 "capitalised": "seqm4(successd(selm3(ifltvar(4, 8), mr, MF)), selm3(ifltvar(4, 8), mr, MR), seqm4(mf, FAILUREL, IFLTVAR(2, 4), IFLTVAR(1, 4)), PROBM3(MF, FAILUREL, MR))",
								 "trimmed": ['seqm4', 'successd', 'selm3', 'ifltvar', 'mr', 'selm3', 'ifltvar', 'mr', 'seqm4', 'mf'],
								 "ratio": 0.526315789474})
		self.tests.append({"chromosome": "seqm4(seqm3(mf, seqm3(successl, ml, mf), mf), ifgevar(4, 4), successl, seqm4(mf, ifgecon(4, -0.50), ml, successl))",
								 "capitalised": "seqm4(seqm3(mf, seqm3(successl, ml, mf), mf), ifgevar(4, 4), successl, seqm4(mf, ifgecon(4, -0.5), ml, SUCCESSL))",
								 "trimmed": ['seqm4', 'seqm3', 'mf', 'seqm3', 'successl', 'ml', 'mf', 'mf', 'ifgevar', 'successl', 'seqm4', 'mf', 'ifgecon', 'ml'],
								 "ratio": 0.933333333333})
		self.tests.append({"chromosome": "failured(selm4(selm3(failured(ml), failured(failurel), selm4(mf, ml, mf, ifltcon(1, -0.43))), mr, probm3(probm2(ifltvar(7, 5), ifgevar(5, 9)), probm3(ifgevar(4, 8), mf, ifltvar(2, 2)), selm2(set(1, 0.581), successl)), probm3(seqm2(ifgevar(9, 8), mr), successd(ml), seqm4(mr, ifgevar(1, 7), ifltvar(9, 2), mr))))",
								 "capitalised": "failured(selm4(selm3(failured(ml), failured(FAILUREL), selm4(mf, ML, MF, IFLTCON(1, -0.43))), mr, PROBM3(PROBM2(IFLTVAR(7, 5), IFGEVAR(5, 9)), PROBM3(IFGEVAR(4, 8), MF, IFLTVAR(2, 2)), SELM2(SET(1, 0.581), SUCCESSL)), PROBM3(SEQM2(IFGEVAR(9, 8), MR), SUCCESSD(ML), SEQM4(MR, IFGEVAR(1, 7), IFLTVAR(9, 2), MR))))",
								 "trimmed": ['failured', 'selm4', 'selm3', 'failured', 'ml', 'failured', 'selm4', 'mf'],
								 "ratio": 0.228571428571})
		self.tests.append({"chromosome": "probm3(repeat(seqm4(successl, mf, mr, mf), 9), repeat(seqm4(successl, mf, mr, mf), 9), probm4(repeat(seqm4(successl, mf, mr, mf), 9), seqm4(successl, set(1, 0.505), ifgevar(6, 6), mr), probm4(ifgevar(8, 2), ifltcon(1, -0.30), mf, ifgevar(2, 1)), ifgevar(2, 1)))",
								 "capitalised": "probm3(repeat(seqm4(successl, mf, mr, mf), 9), repeat(seqm4(successl, mf, mr, mf), 9), probm4(repeat(seqm4(successl, mf, mr, mf), 9), seqm4(successl, set(1, 0.505), ifgevar(6, 6), mr), probm4(ifgevar(8, 2), ifltcon(1, -0.3), mf, ifgevar(2, 1)), ifgevar(2, 1)))",
								 "trimmed": ['probm3', 'repeat', 'seqm4', 'successl', 'mf', 'mr', 'mf', 'repeat', 'seqm4', 'successl', 'mf', 'mr', 'mf', 'probm4', 'repeat', 'seqm4', 'successl', 'mf', 'mr', 'mf', 'seqm4', 'successl', 'set', 'ifgevar', 'mr', 'probm4', 'ifgevar', 'ifltcon', 'mf', 'ifgevar', 'ifgevar'],
								 "ratio": 1.0})
		self.tests.append({"chromosome": "seqm3(ifltcon(8, 0.877), seqm4(mf, ifgevar(8, 1), selm2(ifltcon(4, -0.77), mr), successl), selm2(ifltcon(4, -0.77), mr))",
								 "capitalised": "seqm3(ifltcon(8, 0.877), seqm4(mf, ifgevar(8, 1), selm2(ifltcon(4, -0.77), mr), successl), selm2(ifltcon(4, -0.77), mr))",
								 "trimmed": ['seqm3', 'ifltcon', 'seqm4', 'mf', 'ifgevar', 'selm2', 'ifltcon', 'mr', 'successl', 'selm2', 'ifltcon', 'mr'],
								 "ratio": 1.0})
		self.tests.append({"chromosome": "seqm4(successd(seqm2(ifltcon(4, -0.61), ml)), failured(seqm4(mr, mf, successl, ifltcon(2, 0.752))), seqm4(mr, probm4(ifgevar(4, 6), mr, probm3(ifgevar(2, 5), probm3(ifgevar(2, 5), set(2, -0.53), successl), probm3(ifltvar(5, 4), mf, successl)), mr), probm3(set(1, -0.49), selm2(failurel, ifltcon(1, 0.936)), successd(ifgevar(1, 9))), mf), probm3(ifgevar(2, 5), probm3(ifgevar(2, 5), probm3(ifgevar(2, 5), set(2, -0.53), successl), probm3(ifltvar(5, 4), ifgevar(7, 2), successl)), probm3(ifltvar(5, 4), probm3(ifgevar(2, 5), probm3(ifgevar(2, 5), mr, successl), probm3(ifltvar(5, 4), successl, successl)), successl)))",
								 "capitalised": "seqm4(successd(seqm2(ifltcon(4, -0.61), ml)), failured(seqm4(mr, mf, SUCCESSL, IFLTCON(2, 0.752))), SEQM4(MR, PROBM4(IFGEVAR(4, 6), MR, PROBM3(IFGEVAR(2, 5), PROBM3(IFGEVAR(2, 5), SET(2, -0.53), SUCCESSL), PROBM3(IFLTVAR(5, 4), MF, SUCCESSL)), MR), PROBM3(SET(1, -0.49), SELM2(FAILUREL, IFLTCON(1, 0.936)), SUCCESSD(IFGEVAR(1, 9))), MF), PROBM3(IFGEVAR(2, 5), PROBM3(IFGEVAR(2, 5), PROBM3(IFGEVAR(2, 5), SET(2, -0.53), SUCCESSL), PROBM3(IFLTVAR(5, 4), IFGEVAR(7, 2), SUCCESSL)), PROBM3(IFLTVAR(5, 4), PROBM3(IFGEVAR(2, 5), PROBM3(IFGEVAR(2, 5), MR, SUCCESSL), PROBM3(IFLTVAR(5, 4), SUCCESSL, SUCCESSL)), SUCCESSL)))",
								 "trimmed": ['seqm4', 'successd', 'seqm2', 'ifltcon', 'ml', 'failured', 'seqm4', 'mr', 'mf'],
								 "ratio": 0.15})
		self.tests.append({"chromosome": "seqm4(repeat(mf, 7), successd(mr), mr, selm3(probm2(mr, ifltcon(5, -0.60)), mr, successl))",
								 "capitalised": "seqm4(repeat(mf, 7), successd(mr), mr, selm3(probm2(mr, ifltcon(5, -0.6)), mr, SUCCESSL))",
								 "trimmed": ['seqm4', 'repeat', 'mf', 'successd', 'mr', 'mr', 'selm3', 'probm2', 'mr', 'ifltcon', 'mr'],
								 "ratio": 0.916666666667})
		self.tests.append({"chromosome": "selm3(seqm4(ml, mf, ifgecon(4, 0.193), seqm4(ml, mf, ifltcon(1, 0.857), ifgevar(1, 9))), mf, probm4(ifltcon(1, 0.857), mf, mf, mf))",
								 "capitalised": "selm3(seqm4(ml, mf, ifgecon(4, 0.193), seqm4(ml, mf, ifltcon(1, 0.857), ifgevar(1, 9))), mf, PROBM4(IFLTCON(1, 0.857), MF, MF, MF))",
								 "trimmed": ['selm3', 'seqm4', 'ml', 'mf', 'ifgecon', 'seqm4', 'ml', 'mf', 'ifltcon', 'ifgevar', 'mf'],
								 "ratio": 0.6875})
		self.tests.append({"chromosome": "selm2(seqm4(seqm2(mf, ifgecon(2, -0.01)), failured(ml), mf, seqm4(set(2, 0.406), mr, mr, ifltvar(3, 6))), seqm4(mf, ifgecon(2, -0.01), seqm3(ifltcon(4, 0.669), mf, mf), seqm2(ifltcon(5, -0.76), ifltcon(7, -0.68))))",
								 "capitalised": "selm2(seqm4(seqm2(mf, ifgecon(2, -0.01)), failured(ml), MF, SEQM4(SET(2, 0.406), MR, MR, IFLTVAR(3, 6))), seqm4(mf, ifgecon(2, -0.01), seqm3(ifltcon(4, 0.669), mf, mf), SEQM2(IFLTCON(5, -0.76), IFLTCON(7, -0.68))))",
								 "trimmed": ['selm2', 'seqm4', 'seqm2', 'mf', 'ifgecon', 'failured', 'ml', 'seqm4', 'mf', 'ifgecon', 'seqm3', 'ifltcon', 'mf', 'mf'],
								 "ratio": 0.608695652174})
		self.tests.append({"chromosome": "selm4(failured(ml), seqm4(set(2, -0.48), mf, seqm4(seqm4(mf, mf, ifgevar(4, 2), ml), probm4(seqm4(ifltvar(9, 2), successl, mr, ifltvar(9, 2)), seqm2(mf, set(1, -0.17)), selm3(mr, ifgevar(7, 9), ml), seqm3(ifgecon(1, -0.35), successl, ifgevar(2, 7))), mf, ifgevar(4, 5)), failured(ml)), successl, failurel)",
								 "capitalised": "selm4(failured(ml), seqm4(set(2, -0.48), mf, seqm4(seqm4(mf, mf, ifgevar(4, 2), ml), probm4(seqm4(ifltvar(9, 2), successl, mr, ifltvar(9, 2)), seqm2(mf, set(1, -0.17)), selm3(mr, IFGEVAR(7, 9), ML), seqm3(ifgecon(1, -0.35), successl, ifgevar(2, 7))), mf, ifgevar(4, 5)), failured(ml)), SUCCESSL, FAILUREL)",
								 "trimmed": ['selm4', 'failured', 'ml', 'seqm4', 'set', 'mf', 'seqm4', 'seqm4', 'mf', 'mf', 'ifgevar', 'ml', 'probm4', 'seqm4', 'ifltvar', 'successl', 'mr', 'ifltvar', 'seqm2', 'mf', 'set', 'selm3', 'mr', 'seqm3', 'ifgecon', 'successl', 'ifgevar', 'mf', 'ifgevar', 'failured', 'ml'],
								 "ratio": 0.885714285714})
		self.tests.append({"chromosome": "selm4(seqm4(mr, set(1, -0.67), seqm4(ifgevar(1, 4), selm2(ml, mr), mf, successl), mf), seqm4(mr, successl, seqm4(set(1, 0.678), set(1, -0.15), mf, set(1, 0.497)), mf), probm2(successl, mr), seqm4(mf, set(1, -0.15), ml, ml))",
								 "capitalised": "selm4(seqm4(mr, set(1, -0.67), seqm4(ifgevar(1, 4), selm2(ml, MR), mf, successl), mf), seqm4(mr, successl, seqm4(set(1, 0.678), set(1, -0.15), mf, set(1, 0.497)), mf), PROBM2(SUCCESSL, MR), SEQM4(MF, SET(1, -0.15), ML, ML))",
								 "trimmed": ['selm4', 'seqm4', 'mr', 'set', 'seqm4', 'ifgevar', 'selm2', 'ml', 'mf', 'successl', 'mf', 'seqm4', 'mr', 'successl', 'seqm4', 'set', 'set', 'mf', 'set', 'mf'],
								 "ratio": 0.689655172414})
		self.tests.append({"chromosome": "seqm3(probm2(mr, successl), mf, seqm3(seqm3(successl, successl, ifgecon(9, 0.165)), failured(seqm3(probm3(successl, successd(mr), probm3(ifltcon(4, 0.550), ifgevar(5, 9), mf)), failured(ifgecon(9, -0.01)), probm2(probm3(successd(mr), ifgevar(6, 4), ifltvar(5, 8)), selm3(ifgecon(6, -0.91), ml, ifgecon(2, 0.091))))), ml))",
								 "capitalised": "seqm3(probm2(mr, successl), mf, seqm3(seqm3(successl, successl, ifgecon(9, 0.165)), failured(seqm3(probm3(successl, successd(mr), probm3(ifltcon(4, 0.55), ifgevar(5, 9), mf)), FAILURED(IFGECON(9, -0.01)), PROBM2(PROBM3(SUCCESSD(MR), IFGEVAR(6, 4), IFLTVAR(5, 8)), SELM3(IFGECON(6, -0.91), ML, IFGECON(2, 0.091))))), ML))",
								 "trimmed": ['seqm3', 'probm2', 'mr', 'successl', 'mf', 'seqm3', 'seqm3', 'successl', 'successl', 'ifgecon', 'failured', 'seqm3', 'probm3', 'successl', 'successd', 'mr', 'probm3', 'ifltcon', 'ifgevar', 'mf'],
								 "ratio": 0.606060606061})
		self.tests.append({"chromosome": "probm2(seqm4(mf, mf, mr, mf), successd(seqm2(mf, seqm4(mf, set(2, -0.97), mr, mf))))",
								 "capitalised": "probm2(seqm4(mf, mf, mr, mf), successd(seqm2(mf, seqm4(mf, set(2, -0.97), mr, mf))))",
								 "trimmed": ['probm2', 'seqm4', 'mf', 'mf', 'mr', 'mf', 'successd', 'seqm2', 'mf', 'seqm4', 'mf', 'set', 'mr', 'mf'],
								 "ratio": 1.0})
		self.tests.append({"chromosome": "successd(selm2(seqm3(mf, mf, seqm3(mr, set(2, 0.272), mf)), probm2(failurel, seqm4(ifgevar(7, 4), mr, ifgecon(3, -0.49), ifgevar(7, 7)))))",
								 "capitalised": "successd(selm2(seqm3(mf, mf, seqm3(mr, set(2, 0.272), mf)), PROBM2(FAILUREL, SEQM4(IFGEVAR(7, 4), MR, IFGECON(3, -0.49), IFGEVAR(7, 7)))))",
								 "trimmed": ['successd', 'selm2', 'seqm3', 'mf', 'mf', 'seqm3', 'mr', 'set', 'mf'],
								 "ratio": 0.5625})								 
		self.tests.append({"chromosome": "seqm4(ml, probm2(set(2, 0.550), ifgevar(3, 6)), selm4(mf, ifgevar(6, 2), mf, probm2(set(2, 0.550), ifgevar(3, 6))), mf)",
								 "capitalised": "seqm4(ml, probm2(set(2, 0.55), ifgevar(3, 6)), selm4(mf, IFGEVAR(6, 2), MF, PROBM2(SET(2, 0.55), IFGEVAR(3, 6))), mf)",
								 "trimmed": ['seqm4', 'ml', 'probm2', 'set', 'ifgevar', 'selm4', 'mf', 'mf'],
								 "ratio": 0.615384615385})

	def redundancyTests(self):
		
		for i in range(0,16,1):
			
			print i
			
			# test = self.getChromosome(i)
			chromosome = self.tests[i]["chromosome"]
					
			tree = self.primitivetree.from_string(chromosome, self.pset)			
			rType = tree.root.ret
			
			if tree[0] in self.pset.primitives[rType] or tree[0] in self.pset.decorators[rType]:
				
				# greedy				
				self.resetLists()	
				self.parseSubtreeGreedy(tree)
				self.trailingNodesGreedy(tree)
				self.capitaliseOutput()				
				chromosome = self.rebuildChromosome()
				
				# lazy				
				self.resetLists()				
				self.parseSubtreeLazy(tree)				
				self.trailingNodesLazy(tree)
				self.removeConstants()
				
				# verify results	
				ratio = self.calculateRatio(tree)
				self.checkResult(i, tree, ratio, chromosome)
				
			else:
				print "Invalid tree"
	
	def checkResult(self, i, tree, ratio, chromosome):
		
		# chromosomeMatches = self.checkChromosome(i, chromosome)
		# outputMatches = self.checkOutput(i)
		# ratioMatches = self.checkRatio(i, ratio)
		
		chromosomeMatches = chromosome == self.tests[i]["capitalised"]
		outputMatches = self.output == self.tests[i]["trimmed"]
		ratioMatches = str(ratio) == str(self.tests[i]["ratio"])
		
		if not chromosomeMatches or not outputMatches or not ratioMatches:
			print ""
			print chromosomeMatches
			print outputMatches
			print ratioMatches
			print ""
			print str(tree)+"\n"
			print str(chromosome)+"\n"
			print str(self.output)+"\n"
			self.printRatioCalculation(tree)
			print ""

	def checkRedundancy(self, chromosome):
		
		tree = self.primitivetree.from_string(chromosome, self.pset)			
		rType = tree.root.ret
		
		if tree[0] in self.pset.primitives[rType] or tree[0] in self.pset.decorators[rType]:
			
			# greedy				
			self.resetLists()	
			self.parseSubtreeGreedy(tree)
			self.trailingNodesGreedy(tree)
			self.capitaliseOutput()				
			chromosome = self.rebuildChromosome()
			
			# lazy				
			self.resetLists()				
			self.parseSubtreeLazy(tree)				
			self.trailingNodesLazy(tree)
			self.removeConstants()
			
			# print results	
			print str(tree)+"\n"
			print str(chromosome)+"\n"
			print str(self.output)+"\n"
			self.printRatioCalculation(tree)
			
		else:
			print "Invalid tree"

	def parseSubtreeLazy(self, tree):
		
		returnStatus = "ambiguous"
		
		self.output.append(tree[0].name)
		self.trailingNodesList.append(self.active[-1])
		
		if tree[0].name == "repeat": self.repeatNodes.append("repeat")
					
		if tree[0].name in self.compositeNodes or len(tree) == 1:
			returnStatus = self.parseLeaf(tree)
				
		else:
			
			sequenceStatus = "success"
			
			lenCount = 1
			self.active.append(self.active[-1])
				
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				if tree[0].name in ["successd", "failured"]:
					activity = self.parseSubtreeActivity(tree)
					returnStatus = "success" if tree[0].name == "successd" else "failure"
					if not activity: self.active[-1] = False
				
				status = self.parseSubtreeLazy(subtree)
				
				if tree[0].name in self.sequenceNodes and status == "failure":
					sequenceStatus = "failure"
					self.active[-1] = False
				if tree[0].name in self.sequenceNodes and status == "ambiguous":
					sequenceStatus = "ambiguous" if sequenceStatus != "failure" else "failure"
				if tree[0].name in self.fallbackNodes and status == "success":
					returnStatus = "success"
					self.active[-1] = False
				if tree[0].name in self.probabilityNodes: returnStatus = self.parseProbabilityNode(status)
				if tree[0].name == "successd": returnStatus = "success"
				if tree[0].name == "failured": returnStatus = "failure"
				if tree[0].name == "repeat": 
					if lenCount > len(subtree) + 1: 
						self.trailingNodesList[-1] = False
					returnStatus = status
			self.active.pop()
			
		if tree[0].name in self.sequenceNodes: return sequenceStatus
		else: return returnStatus

	def parseSubtreeGreedy(self, tree):
		
		returnStatus = "ambiguous"
		
		if self.active[-1] == True: self.output.append(tree[0].name)
		# else: self.output.append(tree[0].name.upper())
		else: self.output.append(tree[0].name)
		self.trailingNodesList.append(self.active[-1])
		
		if tree[0].name in self.compositeNodes or len(tree) == 1:
			returnStatus = self.parseLeaf(tree)
				
		else:
			
			sequenceStatus = "success"
			
			lenCount = 1
			self.active.append(self.active[-1])
				
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				if tree[0].name in ["successd", "failured"]:
					activity = self.parseSubtreeActivity(tree)
					returnStatus = "success" if tree[0].name == "successd" else "failure"
					if not activity: self.active[-1] = False
				
				status = self.parseSubtreeGreedy(subtree)
				
				if tree[0].name in self.sequenceNodes and status == "failure":
					sequenceStatus = "failure"
					self.active[-1] = False
				if tree[0].name in self.sequenceNodes and status == "ambiguous":
					sequenceStatus = "ambiguous" if sequenceStatus != "failure" else "failure"
				if tree[0].name in self.fallbackNodes and status == "success":
					sequenceStatus = "success"
					self.active[-1] = False
				if tree[0].name in self.probabilityNodes: returnStatus = self.parseProbabilityNode(status)
				if tree[0].name == "successd": returnStatus = "success"
				if tree[0].name == "failured": returnStatus = "failure"
				if tree[0].name == "repeat": returnStatus = status
			self.active.pop()
		
		if tree[0].name in self.sequenceNodes: return sequenceStatus
		else: return returnStatus

	def parseLeaf(self, tree):
		returnStatus = "ambiguous"
		node = str(tree[0].name)
		if node in self.successNodes: returnStatus = "success"
		if node in self.failureNodes: returnStatus = "failure"
		if node == "set": returnStatus = self.parseCompositeNode(tree, True)
		if node in self.conditionNodes: returnStatus = self.parseCompositeNode(tree, True)
		return returnStatus

	def parseProbabilityNode(self, status):
		probReturnStatus = ""
		if status == "ambiguous":
			probReturnStatus = "ambiguous"
		if probReturnStatus != "ambiguous":
			if status == "success" and probReturnStatus != "failure":
				probReturnStatus = "success"
			elif status == "failure" and probReturnStatus != "success":
				probReturnStatus = "failure"
			else:
				probReturnStatus = "ambiguous"
		# print "probReturnStatus " + status + " " +probReturnStatus	
		return probReturnStatus

	def parseCompositeNode(self, tree, greedy):

		returnStatus = "ambiguous"
		
		parent = tree[0].name
		
		slice_ = tree.searchSubtree(1)
		chromosome = tree[slice_]
		child1 = gp.PrimitiveTree(chromosome)
		
		slice_ = tree.searchSubtree(2)
		chromosome = tree[slice_]
		child2 = gp.PrimitiveTree(chromosome)
		
		self.composites.append(parent)
		
		self.output.append(str(child1))
		self.output.append(str(child2))
		self.trailingNodesList.append(self.active[-1])
		self.trailingNodesList.append(self.active[-1])
		# if not greedy:
			# trailingNodesList.append(active[-1])
			# trailingNodesList.append(active[-1])
		
		if parent == "ifgevar" and child1 == child2:
			returnStatus = "success"
		
		if parent == "ifltvar":
			if child1 == child2: returnStatus = "failure"
		
		if parent == "ifltcon":
			if child2 == -1: returnStatus = "failure"
			if int(child1[0].name) < 4:
				if float(self.blackboard[int(child1[0].name)]) < float(child2[0].name): returnStatus = "success"
				else: returnStatus = "failure"
		
		if parent == "ifgecon":
			if child2 == -1: returnStatus = "success"
			if int(child1[0].name) < 4:
				if float(self.blackboard[int(child1[0].name)]) >= float(child2[0].name): returnStatus = "success"
				else: returnStatus = "failure"
			
		if parent == "set":
			returnStatus = "success"
			self.blackboard[int(child1[0].name)] = child2[0].name
		
		# print returnStatus
		return returnStatus

	def parseSubtreeActivity(self, tree):
		
		if tree[0].name in self.actionNodes:
			return True
		else:
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				activity = self.parseSubtreeActivity(subtree)
				if activity: 
					return True
		
		return False

	def parseSubtreeActuation(self, tree):
		
		if tree[0].name in self.actuationNodes:
			return True
		else:
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				activity = self.parseSubtreeActuation(subtree)
				if activity: 
					return True
		
		return False

	def trailingNodesLazy(self, tree):
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, True)
		for i in range(len(self.trailingNodesList) - 1, -1, -1):
			if not self.trailingNodesList[i]:
				self.output.pop(i)

	def trailingNodesGreedy(self, tree):
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, True)

	def trailingNodes(self, tree, slice_, last):
		
		subtreeSlice = slice_
		chromosome = tree[slice_]
		subtree = gp.PrimitiveTree(chromosome)
		parentName = subtree[0].name
		# print "SUBTREE "+str(subtree)
		
		index = slice_.start + 1
		limit = slice_.stop
		slices = []

		while (index < limit):
			slice_ = tree.searchSubtree(index)
			chromosome = tree[slice_]
			subSubtree = gp.PrimitiveTree(chromosome)
			slices.append(slice_)
			index += len(subSubtree)
		
		activeSubtree = False
		probNodeStatus = False
		nextSubtreeActive = False # from parseSubtree
		
		parentIsLast = last
		childIsLast = last
		
		for i in range(len(slices) - 1, -1, -1):
		
			chromosome = tree[slices[i]]
			subSubtree = gp.PrimitiveTree(chromosome)
			childName = subSubtree[0].name
			# print "subSubtree "+str(subSubtree)
				
			if i < len(slices) - 1 and activeSubtree and nextSubtreeActive and parentName not in self.probabilityNodes:
				childIsLast = False
			
			if parentName in self.probabilityNodes or childName not in self.compositeNodes:
				activity = self.parseSubtreeActuation(subSubtree)
				if self.trailingNodesList[slices[i].start]: activeSubtree = (activeSubtree or activity)
				# print activity
				# print activeSubtree
				# print ""
				
				if childIsLast and not activeSubtree and parentName not in self.probabilityNodes:
					if not parentName == "repeat" or i == 0:
						for j in range(slices[i].start, slices[i].stop):
							self.trailingNodesList[j] = False
				elif childName not in self.compositeNodes:
					probNodeStatus = True
					trailingSubtree = childIsLast or parentName == "successd" or parentName == "failured"
					self.trailingNodes(tree, slices[i], trailingSubtree)
			
			if childIsLast and not activeSubtree and childName in self.compositeNodes and parentName not in self.probabilityNodes:
				if not parentName == "repeat" or i == 0:
					for j in range(slices[i].start, slices[i].stop):
						self.trailingNodesList[j] = False
			
			if self.trailingNodesList[slices[i].start]:
				nextSubtreeActive = True
			
		if parentIsLast and parentName in self.probabilityNodes and not probNodeStatus:
			for i in range(subtreeSlice.start, subtreeSlice.stop):
				self.trailingNodesList[i] = False

	def capitaliseOutput(self):
		for i in range(len(self.output)):
			if self.trailingNodesList[i] == False:
				self.output[i] = self.output[i].upper()

	def removeConstants(self):
		for j in range(len(self.output) - 1, -1, -1):
			if self.output[j] in self.compositeNodes:
				if self.is_number(self.output[j+2]): self.output.pop(j+2)
				if self.is_number(self.output[j+1]): self.output.pop(j+1)

	def calculateRatio(self, tree):
		treeLength = len(tree) - (len(self.composites) * 2) - len(self.repeatNodes)
		outputLength = len(self.output)
		ratio = float(outputLength) / float(treeLength)
		return ratio

	def printRatioCalculation(self, tree):
		treeLength = len(tree) - (len(self.composites) * 2) - len(self.repeatNodes)
		outputLength = len(self.output)
		ratio = float(outputLength) / float(treeLength)
		print "original tree length: "+str(len(tree))
		print "repeat nodes: "+str(len(self.repeatNodes))
		print "composite nodes: "+str(len(self.composites))
		print "final tree length: "+str(treeLength)
		print "converted tree length: "+str(outputLength)
		print "\nratio: "+str(ratio)

	def rebuildChromosome(self):
		
		childrenRemaining = []
		chromosome = ""
		for i in range(len(self.output)):
			
			node = self.output[i]
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				children = 0
				if node.lower() == "repeat": children = 2
				elif node.lower() in self.decoratorNodes: children = 1
				else: children = int(node[-1])			
				childrenRemaining.append(children)
				chromosome += node +"("
			
			elif node.lower() in self.compositeNodes:
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				childrenRemaining.append(2)
				chromosome += node +"("
			
			else:	
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1: chromosome += node + ", "
				else: chromosome += node
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for childQty in reversed(childrenRemaining):
					if childQty == 0: 
						childrenRemaining.pop()
						chromosome += ")"
					else: break
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0 and i < len(self.output) - 1:
					chromosome += ", "
			
			
		for node in childrenRemaining:
			chromosome += ")"
		
		# print chromosome
		return chromosome

	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

