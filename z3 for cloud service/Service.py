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

    # Simple cloud service
    @staticmethod
    def SyncSer(nodes, bound, pre_condition):
        if pre_condition == True:
            assert len(nodes) >= 2

            target_num = len(nodes) - 1
            constraints = []
            for i in range(target_num):
                for j in range(bound):
                    constraints += [ nodes[0]['data'][j] == nodes[i + 1]['data'][j] ]
                    constraints += [ nodes[0]['time'][j] == nodes[i + 1]['time'][j] ]
            return Conjunction(constraints)
        else:
            return True

    @staticmethod
    def BufferSer(nodes, bound, pre_condition):
        if pre_condition == True:
            assert len(nodes) == 2

            constraints = []
            for i in range(bound):
                constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
                constraints += [ nodes[0]['time'][i] <  nodes[1]['time'][i] ]
            for i in range(bound - 1):
                constraints += [ nodes[0]['time'][i + 1] > nodes[1]['time'][i] ]

            return Conjunction(constraints)
        else:
            return True

    @staticmethod
    def MergeSer(nodes, bound, pre_condition):
        if pre_condition == True: 
            assert 2 <= len(nodes) <=3 

            if len(nodes) == 2:
                constraints = []
                for i in range(bound):
                    constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
                    constraints += [ nodes[0]['time'][i] == nodes[1]['time'][i] ]
                return Conjunction(constraints)
            elif len(nodes) == 3:
                return Service.Merge(nodes, bound)
        else:
            return True
        
    def Merge(nodes, bound, idx_1 = 0, idx_2 = 0): 
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
        return Or(And(Conjunction(constraints_1), Service.Merge(nodes, bound, idx_1 + 1, idx_2)),
                  And(Conjunction(constraints_2), Service.Merge(nodes, bound, idx_1, idx_2 + 1)))

    @staticmethod
    def RouterSer(nodes, bound, pre_condition):
        if pre_condition == True:
            assert len(nodes) == 3
            new_nodes = [nodes[1], nodes[2], nodes[0]]
            return Service.Merge(new_nodes, bound)
        else:
            return True   
    

    
   

    
        

