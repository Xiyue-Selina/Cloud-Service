from Cloud import *

Serv1 = Service('Sync', 'True', ('A', 'B'))
Serv2 = Service('Buffer', 'True', ('C', 'D'))
interChoice = Cloud()
interChoice.compose('InChoice', Serv1, Serv2, 1)
exterChoice = Cloud()
exterChoice.compose('ExChoice', Serv1, Serv2, 1)

result1, counterexample1, smt = exterChoice.Refine(interChoice, 10)
result2, counterexample2, smt = interChoice.Refine(exterChoice, 10)
print(result1)
print(counterexample1)
print(result2)
print(counterexample2)
