

# base class for all pddl objects
class PDDLElement():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# base class for binary predicates
class Predicate(PDDLElement):
    def __init__(self, name):
        PDDLElement.__init__(self, name)

    def ToPDDL(self):
        return self.name


# conditional predicate (true\false)
class ConditionalPredicate(PDDLElement):
    def __init__(self, predicate, state):
        PDDLElement.__init__(self, str(predicate))
        self.predicate = predicate
        self.state = state

    def ToPDDL(self):
        if self.state:
            return self.name
        else:
            return "not (" + self.name + ")"

    def __str__(self):
        return self.name


# timed conditional predicate (at start\at end\over all) and (true\false)
class TimedConditionalPredicate(ConditionalPredicate):
    def __init__(self, predicate, time, state):
        ConditionalPredicate.__init__(self, predicate, state)
        if time in ["at start", "at end", "over all"]:
                self.time = time
        else:
                raise ValueError('Invalid time condition at TimedConditionalPredicate initilization')

    def ToPDDL(self):
        return self.time + " (" + ConditionalPredicate.ToPDDL(self) + ")"

    def __str__(self):
        return self.name


# base class for numeric functions
class Function(PDDLElement):
    def __init__(self, name):
        PDDLElement.__init__(self, name)


class AssignedFunction(PDDLElement):
    def __init__(self, name, func, val):
        PDDLElement.__init__(self, name)
        self.function = func
        self._value = val

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        if self._value != value:
            self._value = value

    def ToPDDL(self):
        st = "= (" + str(self.function) + ") " + str(self._value)
        return st


class StateVariable(Function):
    def __init__(self, name):
        Function.__init__(self, name)


class Battery(Function):
    def __init__(self, name):
        Function.__init__(self, name)


# control variable class
class ControlVariable(PDDLElement):
    def __init__(self, name, lb, ub):
        PDDLElement.__init__(self, name)
        self.lb = lb
        self.ub = ub

    def ToPDDL(self):
        st = "(:control-variable " + self.name + "\n"
        st = st + "\t:bounds (and (>= ?value " + str(self.lb) + ") "
        st = st + "(<= ?value " + str(self.ub) +"))\n)"
        return st

    def GetBounds(self):
        return [self.lb, self.ub]
            

# control vector class
class ControlVariableVector(PDDLElement):
    def __init__(self, name, u1, u2, norm):
        PDDLElement.__init__(self, name)
        self.u1 = u1
        self.u2 = u2
        self.norm = norm

    def ToPDDL(self):
        st = "(:control-variable-vector " + self.name + "\n"
        st = st + "\t:control-variables ((" + str(self.u1) + ") (" + str(self.u2) + "))\n"
        st = st + "\t:max-norm " + str(self.norm) + "\n)"
        return st


# control variable derivative - acceleration if the control vectors are velocities
class ControlVariableDerivative(PDDLElement):
    def __init__(self, name, lb, ub, contVar):
        PDDLElement.__init__(self, name)
        self.lb = lb
        self.ub = ub
        self.ControlVar = contVar

    def ToPDDL(self):
        st = "(:control-variable-derivative " + self.name + "\n"
        st = st + "\t:control-variable " + str(self.ControlVar) + "\n"
        st = st + "\t:bounds (and (>= ?value " + str(self.lb) + ") "
        st = st + "(<= ?value " + str(self.ub) +"))\n)"
        return st

    @property
    def ControlVariable(self):
        return self.ControlVar

    def GetBounds(self):
        return [self.lb, self.ub]


# initialized function (value)
class InitializedFunction():
    def __init__(self, function, inequality, value):
        self.name = str(function)
        self.function = function
        self.value = value
        if inequality in [">=","<=","=="]:
                self.inequality = inequality
        else:
                raise ValueError('Invlid ineqaulity symbol')

    def ToPDDL(self):
        return self.inequality + " (" + self.name + ") " + str(self.value)

    def __str__(self):
        return self.name


