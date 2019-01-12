from z3 import *
from Service import *


class Composition:

    # Composition operations for cloud service
    @staticmethod
    def SeqComp(ser1, ser2, pre_ser1, pre_ser2, nodes, bound):
   
        if pre_ser1 == pre_ser2 == True:
            
            constraints = []
            for i in range(bound):
                # index 1 and 2 correspondes to the output node of ser1 and input node of ser2
                constraints += [ nodes[1]['data'][i] == nodes[2]['data'][i] ] 
                constraints += [ nodes[1]['time'][i] == nodes[2]['time'][i] ]
            
            return And(ser1(nodes[:2], bound, pre_ser1), ser2(nodes[2:len(nodes)], bound, pre_ser2), Conjunction(constraints))
        else:
            return True

    @staticmethod
    def ExChoice(ser1, ser2, pre_ser1, pre_ser2, nodes, bound):

        if pre_ser1 == pre_ser2 == True:
            return And(ser1(nodes[:2], bound, pre_ser1), ser2(nodes[2:len(nodes)], bound, pre_ser2))
        elif pre_ser1 == True and pre_ser2 == False:
            return ser1(nodes[:2], bound, pre_ser1)
        elif pre_ser1 == False and pre_ser2 == True:
            return ser2(nodes[2:len(nodes)], bound, pre_ser2)
        else:
            return True

    @staticmethod
    def InChoice(ser1, ser2, pre_ser1, pre_ser2, nodes, bound): 
        # The intersection of the two input nodes is not empty should be added here. But need more clarity for the needs

        if pre_ser1 == pre_ser2 == True:
            return Or(ser1(nodes[:2], bound, pre_ser1), ser2(nodes[2:len(nodes)], bound, pre_ser2))
        else:
            return True

    @staticmethod
    def ConChoice(ser1, ser2, pre_ser1, pre_ser2, nodes, bound, bool_con): 
        # Consider about the optimization of the extra parameter later 


        if bool_con == True:
            return ser1(nodes[:2], bound, pre_ser1)
        else:
            return ser2(nodes[2:len(nodes)], bound, pre_ser2)

    @staticmethod
    def ParallelComp(ser1, ser2, pre_ser1, pre_ser2, nodes, bound):

        if pre_ser1 == pre_ser2 == True:
            return And(ser1(nodes[:2], bound, pre_ser1), ser2(nodes[2:len(nodes)], bound, pre_ser2))
        else:
            return True

    @staticmethod
    def SyncParallel(ser1, ser2, pre_ser1, pre_ser2, nodes, bound):

        if pre_ser1 == pre_ser2 == True:
            constraints = []
            for i in range(bound):
                constraints += [ nodes[0]['data'][i] == nodes[2]['data'][i] ]
                constraints += [ nodes[0]['time'][i] == nodes[2]['time'][i] ]
            return And(ser1(nodes[:2], bound, pre_ser1), ser2(nodes[2:len(nodes)], bound, pre_ser2), Conjunction(constraints))
        else:
            return True