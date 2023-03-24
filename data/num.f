      IMPLICIT REAL*8 (A-H, L-Z)
      real m1,m2,tb0,mx,mx2,tbx,eccx,t1,t2,Num1,Num2,Num3
      real N1,N,mx22,dm,pe,rate
      integer I,J,K
      OPEN(14,file='BHform.dat',status='unknown')
      open(100,file='BHform.out',status='unknown')

      do I = 1, 10000000
      read(14,*)m1,m2,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1,
     &      eccx1,kwx1,kwx2,kwx11,kwx22,t2,t3
      rate = 7.8e-6*m2*m1**(-2.7)
      N = rate*dtt
       if((kwx11.eq.14.and.kwx22.eq.13)
     & .and.eccx.ge.0.0)then
      
      rate1 = rate1+rate  
      N1 = N1 + N
       write(100,10)m1,m2,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1,
     &      eccx1,kwx1,kwx2,kwx11,kwx22,t2,t3,rate1
       endif

       enddo


10    FORMAT(11f11.3,4i6,2f11.4,1E11.3)
       end