# timed initialized function (at start\at end\over all) and value
class TimedInitializedFunction():
    def __init__(self, function, inequality, value, time):
        self.name = str(function)
        self.initFunction = InitializedFunction(function, inequality, value)
        if time in ["at start", "at end", "over all"]:
                self.time = time
        else:
                raise ValueError('Invalid time condition')

    def ToPDDL(self):
        return self.time + " (" + self.initFunction.ToPDDL() + ")"

    def __str__(self):
        return self.name


# class for numeric effects in durative actions
class NumericEffect():
    def __init__(self, incdec, function, op, control, normpwr, coefficient=1):
        if incdec in ["increase", "decrease"]:
            self.incdec = incdec
        else:
            raise ValueError('Invalid numeric operation')

        self.name = incdec + " " + str(function)
        self.function = function
        self.op = op
        self.coefficient = coefficient
        self.control = control

        if normpwr is not None:
            if normpwr in ["norm", "norm-sq"]:
                self.normpwr = normpwr
            else:
                raise ValueError('Invalid control vector norm type')
        else:
            self.normpwr = None

    @property
    def IncDec(self):
        return self.incdec

    @property
    def Output(self):
        return self.function

    @property
    def Input(self):
        return self.control

    def __str__(self):
        return self.name

    def ToPDDL(self):
        if self.normpwr is None:
            st = self.incdec + " (" + str(self.function) + ") (" + self.op + " "
            st = st + str(self.coefficient) + " (" + str(self.control) + ") #t)"
        else:
            st = self.incdec + " (" + str(self.function) + ") (" + self.op + " "
            st = st + str(self.coefficient) + " (" + self.normpwr + " (" + str(self.control) + ")) #t)"
        return st


# base class for all regions
class Region(PDDLElement):
    def __init__(self, name, parameters):
        PDDLElement.__init__(self, name)
        self.parameters = parameters

    def GetType(self):
        return

    def GetGrounded(self, states):
        return

    def GetParams(self):
        return self.parameters


# rectangular region
class RectRegion(Region):
    def __init__(self, name, parameters, corner, width, height):
        Region.__init__(self, name, parameters)
        self.corner = corner
        self.width = width
        self.height = height

    def ToPDDL(self):
        st = "(:region " + self.name + "\n"
        st = st + "\t:parameters (?" + self.parameters[0] + " ?" + self.parameters[1] + ")\n"
        st = st + "\t:condition (and (in-rect (?" + self.parameters[0] + " ?" + self.parameters[1] + ") "
        st = st + ":corner (" + str(self.corner[0]) + " " + str(self.corner[1]) + ") "
        st = st + ":width " + str(self.width) + " :height " + str(self.height) + "))\n)"
        return st

    def __str__(self):
        return self.name

    def GetType(self):
        return "rect-region"

    def GetGrounded(self, states):
        return RectRegion(self.name, states, self.corner, self.width, self.height)


# circlar region
class CircleRegion(Region):
    def __init__(self, name, parameters, center, r):
        Region.__init__(self, name, parameters)
        self.center = center
        self.r = r

    def ToPDDL(self):
        st = "(:region " + self.name + "\n"
        st = st + "\t:parameters (?" + self.parameters[0] + " ?" + self.parameters[1] + ")\n"
        st = st + "\t:condition (and (in-circle (?" + self.parameters[0] + " ?" + self.parameters[1]+") "
        st = st + ":center (" + str(self.center[0]) + " " + str(self.center[1]) + ") "
        st = st + ":r " + str(self.r) + "))\n)"
        return st

    def __str__(self):
        return self.name

    def GetType(self):
        return "circle-region"

    def GetGrounded(self, states):
        return CircleRegion(self.name, states, self.center, self.r)


# polygonal region
class PolyRegion(Region):
    def __init__(self, name, parameters, vertices):
        Region.__init__(self, name, parameters)
        self.vertices = vertices

    def ToPDDL(self):
        ver = "("
        for v in self.vertices:
            ver = ver + "(" + str(v[0]) + " " + str(v[1]) + ")"
        ver = ver + ")"
        st = "(:region " + self.name + "\n"
        st = st + "\t:parameters (?" + self.parameters[0] + " ?" + self.parameters[1] + ")\n"
        st = st + "\t:condition (and (in-poly (?" + self.parameters[0] + " ?" + self.parameters[1] + ") "
        st = st + ":vertices " + ver + "))\n)"
        return st

    def __str__(self):
        return self.name

    def GetType(self):
        return "poly-region"

    def GetGrounded(self, states):
        return PolyRegion(self.name, states, self.vertices)


