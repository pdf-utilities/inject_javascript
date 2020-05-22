#!/usr/bin/env python3


from inspect import currentframe


def notice(message):
    """
    Custom warning notifier
    """
    caller = currentframe().f_back.f_code.co_name
    lineno = currentframe().f_back.f_lineno
    msg = 'Notice: {0} {1}\n\t{2}'.format(lineno, caller, message)
    print(msg)


def error(message):
    """
    Cusotm Exception _thrower_
    """
    caller = currentframe().f_back.f_code.co_name
    lineno = currentframe().f_back.f_lineno
    msg = '\n\t{0} {1} reports: {2}'.format(lineno, caller, message)
    raise Exception(msg)
