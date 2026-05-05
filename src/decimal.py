class Decimal:
    def __init__(self, value):
        if isinstance(value, str):
            self._str = value
        else:
            self._str = "{:.12f}".format(float(value)).rstrip("0").rstrip(".")
            if self._str == "":
                self._str = "0"

    def quantize(self, other):
        pattern = str(other)
        if "." in pattern:
            decimals = len(pattern.split(".")[1])
        else:
            decimals = 0
        fmt = "{:." + str(decimals) + "f}"
        return Decimal(fmt.format(float(self._str)))

    def __str__(self):
        return self._str
