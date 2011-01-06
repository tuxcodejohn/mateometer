#!/usr/bin/python
#__e
#
#
# These formulas are simplified models of a helmholtz resonator
#  All constant values are taylored to be used with .5l bottle of Mate
#  at 20 centigrade at 1013hPa :-D
#
#

import math





def matefill_by_f_aprox1(f):
    return (0.95936658171875 - ( 24559.784492173  / f **2))


def matefill_by_f_aprox2(f):
    return ( 1.02- ( 25000 / f **2))


def freq_by_matefill_aprox2(fill):
    return abs( (24560 /(1-fill))**.5)
