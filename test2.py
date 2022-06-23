minC = 540
step = 610-540
index = 3
handMax = 7


def getCoords(minC, step, index, handMax, lenHand):
    coords = (minC + index*step + (handMax - lenHand)*70/2)
    return coords


lenHand = [7,6,5,4,3,2,1]
for hand in lenHand:
    print("Hand: {}".format(hand))
    for index in range(hand):
        print(str(getCoords(minC, step, index, handMax, hand)))