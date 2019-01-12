from Cloud import *

interChoice = Cloud()
interChoice.compose('InChoice', 'SyncSer', 'BufferSer', 'True', 'True', 'A', 'B', 'C', 'D')

exterChoice = Cloud()
exterChoice.compose('ExChoice', 'SyncSer', 'BufferSer', 'True', 'True', 'A', 'B', 'C', 'D')

result1, counterexample1, smt = exterChoice.Refine(interChoice, 10)
result2, counterexample2, smt = interChoice.Refine(exterChoice, 10)
print(result1)
print(counterexample1)
print(result2)
print(counterexample2)