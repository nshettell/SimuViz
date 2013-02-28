class Vector:
    def __init__(self,pos):
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def translate(self,trans):
        new_i=self.i
        new_j=self.j
        new_k=self.k
        for v in trans:
            new_i+=v[0]*trans[v]
            new_j+=v[1]*trans[v]
            new_k+=v[2]*trans[v]
        return (new_i,new_j,new_k)
    def magnitude(self):
        return (self.i**2+self.j**2+self.k**2)**0.5
################################################################################
def size(l_info):
    l=l_info.split()
    S=[int(p) for p in l]
    return S[0],S[1],S[2]
################################################################################
def site(info):
    Basis=[]
    while info[0]!='\n' and info[0]!='\r\n':
        Basis+=[[float(p) for p in info[0].split()]]
        info=info[1:]
    return Basis,info[1:]
################################################################################
def vectors(info):
    bx=[float(p) for p in info[0].split()]
    by=[float(p) for p in info[1].split()]
    bz=[float(p) for p in info[2].split()]
    return bx,by,bz
################################################################################
def bonds(info):
    Bonds=[]
    while info!=[] and info[0]!='\n' and info[0]!='\r\n':
        temp=info[0].split(',')
        Bonds+=[([float(p) for p in temp[0].split()],[float(p) for p in temp[1].split()])]
        info=info[1:]
    return Bonds
################################################################################
def l_dict(Lx,Ly,Lz,bx,by,bz,site):
    D={}
    for pos in site:
        u={Vector(pos).translate({tuple(bx):i,tuple(by):j,tuple(bz):k}):[]\
           for i in range(Lx) for j in range(Ly) for k in range(Lz)}
        D.update(u)
    return D
################################################################################
def extrema(lattice):
    mx=max([p[0] for p in lattice])
    my=max([p[1] for p in lattice])
    mz=max([p[2] for p in lattice])
    return mx,my,mz
################################################################################
def bond_list(Lx,Ly,Lz,mx,my,mz,bx,by,bz,bonds):
    B=[]
    for b in bonds:
        u=[((Vector(b[0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})),\
            (Vector(b[1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})))
           for i in range(Lx) for j in range(Ly) for k in range(Lz)]
        u=filter(lambda i: i[0][0]<=mx and i[1][0]<=mx and i[0][1]<=my\
                 and i[1][1]<=my and i[0][2]<=mz and i[1][2]<=mz, u)
        B+=u
    return B
################################################################################
def l_spin(Lx,Ly,Lz,bx,by,bz,sites,lattice,info):
    L=len(sites)
    c_max=len(info)/(Lx*Ly*Lz*L)
    counter=0
    while counter<c_max:
        for k in range(Lz):
            for j in range(Ly):
                for i in range(Lx):
                    s_l=0
                    for s in sites:
                        pos=Vector(s).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                        loc=counter*Lz*Ly*Lx*L+k*Ly*Lx*L+j*Lx*L+i*L+s_l
                        spin=info[loc]
                        lattice[pos]+=[spin]
                        s_l+=1
        counter+=1
    return lattice,c_max
################################################################################
def light_list(Lx,Ly,Lz,bx,by,bz,sites):
    L=[]
    for i in range(0,Lx+16,16):
        for j in range(0,Ly+16,16):
            for k in range(-8,Lz,16):
                for s in sites:
                    p=Vector(s).translate({tuple(bx):i+0.5,tuple(by):j+0.5,tuple(bz):k+0.5})
                    L+=[p]
    return L
################################################################################
def b_dict(Lx,Ly,Lz,bx,by,bz,bond):
    D={}
    for pos in bond:
        u={(Vector(pos[0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k}),\
           Vector(pos[1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})):[]
           for i in range(Lx) for j in range(Ly) for k in range(Lz)}
        D.update(u)
    return D
################################################################################
def b_spin(Lx,Ly,Lz,bx,by,bz,bonds,lattice,info):
    L=len(bonds)
    c_max=len(info)/(Lx*Ly*Lz*L)
    counter=0
    while counter<c_max:
        for k in range(Lz):
            for j in range(Ly):
                for i in range(Lx):
                    s_l=0
                    for s in bonds:
                        pos=(Vector(s[0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k}),\
                             Vector(s[1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k}))
                        loc=counter*Lz*Ly*Lx*L+k*Ly*Lx*L+j*Lx*L+i*L+s_l
                        spin=info[loc]
                        lattice[pos]+=[spin]
                        s_l+=1
        counter+=1
    return lattice,c_max
################################################################################
def b_light_list(Lx,Ly,Lz,bx,by,bz,bonds):
    B=[]
    for b in bonds:
        if b[0] not in B:
            B+=[b[0]]
        if b[1] not in B:
            B+=[b[1]]
    L=[]
    for i in range(0,Lx+16,16):
        for j in range(0,Ly+16,16):
            for k in range(-8,Lz,16):
                for b in B:
                    p=Vector(b).translate({tuple(bx):i+0.5,tuple(by):j+0.5,tuple(bz):k+0.5})
                    L+=[p]
    return L