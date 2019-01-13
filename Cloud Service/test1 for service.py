from Cloud import *

sync = Cloud()
sync.config('Sync', 'True', 'A', 'B')
buffer = Cloud()
buffer.config('Buffer', 'True', 'A', 'B' )

result, counterexample, smt = buffer.Refine(sync, 10)

print(result)
print(counterexample)