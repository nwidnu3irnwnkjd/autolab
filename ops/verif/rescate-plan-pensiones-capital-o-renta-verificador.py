# Verificador fiscal (independiente). Escala estatal art. 63.1 leida del BOE 2/10/2026; CCAA de params (verificadas en verificacion-irpf).
import json, subprocess, sys
R="/Users/andonimcbpro/Claude Code/autolab/projects/decidir/"
CC=json.load(open(R+"data/params.json"))["irpf_2026"]["ccaa"]
EST=[(0,9.5),(12450,12),(20200,15),(35200,18.5),(60000,22.5),(300000,24.5)]
def tramos(b,t):
    s=0
    for i,(lo,r) in enumerate(t):
        hi=t[i+1][0] if i+1<len(t) else 1e18
        s+=max(0,min(b,hi)-lo)*r/100
    return s
def mins(c,h,edad65=False):
    def m(p,d): return p+(1150 if edad65 else 0)+sum(d[min(i,3)] for i in range(h))
    mm=CC[c].get("minimo")
    # incremento por edad autonomico no disponible: se usa el estatal 1.150 tambien (solo para sensibilidad)
    return m(5550,[2400,2700,4000,4500]), (m(mm["contribuyente"],mm["descendientes"]) if mm else m(5550,[2400,2700,4000,4500]))
def cuota(b,c,h,e65=False):
    me,mc=mins(c,h,e65); ea=CC[c]["escala_general"]
    return tramos(b,EST)-tramos(min(b,me),EST)+tramos(b,ea)-tramos(min(b,mc),ea)
def red20(I):  # art. 20 (RDL 4/2024); I = rendimiento neto a efectos del art. 20 (integro - gastos a-e; pensionista: = integro)
    if I<=14852: return 7302
    if I<=17673.52: return 7302-1.75*(I-14852)
    if I<19747.5: return 2364.34-1.14*(I-17673.52)
    return 0
def base_real(I):  # art. 19.2.f (2.000) + art. 20, saldo no negativo
    return max(0.0, I-min(2000,I)-red20(I))
def fac(n,g): return sum((1+g)**-k for k in range(n))
def run(d, real=False, e65=False):
    S,O,n,g,c,h,x=d["saldo"],d["otras"],int(d["anos"]),d["rentab"]/100,d["ccaa"],int(d["hijos"]),d["pctCapital"]/100
    B=(lambda I: base_real(I)) if real else (lambda I: I)
    T=lambda I: cuota(B(I),c,h,e65)
    t0=T(O); cap=T(O+S)-t0; a=fac(n,g); A=S/a; tr=T(O+A)-t0
    C=S*x; Am=(S-C)/a; m0=T(O+C+Am)-t0; m1=T(O+Am)-t0
    serie=[(T(O+S/fac(k,g))-t0)*fac(k,g) for k in range(1,41)]
    mn=min(serie); nopt=next(k for k in range(1,41) if serie[k-1]<=mn+1)
    return dict(pagoRenta=A,impCapital=cap,vanImpRenta=tr*a,vanImpMixto=m0+m1*(a-1),ahorroRenta=cap-tr*a,nOptimo=nopt,ahorroOptimo=cap-serie[nopt-1],impRenta=n*tr)
S=[dict(saldo=60000,ccaa="madrid",otras=15000,hijos=0,anos=10,rentab=2,pctCapital=50),
   dict(saldo=120000,ccaa="cataluna",otras=22000,hijos=1,anos=12,rentab=3,pctCapital=30),
   dict(saldo=35000,ccaa="valencia",otras=11000,hijos=0,anos=6,rentab=1,pctCapital=50),
   dict(saldo=250000,ccaa="andalucia",otras=40000,hijos=2,anos=20,rentab=4,pctCapital=25)]
if __name__=="__main__":
    js=open(R+"calcs/rescate-plan-pensiones-capital-o-renta.js").read().split("function eur(")[0]
    out=subprocess.run(["osascript","-l","JavaScript","-e",js+"\nJSON.stringify("+json.dumps(S)+".map(function(d){var r=calcular(d);delete r.serieN;return r;}));"],capture_output=True,text=True)
    J=json.loads(out.stdout); bad=0
    for d,j in zip(S,J):
        p=run(d,real=True); diff={k:(round(j[k],2),round(v,2)) for k,v in p.items() if abs(j[k]-v)>1}
        bad+=len(diff); print(d["ccaa"],{k:round(v,2) for k,v in p.items()},"OK" if not diff else diff)
    print("discrepancias JS vs verificador:",bad)
