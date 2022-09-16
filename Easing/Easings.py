# Formulas from https://easings.net/
# Write with coilpot
import math

class Easings:
    def easeLinear(x):
        return x
    def easeInSine(x):
        return 1 - math.cos(x * math.pi / 2)
    def easeOutSine(x):
        return math.sin(x * math.pi / 2)
    def easeInOutSine(x):
        return -(math.cos(x * math.pi) - 1) / 2
    def easeInQuad(x):
        return x * x
    def easeOutQuad(x):
        return 1 - (1 - x) * (1 - x)
    def easeInOutQuad(x):
        if x < 0.5:
            return 2 * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 2) / 2
    def easeInCubic(x):
        return x * x * x
    def easeOutCubic(x):
        return 1 - math.pow(1 - x, 3)
    def easeInOutCubic(x):
        if x < 0.5:
            return 4 * x * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 3) / 2
    def easeInQuart(x):
        return x * x * x * x
    def easeOutQuart(x):
        return 1 - math.pow(1 - x, 4)
    def easeInOutQuart(x):
        if x < 0.5:
            return 8 * x * x * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 4) / 2
    def easeInQuint(x):
        return x * x * x * x * x
    def easeOutQuint(x):
        return 1 - math.pow(1 - x, 5)
    def easeInOutQuint(x):
        if x < 0.5:
            return 16 * x * x * x * x * x
        else:
            return 1 - math.pow(-2 * x + 2, 5) / 2
    def easeInExpo(x):
        if x == 0:
            return 0
        else:
            return math.pow(2, 10 * (x - 1))
    def easeOutExpo(x):
        if x == 1:
            return 1
        else:
            return -math.pow(2, -10 * x) + 1
    def easeInOutExpo(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            if x < 0.5:
                return math.pow(2, 20 * x - 10) / 2
            else:
                return (2 - math.pow(2, -20 * x + 10)) / 2
    def easeInCirc(x):
        return 1 - math.sqrt(1 - x * x)
    def easeOutCirc(x):
        return math.sqrt(1 - math.pow(1 - x, 2))
    def easeInOutCirc(x):
        if x < 0.5:
            return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
        else:
            return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2
    def easeInBack(x):
        return 2.70158 * x * x * x - 1.70158 * x * x
    def easeOutBack(x):
        return 1 + 2.70158 * math.pow(x - 1, 3) + 1.70158 * math.pow(x - 1, 2)
    def easeInOutBack(x):
        n0 = 1.70158
        n1 = n0 * 1.525
        if x < 0.5:
            return (math.pow(2 * x, 2) * ((n1 + 1) * 2 * x - n1)) / 2
        else:
            return (math.pow(2 * x - 2, 2) * ((n1 + 1) * (x * 2 - 2) + n1) + 2) / 2
    def easeInElastic(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            n2 = 2 * math.pi / 3
            return -math.pow(2, 10 * (x - 1)) * math.sin((x * 10 - 10.75) * n2)
    def easeOutElastic(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            n3 = 2 * math.pi / 3
            return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * n3) + 1
    def easeInOutElastic(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            n4 = 2 * math.pi / 4.5
            if x < 0.5:
                return math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * n4) / 2
            else:
                return math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * n4) / 2 + 1
    def easeInBounce(x):
        return 1 - Easings.easeOutBounce(1 - x)
    def easeOutBounce(x):
        n5 = 7.5625
        d0 = 2.75
        if x < 1 / d0:
            return n5 * x * x
        elif x < 2 / d0:
            return n5 * (x - 1.5 / d0) * x + 0.75
        elif x < 2.5 / d0:
            return n5 * (x - 2.25 / d0) * x + 0.9375
        else:
            return n5 * (x - 2.625 / d0) * x + 0.984375
    def easeInOutBounce(x):
        if x < 0.5:
            return (1 - Easings.easeOutBounce(1 - x * 2)) / 2
        else:
            return (1 + Easings.easeOutBounce(x * 2 - 1)) / 2

    # value, easeid (int)
    def Ease(x, id:int):
        if id == 0:
            return Easings.easeLinear(x)
        elif id == 1:
            return Easings.easeInSine(x)
        elif id == 2:
            return Easings.easeOutSine(x)
        elif id == 3:
            return Easings.easeInOutSine(x)
        elif id == 4:
            return Easings.easeInQuad(x)
        elif id == 5:
            return Easings.easeOutQuad(x)
        elif id == 6:
            return Easings.easeInOutQuad(x)
        elif id == 7:
            return Easings.easeInCubic(x)
        elif id == 8:
            return Easings.easeOutCubic(x)
        elif id == 9:
            return Easings.easeInOutCubic(x)
        elif id == 10:
            return Easings.easeInQuart(x)
        elif id == 11:
            return Easings.easeOutQuart(x)
        elif id == 12:
            return Easings.easeInOutQuart(x)
        elif id == 13:
            return Easings.easeInQuint(x)
        elif id == 14:
            return Easings.easeOutQuint(x)
        elif id == 15:
            return Easings.easeInOutQuint(x)
        elif id == 16:
            return Easings.easeInExpo(x)
        elif id == 17:
            return Easings.easeOutExpo(x)
        elif id == 18:
            return Easings.easeInOutExpo(x)
        elif id == 19:
            return Easings.easeInCirc(x)
        elif id == 20:
            return Easings.easeOutCirc(x)
        elif id == 21:
            return Easings.easeInOutCirc(x)
        elif id == 22:
            return Easings.easeInBack(x)
        elif id == 23:
            return Easings.easeOutBack(x)
        elif id == 24:
            return Easings.easeInOutBack(x)
        elif id == 25:
            return Easings.easeInElastic(x)
        elif id == 26:
            return Easings.easeOutElastic(x)
        elif id == 27:
            return Easings.easeInOutElastic(x)
        elif id == 28:
            return Easings.easeInBounce(x)
        elif id == 29:
            return Easings.easeOutBounce(x)
        elif id == 30:
            return Easings.easeInOutBounce(x)

    def EaseS(x, id:str):
        id = id.lower()
        if id == "linear":
            return Easings.easeLinear(x)
        elif id == "insine":
            return Easings.easeInSine(x)
        elif id == "outsine":
            return Easings.easeOutSine(x)
        elif id == "inoutsine":
            return Easings.easeInOutSine(x)
        elif id == "inquad":
            return Easings.easeInQuad(x)
        elif id == "outquad":
            return Easings.easeOutQuad(x)
        elif id == "inoutquad":
            return Easings.easeInOutQuad(x)
        elif id == "incubic":
            return Easings.easeInCubic(x)
        elif id == "outcubic":
            return Easings.easeOutCubic(x)
        elif id == "inoutcubic":
            return Easings.easeInOutCubic(x)
        elif id == "inquart":
            return Easings.easeInQuart(x)
        elif id == "outquart":
            return Easings.easeOutQuart(x)
        elif id == "inoutquart":
            return Easings.easeInOutQuart(x)
        elif id == "inquint":
            return Easings.easeInQuint(x)
        elif id == "outquint":
            return Easings.easeOutQuint(x)
        elif id == "inoutquint":
            return Easings.easeInOutQuint(x)
        elif id == "inexpo":
            return Easings.easeInExpo(x)
        elif id == "outexpo":
            return Easings.easeOutExpo(x)
        elif id == "inoutexpo":
            return Easings.easeInOutExpo(x)
        elif id == "incirc":
            return Easings.easeInCirc(x)
        elif id == "outcirc":
            return Easings.easeOutCirc(x)
        elif id == "inoutcirc":
            return Easings.easeInOutCirc(x)
        elif id == "inback":
            return Easings.easeInBack(x)
        elif id == "outback":
            return Easings.easeOutBack(x)
        elif id == "inoutback":
            return Easings.easeInOutBack(x)
        elif id == "inelastic":
            return Easings.easeInElastic(x)
        elif id == "outelastic":
            return Easings.easeOutElastic(x)
        elif id == "inoutelastic":
            return Easings.easeInOutElastic(x)
        elif id == "inbounce":
            return Easings.easeInBounce(x)
        elif id == "outbounce":
            return Easings.easeOutBounce(x)
        elif id == "inoutbounce":
            return Easings.easeInOutBounce(x)
