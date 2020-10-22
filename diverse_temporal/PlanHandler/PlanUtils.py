import json
import re
import copy
from enum import Enum


class Planner(Enum):
    scotty = 1
    optic_plus = 2
    optic = 3


class TemporalPlanReader():
    plan = None
    def __init__(self, planner, planFile = None):
        if planner == Planner.scotty:
            if planFile == None:
                raise ValueError("missing json plan file")
            else:
                with open(planFile) as f:
                    planData = json.load(f)
                self.plan = ScottyTemporalPlanParser(planData["plan"]).GetPlan()
        # elif planner == Planner.optic_plus:
        else:
            with open(planFile, 'r') as fp:
                optic_data = fp.read()
            self.plan = OpticTemporalPlanParser(optic_data,planner).GetPlan()

    def GetPlan(self):
        return self.plan


class ScottyTemporalPlanParser():
    def __init__(self, planData):
        self.events = {}
        self.segments = {}
        ind = 0
        try:
            self.objective = planData["objective"]
        except:
            raise Exception("No plan found")

        self.steps = planData["num-steps"]
        self.makespan = planData["makespan"]

        if len(planData["steps"]) < 1:
            raise ValueError("No plan has been found")

        for step in planData["steps"]:
            index = int(step["index"])
            relatedEvent = int(step["related-step-index"])
            activity = step["action"].lower()

            startTime = round(float(step["step-time"])*1000)/1000.0

            if relatedEvent in self.events:
                isStart = False
                start_e = self.events[relatedEvent]
                s = TemporalSegment(ind, activity, start_e.StartTime, startTime)
                self.segments[start_e.startTime] = s
                duration = startTime - start_e.StartTime
                ind = ind + 1
            else:
                isStart = True
                duration = round(float(step["duration"])*1000)/1000.0
            e = TemporalEvent(index, startTime, duration, activity, isStart, relatedEvent)
            self.events[index] = e
            self.activitiesNum = ind
            tempSeg = {}
            ind = 0
            for i in sorted(self.segments.keys()):
                tempSeg[ind] = self.segments[i]

    def GetPlan(self):
        return IntrimTemporalPlan(self.events, self.segments, self.steps)


class OpticTemporalPlanParser():
    def __init__(self, optic_data, planner):
        self.events = {}
        self.segments = {}
        self.steps = None
        self.planner = planner

        data = re.search("(?s);;;;\s*(.*)\s*",optic_data).group(1)

        # check if any solution was found
        isSol = re.search("Solution Found", data)
        if isSol is None:
            raise Exception("No plan found")

        # pre process the text of the plan
        data = re.sub("(?m)^Solution Found\n", "", data)
        data = re.sub("(?m)^\s*;.*?\n", "", data)
        data = data.rstrip()

        if self.planner == Planner.optic_plus:
            actions = re.findall("(\d*\.\d{3}):\s\((\S+?)\)\s\[(\d*\.\d{3})\]\s;\s\((\d*)\)", data)
        if self.planner == Planner.optic:
            actions = re.findall("(\d*\.\d{3}):\s\((\S+?)\)\s*\[(\d*\.\d{3})\]", data)

        self.steps = len(actions)*2

        # iterate over action in the plan to construct the plan structure and snap actions structure
        ind = 0
        temp_events = {}
        for action in actions:
            start_time = round(float(action[0]),3)
            duration = round(float(action[2]),3)
            end_time = round(start_time+duration,3)
            activity = action[1]
            seg = TemporalSegment(ind, activity, start_time, start_time + duration)
            self.segments[ind] = seg
            if start_time in temp_events:
                start_time = start_time+ 0.0001
            temp_events[start_time] = [activity, start_time, duration, True, end_time]
            if end_time in temp_events:
                end_time = end_time+0.0001
            temp_events[end_time] = [activity, end_time ,duration, False, start_time]
            ind = ind+1
        ordered = sorted(temp_events)
        ind = 0
        for t in ordered:
            e = temp_events[t]
            related = ordered.index(e[4])
            event = TemporalEvent(ind, t, e[2], e[0], e[3], related)
            self.events[ind] = event
            ind = ind + 1


    def GetPlan(self):
        return IntrimTemporalPlan(self.events, self.segments, self.steps)