# max distance between agents (semi-region)
class DistRegion(Region):
    def __init__(self, name, parameters, d):
        Region.__init__(self, name, parameters)
        self.d = d

    def ToPDDL(self):
        st = "(:region " + self.name + "\n"
        st = st + "\t:parameters (?" + self.parameters[0] + " ?" + self.parameters[1]
        st = st + " ?" + self.parameters[2] + " ?" + self.parameters[3] + ")\n"
        st = st + "\t:condition (and (max-distance ((?" + self.parameters[0] + " ?" + self.parameters[1]
        st = st+") (?" + self.parameters[2] + " ?" + self.parameters[3] + ")) :d " + str(self.d)+"))\n)"
        return st

    def __str__(self):
        return self.name

    def GetType(self):
        return "maxdist-region"

    def GetGrounded(self, states):
        return PolyRegion(self.name, states, self.d)


# convex inequalities region
class ConvRegion(Region):
    def __init__(self, name, parameters, cond):
        Region.__init__(self, name, parameters)
        self.cond = cond

    def ToPDDL(self):
        st = "(:region " + self.name + "\n"
        st = st + "\t:parameters (?" + self.parameters[0] + " ?" + self.parameters[1]
        st = st + " ?" + self.parameters[2] + " ?" + self.parameters[3] + ")\n"
        st = st + "\t:condition (and (\n"
        cond = ""
        for c in self.cond:
            cond = cond + "\t\t(" + str(c[0]) + " (" + c[2] + " "
            cond = cond + "(" + c[1][0][0] + " " + c[1][0][1] + " (" + c[1][0][2] + " ?" + c[1][0][3] + " ?" + c[1][0][4] + ")) "
            cond = cond + "(" + c[1][1][0] + " " + c[1][1][1] + " (" + c[1][1][2] + " ?" + c[1][1][3] + " ?" + c[1][1][4] + "))) " + str(c[3]) + ")\n"
        st = st + cond
        st = st + "\t)\n)"
        return st

    def __str__(self):
        return self.name

    def GetType(self):
        return "conv-region"

    def GetGrounded(self, states):
        return ConvRegion(self.name, states, self.cond)


class TimedGroundedRegion(PDDLElement):
    def __init__(self, region, time):
        PDDLElement.__init__(self, region.name)
        self.region = region
        if time in ["at start", "at end", "over all"]:
            self.time = time
        else:
            raise ValueError('Invalid time condition')

    def __str__(self):
        return self.name

    def ToPDDL(self):
        st = self.time + " (inside (" + self.name
        params = self.region.parameters
        for p in params:
            st = st + " (" + str(p) + ")"
        st = st + "))"
        return st

    @property
    def Region(self):
        return str(self.region)


class System(PDDLElement):
    def __init__(self, name, states, controls, battery=None, param=1):
        PDDLElement.__init__(self, name)
        self.param = param
        self.battery = battery
        self.states = {"x": states[0], "y": states[1]}
        self.controls = {"x": controls[0], "y": controls[1]}
        self.accelerations = {}

    def SetAcceleration(self, acc):
        if str(acc.ControlVariable) == str(self.controls["x"]):
            self.accelerations["x"] = acc
        elif str(acc.ControlVariable) == str(self.controls["y"]):
            self.accelerations["y"] = acc
        else:
            raise ValueError("No corresponding control variable in system: " + self.name)

    def __str__(self):
        return self.name

    def GetInput(self):
        return self.controls

    def GetState(self):
        return self.states

    def GetInputDerivatives(self):
        return self.accelerations

    @property
    def Param(self):
        return self.param

    def ToPDDL(self):
        st = "(:system " + self.name + "\n"
        st = st + "\t:input ((" + str(self.controls["x"]) + ") (" + str(self.controls["y"]) + "))\n"
        st = st + "\t:output ((" + str(self.states["x"]) + ") (" + str(self.states["y"]) + "))\n"
        if self.battery is not None:
            st = st + "\t:battery ((" + str(self.battery) + "))\n"
        else:
            st = st + "\t:battery ()\n"
        st = st + "\t:parameters ("
        for p in self.param:
            st = st + "(" + str(p) + ") "
        st = st.rstrip()
        st = st + ")\n)"
        return st

    def isControl(self, control):
        if control in self.controls.values():
            return True
        return False

    def isState(self, state):
        if state in self.states.values():
            return True
        return False

    def isBattery(self, bat):
        if self.battery is None:
            return False
        if bat is self.battery:
            return True


