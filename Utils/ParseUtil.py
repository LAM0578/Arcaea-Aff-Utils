
class ParseUtil:
    
    # Try parse input to int. If fail, return input self.
    def TryParseInt(x):
        try:
            return int(x)
        except:
            return x

    # Try parse input to float. If fail, return input self.
    def TryParseFloat(x):
        try:
            return float(x)
        except:
            return x

    # If parse success, return true
    def CanParseInt(x) -> bool:
        try:
            int(x)
            return True
        except:
            return False

    # If parse success, return true
    def CanParseFloat(x) -> bool:
        try:
            float(x)
            return True
        except:
            return False

    def ParseBool(content) -> bool:
        if type(content) is int or float:
            return float(content) != 0
        elif type(content) is str:
            tempstr = str(content).lower()
            isnumber = ParseUtil.CanParseFloat(tempstr)
            if isnumber:
                return ParseUtil.ParseBool(float(tempstr))
            if tempstr == 'true':
                return True
            elif tempstr == 'false':
                return False
        else:
            return False