class IntrimTemporalPlan():
    def __init__(self, events, segments, steps):
        self.events = events
        self.segments = segments
        self.steps = steps

    def GetSnapPlan(self, Map = []):
        localEvents = copy.deepcopy(self.events)
        if len(Map) > 0:
            localEvents = self.RevertToOriginalEventsSpace(localEvents, Map)
        return localEvents

    def RevertToOriginalEventsSpace(self, events, Map=[]):
        if len(Map) == 0:
            return events
        else:
            pattern = re.compile("(?s)(.*?\-)(.*)")
            for i in range(len(Map)):
                map = Map[i]
                for j in range(self.steps):
                    m = pattern.match(events[j].Name)
                    events[j].Name = m.group(1)+map[m.group(2)]
            return events


    def GetPlan(self, Map = []):
        localSegments = copy.deepcopy(self.segments)
        if len(Map) > 0:
            localSegments = self.RevertToOriginalSegmentsSpace(localSegments, Map)
        return localSegments


    def RevertToOriginalSegmentsSpace(self, segments, Map=[]):
        if len(Map) == 0:
            return segments
        else:
            for i in range(len(Map)):
                map = Map[i]
                for key in self.segments.keys():
                    segments[key].Activity = map[segments[key].Activity]
            return segments

    def GetPlanObject(self, Map=[]):
        # print ("hello before reverting to original plan space")
        snapplan = self.GetSnapPlan(Map)
        plan = self.GetPlan(Map)
        # print (plan)
        return TemporalPlan(snapplan, plan, self.steps)


class TemporalPlan():
    def __init__(self, events, segments, steps):
        """
        Constractor of the temporal Plan object
        :param events: dictionary of events where the keys are the event index and the value is event object
        :param segments: dictionary of durative actions, key is the order value is the durative action
        :param steps: number of steps/events in the plan
        """
        self.events = events
        self.segments = segments
        self.steps = steps

    def PrintSnapPlan(self):
        """
        print the events of the plan (the snap action) in the plan order
        :return: string containing the plan
        """
        st = ""
        for i in range(self.steps):
            st = st + self.events[i].ToString() + "\n"
        st = st.rstrip()
        return st

    def PrintPlan(self):
        """
        print the temporal plan
        :return: string containing the plan
        """
        st = ""
        for i in sorted(self.segments.keys()):
            st = st + self.segments[i].ToString() + "\n"
        st = st.rstrip()
        return st

    def GetSnapPlanAsList(self):
        """
        returns the snap action plan, or the events as an ordered list of tuples
        :return: list of tuples
        """
        snaplist = []
        for i in range(self.steps):
            snaplist.append(self.events[i].GetAsTuple())
        return snaplist

    def GetPlanAsList(self):
        """
        returns the temporal actions in durative action triplets tuple, as an ordered list
        :return: list of tuples
        """
        planlist = []
        for i in sorted(self.segments.keys()):
            planlist.append(self.segments[i].GetAsTuple())
        return planlist

    def WritePlanTofile(self, filename):
        """
        Write the plans to file (both long and short versions, in that order)
        :param filename: full path the plan file to be created
        :return: None
        """
        planTxt = "Temporal Short Plan:\n" + self.PrintPlan() + "\n\n"
        planTxt = planTxt + "SnapActions Long Plan:\n" + self.PrintSnapPlan()
        f = open(filename, "w")
        f.write(planTxt)
        f.close()


class TemporalSegment():
    def __init__(self, index, activity, startTime, finalTime):
        self.activity = activity
        self.index = index
        self.startTime = startTime
        self.finalTime = finalTime

    def __str__(self):
        return self.activity

    def ToString(self):
        st = self.activity + "\t" + "{0:.3f}".format(self.startTime) + "\t" + "{0:.3f}".format(self.finalTime - self.startTime) + "\t(" + "{0:.3f}".format(self.finalTime) + ")"
        return st

    def GetAsTuple(self):
        duration = self.finalTime - self.startTime
        tup = (self.activity, self.startTime, duration)
        return tup

    @property
    def Activity(self):
        return self.activity

    @Activity.setter
    def Activity(self, name):
        self.activity = name


