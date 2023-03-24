      IMPLICIT REAL*8 (A-H, L-Z)
      real*8 t(100000000)
      real*8 porb1,md1,dt1,dt2,dt3(1000,1000),dm,N,kwT(30000000)
      real*8 tb0,mx,mx2,tbx,eccx,spin2,t1,t2,inc,Kv,rate

      integer i,j,k
      open(4,file='num.dat',status='unknown')
      open(1002,file='BHform.dat',status='unknown')    
      pi = 3.1415    
      Rsun = 6.96d8
      Msun = 1.989d30
      CG= 6.67d-11

      t(0) = 1.0d6
      

      do k = 1, 100000000
      read(4,*)m1,m2,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1,
     &      eccx1,mv0,MBOL0,kwx1,kwx2,kw,kw2,t2,dtt
      if(kwx1.eq.13.and.kw.eq.14) goto 40
      rate = 7.8e-6*m2*m1**(-2.7)
      N = rate*dtt
      t(k) = t2

      if(t(k).lt.t(k-1))then
c      print*,t(k),t(k-1)
      rate1 = rate1 + rate

      write(1002,113)m1,m2,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1,
     &      eccx1,kwx1,kwx2,kw,kw2,t2,rate
      endif



 40      continue
      enddo
113    FORMAT(11f11.3,4i6,1f11.4,1E12.3)
112   FORMAT(13f11.3,4i6,1f11.4,1E12.3)


      end

            