class Physical(PDDLElement):
    def __init__(self, name, regionName, param):
        PDDLElement.__init__(self, name)
        # print(name, param)
        self.regionName = regionName
        self._param = param

    @property
    def param(self):
        return self._param

    def __str__(self):
        return self.name

    def ToPDDL(self):
        st = "(:physical " + self.name + "\n"
        if self.regionName == "":
            st = st + "\t:regions ()\n"
        else:
            st = st + "\t:regions ((" + self.regionName + "))\n"
        st = st + "\t:parameters (" + str(self._param) + ")\n)"
        return st


# base class for all types of actions
class Activity(PDDLElement):
    def __init__(self, name):
        PDDLElement.__init__(self, name)
        self.conditions = {}
        self.effects = {}
        self.type = None

    def __str__(self):
        return self.name


# actions class
class Action(Activity):
    def __init__(self, name, params, conds, effs, regionName = None):
        Activity.__init__(self, name, regionName)
        self.params = params
        self.conditions = conds
        self.effects = effs

    def GetType(self):
        return "action"

    def __str__(self):
        return self.name

    def ToPDDL(self):
        st = "(:action " + self.name + "\n"
        st = st + "\t:parameters ("
        for p in self.params:
            st = st + "?" + p + " "
        st = st.rstrip()
        st = st + ")\n"
        st = st + "\t:preconditions (and\n"
        for precond in self.conditions:
            st = st + "\t\t(" + precond.ToPDDL() + ")\n"
        st = st + "\t)\n\t:effect (and\n"
        for eff in self.effects:
            st = st + "\t\t(" + eff.ToPDDL() + ")\n"
        st = st + "\t)\n)"
        return st


class DurativeAction(Activity):
    def __init__(self, name, params, durs, conds, effs):
        Activity.__init__(self, name)
        self.parameters = params
        self.durations = durs
        self.conditions = conds
        self.effects = effs

    def GetParams(self):
        return self.parameters

    def GetDuration(self):
        return self.durations

    def GetConditions(self):
        return self.conditions

    def GetEffects(self):
        return self.effects

    def GetType(self):
        return "durative-action"

    def AddEffect(self, eff):
        self.effects.append(eff)

    def AddCondition(self, cond):
        self.conditions.append(cond)

    def ToPDDL(self):
        st = "\t(:durative-action " + self.name + "\n"
        st = st + "\t\t:parameters ("
        ps = False
        for p in self.parameters:
            st = st + p + ","
            ps = True
        if ps:
            st = st[:-1]
        st = st + ")\n"
        st = st + "\t\t:duration (and (>= ?duration " + str(self.durations[0]) + ") (<= ?duration " + str(self.durations[1]) + "))\n"
        st = st + "\t\t:condition (and\n"
        for cond in self.conditions:
            st = st + "\t\t\t(" + cond.ToPDDL() + ")\n"
        st = st + "\t\t)\n"
        st = st + "\t\t:effect (and\n"
        for eff in self.effects:
            st = st + "\t\t\t(" + eff.ToPDDL() + ")\n"
        st = st + "\t\t)\n\t)\n"
        return st


class Metric(PDDLElement):
    def __init__(self, name, val):
        PDDLElement.__init__(self, name)
        self.value = val

    def ToPDDL(self):
        st = "(* " + str(self.value) + " (" + self.name + "))"
        return st


