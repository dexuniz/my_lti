# -*- coding: utf-8 -*-

def get_id(string):
    deb=string.find('"')
    fin=string.find('"',deb+1)
    res=string[deb+1:fin]
    return res