from file import *
def POM(T):
    a=values(T)
    b=[]
    if(len(a)==2):
        for i in range(5):
            b.append(((a[1][i]-a[0][i])/(a[1][0]-a[0][0]))*(T-a[0][0])+a[0][i])
        return b
    return a
def reynoldsnum(P,U,l,M):
    return((P*U*l)/M)
def Grashofnum(b,tempdiff,length,V):
    return((9.81*b*tempdiff*(length**3))/(V*V))
class nusseltnum:
    def __init__(self):
        self.re=[4,40,4000,40000,400000]
        self.c=[0.989,0.911,0.683,0.193,0.027]
        self.m=[0.33,0.385,0.466,0.618,0.805]
    def flatforcedlaminar(self,reynolds,Pr):
        return(0.664*(reynolds**0.5)*(Pr**0.333))
    def flatforcedturbulent(self,reynolds,Pr):
        return(2*0.0296*(reynolds**0.8)*(Pr**0.333))
    def flatfree(self,Gr,Pr):
        if(Gr*Pr<=(10**4)):
            return(1.1*((Gr*Pr)**0.143))
        elif(Gr*Pr<=(10**9)):
            return(0.59*((Gr*Pr)**0.25))
        else:
            return(0.13*((Gr*Pr)**0.333))
    def cyextforce(self,Re,Pr):
        for i in range(len(self.re)):
            if(Re<=self.re[i]):
                return(self.c[i]*(Re**self.m[i])*(Pr**0.333))
    def cyextfree(self,Gr,Pr):
        if(Gr*Pr<=(10**8)):
            return(0.59*((Gr*Pr)**0.25))
        elif(Gr*Pr<=(10**12)):
            return(0.1*((Gr*Pr)**0.333))
    def cyintforcelaminar(self,reynolds,Pr,r):
        return(3.66+(0.068*reynolds*Pr)/(1+0.04*((reynolds*Pr*r)**0.67)))
    def cyintforceturbulent(self,Re,Pr):
        return(0.023*(Re**0.8)*(Pr**0.333))
    def spheforce(self,Re):
        return(0.37*(Re**0.6))
    def sphefree(self,Gr,Pr):
        return(2+0.43*((Gr*Pr)**0.25))
class Flatplate:
    def __init__(self,convection,x,y,z,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.length=x
        self.breadth=y
        self.thickness=z
        self.U=U
        self.temp=T
        self.reynolds=0
        self.nusselt=0
        self.Pr=Pr
        self.K=K
        self.gr=0
        self.td=t
        self.P=P
        self.M=M*(10**(-5))
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.length,self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.length,self.M/self.P)
    def dim2(self):
        if(self.convection=="forced" and self.reynolds<=5*(10**5)):
            self.nusselt=nusseltnum.flatforcedlaminar(self,self.reynolds,self.Pr)
        elif(self.convection=="forced" and self.reynolds>5*(10**5)):
            self.nusselt=nusseltnum.flatforcedturbulent(self,self.reynolds,self.Pr)
        elif(self.convection=="free"):
            self.nusselt=nusseltnum.flatfree(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round((self.nusselt*self.K)/self.length,2)
    def htrate(self):
        self.rate=round((self.htcoef*self.length*self.breadth*self.td),2)
    def ret(self):
        if(self.gr==0):
            return([str(round(self.reynolds,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Reynolds number(PUL/M)"])
        return([str(round(self.gr,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Grashoff number"])
class Cylindrical:
    def __init__(self,convection,flow,x,D,d,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.length=x
        self.diameter=D
        self.indiameter=d
        self.reynolds=0
        self.gr=0
        self.U=U
        self.temp=T
        self.P=P
        self.M=M*(10**(-5))
        self.K=K
        self.Pr=Pr
        self.nusselt=0
        self.td=t
        self.flow=flow
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.diameter,self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.length,self.M/self.P)
    def dim2(self):
        if(self.flow=="external" and self.convection=="forced"):
            self.nusselt=nusseltnum.cyextforce(self,self.reynolds,self.Pr)
        elif(self.flow=="external" and self.convection=="free"):
            self.nusselt=nusseltnum.cyextfree(self,self.gr,self.Pr)
        elif(self.flow=="internal" and self.convection=="forced" and self.reynolds<=5*(10**5)):
            self.nusselt=nusseltnum.cyintforcelaminar(self,self.gr,self.Pr,(self.diameter/self.indiameter))
        elif(self.flow=="internal" and self.convection=="forced" and self.reynolds>5*(10**5)):
            self.nusselt=nusseltnum.cyintforceturbulent(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round(((self.nusselt*self.K)/self.diameter),2)
    def htrate(self):
        self.rate=round((self.htcoef*self.length*self.diameter*self.td),2)
    def ret(self):
        if(self.gr==0):
            return([str(round(self.reynolds,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Reynolds number(PUL/M)"])
        return([str(round(self.gr,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Grashoff number"])
        
class Sphere:
    def __init__(self,convection,d,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.diameter=d
        self.U=U
        self.temp=T
        self.P=P
        self.M=M*(10**(-5))
        self.K=K
        self.Pr=Pr
        self.reynolds=0
        self.nusselt=0
        self.td=t
        self.gr=0
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.diameter,self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.diameter,self.M/self.P)
    def dim2(self):
        if(self.convection=="forced"):
            self.nusselt=nusseltnum.spheforce(self,self.reynolds)
        elif(self.convection=="free"):
            self.nusselt=nusseltnum.sphefree(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round((self.nusselt*self.K)/self.diameter,2)
    def htrate(self):
        self.rate=round((self.htcoef*3.14*self.diameter*self.diameter*self.td),2)
    def ret(self):
        if(self.gr==0):
            return([str(round(self.reynolds,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Reynolds number(PUL/M)"])
        return([str(round(self.gr,2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate),"Grashoff number"])
def display(convection,velocity,typeht,shape,length,breadth,thickness,surftemp,surrtemp):
    surftemp=int(surftemp)+273
    surrtemp=int(surrtemp)+273
    a=POM((int(surftemp)+int(surrtemp))//2)
    if(shape=="flatplate"):
        f=Flatplate(convection,float(length),float(breadth),float(thickness),float(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        f.dim1()
        f.dim2()
        f.htcoeff()
        f.htrate()
        return(f.ret())
    elif(shape=="cylinder"):
        c=Cylindrical(convection,typeht,float(length),float(breadth),float(thickness),float(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        c.dim1()
        c.dim2()
        c.htcoeff()
        c.htrate()
        return(c.ret())
    elif(shape=="sphere"):
        s=Sphere(convection,float(breadth),float(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        s.dim1()
        s.dim2()
        s.htcoeff()
        s.htrate()
        return(s.ret())
