
class KilobotNodes():
	
	def __init__(self, pset):
		
		pset.addPrimitive(self.selm2, [str, str],  str)
		pset.addPrimitive(self.seqm2, [str, str],  str)
		pset.addPrimitive(self.probm2, [str, str],  str)
		pset.addPrimitive(self.selm3, [str, str, str],  str)
		pset.addPrimitive(self.seqm3, [str, str, str],  str)
		pset.addPrimitive(self.probm3, [str, str, str],  str)
		pset.addPrimitive(self.selm4, [str, str, str, str],  str)
		pset.addPrimitive(self.seqm4, [str, str, str, str],  str)
		pset.addPrimitive(self.probm4, [str, str, str, str],  str)

		pset.addDecorator(self.successd, [], [str],  str)
		pset.addDecorator(self.failured, [], [str],  str)
		pset.addDecorator(self.repeat, [kilobotRepetitions], [str],  str)

		pset.addCondition(self.ifltvar, [kilobotReadIndex, kilobotReadIndex], str)
		pset.addCondition(self.ifltcon, [kilobotReadIndex, float], str)
		pset.addCondition(self.ifgevar, [kilobotReadIndex, kilobotReadIndex], str)
		pset.addCondition(self.ifgecon, [kilobotReadIndex, float], str)

		pset.addAction(self.mf, [], str)
		pset.addAction(self.ml, [], str)
		pset.addAction(self.mr, [], str)
		pset.addAction(self.successl, [], str)
		pset.addAction(self.failurel, [], str)
		pset.addAction(self.set, [kilobotWriteIndex, float], str)

		pset.addEphemeralConstant("kilobotWriteIndex", lambda: random.randint(1,2), kilobotWriteIndex)
		pset.addEphemeralConstant("kilobotReadIndex", lambda: random.randint(1,9), kilobotReadIndex)
		pset.addEphemeralConstant("kilobotConstant", lambda: random.uniform(-1, 1), float)
		pset.addEphemeralConstant("kilobotrepetitions", lambda: random.randint(1,9), kilobotRepetitions)

	def seqm2(): print ""
	def selm2(): print ""
	def probm2(): print ""
	def seqm3(): print ""
	def selm3(): print ""
	def probm3(): print ""
	def seqm4(): print ""
	def selm4(): print ""
	def probm4(): print ""
	def set(): print ""
	def mf(): print ""
	def ml(): print ""
	def mr(): print ""
	def ifltvar(): print ""
	def ifltcon(): print ""
	def ifgevar(): print ""
	def ifgecon(): print ""
	def successl(): print ""
	def failurel(): print ""
	def repeat(): print ""
	def successd(): print ""
	def failured(): print ""

class kilobotReadIndex(): x = 1
class kilobotWriteIndex(): x = 1
class kilobotConstant(): x = 1
class kilobotRepetitions(): x = 1
