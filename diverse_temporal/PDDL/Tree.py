import queue


class Node:
    def __init__(self, obj):
        self.parent = None
        self.children = []
        self.content = obj

    def GetParent(self):
        return self.parent

    def SetParent(self, par):
        self.parent = par

    def GetChildren(self):
        return self.children

    def AddChild(self, node):
        self.children.append(node)
        node.SetParent(self)

    def IsLeaf(self):
        if len(self.children) == 0:
            return True
        return False

    def IsRoot(self):
        if self.parent is None:
            return True
        return False

    def GetValue(self):
        return self.content

    def SetValue(self, obj):
        self.content = obj

    def __str__(self):
        return str(self.content)


    def __searchTree(self, obj):
        Q = queue.Queue()
        Q.put(self)
        while Q.qsize() > 0:
            node = Q.get()
            if node.content == obj:
                return node
            children = node.GetChildren()
            for n in children:
                Q.put(n)
        return None

    def GetSubTree(self, obj):
        return self.__searchTree(obj)


    def GetDescendant(self, obj):
        subT  = self.__searchTree(obj)
        Q = queue.Queue()
        Q.put(subT)
        L = []
        while Q.qsize() > 0 :
            node = Q.get()
            L.append(str(node))
            children = node.GetChildren()
            for child in children:
                Q.put(child)
        return L


    def PrintContent(self):
        L = self.GetDescendant(self.content)
        return L