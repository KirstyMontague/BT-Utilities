
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
								 "capitalised": "failured(selm4(selm3(failured(ml), failured(FAILUREL), selm4(mf, ML, MF, IFLTCON(1, -0.43))), MR, PROBM3(PROBM2(IFLTVAR(7, 5), IFGEVAR(5, 9)), PROBM3(IFGEVAR(4, 8), MF, IFLTVAR(2, 2)), SELM2(SET(1, 0.581), SUCCESSL)), PROBM3(SEQM2(IFGEVAR(9, 8), MR), SUCCESSD(ML), SEQM4(MR, IFGEVAR(1, 7), IFLTVAR(9, 2), MR))))",
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
		self.tests.append({"chromosome": "probm2(seqm3(selm3(mr, ifgevar(6, 7), seqm3(mr, mf, seqm3(seqm3(mr, ifgevar(9, 4), mf), mf, seqm3(mr, mf, mf)))), mf, seqm3(selm3(ifltvar(4, 1), ifgevar(6, 7), seqm3(selm3(mf, mr, ifgevar(7, 2)), mr, seqm3(mr, mf, mf))), mf, mf)), seqm3(selm3(mr, ifgevar(6, 7), seqm3(mr, selm3(mf, mr, ifgevar(7, 2)), seqm3(seqm3(mr, ifgevar(9, 4), mf), mf, seqm3(mr, mf, mf)))), mf, seqm3(selm3(ifltvar(4, 1), ifgevar(6, 7), seqm3(selm3(mf, mr, ifltcon(2, -0.54)), mr, mr)), mf, mf)))",
								 "capitalised": "probm2(seqm3(selm3(mr, IFGEVAR(6, 7), SEQM3(MR, MF, SEQM3(SEQM3(MR, IFGEVAR(9, 4), MF), MF, SEQM3(MR, MF, MF)))), mf, seqm3(selm3(ifltvar(4, 1), ifgevar(6, 7), seqm3(selm3(mf, MR, IFGEVAR(7, 2)), mr, seqm3(mr, mf, mf))), mf, mf)), seqm3(selm3(mr, IFGEVAR(6, 7), SEQM3(MR, SELM3(MF, MR, IFGEVAR(7, 2)), SEQM3(SEQM3(MR, IFGEVAR(9, 4), MF), MF, SEQM3(MR, MF, MF)))), mf, seqm3(selm3(ifltvar(4, 1), ifgevar(6, 7), seqm3(selm3(mf, MR, IFLTCON(2, -0.54)), mr, mr)), mf, mf)))",
								 "trimmed": ['probm2', 'seqm3', 'selm3', 'mr', 'mf', 'seqm3', 'selm3', 'ifltvar', 'ifgevar', 'seqm3', 'selm3', 'mf', 'mr', 'seqm3', 'mr', 'mf', 'mf', 'mf', 'mf', 'seqm3', 'selm3', 'mr', 'mf', 'seqm3', 'selm3', 'ifltvar', 'ifgevar', 'seqm3', 'selm3', 'mf', 'mr', 'mr', 'mf', 'mf'],
								 "ratio": 0.492753623188})
		self.tests.append({"chromosome": "seqm4(selm3(seqm2(successl, failurel), selm3(mf, mf, successl), seqm3(mr, ifltcon(4, 0.115), ifltcon(6, 0.72))), successd(selm3(mf, ifltvar(8, 5), mf)), selm4(seqm4(successl, seqm3(ml, selm3(mf, ifltvar(1, 6), successl), ifltcon(6, -0.35)), mf, mf), probm4(ifgevar(9, 8), ifgevar(8, 8), set(1, -0.37), ifltvar(9, 7)), mf, mf), seqm3(seqm4(ml, mf, set(2, 0.892), ifltcon(3, -0.91)), ifgevar(2, 5), repeat(ifgevar(9, 8), 6)))",
								 "capitalised": "seqm4(selm3(seqm2(successl, failurel), selm3(mf, MF, SUCCESSL), SEQM3(MR, IFLTCON(4, 0.115), IFLTCON(6, 0.72))), successd(selm3(mf, IFLTVAR(8, 5), MF)), selm4(seqm4(successl, seqm3(ml, selm3(mf, IFLTVAR(1, 6), SUCCESSL), ifltcon(6, -0.35)), mf, mf), probm4(ifgevar(9, 8), ifgevar(8, 8), set(1, -0.37), ifltvar(9, 7)), mf, MF), seqm3(seqm4(ml, mf, SET(2, 0.892), IFLTCON(3, -0.91)), IFGEVAR(2, 5), REPEAT(IFGEVAR(9, 8), 6)))",
								 "trimmed": ['seqm4', 'selm3', 'seqm2', 'successl', 'failurel', 'selm3', 'mf', 'successd', 'selm3', 'mf', 'selm4', 'seqm4', 'successl', 'seqm3', 'ml', 'selm3', 'mf', 'ifltcon', 'mf', 'mf', 'probm4', 'ifgevar', 'ifgevar', 'set', 'ifltvar', 'mf', 'seqm3', 'seqm4', 'ml', 'mf'],
								 "ratio": 0.652173913043})
		self.tests.append({"chromosome": "seqm2(selm4(ifgecon(6, 0.689), probm4(ifgecon(1, -0.52), mr, mr, ifgevar(6, 4)), seqm3(mr, mr, mf), successl), mf)",
								 "capitalised": "seqm2(selm4(ifgecon(6, 0.689), probm4(ifgecon(1, -0.52), mr, mr, ifgevar(6, 4)), seqm3(mr, mr, mf), SUCCESSL), mf)",
								 "trimmed": ['seqm2', 'selm4', 'ifgecon', 'probm4', 'ifgecon', 'mr', 'mr', 'ifgevar', 'seqm3', 'mr', 'mr', 'mf', 'mf'],
								 "ratio": 0.928571428571})
		self.tests.append({"chromosome": "selm2(failured(failured(seqm3(ifltcon(4, -0.39), mr, ifltvar(4, 5)))), seqm2(selm2(seqm4(selm2(seqm4(mf, ml, set(1, 0.639), set(1, 0.739)), probm3(ifgecon(1, -0.9), mf, ifltcon(5, 0.031))), ml, set(1, 0.639), set(1, 0.739)), ifltvar(4, 5)), selm4(mf, failurel, ifgecon(7, 0.408), failurel)))",
								 "capitalised": "selm2(failured(failured(seqm3(ifltcon(4, -0.39), mr, IFLTVAR(4, 5)))), seqm2(selm2(seqm4(selm2(seqm4(mf, ml, set(1, 0.639), set(1, 0.739)), PROBM3(IFGECON(1, -0.9), MF, IFLTCON(5, 0.031))), ml, set(1, 0.639), set(1, 0.739)), IFLTVAR(4, 5)), selm4(mf, FAILUREL, IFGECON(7, 0.408), FAILUREL)))",
								 "trimmed": ['selm2', 'failured', 'failured', 'seqm3', 'ifltcon', 'mr', 'seqm2', 'selm2', 'seqm4', 'selm2', 'seqm4', 'mf', 'ml', 'set', 'set', 'ml', 'set', 'set', 'selm4', 'mf'],
								 "ratio": 0.689655172414})

		self.tests.append({"chromosome": "seqm3(seqm2(successd(ifltcon(8, 0.867)), selm2(ml, selm3(selm4(mf, successl, failurel, ifgevar(4, 6)), mr, selm4(ifltvar(6, 3), mf, ifgecon(3, 0.405), ml)))), seqm4(successl, mf, mf, selm4(ifgecon(4, 0.037), mf, ifgecon(3, 0.405), ml)), failured(probm4(ifltcon(6, -0.7), ifltcon(8, -0.29), successl, ifgevar(8, 4))))",
								 "capitalised": "seqm3(seqm2(successd(IFLTCON(8, 0.867)), selm2(ml, SELM3(SELM4(MF, SUCCESSL, FAILUREL, IFGEVAR(4, 6)), MR, SELM4(IFLTVAR(6, 3), MF, IFGECON(3, 0.405), ML)))), seqm4(successl, mf, mf, selm4(ifgecon(4, 0.037), mf, IFGECON(3, 0.405), ML)), FAILURED(PROBM4(IFLTCON(6, -0.7), IFLTCON(8, -0.29), SUCCESSL, IFGEVAR(8, 4))))",
								 "trimmed": ['seqm3', 'seqm2', 'successd', 'selm2', 'ml', 'seqm4', 'successl', 'mf', 'mf', 'selm4', 'ifgecon', 'mf'],
								 "ratio": 0.363636363636})
		self.tests.append({"chromosome": "seqm4(seqm3(set(1, 0.143), ifgecon(7, -0.05), mf), selm3(ml, failurel, mr), seqm4(mf, failurel, mr, repeat(set(1, 0.6), 3)), probm3(successl, seqm4(seqm2(ifgevar(1, 8), ifgecon(1, -0.61)), failured(successl), probm2(ml, successl), seqm2(mr, ifltvar(4, 8))), successl))",
								 "capitalised": "seqm4(seqm3(set(1, 0.143), ifgecon(7, -0.05), mf), selm3(ml, FAILUREL, MR), seqm4(mf, FAILUREL, MR, REPEAT(SET(1, 0.6), 3)), PROBM3(SUCCESSL, SEQM4(SEQM2(IFGEVAR(1, 8), IFGECON(1, -0.61)), FAILURED(SUCCESSL), PROBM2(ML, SUCCESSL), SEQM2(MR, IFLTVAR(4, 8))), SUCCESSL))",
								 "trimmed": ['seqm4', 'seqm3', 'set', 'ifgecon', 'mf', 'selm3', 'ml', 'seqm4', 'mf'],
								 "ratio": 0.3})
		self.tests.append({"chromosome": "seqm4(seqm3(seqm3(successd(mf), ml, mf), ifltvar(1, 3), mf), successd(mf), failurel, seqm4(ml, mf, failurel, ifgevar(5, 8)))",
								 "capitalised": "seqm4(seqm3(seqm3(successd(mf), ml, mf), IFLTVAR(1, 3), MF), SUCCESSD(MF), FAILUREL, SEQM4(ML, MF, FAILUREL, IFGEVAR(5, 8)))",
								 "trimmed": ['seqm4', 'seqm3', 'seqm3', 'successd', 'mf', 'ml', 'mf'],
								 "ratio": 0.411764705882})
		self.tests.append({"chromosome": "failured(selm4(selm3(failured(ml), failured(mf), selm4(mf, ml, mf, ifltcon(1, -0.43))), mf, selm2(ml, successl), probm3(seqm2(ifgevar(9, 8), mr), successd(ml), probm4(mr, ifgevar(1, 7), failurel, mr))))",
								 "capitalised": "failured(selm4(selm3(failured(ml), failured(mf), selm4(mf, ML, MF, IFLTCON(1, -0.43))), MF, SELM2(ML, SUCCESSL), PROBM3(SEQM2(IFGEVAR(9, 8), MR), SUCCESSD(ML), PROBM4(MR, IFGEVAR(1, 7), FAILUREL, MR))))",
								 "trimmed": ['failured', 'selm4', 'selm3', 'failured', 'ml', 'failured', 'mf', 'selm4', 'mf'],
								 "ratio": 0.333333333333})
		self.tests.append({"chromosome": "seqm3(selm3(repeat(mf, 7), probm2(ifgecon(7, 0.177), ifltcon(6, 0.344)), selm4(ifgecon(2, 0.349), ifgecon(5, -0.03), ifltvar(6, 1), ifgevar(2, 1))), repeat(seqm4(ifltvar(6, 1), ml, mf, set(2, -0.35)), 9), probm4(selm2(ifgevar(7, 4), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1))), seqm4(successl, probm4(selm2(ifgevar(7, 4), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1))), seqm4(successl, ifltvar(7, 2), mr, set(1, 0.15)), probm4(mr, ifltcon(1, -0.3), ifltcon(6, -0.88), ifltcon(1, -0.3)), ifltcon(1, -0.3)), mr, set(1, 0.15)), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1)), ifltcon(1, -0.3)))",
								 "capitalised": "seqm3(selm3(repeat(mf, 7), PROBM2(IFGECON(7, 0.177), IFLTCON(6, 0.344)), SELM4(IFGECON(2, 0.349), IFGECON(5, -0.03), IFLTVAR(6, 1), IFGEVAR(2, 1))), repeat(seqm4(ifltvar(6, 1), ml, mf, set(2, -0.35)), 9), probm4(selm2(ifgevar(7, 4), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1))), seqm4(successl, probm4(selm2(ifgevar(7, 4), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1))), seqm4(successl, ifltvar(7, 2), mr, set(1, 0.15)), probm4(mr, ifltcon(1, -0.3), ifltcon(6, -0.88), ifltcon(1, -0.3)), ifltcon(1, -0.3)), mr, SET(1, 0.15)), probm4(mf, ifltcon(1, -0.3), mf, ifgevar(2, 1)), ifltcon(1, -0.3)))",
								 "trimmed": ['seqm3', 'selm3', 'repeat', 'mf', 'repeat', 'seqm4', 'ifltvar', 'ml', 'mf', 'set', 'probm4', 'selm2', 'ifgevar', 'probm4', 'mf', 'ifltcon', 'mf', 'ifgevar', 'seqm4', 'successl', 'probm4', 'selm2', 'ifgevar', 'probm4', 'mf', 'ifltcon', 'mf', 'ifgevar', 'seqm4', 'successl', 'ifltvar', 'mr', 'set', 'probm4', 'mr', 'ifltcon', 'ifltcon', 'ifltcon', 'ifltcon', 'mr', 'probm4', 'mf', 'ifltcon', 'mf', 'ifgevar', 'ifltcon'],
								 "ratio": 0.836363636364})
		self.tests.append({"chromosome": "seqm3(seqm2(ml, mf), mf, probm4(probm3(ifgecon(1, 0.849), mf, failurel), ifltcon(8, -0.81), repeat(failurel, 1), set(2, -0.13)))",
								 "capitalised": "seqm3(seqm2(ml, mf), mf, probm4(probm3(ifgecon(1, 0.849), mf, failurel), ifltcon(8, -0.81), repeat(FAILUREL, 1), set(2, -0.13)))",
								 "trimmed": ['seqm3', 'seqm2', 'ml', 'mf', 'mf', 'probm4', 'probm3', 'ifgecon', 'mf', 'failurel', 'ifltcon', 'repeat', 'set'],
								 "ratio": 0.928571428571})
		self.tests.append({"chromosome": "probm4(successd(seqm2(ifltcon(4, -0.61), ml)), failured(successd(failurel)), seqm4(failured(mr), probm4(ifgevar(4, 6), mr, mr, mr), probm3(ifltvar(5, 1), successl, ifgevar(7, 9)), ifgevar(9, 8)), probm3(seqm2(failurel, ifltcon(1, 0.936)), probm3(ifgevar(2, 5), set(2, -0.53), successl), probm3(ifltvar(5, 4), ifgecon(7, 0.852), successl)))",
								 "capitalised": "probm4(successd(seqm2(ifltcon(4, -0.61), ml)), failured(SUCCESSD(FAILUREL)), seqm4(failured(mr), PROBM4(IFGEVAR(4, 6), MR, MR, MR), PROBM3(IFLTVAR(5, 1), SUCCESSL, IFGEVAR(7, 9)), IFGEVAR(9, 8)), probm3(SEQM2(FAILUREL, IFLTCON(1, 0.936)), PROBM3(IFGEVAR(2, 5), SET(2, -0.53), SUCCESSL), PROBM3(IFLTVAR(5, 4), IFGECON(7, 0.852), SUCCESSL)))",
								 "trimmed": ['probm4', 'successd', 'seqm2', 'ifltcon', 'ml', 'failured', 'seqm4', 'failured', 'mr', 'probm3'],
								 "ratio": 0.30303030303})
		self.tests.append({"chromosome": "seqm4(mf, successd(seqm2(ml, set(2, -0.45))), successd(seqm4(mf, seqm4(failurel, failurel, mr, mr), successd(seqm4(mf, failurel, mr, successl)), mr)), ifgecon(8, -0.43))",
								 "capitalised": "seqm4(mf, successd(seqm2(ml, set(2, -0.45))), successd(seqm4(mf, seqm4(FAILUREL, FAILUREL, MR, MR), SUCCESSD(SEQM4(MF, FAILUREL, MR, SUCCESSL)), MR)), IFGECON(8, -0.43))",
								 "trimmed": ['seqm4', 'mf', 'successd', 'seqm2', 'ml', 'set', 'successd', 'seqm4', 'mf', 'seqm4'],
								 "ratio": 0.454545454545})
		self.tests.append({"chromosome": "seqm2(selm3(seqm2(mf, ml), seqm2(mf, ml), seqm4(mf, selm3(ifltvar(4, 6), seqm2(mf, ml), seqm4(ifgevar(5, 4), set(1, 0.306), ifltvar(4, 5), set(2, 0.74))), ifltvar(4, 5), mr)), mf)",
								 "capitalised": "seqm2(selm3(seqm2(mf, ml), SEQM2(MF, ML), SEQM4(MF, SELM3(IFLTVAR(4, 6), SEQM2(MF, ML), SEQM4(IFGEVAR(5, 4), SET(1, 0.306), IFLTVAR(4, 5), SET(2, 0.74))), IFLTVAR(4, 5), MR)), mf)",
								 "trimmed": ['seqm2', 'selm3', 'seqm2', 'mf', 'ml', 'mf'],
								 "ratio": 0.260869565217})
		self.tests.append({"chromosome": "seqm4(probm4(selm4(successl, ifltcon(5, 0.579), mf, set(2, 0.85)), probm2(set(1, 0.604), failurel), probm4(ifltvar(1, 4), selm3(mf, successl, ml), selm4(successl, ifltcon(5, 0.579), mf, set(2, -0.83)), mf), successd(successd(mf))), repeat(successd(mf), 6), selm2(seqm4(ml, ml, ifltvar(3, 1), ifgevar(7, 4)), successd(failurel)), seqm4(selm2(set(2, 0.406), failurel), seqm3(mf, successl, ml), ifgecon(9, 0.962), set(1, -0.81)))",
								 "capitalised": "seqm4(probm4(selm4(successl, IFLTCON(5, 0.579), MF, SET(2, 0.85)), probm2(set(1, 0.604), failurel), probm4(ifltvar(1, 4), selm3(mf, SUCCESSL, ML), selm4(successl, IFLTCON(5, 0.579), MF, SET(2, -0.83)), mf), successd(successd(mf))), repeat(successd(mf), 6), selm2(seqm4(ml, ml, ifltvar(3, 1), ifgevar(7, 4)), successd(FAILUREL)), seqm4(selm2(set(2, 0.406), FAILUREL), seqm3(mf, successl, ml), IFGECON(9, 0.962), SET(1, -0.81)))",
								 "trimmed": ['seqm4', 'probm4', 'selm4', 'successl', 'probm2', 'set', 'failurel', 'probm4', 'ifltvar', 'selm3', 'mf', 'selm4', 'successl', 'mf', 'successd', 'successd', 'mf', 'repeat', 'successd', 'mf', 'selm2', 'seqm4', 'ml', 'ml', 'ifltvar', 'ifgevar', 'successd', 'seqm4', 'selm2', 'set', 'seqm3', 'mf', 'successl', 'ml'],
								 "ratio": 0.739130434783})
		self.tests.append({"chromosome": "seqm2(successl, successd(seqm4(seqm4(mf, mf, ifgevar(4, 2), ml), set(2, -0.0), selm4(failurel, set(2, 0.39), mr, set(2, -0.26)), selm3(successl, ifgecon(8, 0.27), selm3(ml, ifltvar(3, 5), mf)))))",
								 "capitalised": "seqm2(successl, successd(seqm4(seqm4(mf, mf, ifgevar(4, 2), ml), set(2, -0.0), selm4(failurel, set(2, 0.39), MR, SET(2, -0.26)), selm3(SUCCESSL, IFGECON(8, 0.27), SELM3(ML, IFLTVAR(3, 5), MF)))))",
								 "trimmed": ['seqm2', 'successl', 'successd', 'seqm4', 'seqm4', 'mf', 'mf', 'ifgevar', 'ml', 'set', 'selm4', 'failurel', 'set', 'selm3'],
								 "ratio": 0.636363636364})
		self.tests.append({"chromosome": "probm4(seqm2(failured(mf), probm2(mf, set(2, -0.16))), seqm4(failured(successl), selm4(ifgecon(6, 0.807), successd(mf), failurel, seqm2(failured(mf), probm2(mf, ml))), repeat(ifgecon(9, -0.44), 6), successl), seqm3(probm2(mf, ifgecon(1, 0.519)), probm2(mf, set(2, -0.16)), failurel), selm3(probm3(ifgecon(3, -0.9), ifgecon(3, -0.69), seqm4(successl, mf, mr, ifgevar(4, 2))), seqm2(mr, mf), seqm2(failured(mf), probm2(mf, set(2, -0.16)))))",
								 "capitalised": "probm4(seqm2(failured(mf), PROBM2(MF, SET(2, -0.16))), seqm4(FAILURED(SUCCESSL), SELM4(IFGECON(6, 0.807), SUCCESSD(MF), FAILUREL, SEQM2(FAILURED(MF), PROBM2(MF, ML))), REPEAT(IFGECON(9, -0.44), 6), SUCCESSL), seqm3(probm2(mf, ifgecon(1, 0.519)), probm2(mf, set(2, -0.16)), FAILUREL), selm3(probm3(ifgecon(3, -0.9), ifgecon(3, -0.69), seqm4(successl, mf, mr, ifgevar(4, 2))), seqm2(mr, mf), SEQM2(FAILURED(MF), PROBM2(MF, SET(2, -0.16)))))",
								 "trimmed": ['probm4', 'seqm2', 'failured', 'mf', 'seqm4', 'seqm3', 'probm2', 'mf', 'ifgecon', 'probm2', 'mf', 'set', 'selm3', 'probm3', 'ifgecon', 'ifgecon', 'seqm4', 'successl', 'mf', 'mr', 'ifgevar', 'seqm2', 'mr', 'mf'],
								 "ratio": 0.48})
		self.tests.append({"chromosome": "seqm3(seqm3(seqm3(seqm3(mr, mf, ifgevar(4, 4)), successl, set(2, -0.55)), mf, ifgevar(3, 3)), ifltcon(4, 0.238), seqm3(seqm3(ml, mf, set(2, 0.166)), ifgevar(3, 3), mf))",
								 "capitalised": "seqm3(seqm3(seqm3(seqm3(mr, mf, ifgevar(4, 4)), successl, set(2, -0.55)), mf, ifgevar(3, 3)), ifltcon(4, 0.238), seqm3(seqm3(ml, mf, set(2, 0.166)), ifgevar(3, 3), mf))",
								 "trimmed": ['seqm3', 'seqm3', 'seqm3', 'seqm3', 'mr', 'mf', 'ifgevar', 'successl', 'set', 'mf', 'ifgevar', 'ifltcon', 'seqm3', 'seqm3', 'ml', 'mf', 'set', 'ifgevar', 'mf'],
								 "ratio": 1.0})
		self.tests.append({"chromosome": "probm2(failured(selm2(repeat(ifgecon(2, 0.548), 8), selm2(probm3(probm3(failurel, ifltvar(1, 1), mf), ifltvar(1, 5), mf), seqm4(ifgecon(8, -0.31), set(1, -0.54), mr, mf)))), successd(selm2(selm3(failurel, seqm4(mf, set(1, -0.39), mr, ifltvar(7, 4)), mf), set(1, -0.39))))",
								 "capitalised": "probm2(failured(selm2(repeat(ifgecon(2, 0.548), 8), selm2(probm3(probm3(failurel, ifltvar(1, 1), mf), ifltvar(1, 5), mf), seqm4(ifgecon(8, -0.31), set(1, -0.54), mr, mf)))), successd(selm2(selm3(failurel, seqm4(mf, set(1, -0.39), mr, ifltvar(7, 4)), mf), SET(1, -0.39))))",
								 "trimmed": ['probm2', 'failured', 'selm2', 'repeat', 'ifgecon', 'selm2', 'probm3', 'probm3', 'failurel', 'ifltvar', 'mf', 'ifltvar', 'mf', 'seqm4', 'ifgecon', 'set', 'mr', 'mf', 'successd', 'selm2', 'selm3', 'failurel', 'seqm4', 'mf', 'set', 'mr', 'ifltvar', 'mf'],
								 "ratio": 0.965517241379})
		self.tests.append({"chromosome": "selm4(failured(probm2(ml, ml)), selm4(mf, probm3(mf, set(2, 0.798), ifltcon(6, -0.09)), ifltvar(3, 6), probm3(set(1, 0.011), selm3(ifgecon(1, -0.18), mr, ifgecon(6, 0.907)), mr)), probm4(selm3(failurel, mf, ifltcon(2, -0.46)), seqm2(mf, ifgevar(5, 1)), seqm3(ifltvar(3, 6), failurel, ifltcon(7, 0.189)), selm3(ifgecon(1, -0.18), mr, ifgevar(7, 3))), selm3(successl, mr, ifltvar(9, 4)))",
								 "capitalised": "selm4(failured(probm2(ml, ml)), selm4(mf, PROBM3(MF, SET(2, 0.798), IFLTCON(6, -0.09)), IFLTVAR(3, 6), PROBM3(SET(1, 0.011), SELM3(IFGECON(1, -0.18), MR, IFGECON(6, 0.907)), MR)), PROBM4(SELM3(FAILUREL, MF, IFLTCON(2, -0.46)), SEQM2(MF, IFGEVAR(5, 1)), SEQM3(IFLTVAR(3, 6), FAILUREL, IFLTCON(7, 0.189)), SELM3(IFGECON(1, -0.18), MR, IFGEVAR(7, 3))), SELM3(SUCCESSL, MR, IFLTVAR(9, 4)))",
								 "trimmed": ['selm4', 'failured', 'probm2', 'ml', 'ml', 'selm4', 'mf'],
								 "ratio": 0.179487179487})
		self.tests.append({"chromosome": "seqm4(mf, set(2, 0.55), selm4(ml, ifgecon(6, 0.737), set(1, 0.861), mr), mf)",
								 "capitalised": "seqm4(mf, set(2, 0.55), selm4(ml, IFGECON(6, 0.737), SET(1, 0.861), MR), mf)",
								 "trimmed": ['seqm4', 'mf', 'set', 'selm4', 'ml', 'mf'],
								 "ratio": 0.666666666667})
		self.tests.append({"chromosome": "seqm2(seqm2(mf, ml), successd(mf))",
								 "capitalised": "seqm2(seqm2(mf, ml), successd(mf))",
								 "trimmed": ['seqm2', 'seqm2', 'mf', 'ml', 'successd', 'mf'],
								 "ratio": 1.0})
		self.tests.append({"chromosome": "seqm4(selm3(seqm2(successl, failurel), selm3(mf, seqm2(successl, ifgevar(8, 8)), successl), seqm3(mr, ifltcon(4, 0.115), ifltcon(6, 0.72))), selm3(mf, mf, ml), selm4(seqm4(mf, ifltcon(1, -0.29), mf, mf), probm4(successl, set(1, 0.692), ifltcon(1, -0.96), ifltvar(9, 7)), seqm2(successl, mf), successd(seqm4(successl, set(1, 0.692), set(1, 0.692), ifltvar(9, 7)))), seqm3(seqm4(ml, mf, mr, ifltcon(3, -0.91)), ifgecon(9, -0.7), ml))",
								 "capitalised": "seqm4(selm3(seqm2(successl, failurel), selm3(mf, SEQM2(SUCCESSL, IFGEVAR(8, 8)), SUCCESSL), SEQM3(MR, IFLTCON(4, 0.115), IFLTCON(6, 0.72))), selm3(mf, MF, ML), selm4(seqm4(mf, ifltcon(1, -0.29), MF, MF), probm4(successl, set(1, 0.692), ifltcon(1, -0.96), ifltvar(9, 7)), seqm2(successl, mf), SUCCESSD(SEQM4(SUCCESSL, SET(1, 0.692), SET(1, 0.692), IFLTVAR(9, 7)))), seqm3(seqm4(ml, mf, mr, IFLTCON(3, -0.91)), IFGECON(9, -0.7), ML))",
								 "trimmed": ['seqm4', 'selm3', 'seqm2', 'successl', 'failurel', 'selm3', 'mf', 'selm3', 'mf', 'selm4', 'seqm4', 'mf', 'ifltcon', 'probm4', 'successl', 'set', 'ifltcon', 'ifltvar', 'seqm2', 'successl', 'mf', 'seqm3', 'seqm4', 'ml', 'mf', 'mr'],
								 "ratio": 0.553191489362})
		self.tests.append({"chromosome": "seqm2(seqm4(successl, mf, ml, mf), ifgevar(8, 8))",
								 "capitalised": "seqm2(seqm4(successl, mf, ml, mf), IFGEVAR(8, 8))",
								 "trimmed": ['seqm2', 'seqm4', 'successl', 'mf', 'ml', 'mf'],
								 "ratio": 0.857142857143})
		self.tests.append({"chromosome": "selm2(failured(successd(seqm3(ifltcon(4, -0.39), mr, successl))), seqm2(selm2(seqm4(mf, ml, seqm2(ml, selm4(failurel, ifltcon(3, -0.65), probm2(ifltcon(9, -0.34), mf), selm2(ifgecon(8, 0.38), mf))), mf), mf), selm4(ifltvar(3, 1), mf, ifltcon(5, 0.031), selm2(ifgecon(8, 0.38), mf))))",
								 "capitalised": "selm2(failured(successd(seqm3(ifltcon(4, -0.39), mr, SUCCESSL))), seqm2(selm2(seqm4(mf, ml, seqm2(ml, selm4(failurel, ifltcon(3, -0.65), probm2(ifltcon(9, -0.34), mf), selm2(ifgecon(8, 0.38), mf))), mf), MF), selm4(ifltvar(3, 1), mf, IFLTCON(5, 0.031), SELM2(IFGECON(8, 0.38), MF))))",
								 "trimmed": ['selm2', 'failured', 'successd', 'seqm3', 'ifltcon', 'mr', 'seqm2', 'selm2', 'seqm4', 'mf', 'ml', 'seqm2', 'ml', 'selm4', 'failurel', 'ifltcon', 'probm2', 'ifltcon', 'mf', 'selm2', 'ifgecon', 'mf', 'mf', 'selm4', 'ifltvar', 'mf'],
								 "ratio": 0.8125})




	def redundancyTests(self):
		
		for i in range(0,40,1):
			
			print i
			
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
				self.removeRedundantNodes()
				self.removeConstants()
				
				# verify results	
				ratio = self.calculateRatio(tree)
				self.checkResult(i, tree, ratio, chromosome)
				
			else:
				print "Invalid tree"
	
	def checkResult(self, i, tree, ratio, chromosome):
		
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
			
			print ""
			print self.formatChromosome(self.output)
			print ""
			
			# lazy				
			self.resetLists()				
			self.parseSubtreeLazy(tree)				
			self.trailingNodesLazy(tree)
			self.removeRedundantNodes()
			self.removeConstants()
			
			# print results	
			print str(tree)+"\n"
			print str(chromosome)+"\n"
			print str(self.output)+"\n"
			self.printRatioCalculation(tree)
			
			ratio = self.calculateRatio(tree)
			
			results = "\n"
			results += "		self.tests.append({\"chromosome\": \""+str(tree)+"\",\n"
			results += "								 \"capitalised\": \""+str(chromosome)+"\",\n"
			results += "								 \"trimmed\": "+str(self.output)+",\n"
			results += "								 "+str(ratio)+"})"
			
			with open('results.txt', 'w') as f:
				print >> f, results
			
		else:
			print "Invalid tree"

	def parseSubtreeLazy(self, tree):
		
		returnStatus = "ambiguous"
		node = tree[0].name
		
		self.output.append(node)
		self.trailingNodesList.append(self.active[-1])
		
		if node == "repeat": self.repeatNodes.append("repeat")
					
		if node in self.compositeNodes or len(tree) == 1:
			returnStatus = self.parseLeaf(tree)
		else:
			
			if node in self.sequenceNodes: returnStatus = "success"
			elif node in self.fallbackNodes: returnStatus = "failure"
			elif node in self.probabilityNodes: returnStatus = ""
			
			index = 1
			self.active.append(self.active[-1])
				
			while (index < len(tree)):
				slice_ = tree.searchSubtree(index)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				firstSubtree = index == 1
				index += len(subtree)
				
				# children of success/failure decorators must contain motor commands, or a set node if we aren't in
				# the last subtree (a bit crude because we don't know whether subsequent trees contain any activity)
				if node in ["successd", "failured"]:
					if not self.evaluateSubtreeActivity(tree, index == len(tree)):
						self.active[-1] = False
				
				status = self.parseSubtreeLazy(subtree)
				returnStatus = self.evaluateChildNode(node, status, returnStatus, firstSubtree)
				
			self.active.pop()
			
		return returnStatus

	def parseSubtreeGreedy(self, tree):
		
		returnStatus = "ambiguous"
		node = tree[0].name
		
		self.output.append(node)
		self.trailingNodesList.append(self.active[-1])
		
		if node in self.compositeNodes or len(tree) == 1:
			returnStatus = self.parseLeaf(tree)
		else:
			
			if node in self.sequenceNodes: returnStatus = "success"
			elif node in self.fallbackNodes: returnStatus = "failure"
			elif node in self.probabilityNodes: returnStatus = ""
			
			index = 1
			self.active.append(self.active[-1])
				
			while (index < len(tree)):
				slice_ = tree.searchSubtree(index)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				firstSubtree = index == 1
				index += len(subtree)
				
				# children of success/failure decorators must contain motor commands, or a set node if we aren't in
				# the last subtree (a bit crude because we don't know whether subsequent trees contain any activity)
				if node in ["successd", "failured"]:
					if not self.evaluateSubtreeActivity(tree, index == len(tree)):
						self.active[-1] = False
				
				status = self.parseSubtreeGreedy(subtree)
				returnStatus = self.evaluateChildNode(node, status, returnStatus, firstSubtree)
			
			self.active.pop()
		
		return returnStatus

	def parseLeaf(self, tree):
		returnStatus = "ambiguous"
		node = str(tree[0].name)
		if node in self.successNodes: returnStatus = "success"
		if node in self.failureNodes: returnStatus = "failure"
		if node == "set": returnStatus = self.evaluateCompositeNode(tree, True)
		if node in self.conditionNodes: returnStatus = self.evaluateCompositeNode(tree, True)
		return returnStatus

	def evaluateChildNode(self, node, status, returnStatus, firstSubtree):
		if node in self.sequenceNodes: returnStatus = self.evaluateSequenceNode(status, returnStatus)
		elif node in self.fallbackNodes: returnStatus = self.evaluateFallbackNode(status, returnStatus)
		elif node in self.probabilityNodes: returnStatus = self.evaluateProbabilityNode(status, returnStatus)
		elif node == "successd": returnStatus = "success"
		elif node == "failured": returnStatus = "failure"
		elif node == "repeat" and firstSubtree: returnStatus = status
		return returnStatus

	def evaluateSequenceNode(self, status, sequenceStatus):
		if status == "failure":
			sequenceStatus = "failure"
			self.active[-1] = False
		if status == "ambiguous" and sequenceStatus != "failure":
			sequenceStatus = "ambiguous"
		return sequenceStatus

	def evaluateFallbackNode(self, status, fallbackStatus):
		if status == "success":
			fallbackStatus = "success"
			self.active[-1] = False
		if status == "ambiguous" and fallbackStatus != "success":
			fallbackStatus = "ambiguous"
		return fallbackStatus

	def evaluateProbabilityNode(self, status, probReturnStatus):
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

	def evaluateCompositeNode(self, tree, greedy):

		returnStatus = "ambiguous"
		
		parent = tree[0].name
		
		slice_ = tree.searchSubtree(1)
		chromosome = tree[slice_]
		child1 = gp.PrimitiveTree(chromosome)
		index1 = int(child1[0].name)
		
		slice_ = tree.searchSubtree(2)
		chromosome = tree[slice_]
		child2 = gp.PrimitiveTree(chromosome)
		
		self.composites.append(parent)
		
		self.output.append(str(child1))
		self.output.append(str(child2))
		self.trailingNodesList.append(self.active[-1])
		self.trailingNodesList.append(self.active[-1])
		
		# ifgevar and ifltvar need updated to take into account whether
		# blackboard entries were set in the children of probabilistic nodes
		
		if parent == "ifgevar":
			index2 = int(child2[0].name)
			if index1 == index2: returnStatus = "success"
			elif index1 < 4 and index2 < 4:
				returnStatus = "success" if float(self.blackboard[index1]) >= float(self.blackboard[index2]) else "failure"
		
		if parent == "ifltvar":
			index2 = int(child2[0].name)
			if index1 == index2: returnStatus = "failure"
			elif index1 < 4 and index2 < 4:
				returnStatus = "success" if float(self.blackboard[index1]) < float(self.blackboard[index2]) else "failure"
		
		if parent == "ifltcon":
			value2 = float(child2[0].name)
			if value2 == -1: returnStatus = "failure"
			elif index1 < 4:
				if float(self.blackboard[index1]) < value2: returnStatus = "success"
				else: returnStatus = "failure"
		
		if parent == "ifgecon":
			value2 = float(child2[0].name)
			if value2 == -1: returnStatus = "success"
			elif index1 < 4:
				if float(self.blackboard[index1]) >= value2: returnStatus = "success"
				else: returnStatus = "failure"
			
		if parent == "set":
			returnStatus = "success"
			self.blackboard[index1] = float(child2[0].name)
		
		return returnStatus

	def evaluateSubtreeActivity(self, tree, last):
		
		if tree[0].name in self.actionNodes:
			return True
		else:
			index = 1
			while (index < len(tree)):
				slice_ = tree.searchSubtree(index)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				index += len(subtree)
				
				activity = self.evaluateSubtreeActuation(subtree) if last else self.evaluateSubtreeActivity(subtree, last)
				if activity: 
					return True
		
		return False

	def evaluateSubtreeActuation(self, tree):
		
		if tree[0].name in self.actuationNodes:
			return True
		else:
			index = 1
			while (index < len(tree)):
				slice_ = tree.searchSubtree(index)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				index += len(subtree)
				
				activity = self.evaluateSubtreeActuation(subtree)
				if activity: 
					return True
		
		return False

	def trailingNodesLazy(self, tree):
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, True, True, "")
	
	def trailingNodesGreedy(self, tree):
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, True, True, "")

	def trailingNodes(self, tree, slice_, last, lastInSubtree, indent):
		
		indent += "   "
		
		subtree = gp.PrimitiveTree(tree[slice_])
		nodeName = subtree[0].name
		
		index = slice_.start + 1
		limit = slice_.stop
		slices = []

		while (index < limit):
			slices.append(tree.searchSubtree(index))
			subSubtree = gp.PrimitiveTree(tree[slices[-1]])
			index += len(subSubtree)
		
		activeSubtree = False
		probNodeStatus = False
		
		nodeIsLast = last
		childIsLastInTree = last
		childIsLastInSubtree = lastInSubtree
		
		for i in range(len(slices) - 1, -1, -1):
		
			chromosome = tree[slices[i]]
			subSubtree = gp.PrimitiveTree(chromosome)
			childName = subSubtree[0].name
				
			if i < len(slices) - 1 and activeSubtree and nodeName not in self.probabilityNodes:
				childIsLastInTree = False
				if nodeName not in ["successd", "failured"]:
					childIsLastInSubtree = False
			
			# don't need to check composite nodes unless their parent is a probability node
			if nodeName in self.probabilityNodes or childName not in self.compositeNodes:
				
				# check for motor commands, or set nodes if we're at the end of the whole tree
				if childIsLastInTree: activity = self.evaluateSubtreeActuation(subSubtree)
				else: activity = self.evaluateSubtreeActivity(subSubtree, childIsLastInSubtree)
				
				# this subtree can only be active if it hasn't already been flagged as redundant
				if self.trailingNodesList[slices[i].start]: activeSubtree = (activeSubtree or activity)
				
				# only flag nodes as redundant if we're at the end of a subtree and the parent isn't a probability node
				if childIsLastInSubtree and not activeSubtree and nodeName not in self.probabilityNodes:
					if not nodeName == "repeat" or i == 0:
						for j in range(slices[i].start, slices[i].stop):
							self.trailingNodesList[j] = False
				
				# otherwise call trailingNodes on this subtree unless this is a terminal with no effects
				elif childName not in self.compositeNodes + ["successl", "failurel"]:
					# if parent is a probability node we need to check that at least one child has some effect
					if activeSubtree: probNodeStatus = True
					# if the parent is a success/failure decorator the child is last in its subtree
					trailingSubtree = childIsLastInSubtree or nodeName in ["successd", "failured"]
					self.trailingNodes(tree, slices[i], childIsLastInTree, trailingSubtree, indent)
			
			# if subtree is inactive and isn't the child of a probability node
			if not activeSubtree and nodeName not in self.probabilityNodes:
				# and isn't a repeat decorator below the root node
				if not nodeName == "repeat" or i == 0:
					# check for motor commands, or set nodes if we're at the end of the whole tree
					markAsInactive = False
					if childIsLastInTree and childName in self.compositeNodes + ["successl", "failurel"]: markAsInactive = True
					elif childIsLastInSubtree and childName in self.conditionNodes + ["successl", "failurel"]: markAsInactive = True
					# flag subtree as redundant
					if markAsInactive:
						for j in range(slices[i].start, slices[i].stop):
							self.trailingNodesList[j] = False
			
		# if this is a probability node with no active children then flag whole subtree as redundant
		if nodeIsLast and nodeName in self.probabilityNodes and not probNodeStatus:
			for i in range(slice_.start+1, slice_.stop):
				self.trailingNodesList[i] = False

	def capitaliseOutput(self):
		for i in range(len(self.output)):
			if self.trailingNodesList[i] == False:
				self.output[i] = self.output[i].upper()

	def removeRedundantNodes(self):
		for i in range(len(self.trailingNodesList) - 1, -1, -1):
			if not self.trailingNodesList[i]:
				self.output.pop(i)

	def removeConstants(self):
		for i in range(len(self.output) - 1, -1, -1):
			if self.is_number(self.output[i]):
				self.output.pop(i)

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

	def formatChromosome(self, chromosome):
		
		tree = ""
		indent = ""
		lineEnding = "\n"
		
		childrenRemaining = []
		insideComposite = 0
		insideSubtree = True
		
		for i in range(len(chromosome)):
			
			node = chromosome[i]
			
			# ======= inner nodes =======
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
				
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
				if node.lower() == "repeat": childrenRemaining.append(2)
				elif node.lower() in self.decoratorNodes: childrenRemaining.append(1)
				else: childrenRemaining.append(int(node[-1]))
				
				# check if any children are inner nodes
				insideSubtree = False
				composites = 0
				j = i + 1
				limit = j + childrenRemaining[-1]
				while j < limit:
					if chromosome[j].lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
						insideSubtree = True
						break
					if chromosome[j].lower() in self.compositeNodes:
						limit += 2
					j += 1
				
				# if all children are terminals print them on one line
				if insideSubtree:
					tree += indent + node +"(" + lineEnding
					indent += "   "
				else:
					lineEnding = ""
					tree += indent + node +"("
			
			# ==== composite nodes ====
			
			elif node.lower() in self.compositeNodes:
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				if insideSubtree: tree += indent
				tree += node + "(" + chromosome[i+1] + ", " + chromosome[i+2] + ")"
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0: tree += ", "
				tree += lineEnding
				insideComposite = 2
				
			elif insideComposite > 0:
				insideComposite -= 1
				continue
			
			# ======= terminals =======
			
			else:
				comma = ", " if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1 else ""
				if insideSubtree: tree += indent
				tree += node + comma + lineEnding
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
			
			# ==== closing brackets ====
			
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for i in range(len(childrenRemaining) - 1, -1, -1):
					if childrenRemaining[i] == 0: 
						childrenRemaining.pop()
						if insideSubtree: 
							indent = indent[0:-3]
							tree += indent
						insideSubtree = True
						lineEnding = "\n"
						comma = "" if i == 0 or childrenRemaining[i-1] == 0 else ", "
						tree += ")" + comma + lineEnding
					else: break
		
		return tree

	def printChromosome(self, chromosome):
		
		tree = self.primitivetree.from_string(chromosome, self.pset)
		self.resetLists()
		self.parseSubtreeGreedy(tree)
		chromosome = self.rebuildChromosome()
		print "\n"+self.formatChromosome(self.output)+"\n"

	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

