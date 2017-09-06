def special():
    return "I'm so special that I got a bodyguard :)"


def not_special():
    return "I'm just boring"


def impossible():
    return "No one should ever get here."


def bomb():
    raise NotImplementedError("%s is not supported on this platform" % __file__)
