from Cloud import *

# Case study
Serv1 = Service('Sync', 'True', ('A', 'B'))
Serv2 = Service('Router', 'True', ('C', 'D', 'E'))
Serv3 = Service('Sync', 'True', ('C', 'F'))
TravelPack1 = Cloud()
TravelPack1.compose('SeqComp', Serv1, Serv2, 1)
TravelPack1.config('Merger', 'True', 'D', 'E', 'F')
TravelPack2 = Cloud()
TravelPack2.compose('SeqComp', Serv1, Serv3, 1)



result1, counterexample1, smt = TravelPack1.Refine(TravelPack2, 10)
result2, counterexample2, smt = TravelPack2.Refine(TravelPack1, 10)
print(result1)
print(counterexample1)
print(result2)
print(counterexample2)