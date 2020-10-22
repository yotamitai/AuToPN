import sys
import os
import re
from PDDLSTypes import *
from PDDLSParser import *


#def main():
#	"""main planning loop"""
#	if len(sys.argv) < 4:
#		print("Usage: Jordy.py <domain> <problem>")
#		return
#	
#	domainFile = sys.argv[1]
#	problemFile = sys.argv[2]
#
#	# parse PDDL files
#	parser = PDDLParser(domainFile, problemFile)
#
#	# generate lifted PDDL object
#	liftedPDDL = parser.GetLifted()
#
#	# generate grounded PDDL object
#	groundedPDDL = liftedPDDL.Ground()


def test():

	p = PDDLSParser("../Domains/aliens_domain.pddl", "../Domains/aliens_problem.pddl")
	I = p.GetParsedInstance()


	#print I

	#a1 = [('*', '1.0', '-', 'x1', 'x2'), ('*', '2.414', '-', 'y1', 'y2')]
	#a2 = [('*', '-2.0', '-', 'x1', 'x2'), ('*', '0.414', '-', 'y1', 'y2')]
	#in1 = ['<=', a1, '+', '2.1']
	#in2 = ['<=', a2, '+', '32.1']
	#cond = [in1, in2]

	#print cond
	#r = ConvRegion("mission", ("x1","y1", "x2", "y2"), cond)
	#print r

	#r = System("auv",["x","y"], ["vel-x","vel-y"],"bb")
	#print r
	
	#print r.ToPDDL()

	#st = "(* -1.0 (- ?x1 ?x2)) (* 2.414 (- ?y1 ?y2))"
	#a = re.findall("\(([*\/])\s*([-]?\d+[.]\d*)\s*\(([-+])\s*\?(\S+)\s*\?(\S+)\)\)", st)
	#print a
	
	#print type(r)



if __name__ == "__main__":
	#main()
	test()








    