class TemporalEvent():
    def __init__(self, index, startT, duration, action, isStart, relatedEvent):
        self.index = index
        self.startTime = startT
        self.duration = duration
        self.endtime = self.startTime + self.duration
        self.activity = action
        self.isStart = isStart
        self.relatedEvent = relatedEvent
        if self.isStart:
            self.eventName = "START-" + self.activity
        else:
            self.eventName = "  END-" + self.activity

    def __str__(self):
        return self.eventName

    def ToString(self):
        st = str(self.index) + "\t" + "{0:.3f}".format(self.startTime) + "\t[ " + "{0:.3f}".format(self.duration) \
             + " :\t" + str(self.relatedEvent) + "]\t" + self.eventName
        return st

    def GetAsTuple(self):
        return (self.index, self.startTime, self.duration, self.relatedEvent, self.eventName)

    @property
    def StartTime(self):
        return self.startTime

    @property
    def Name(self):
        return self.eventName

    @Name.setter
    def Name(self, name):
        self.eventName = name














# class PlanReader():
#     def __init__(self, jsonPlanFile):
#         with open(jsonPlanFile) as f:
#             planData = json.load(f)
#         self.plan = Plan(planData["plan"])
#
#     def GetPlan(self):
#         return self.plan


# class Plan():
#     def __init__(self, planData):
#         self.events = {}
#         self.segments = {}
#         self.IC = {}
#         self.input2sys = {}
#         ind = 0
#
#         self.objective = planData["objective"]
#         self.steps = planData["num-steps"]
#         self.makespan = planData["makespan"]
#
#         if len(planData["steps"]) < 1:
#             raise ValueError("No plan has been found")
#
#         for key in planData["steps"][0]["control-variables-nextstage"].keys():
#             self.IC[key.lower()] = 0.0
#
#         for step in planData["steps"]:
#             index = int(step["index"])
#             relatedEvent = int(step["related-step-index"])
#             activity = step["action"].lower()
#             init_states = {}
#             for key, val in step["state-variables"].items():
#                 init_states[key.lower()] = val
#             controls = {}
#             for key, val in step["control-variables-nextstage"].items():
#                 controls[key.lower()] = round(val, 3)
#             startTime = round(float(step["step-time"])*1000)/1000.0
#
#             if relatedEvent in self.events:
#                 isStart = False
#                 start_e = self.events[relatedEvent]
#                 s = Segment(ind, activity, start_e.StartTime, startTime, start_e.States, init_states, start_e.Controls, controls)
#                 self.segments[start_e.startTime] = s
#                 duration = startTime - start_e.StartTime
#                 ind = ind + 1
#             else:
#                 isStart = True
#                 duration = round(float(step["duration"])*1000)/1000.0
#             e = Event(index, startTime, duration, activity, isStart, init_states, controls, relatedEvent)
#             self.events[index] = e
#             self.activitiesNum = ind
#             tempSeg = {}
#             ind = 0
#             for i in sorted(self.segments.keys()):
#                 tempSeg[ind] = self.segments[i]
#
#     def __str__(self):
#         return "plan"
#
#     def MapInput2Sys(self, controlVars, systems):
#         for func in self.IC.keys():
#             if func in controlVars.keys():
#                 for sys in systems.keys():
#                     if systems[sys].isControl(controlVars[func]):
#                         self.input2sys[func] = sys
#
#     def RevertToOriginalEventsSpace(self, events, Map=[]):
#         if len(Map) == 0:
#             return events
#         else:
#             pattern = re.compile("(?s)(.*?\-)(.*)")
#             for i in range(len(Map)):
#                 map = Map[i]
#                 # print (map)
#                 for j in range(self.steps):
#                     m = pattern.match(events[j].Name)
#                     events[j].Name = m.group(1)+map[m.group(2)]
#             return events
#
#     def RevertToOriginalSegmentsSpace(self, segments, Map=[]):
#         if len(Map) == 0:
#             return segments
#         else:
#             for i in range(len(Map)):
#                 map = Map[i]
#                 for key in self.segments.keys():
#                     segments[key].Activity = map[segments[key].Activity]
#             return segments
#
#
#     def PrintPlan(self, Map=[]):
#         st = ""
#         localEvents = copy.deepcopy(self.events)
#         localEvents = self.RevertToOriginalEventsSpace(localEvents, Map)
#         for i in range(self.steps):
#             st = st + localEvents[i].ToString() + "\n"
#         return st
#
#     def PrintSegments(self, Map=[]):
#         st = ""
#         localSegments = copy.deepcopy(self.segments)
#         localSegments = self.RevertToOriginalSegmentsSpace(localSegments, Map)
#         for i in sorted(localSegments.keys()):
#             st = st + localSegments[i].ToString() + "\n"
#         return st
#
#     @property
#     def GetPlan(self):
#         return self.segments
#
#     def GetEvents(self, Map=[]):
#         if len(Map) > 0:
#             localEvents = copy.deepcopy(self.events)
#             localEvents = self.RevetToOriginalEventsSpace(localEvents, Map)
#             return localEvents
#         return self.events
#
#     def isEqual(self, l1, l2):
#         if len(l1) != len(l2):
#             return False
#         for i in xrange(len(l1)):
#             if l1[i] != l2[i]:
#                 return False
#         return True