# class PDDLSInstance(PDDLElement):
#     elements = {}
#     def __init__(self, name):
#         PDDLElement.__init__(self, name)
#         self.elements["name"] = name
#
#     def AddRequirements(self, req):
#         self.elements["requirements"] = req
#
#     def GetRequirements(self):
#         return self.elements["requirements"]
#
#     def AddPredicates(self, preds):
#         self.elements["predicates"] = preds
#
#     def GetPredicates(self):
#         return self.elements["predicates"]
#
#     def AddFunctions(self, funcs):
#         self.elements["functions"] = funcs
#
#     def GetFunctions(self):
#         return self.elements["functions"]
#
#     def AddControlVariables(self, contvars):
#         self.elements["control_variables"] = contvars
#
#     def GetControlVariables(self):
#         return self.elements["control_variables"]
#
#     def AddControlVariablesDerivative(self, contvarsder):
#         self.elements["control_variables_derivative"] = contvarsder
#
#     def GetControlVariablesDerivative(self):
#         return self.elements["control_variables_derivative"]
#
#     def AddControlVariableVectors(self, vecs):
#         self.elements["control_variable_vectors"] = vecs
#
#     def GetControlVariableVectors(self):
#         return self.elements["control_variable_vectors"]
#
#     def AddSystems(self, systems):
#         self.elements["systems"] = systems
#
#     def GetSystems(self):
#         return self.elements["systems"]
#
#     def AddRegions(self, regions):
#         self.elements["regions"] = regions
#         return
#
#     def GetRegions(self):
#         return self.elements["regions"]
#
#     def AddPhysicals(self, phys):
#         self.elements["physicals"] = phys
#         return
#
#     def GetPhysicals(self):
#         return self.elements["physicals"]
#
#     def AddActivities(self, acts):
#         self.elements["activities"] = acts
#
#     def GetActivities(self):
#         return self.elements["activities"]
#
#     def AddInitState(self, initState):
#         self.elements["init"] = initState
#
#     def GetInitState(self):
#         return self.elements["init"]
#
#     def GenerateDomainFile(self, domainFileName):
#         # generate name
#         domainTxt = "(define (" + self.elements["name"] + ")\n"
#
#         # generate requirements
#         domainTxt = domainTxt + "(:" + self.elements["requirements"] + ")\n\n"
#
#         # generate predicates
#         domainTxt = domainTxt + "(:predicates\n"
#         for _, pred in self.elements["predicates"].iteritems():
#             domainTxt = domainTxt + "\t(" + str(pred) + ")\n"
#
#         # generate functions
#         domainTxt = domainTxt + ")\n\n(:functions\n"
#         for _, func in self.elements["functions"].iteritems():
#             domainTxt = domainTxt + "\t(" + str(func) + ")\n"
#         domainTxt = domainTxt + ")\n\n"
#
#         # generate control variables
#         for _, contVar in self.elements["control_variables"].iteritems():
#             domainTxt = domainTxt + contVar.ToPDDL() + "\n"
#         domainTxt = domainTxt + "\n"
#
#         # generate control variable vectors
#         for _, contVarVec in self.elements["control_variable_vectors"].iteritems():
#             domainTxt = domainTxt + contVarVec.ToPDDL() + "\n"
#         domainTxt = domainTxt + "\n"
#
#         # generate systems
#         for _, sys in self.elements["systems"].iteritems():
#             domainTxt = domainTxt + sys.ToPDDL() + "\n"
#         domainTxt = domainTxt + "\n"
#
#         # generate regions
#         for _, region in self.elements["regions"].iteritems():
#             domainTxt = domainTxt + region.ToPDDL() + "\n"
#         domainTxt = domainTxt + "\n"
#
#         # generate physicals
#         for _, phy in self.elements["physicals"].iteritems():
#             domainTxt = domainTxt + phy.ToPDDL() + "\n"
#         domainTxt = domainTxt + "\n"
#
#         # generate activities
#         for _, activity in self.elements["activities"].iteritems():
#             domainTxt = domainTxt + activity.ToPDDL() + "\n"
#         domainTxt = domainTxt + ")"
#
#         # TODO: write to file
#         return domainTxt
#
#     def __str__(self):
#         return self.name
#
#
#

