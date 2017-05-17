# -*- coding: utf-8 -*-

def match_exo(r,exos):
    exos_selec=[]
    for i in r:
        i=int(i)
        exos_selec.append(exos[i][0])
    return exos_selec