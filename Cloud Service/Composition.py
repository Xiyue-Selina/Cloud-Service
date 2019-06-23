from Service import *

class Composition:

    def __init__(self, composition, serv1, serv2, index, bool_con = True):
        self.composition = composition
        self.serv1 = serv1
        self.serv2 = serv2
        self.index = index
        self.bool_con = bool_con
        self.valueFunctions = { 'SeqComp': self.SeqComp,
                                'ExChoice': self.ExChoice,
                                'InChoice': self.InChoice,
                                'ConChoice': self.ConChoice,
                                'ParallelComp': self.ParallelComp,
                                'SyncParallel': self.SyncParallel,
                              }

    # Composition operations for cloud service
    def SeqComp(self, bound, nodesParam1, nodesParam2):
        if self.serv1.preCondition == self.serv2.preCondition == True:
            constraints = []
            for i in range(bound):
                # index is used to indicate the node under specification when there are more than two output nodes
                constraints += [ nodesParam1[self.index]['data'][i] == nodesParam2[0]['data'][i] ] 
                constraints += [ nodesParam1[self.index]['time'][i] == nodesParam2[0]['time'][i] ]

            return And( self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1),
                        self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2),
                        Conjunction(constraints))
        else:
            return True

    def ExChoice(self, bound, nodesParam1, nodesParam2):

        if self.serv1.preCondition == self.serv2.preCondition == True:
            return And( self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1),
                        self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2))
        elif self.serv1.preCondition == True and self.serv2.preCondition == False:
            return self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1)
        elif self.serv1.preCondition == False and self.serv2.preCondition == True:
            return self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2)
        else:
            return True

    def InChoice(self, bound, nodesParam1, nodesParam2): 
        # The intersection of the two input nodes is not empty can be realized by renaming
        if self.serv1.preCondition == self.serv2.preCondition == True:
            return Or( self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1),
                       self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2))
        else:
            return True

    def ConChoice(self, bound, nodesParam1, nodesParam2): 

        if self.bool_con == True:
            return self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1)
        else:
            return self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2)

    def ParallelComp(self, bound, nodesParam1, nodesParam2):

        if self.serv1.preCondition == self.serv2.preCondition == True:
            return And( self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1),
                        self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2))
        else:
            return True

    def SyncParallel(self, bound, nodesParam1, nodesParam2):

        if self.serv1.preCondition == self.serv2.preCondition == True:
            constraints = []
            for i in range(bound):
                constraints += [ nodesParam1[0]['data'][i] == nodesParam2[0]['data'][i] ]
                constraints += [ nodesParam1[0]['time'][i] == nodesParam2[0]['time'][i] ]
            return And( self.serv1.valueFunctions[self.serv1.service](bound, nodesParam1),
                        self.serv2.valueFunctions[self.serv2.service](bound, nodesParam2),
                        Conjunction(constraints))
        else:
            return True