# class Event():
#     def __init__(self, index, startTime, duration, action, isStart, states, inputs, relatedEvent):
#         self.index = index
#         self.startTime = startTime
#         self.duration = duration
#         self.endtime = startTime + duration
#         self.activity = action
#         self.isStart = isStart
#         self.states = states
#         self.inputs = inputs
#         self.relatedEvent = relatedEvent
#         if self.isStart:
#             self.eventName = "START-" + self.activity
#         else:
#             self.eventName = "  END-" + self.activity
#
#     def __str__(self):
#         return self.eventName
#
#     def ToString(self):
#         st = str(self.index) + "\t" + "{0:.3f}".format(self.startTime) + "\t[ " + "{0:.3f}".format(self.duration) \
#                 + " :\t" + str(self.relatedEvent) + "]\t" + self.eventName + "\t" + self.Dic2String(self.states) + "\t" + self.Dic2String(self.inputs)
#         return st
#
#
#     @property
#     def Name(self):
#         return self.eventName
#
#     @Name.setter
#     def Name(self, newName):
#         self.eventName = newName
#
#     @property
#     def Duration(self):
#         return self.duration
#
#     @property
#     def Index(self):
#         return self.index
#
#     @property
#     def StartTime(self):
#         return self.startTime
#
#     @property
#     def States(self):
#         return self.states
#
#     @property
#     def Controls(self):
#         return self.inputs
#
#     def Dic2String(self, dic):
#         st = ""
#         for key in dic.keys():
#             if type(dic[key]) is float:
#                 val = "{0:.3f}".format(dic[key])
#             else:
#                 val = str(key)
#             st = st + str(key) + ": " + val + ", "
#         return st


# class Segment():
#     def __init__(self, index, activity, startTime, finalTime, init_states, final_states, init_controls, final_controls):
#         self.activity = activity
#         self.index = index
#         self.startTime = startTime
#         self.finalTime = finalTime
#         self.initStates = init_states
#         self.finalStates = final_states
#         self.initControls = init_controls
#         self.finalControls = final_controls
#
#     @property
#     def Activity(self):
#         return self.activity
#
#     @Activity.setter
#     def Activity(self, newActivityName):
#         self.activity = newActivityName
#
#     def __str__(self):
#         return self.activity
#
#     def GetInitStates(self):
#         return self.initStates.keys()
#
#     def GetInitInputs(self):
#         return self.initControls.keys()
#
#     def ToString(self):
#         duration = self.finalTime - self.startTime
#         # st = str(self.index) + "\t" + "{0:.3f}".format(self.startTime) + "\t" + "{0:.3f}".format(self.finalTime) \
#         #         + "\t" + self.activity #+ "\tInit: " + self.Dic2String(self.initStates) + "\tFinal: " + self.Dic2String(self.finalStates)
#         st = self.activity + "\t" + "{0:.3f}".format(self.startTime) + "\t" + "{0:.3f}".format(self.finalTime - self.startTime) + "\t(" + "{0:.3f}".format(self.finalTime) + ")"
#         return st
#
#     def Dic2String(self, dic):
#         st = ""
#         for key in dic.keys():
#             if type(dic[key]) is float:
#                 val = "{0:.3f}".format(dic[key])
#             else:
#                 val = str(key)
#             st = st + str(key) + ": " + val + ", "
#         return st

