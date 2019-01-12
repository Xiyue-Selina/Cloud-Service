from z3 import *
from Service import *
from Composition import *

# import sys

class Cloud:
    def __init__(self):
        self.services = []
        self.compositions = []

    def config(self, service, pre_condition, *nodes):
        self.services += [(service, pre_condition, nodes)]
        return self

    def compose(self, composition, service1, service2, pre_ser1, pre_ser2, *nodes):
        self.compositions += [(composition, service1, service2, pre_ser1, pre_ser2, nodes)]
        return self
  
    # Refinement function for cloud services  
    def Refine(self, cloudSer, bound):
        assert isinstance(cloudSer, Cloud)
        nodes = {}

        solver = Solver()
        # 1. Constraints for the refinement cloud service generation

        # (1) Constraints for the services
        for ser in self.services:
            for nd in ser[2]:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }

                    # time constraints generation for well-definedness
                    solver.add(nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        solver.add(nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
            
            # service constraints generation for each specific one
            serviceDecl = eval('Service.' + ser[0])
            # parameter generation
            nodesParam = list(map(lambda name: nodes[name], ser[2]))
            preCon = eval(ser[1])

            solver.add(serviceDecl(nodesParam, bound, preCon))
        
        # (2) Constraints for the compositions
        for comp in self.compositions:
            for nd in comp[5]:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }
                # time constraints generation for well-definedness
                solver.add(nodes[nd]['time'][0] >= 0)
                for i in range(bound - 1):
                    solver.add(nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
            #composition constraints generation for each specific composition
            compDecl = eval('Composition.' + comp[0])
            # parameter generation
            ser1 = eval('Service.' + comp[1])
            ser2 = eval('Service.' + comp[2])
            preCon1 = eval(comp[3])
            preCon2 = eval(comp[4])
            nodesParam = list(map(lambda name: nodes[name], comp[5]))
        
            solver.add(compDecl(ser1, ser2, preCon1, preCon2, nodesParam, bound))
        # 2. Constraints generation for the refined cloud service
        
        ReSerConstr = None
        ReCompConstr = None
        ReConstr = None
        UniVar = []
        # (1) Constraints for the services in cloudSer (the refined one)
        for ser in cloudSer.services:
            for nd in ser[2]:
                if nd not in nodes:
                    nodes[nd] ={
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }

                    UniVar += nodes[nd]['time']
                    UniVar += nodes[nd]['data']
                    # time constraints generation for well-definedness
                    tempTimeConstr = (nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        tempTimeConstr = And(tempTimeConstr, nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])

                    if ReSerConstr is None:
                        ReSerConstr = tempTimeConstr
                    else:
                        ReSerConstr = And(ReSerConstr, tempTimeConstr)     
            # Constraint gerneration for each specific refined services
            serviceDecl = eval('Service.' + ser[0])
            # Parameter generation
            preCon = eval(ser[1])
            nodesParam = list(map(lambda name: nodes[name], ser[2]))

            tempSerConstr = serviceDecl(nodesParam, bound, preCon)
            if ReSerConstr is None:
                ReSerConstr = tempSerConstr
            else:
                ReSerConstr = And(tempSerConstr, ReSerConstr)
        # (2) Constraints for the compositions
        for comp in cloudSer.compositions:
            for nd in comp[5]:
                if nd not in nodes:
                    nodes[nd] ={
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }

                    UniVar += nodes[nd]['time']
                    UniVar += nodes[nd]['data']

                    currTimeConstr = (nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        currTimeConstr = And(currTimeConstr, nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
                    if ReCompConstr is None:
                        ReCompConstr = currTimeConstr
                    else:
                        ReCompConstr = And(ReCompConstr, currTimeConstr)
            # constraint generation for refined compositions in the cloud
            compDecl = eval('Composition.' + comp[0])
            # Parameter generation
            ser1 = eval('Service.' + comp[1])
            ser2 = eval('Service.' + comp[2])
            preCon1 = eval(comp[3])
            preCon2 = eval(comp[4])
            nodeParam = list(map(lambda name: nodes[name], comp[5]))

            currCompConstr = compDecl(ser1, ser2, preCon1, preCon2, nodesParam, bound)
            if ReCompConstr is None:
                ReCompConstr = currCompConstr
            else: 
                ReCompConstr = And(currCompConstr, ReCompConstr)

        
        if ReCompConstr is None:
            ReConstr = Not(ReSerConstr)
        elif ReSerConstr is None:
            ReConstr = Not(ReCompConstr)
        else:
            ReConstr = Or(Not(ReSerConstr), Not(ReCompConstr))


        
        if UniVar != []:
            solver.add(Forall(UniVar, ReConstr))
        else:
            solver.add(ReConstr)
        
        RefineResult = solver.check()

        # Result Obtained


        if str(RefineResult) == 'sat':
            return False, solver.model(), solver.to_smt2()
        elif str(RefineResult) == 'unsat':
            return True, None, solver.to_smt2()
        else:
            print('Unknown')

        
                

                    