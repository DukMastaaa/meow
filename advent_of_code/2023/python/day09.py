import numpy as np


# with open("advent_of_code/2023/input/09test.txt", "r") as file:
with open("../input/09test.txt", "r") as file:
    l = [s.strip() for s in file.read().strip().split('\n')]

res = []
# KERNEL = [1, -21, 210, -1330, 5985, -20349, 54264, -116280, 203490, -293930, 352716, -352716, 293930, -203490, 116280, -54264, 20349, -5985, 1330, -210, 21]
KERNEL = [-1, 6, -15, 20, -15, 6]

what = []

for line in l:
    numbers = list(map(int, (s for s in line.split(" ") if s != "")))
    # print(numbers)
    depth = 0
    stack = [np.array(numbers)]
    while np.any(d := np.diff(stack[-1])):
        depth += 1
        # print(d)
        stack.append(d)
    # print(stack)
    # print(depth)
    next_values = [None] * (depth + 1)
    next_values[depth] = stack[-1][0]
    for i in reversed(range(1, depth+1)):
        # print("hm" + str(i))
        next_values[i-1] = stack[i-1][-1] + next_values[i]
        # next_values[i-1] = stack[i-1][0] - next_values[i]
    # print(next_values)
    res.append(next_values[0])

    what.append(np.dot(KERNEL, stack[0]))


print(res[0])
# print(what[0])

print(res == what)

# print(sum(res))
