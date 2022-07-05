from bitstring import BitArray
# run "pip install bitstring" if you don't have it yet

tm = [
    [[1, 1, 1], [4, 1, 1]],
    [[2, 1, 1], [5, 1, -1]],
    [[3, 1, -1], [3, 0, 1]],
    [[3, 1, -1], [0, 1, 1]],
    [[2, 0, -1], [1, 1, 1]]
]
statelen = len(bin(len(tm) - 1)) - 2
history = [BitArray('0b0'), BitArray(uint=0, length=statelen), [0], [0], [0]]     # [tapes, states, positions, starts of tapes, offsets]


def getTape(t):
    return [history[0][history[3][t]:(history[3][t + 1] if t + 1 < len(history[3]) else len(history[0]))], history[1][statelen * t:statelen * (t + 1)], history[2][t], history[4][t]]


def step():
    tape = getTape(len(history[2]) - 1)
    move = tm[tape[1].uint][int(tape[0][tape[2]])]
    newtape = [(BitArray('0b0') if tape[2] + move[2] < 0 else BitArray()) + tape[0][:tape[2]] + BitArray('0b' + str(move[1])) + tape[0][tape[2] + 1:] + (BitArray('0b0') if tape[2] + move[2] >= tape[0].len else BitArray()), BitArray(uint=move[0], length=statelen), max(0, tape[2] + move[2]), tape[3] - min(0, tape[2] + move[2])]
    history[3].append(len(history[0]))
    history[0] += newtape[0]
    history[1] += newtape[1]
    history[2].append(newtape[2])
    history[4].append(newtape[3])


def checkCycles(t):
    while len(history[2]) <= t:
        step()
    tape = getTape(t)
    left = 0
    right = 1
    for i in range(t - 1, -1, -1):
        prev = [history[1][statelen * i:statelen * (i + 1)], history[2][i], history[4][i]]
        offs = -(tape[2] - tape[3] - prev[1] + prev[2])
        left = max(left, -offs)
        right = max(right, offs + 1)
        if prev[0] == tape[1]:
            prev = getTape(i)
            if prev[0][max(0, prev[2] - left):prev[2] + right] == tape[0][max(0, tape[2] - left):tape[2] + right]:
                if not offs:
                    return "cycler with period " + str(t - i)
                if offs > 0:
                    repeatable = prev[0][max(0, prev[2] - left - offs):prev[2] - left]
                    if prev[2] - left - offs <= 0 and ([0] + repeatable).uint == 0:
                        return "translated cycler with period " + str(t - i) + " and translation " + str(-offs)
                else:
                    repeatable = prev[0][prev[2] + right:prev[2] + right - offs]
                    if prev[2] + right - offs >= prev[0].len - 1 and ([0] + repeatable).uint == 0:
                        return "translated cycler with period " + str(t - i) + " and translation " + str(-offs)


print(checkCycles(50))
