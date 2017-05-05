
def get_exo(num_exo):
    num_exo=int(num_exo)
    data=open('./exos/exos.tex').read()
    if num_exo == -1:
        return data
    if num_exo>173:
        num_exo=num_exo+2
    if num_exo>205:
        num_exo=num_exo+1
    for i in range(1,num_exo+4):
        pos_debut1=data[10:].find('\exo')
        pos_debut2=data[10:].find('\pb')
        pos_debut3=data[10:].find('begin{exo}')
        if pos_debut2==-1:
            pos_debut2=pos_debut1+1
        if pos_debut3==-1:
            pos_debut3=pos_debut1+1
        if pos_debut1>pos_debut2 and pos_debut3>pos_debut2:
            data=data[pos_debut2+10:]
        if pos_debut2>pos_debut3 and pos_debut1>pos_debut3:
            data=data[pos_debut3+9:]
        if pos_debut3>pos_debut1 and pos_debut2>pos_debut1:
            data=data[pos_debut1+10:]
    pos_fin1=0
    pos_fin2=0
    pos_fin3=0
    if num_exo==173:
        for i in range (1,3):
            pos_fin1=data[10:].find('\exo',pos_fin1+1)
            pos_fin2=data[10:].find('\pb',pos_fin2+1)
            pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    pos_fin1=data[10:].find('\exo',pos_fin1+1)
    pos_fin2=data[10:].find('\pb',pos_fin2+1)
    pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    if pos_fin2==-1:
        pos_fin2=pos_fin1+1
    if pos_fin3==-1:
        pos_fin3=pos_fin1+1
    if pos_fin1>pos_fin2 and pos_fin3>pos_fin2:
        return data[:pos_fin2+10]
    if pos_fin1>pos_fin3 and pos_fin2>pos_fin3:
        return data[:pos_fin3+10]
    if pos_fin1==-1:
        return data[:-14]
    exotraite = data[:pos_fin1+10]
    return exotraite