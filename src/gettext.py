def bindtextdomain(messages, localedir):
    pass

def textdomain(messages):
    pass

def gettext(s):
    return s

def ngettext(singular, plural, n):
    return singular if n == 1 else plural
