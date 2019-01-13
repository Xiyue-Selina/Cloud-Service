from z3 import *

def Conjunction(constraints):
    assert len(constraints) > 0

    result = None
    for c in constraints:
        if result is None:
            result = c
        else:
            result = And(result, c)

    return result

class Service:

    def __init__(self, service, pre_condition, nodes):
        self.service = service
        self.preCondition = eval(pre_condition)
        self.nodes = nodes
        self.valueFunctions = { 'Sync': self.SyncSer,
                                'Buffer': self.BufferSer,
                                'Merger': self.MergeSer,
                                'Router': self.RouterSer,
                              }

    # Simple cloud services
    def SyncSer(self, bound, nodesParam):
        if self.preCondition == True:
            assert len(self.nodes) >= 2

            target_num = len(self.nodes) - 1
            constraints = []
            for i in range(target_num):
                for j in range(bound):
                    constraints += [ nodesParam[0]['data'][j] == nodesParam[i + 1]['data'][j] ]
                    constraints += [ nodesParam[0]['time'][j] == nodesParam[i + 1]['time'][j] ]
            return Conjunction(constraints)
        else:
            return True

    def BufferSer(self, bound, nodesParam):
        if self.preCondition == True:
            assert len(self.nodes) == 2

            constraints = []
            for i in range(bound):
                constraints += [ nodesParam[0]['data'][i] == nodesParam[1]['data'][i] ]
                constraints += [ nodesParam[0]['time'][i] <  nodesParam[1]['time'][i] ]
            for i in range(bound - 1):
                constraints += [ nodesParam[0]['time'][i + 1] > nodesParam[1]['time'][i] ]

            return Conjunction(constraints)
        else:
            return True

    def Merge(self, bound, nodesParam, idx_1 = 0, idx_2 = 0): 
        assert len(self.nodes) == 3

        if bound == idx_1 + idx_2:
            return True
        constraints_1 = []
        constraints_2 = []
        constraints_1 += [ nodesParam[0]['data'][idx_1] == nodesParam[2]['data'][idx_1 + idx_2]]
        constraints_1 += [ nodesParam[0]['time'][idx_1] == nodesParam[2]['time'][idx_1 + idx_2]]
        constraints_1 += [ nodesParam[0]['time'][idx_1] <  nodesParam[1]['time'][idx_2]]
        constraints_2 += [ nodesParam[1]['data'][idx_2] == nodesParam[2]['data'][idx_1 + idx_2]]
        constraints_2 += [ nodesParam[1]['time'][idx_2] == nodesParam[2]['time'][idx_1 + idx_2]]
        constraints_2 += [ nodesParam[1]['time'][idx_2] <  nodesParam[0]['time'][idx_1]]
        return Or(And(Conjunction(constraints_1), self.Merge(bound, nodesParam, idx_1 + 1, idx_2)),
                  And(Conjunction(constraints_2), self.Merge(bound, nodesParam, idx_1, idx_2 + 1)))

    def MergeSer(self, bound, nodesParam):
        if self.preCondition == True: 
            assert 2 <= len(self.nodes) <=3 

            if len(self.nodes) == 2:
                constraints = []
                for i in range(bound):
                    constraints += [ nodesParam[0]['data'][i] == nodesParam[1]['data'][i] ]
                    constraints += [ nodesParam[0]['time'][i] == nodesParam[1]['time'][i] ]
                return Conjunction(constraints)
            elif len(self.nodes) == 3:
                return self.Merge(bound, nodesParam)
        else:
            return True

    def RouterSer(self, bound, nodesParam):
        if self.preCondition == True:
            assert len(self.nodes) == 3
            new_nodes = [nodesParam[1], nodesParam[2], nodesParam[0]]
            return self.Merge(bound, new_nodes)
        else:
            return True
