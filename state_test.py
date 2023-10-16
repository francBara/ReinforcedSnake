from ship_brain import *
from items import *





state1 = State(ComplexDirection.BOTTOM_LEFT, set())
state2 = State(ComplexDirection.TOP_LEFT, {Direction.DOWN, Direction.UP})
state3 = State(ComplexDirection.BOTTOM_LEFT, set())

print(hash(state1))
print(hash(state2))
print(hash(state3))

print(state1 == state2)
print(state1 == state3)

a = {}

a[state1] = 2
print(a[state3])