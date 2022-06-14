import math

print("LTLSPEC G(F(blackboard.q = 0));")
for r in range(1, 101):
    for q in range(1, 101):
        print("LTLSPEC (blackboard.r = " + str(r) + " & blackboard.q = " + str(q) + ") -> F(blackboard.r = " + str(math.gcd(r, q)) + ");")
print("LTLSPEC blackboard.r = 17 & blackboard.q = 25 -> F(blackboard.r = 10);")
print("LTLSPEC G(F(blackboard.q = 1));")
