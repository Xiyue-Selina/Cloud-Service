from Cloud import *

# Case study

QF1 = Cloud()
QF1.config('Buffer', 'True', 'A', 'B')
QF1.config('Buffer', 'True', 'A', 'C')
QF1.config('Buffer', 'True', 'A', 'D')

QF2 = Cloud()
QF2.config('Buffer', 'True', 'A', 'E')
QF2.config('Sync', 'True', 'E', 'B')
QF2.config('Sync', 'True', 'E', 'C')
QF2.config('Sync', 'True', 'E', 'D')

result1, counterexample1, smt = QF2.Refine(QF1, 10)
result2, counterexample2, smt = QF1.Refine(QF2, 10)
print(result1)
print(counterexample1)
print(result2)
print(counterexample2)