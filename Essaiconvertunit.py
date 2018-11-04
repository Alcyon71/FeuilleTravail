# -*- coding: utf-8 -*-

unitmasse = {'kg': 1000, 'hg': 100, 'dag': 10, 'g': 1, 'dg': 0.1,
             'cg': 0.01, 'mg': 0.001, 'dmg': 0.0001, 'µg': 0.000001}


def convertmasse(dictunit, valeur, unit_in, unit_out):
    return valeur*dictunit[unit_in]/dictunit[unit_out]

print(convertmasse(unitmasse,0.5,'g','dmg'))


for key, value in sorted(unitmasse.iteritems(), key=lambda (k, v): (v, k), reverse=True):
    print(key)

listunit = [key for key, value in sorted(unitmasse.iteritems(), key=lambda (k, v): (v, k), reverse=True)]
print list
#
# for key in unitmasse.keys():
#     print key