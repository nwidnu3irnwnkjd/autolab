"""SEGUNDO oraculo: script independiente del Verificador fiscal (Opus, 2026-10-02), escrito desde la norma (Ley 20/2007 art. 34.1.2.a + FAQ SEPE: el resto se cobra como subvencion de cuota hasta agotar el importe).
Se importa desde capitalizar-paro-o-cobrarlo.py (funcion norma); ejecutado solo imprime sus 4 escenarios contra el JS."""
import json,subprocess,os
JS=open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'projects/decidir/calcs/capitalizar-paro-o-cobrarlo.js')).read().split('function eur')[0]
TOPE=[1225,1400,1575];MIN=[560,749,749];I=0.0325
def norma(n,br,h,ya,inv,cuota):
    # LGSS 270: 70% 180 d, 60% despues; topes/minimos SEPE 2026
    c=[min(max(br*(0.70 if ya+k<=6 else 0.60),MIN[h]),TOPE[h]) for k in range(1,n+1)]
    T=sum(c); V=sum(x*(1-I*k/12) for k,x in enumerate(c,1))
    X=min(inv,V)
    # Ley 20/2007 art.34 regla 1.a in fine + SEPE: el resto se abona como subvencion "hasta agotar el total de la cuantia"
    R=T-X*T/V
    return dict(T=T,V=V,X=X,sub=R,cap=X+R,coste=T-X-R)
def main():
    casos=[(12,1500,0,0,6000,205.88),(18,4000,2,0,20000,300),(9,900,1,4,3000,205.88),(24,2000,0,0,0,350)]
    for cs in casos:
        n,br,h,ya,inv,cu=cs
        d=dict(meses=n,br=br,hijos=h,cobrados=ya,inversion=inv,cuota=cu,arranque=6,actividad='si')
        js=json.loads(subprocess.run(['osascript','-l','JavaScript','-e',JS+'\nJSON.stringify(calcular(%s))'%json.dumps(d)],capture_output=True,text=True).stdout)
        m=norma(*cs)
        print(cs,'| T js %.2f mio %.2f | V js %.2f mio %.2f | capTotal js %.2f mio %.2f | coste js %.2f mio %.2f'%(js['total'],m['T'],js['valorActual'],m['V'],js['capTotal'],m['cap'],js['coste'],m['coste']))
if __name__=='__main__':
    main()
