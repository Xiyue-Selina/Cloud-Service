from Composition import *

class Cloud:
    def __init__(self):
        self.services = []
        self.compositions = []

    def config(self, service, pre_condition, *nodes):
        self.services += [Service(service, pre_condition, nodes)]
        return self

    def compose(self, composition, serv1, serv2, index, bool_con = True):
        self.compositions += [Composition(composition, serv1, serv2, index, bool_con)]
        return self

    # Refinement function for cloud services  
    def Refine(self, cloudSer, bound):
        assert isinstance(cloudSer, Cloud)
        nodes = {}

        solver = Solver()

        # 1. Constraints for the refinement cloud service generation
        # (1) Constraints for the services
        for ser in self.services:
            for nd in ser.nodes:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }

                    # time constraints generation for well-definedness
                    solver.add(nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        solver.add(nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
            # parameter generation
            nodesParam = list(map(lambda name: nodes[name], ser.nodes))
            # service constraints generation for each specific one
            solver.add(ser.valueFunctions[ser.service](bound, nodesParam))

        # (2) Constraints for the compositions
        for comp in self.compositions:
            for nd in comp.serv1.nodes:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }
                # time constraints generation for well-definedness
                solver.add(nodes[nd]['time'][0] >= 0)
                for i in range(bound - 1):
                    solver.add(nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
            # parameter generation
            nodesParam1 = list(map(lambda name: nodes[name], comp.serv1.nodes))
            for nd in comp.serv2.nodes:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                    }
                # time constraints generation for well-definedness
                solver.add(nodes[nd]['time'][0] >= 0)
                for i in range(bound - 1):
                    solver.add(nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])
            # parameter generation
            nodesParam2 = list(map(lambda name: nodes[name], comp.serv2.nodes))
            #composition constraints generation for each specific composition
            solver.add(comp.valueFunctions[comp.composition](bound, nodesParam1, nodesParam2))

        # 2. Constraints generation for the refined cloud service        
        ReSerConstr = None
        ReCompConstr = None
        ReConstr = None
        UniVar = []
        # (1) Constraints for the services in cloudSer (the refined one)
        for ser in cloudSer.services:
            for nd in ser.nodes:
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
            # parameter generation
            nodesParam = list(map(lambda name: nodes[name], ser.nodes))
            # Constraint gerneration for each specific refined services
            tempSerConstr = ser.valueFunctions[ser.service](bound, nodesParam)
            if ReSerConstr is None:
                ReSerConstr = tempSerConstr
            else:
                ReSerConstr = And(tempSerConstr, ReSerConstr)
        # (2) Constraints for the compositions
        for comp in cloudSer.compositions:
            for nd in comp.serv1.nodes:
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
            # parameter generation
            nodesParam1 = list(map(lambda name: nodes[name], comp.serv1.nodes))
            for nd in comp.serv2.nodes:
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
            # parameter generation
            nodesParam2 = list(map(lambda name: nodes[name], comp.serv2.nodes))
            # constraint generation for refined compositions in the cloud
            currCompConstr = comp.valueFunctions[comp.composition](bound, nodesParam1, nodesParam2)
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
            solver.add(ForAll(UniVar, ReConstr))
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
