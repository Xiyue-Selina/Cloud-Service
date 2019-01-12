from Cloud import *

sync = Cloud()
sync.config('SyncSer', 'True', 'A', 'B')

buffer = Cloud()
buffer.config('BufferSer', 'True', 'A', 'B' )

result, counterexample, smt = buffer.Refine(sync, 10)

print(result)
print(counterexample)