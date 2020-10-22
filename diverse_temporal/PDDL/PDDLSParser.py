import sys
import re
from diverse_temporal.PDDL.PDDLSTypes import *
from diverse_temporal.PDDL.PDDLInstance import *


class PDDLSParser():
	def __init__(self, domainFile, problemFile):
		self.domainFile = domainFile
		self.problemFile = problemFile
		self.PlanningInstance = None

	def GetParsedInstance(self):
		fh = open(self.domainFile, "r")
		domainTxt = fh.read()
		domainTxt = domainTxt.lower() + "\n\n"
		fh.close()
		domainTxt = self.__RemoveComments(domainTxt)
		domainTxt = self.__RemoveLastBracket(domainTxt)

		name = self.__ParseName(domainTxt)

		# initialize the planning problem instance
		self.PlanningInstance = PDDLSInstance(name)

		# add the requirements of the pddl domain
		reqs = self.__ParseRequirements(domainTxt)
		self.PlanningInstance.AddRequirements(reqs)

		# add the predicates of the pddl domain
		predicates = self.__ParsePredicates(domainTxt)
		self.PlanningInstance.AddPredicates(predicates)

		functions = self.__ParseFunctions(domainTxt)
		self.PlanningInstance.AddFunctions(functions)

		# add the possible activities in the pddl domain
		activities = self.__ParseActivities(domainTxt, predicates)
		self.PlanningInstance.AddActivities(activities)

		# add initial state
		fh = open(self.problemFile, "r")
		problemTxt = fh.read()
		problemTxt = problemTxt.lower()
		fh.close()
		problemTxt = self.__RemoveComments(problemTxt)
		initState = self.__ParseInitState(problemTxt, predicates, functions)
		self.PlanningInstance.AddInitState(initState)

		goalSet = self.__ParseGoalSet(problemTxt, predicates)
		self.PlanningInstance.AddGoalSet(goalSet)

		metric = self.__ParseMetric(problemTxt)
		self.PlanningInstance.AddMetric(metric)

		return self.PlanningInstance

	def __RemoveComments(self, txt):
		txt = re.sub("(?m)^\s*;.*?\n", "\n", txt)
		return txt

	def __RemoveLastBracket(self, txt):
		m = re.search('(?s)(.*)\)', txt)
		txt = m.group(1)
		txt = txt + '\n(:'
		return txt

	def __ParseName(self, domTxt):
		m = re.search("(?s)\(define\s*\(domain\s(.*?)\)", domTxt)
		return m.group(1)

	def __ParseRequirements(self, domTxt):
		m = re.search("(?s)\((:requirements.*?)\)", domTxt)
		if m is None:
			return None
		reqs = m.group(1)

		m = re.search(":duration-inequalities", reqs)
		if m is None:
			reqs = reqs + " :duration-inequalities"

		m = re.search(":negative-preconditions", reqs)
		if m is None:
			reqs = reqs + " :negative-preconditions"

		m = re.search(":strips", reqs)
		if m is None:
			reqs = reqs + " :strips"
		return reqs

	def __ParsePredicates(self, domTxt):
		preds = {}
		# m = re.search("(?s)\(:predicates\s+(\S+\s+)*?\)", domTxt).group(0)
		m = re.search("(?s)\(:predicates\s*.*?\)\s*\)", domTxt).group(0)
		if m is None:
			return None
		m = re.search("(?s)\(:predicates.*?(\S+.*)\)", m).group(0)
		m = re.search("(?s)\((\S+)\)(.*)", m)
		while m is not None:
			predName = m.group(1)
			p = Predicate(predName)
			preds[predName] = p
			m = m.group(2)
			m = re.search("(?s)\((\S+)\)(.*)", m)
		return preds

	def __ParseFunctions(self, domTxt):
		funcs = {}
		# m = re.search("(?s)\(:functions\s*.*?\)\s*\)", domTxt).group(0)
		m = re.search("(?s)\(:functions\s*(.*?)\)\s*\(\:", domTxt)#.group(0)
		if m is None:
			return None
		m = m.group(0)
		# m = re.search("(?s)\(:functions.*?(\S+.*)\)", m).group(0)
		m = re.search("(?s)\(:functions\s*(.*)\)", m).group(0)
		m = re.search("(?s)\((\S+)\)(.*)", m)
		while m is not None:
			funcName = m.group(1)
			p = Predicate(funcName)
			funcs[funcName] = p
			m = m.group(2)
			m = re.search("(?s)\((\S+)\)(.*)", m)
		return funcs



	def __ParseActivities(self, domTxt, predicates):
		act = {}
		# actions = self.__ParseUngroundedActions(domTxt, predicates)
		duractions = self.__ParseUngroundedDurativeActions(domTxt, predicates)
		# allActivities = actions + duractions
		allActivities = duractions
		for activity in allActivities:
			act[activity.name] = activity
		return act

	def __ParseUngroundedDurativeActions(self, domTxt, predicates):
		duractions = []
		# remove headers first
		domTxt = re.search("(?s)\(define.*?\)\s*\(:requirements.*?\)\s*(.*)", domTxt).group(1)
		# m = re.findall("(?s):durative-action\s*.*?\s*:duration\s*.*?:condition\s*\(and\s*.*?\s*\)\s*:effect\s*\(and\s*.*?\)\s*\)\s*\)\n[\n\(]", domTxt)
		# m = re.findall(
		# 	"(?s)durative-action\s*.*?\s*:duration\s*.*?:condition\s*\(and\s*.*?\s*\)\s*:effect\s*\(and\s*.*?\)\s*\)\s*\(\:|durative-action\s*.*?\s*:duration\s*.*?:condition\s*\(and\s*.*?\s*\)\s*:effect\s*\(and\s*.*?\)\s*\)\s*\Z", domTxt)
		m = re.findall("(?s)(?=(\(:durative-action.*?\(:))", domTxt)
		for daction in m:
			# m_d = re.search("(?s)durative-action\s*(.*?)\s*:duration\s*(.*?):condition\s*\(and\s*(.*?)\s*\)\s*:effect\s*\(and\s*(.*?\))\s+\)", daction)
			m_d = re.search(
				"(?s)\(:durative-action\s*(.*?)\s*:duration\s*\((.*?)\)\s*:condition\s*\(\s*(.*?)\)\s*:effect\s*\((.*?)\)\s*\)\s*\(:",
				daction)
			name = m_d.group(1)
			durations = m_d.group(2)
			cond = m_d.group(3)
			eff = m_d.group(4)

			# parse name and parameters
			m_param = re.search("\s*(.*?)\s*:parameters\s*\((.*?)\)\s*", name)
			if m_param is not None:
				name = m_param.group(1)
				params = m_param.group(2)
				params = re.findall("(?s)\?(\w*)", params)
			else:
				params = []

			# parse durations
			dur_lb = 0
			dur_ub = 0
			m_dur = re.search(
				"(?s)and\s*\(([<>])?[=]?\s*\?duration\s*(\d*[.,]?\d*?)\)\s*\([<>]?[=]?\s*\?duration\s*(\d*[.,]?\d*?)\)",
				durations)
			# m_dur = re.search("(?s)\(\s*and\s*\(\s*\>\s*\=\s*\?duration\s*(\d*[.,]?\d*?)\)\s*\(\<\=\s*\?duration\s*(\d*[.,]?\d*?)\)\)", durations)
			if m_dur is not None:
				if m_dur.group(1) == '<':
					dur_ub = m_dur.group(2)
					dur_lb = m_dur.group(3)
				else:
					dur_ub = m_dur.group(3)
					dur_lb = m_dur.group(2)
			else:
				m_dur = re.search("(?s)\s*=\s*\?duration\s*(\d*[.,]?\d*?)", durations)
				if m_dur is not None:
					dur_lb = m_dur.group(1)
					dur_ub = m_dur.group(1)

			# parse conditions
			parsedConditions = []
			conds = re.findall("\((.*)\)", cond)
			try:
				for cond in conds:
					if cond != "":
						parsedCondition = self.__ParseDurativeConditionsEffects(cond, predicates)
						parsedConditions.append(parsedCondition)
			except Exception as e:
				raise ValueError(str(e) + " " + name)
			# parse effects
			parsedEffects = []
			effs = re.findall("\((.*)\)", eff)
			try:
				for ef in effs:
					# print (ef)
					if ef != "":
						parsedEffect = self.__ParseDurativeConditionsEffects(ef, predicates)
						parsedEffects.append(parsedEffect)
			except Exception as e:
				raise ValueError(str(e) + " " + name)
			action = DurativeAction(name, params, [dur_lb, dur_ub], parsedConditions, parsedEffects)
			duractions.append(action)
		return duractions

	def __ParseDurativeConditionsEffects(self, expr, predicates):
		singleCond = re.search("(?s)(\w+\s\w+)\s*\((.*)\)", expr)

		timedDescriptor = singleCond.group(1)
		rest = singleCond.group(2)
		# regular negative predicate
		isNot = re.search("(?s)\s*not\s\((.*?)\s*\)", rest)
		if isNot != None:
			pred = isNot.group(1)
			if pred not in predicates:
				raise ValueError("Parsing Error: unrecognized predicate " + pred + " in durative action")
			else:
				parsedCondition = TimedConditionalPredicate(predicates[pred], timedDescriptor, False)
		else:
			isPredicate = re.search("(?s)^\s*(.*?)\s*(\)|$)", rest)
			if isPredicate is not None:
				pred = isPredicate.group(1)
				try:
					parsedCondition = TimedConditionalPredicate(predicates[pred], timedDescriptor, True)
				except:
					raise ValueError("Unrecognized predicate " + pred + " in durative action parsing: " + singleCond.group(0))
			else:
				raise ValueError("Unrecognized condition: " + expr)
		return parsedCondition


	def __ParseInitState(self ,probTxt, predicates, functions):
		initF = {}
		m = re.search("(?s)\(:init\s*(.*?)\s*\)\s*\(:goal", probTxt)
		initFunctions = re.findall("(?s)\(\s*=\s*\(.*?\)\s*\d+[.,]?\d*\s*\)", m.group(1))
		f = re.compile("(?s)\(\s*=\s*\(.*?\)\s*\d+[.,]?\d*\s*\)")
		b = f.sub("", m.group(1))
		initPredicates = re.findall("(?s)\(\s*?(\S*?)\s*?\)", b)

		for func in initFunctions:
			m_f = re.search("(?s)\(\s*=\s*\((.*?)\)\s*(\d+[.,]?\d*)\s*\)", func)
			f = m_f.group(1)
			val = m_f.group(2)
			try:
				af = AssignedFunction(f, functions[f], val)
			except:
				raise ValueError("error in function name, in init state parsing: no such function exist in domain")
			initF[f] = af

		for pred in initPredicates:
			try:
				initF[pred] = predicates[pred]
			except:
				raise ValueError("error in predicate name in init state parsing: no such predicate exist in domain " + pred)


		return initF

	# TODO: add support for numeric constraints
	def __ParseGoalSet(self, probTxt, predicates):
		goalF = {}
		notpreds = []
		m = re.search("(?s)\(:goal\s*?\(\s*?and\s*.*?\)\s*?\)\s*?\)", probTxt)

		# negative conditioned predicates
		preds = re.findall("(?s)\(not\s*\((\S*?)\)", m.group(0))
		for pred in preds:
			try:
				goalF[pred] = ConditionalPredicate(predicates[pred], False)
				notpreds.append(pred)
			except:
				raise ValueError("error in predicate name in goal set parsing, no such predicate exist in domain: " + pred)

		# positive conditioned predicates
		preds = re.findall("(?s)\((\S*?)\)", m.group(0))
		for pred in preds:
			try:
				if pred not in notpreds:
					goalF[pred] = ConditionalPredicate(predicates[pred], True)
			except:
				raise ValueError("error in predicate name in goal set parsing, no such predicate exist in domain")

		return goalF


	def __ParseMetric(self, probTxt):
		m = re.search("(?s)\(:metric\s*?minimize\s*?\(\s*?(.*?)\)\s*?\)", probTxt).group(1)
		metricD = m
		return metricD
