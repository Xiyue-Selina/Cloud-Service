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

class Channel:
    @staticmethod
    def Sync(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] == nodes[1]['time'][i] ]

        return Conjunction(constraints)

    @staticmethod
    def Fifo1(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] <  nodes[1]['time'][i] ]
            if i != 0:
                constraints += [ nodes[0]['time'][i] > nodes[1]['time'][i-1] ]

        return Conjunction(constraints)

    @staticmethod
    def Fifo1e(e):
        def Fifo1eInstance(nodes, bound):
            assert len(nodes) == 2
            constraints = []
            constraints += [nodes[1]['data'][0] == 1]
            for i in range(bound-1):
                constraints += [nodes[0]['data'][i] == nodes[1]['data'][i + 1]]
                constraints += [nodes[0]['time'][i] < nodes[1]['time'][i + 1]]
            for i in range(bound):
                constraints += [nodes[0]['time'][i] > nodes[1]['time'][i]]

            return Conjunction(constraints)
        return Fifo1eInstance
        
    @staticmethod
    def SyncDrain(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [nodes[0]['time'][i] == nodes[1]['time'][i]]

        return Conjunction(constraints)
    
    @staticmethod
    def LossySync(nodes, bound, idx = 0, num = 0):
        assert len(nodes) == 2
        if bound == num:
            return True
        if bound == idx:
            return True
        constraints_0 = []
        constraints_1 = []
        constraints_0 += [ nodes[0]['time'][idx] != nodes[1]['time'][num]]
        constraints_1 += [ nodes[0]['data'][idx] == nodes[1]['data'][num]]
        constraints_1 += [ nodes[0]['time'][idx] == nodes[1]['time'][num]]
        return Or(And(Conjunction(constraints_0), Channel.LossySync(nodes, bound, idx + 1, num)),
                  And(Conjunction(constraints_1), Channel.LossySync(nodes, bound, idx + 1, num + 1)))

    @staticmethod
    def Merger(nodes, bound, idx_1 = 0, idx_2 = 0):
        assert len(nodes) == 3
        if bound == idx_1 + idx_2:
            return True
        constraints_1 = []
        constraints_2 = []
        constraints_1 += [ nodes[0]['data'][idx_1] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] <  nodes[1]['time'][idx_2]]
        constraints_2 += [ nodes[1]['data'][idx_2] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] <  nodes[0]['time'][idx_1]]
        return Or(And(Conjunction(constraints_1), Channel.Merger(nodes, bound, idx_1 + 1, idx_2)),
                  And(Conjunction(constraints_2), Channel.Merger(nodes, bound, idx_1, idx_2 + 1)))
