      IMPLICIT REAL*8 (A-H, L-Z)
      real*8 t(100000000)
      real*8 poms,pacc,fre,sn,hc
      real*8 tb0,mx,mx2,tbx,eccx,spin2,t1,t2,inc,Kv,rate

      integer i,j,k
      open(1002,file='hc.dat',status='unknown')    
      pi = 3.1415    
      Rsun = 6.96d8
      Msun = 1.989d30
      CG= 6.67d-11
      poms = 2.25d-22
      L = 2.5d9
      fp = 19.09d-3

      do k = 1, 100

      fre = -5.0+5.0d-2*k
      fre = 10.0**fre
      pacc = 9.0d-30*(1.0+(0.4d-3/fre)**2.0)
      sn = 3.333/L**2.0*(poms+2.0*(1.0+cos(fre/fp)**2.0)*
     & pacc/(2.0*pi*fre)**4.0)*(1.0+0.6*(fre/fp)**2.0)
      hc = log10((fre*sn)**0.5)

      write(1002,113) log10(fre), hc




 40      continue
      enddo
113    FORMAT(11E13.4,4i6,1f11.4,1E12.3)



      end

            
