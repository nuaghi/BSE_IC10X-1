      IMPLICIT REAL*8 (A-H, L-Z)
      real*8 Nt(8000000)
      real*8 mt2(8000000),m1(1000),mt(8000000),m2(1000)
      real*8 kwT(8000000),kw2T(8000000)
      real*8 porb1,md1,dt1,dt2,dt3(1000,1000),dm,N
      real*8 m10,m20,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1
      real*8 eccx1,mv0,MBOL0,kwx1,kwx2,kw,kw2,t2,dtt
      real*8 gne,fe,hcn,hcn2,fndot,fk,kpc,sg,SNR,SNRcr
      real*8 poms,pacc,fre,sn,hn,rate,cl,hn2

      integer i,j,k,np
      open(4,file='num.dat',status='unknown')
      open(1001,file='hchnwd.dat',status='unknown')    

      pi = 3.1415    
      Rsun = 6.96d8
      Msun = 1.989d30
      daysec = 8.64d4
      CG= 6.67d-11
      cl = 3.0d8
      yr = 3.1557d7
      kpc = 3.08568d19
      L = 2.5d9
      fp = 19.09d-3
      Tobs = 4.0*yr
      SNRcr = 5.0

      m1(1) = -5.0
      m2(1) = -22.0

            
      do k = 1, 4876629
      read(4,*)m10,m20,tb0,mx,mx2,tbx,eccx,mx11,mx22,tbx1,
     &      eccx1,mv0,MBOL0,kwx1,kwx2,kw,kw2,t2,dtt

      call random_number(r0)
      call random_number(alpha)  
      r0 = 15.0*r0
      alpha = 2.0*pi*alpha
      rd =sqrt(64.0+r0**2-16.0*r0*cos(alpha))*kpc
      kwT(k) = kw
      kw2T(k) = kw2

      np = int(2.0*(1.0+eccx1)**1.1954/(1.0-eccx1**2.0)**1.5)

      if(tbx1.ge.1.0)then
      gne = 1.0
      else
      gne = np**4.0/32.0*((Bessel_Jn(np-2,np*eccx1)-2.0*eccx1*
     & Bessel_Jn(np-1,np*eccx1)+2.0/np*Bessel_Jn(np,np*eccx1)+
     & 2.0*eccx1*Bessel_Jn(np+1,np*eccx1)-Bessel_Jn(np+2,np*eccx1))**2.0
     & +(1.0-eccx1**2.0)*(Bessel_Jn(np-2,np*eccx1)
     & -2.0*Bessel_Jn(np,np*eccx1)+Bessel_Jn(np+2,np*eccx1))**2.0+ 
     & 4.0/(3.0*np**2.0)*(Bessel_Jn(np,np*eccx1))**2.0)
      endif
      fe = 1.0/(1.0-eccx1**2.0)**3.5*
     & (1.0+73.0/24.0*eccx1**2.0+37.0/96.0*eccx1**4.0)


      fk = 1.0/(tbx1*daysec)
      fre = np*fk
      mchirp = (mx11*mx22)**0.6/(mx11+mx22)**0.2*Msun
      fndot = 9.6*np/pi*(CG*mchirp)**(5.0/3.0)/cl**5.0*
     & (2.0*pi*fk)**(11.0/3.0)*fe
      hcn2 = 2.0/(3.0*pi**(4.0/3.0))*CG**(5.0/3.0)/cl**3.0*
     & mchirp**(5.0/3.0)/rd**2.0*1.0/fre**0.3333*
     & (2.0/np)**(2.0/3.0)*gne/fe
      hcn = (hcn2*min(1.0,fndot*(Tobs/fre)))**0.5
!      hcn = log10(hcn)


      pacc = 9.0d-30*(1.0+(0.4d-3/fre)**2.0)*(1.0+
     & (fre/0.008)**4.0)
      poms = 2.25d-22*(1.0+(2.0d-3/fre)**4.0)
      sn = 3.333/L**2.0*(poms+2.0*(1.0+cos(fre/fp)**2.0)*
     & pacc/(2.0*pi*fre)**4.0)*(1.0+0.6*(fre/fp)**2.0)
      sg = 9.0d-45*fre**(-7.0/3.0)*exp(-fre**0.138-221.0*fre*
     & sin(521.0*fre))*(1.0+tanh(1680.0*(0.00113-fre)))
      hn = fre**0.5*(sn+sg)**0.5
!      hn = log10(hn)
      SNR = hcn/hn

!      hcp = 2.5d-20*(fre/1.0d-3)**(7.0/6.0)
!     & *(mchirp/Msun)**(5.0/3.0)*(15.0*kpc/rd)   !...
!      hcp = log10(hcp)

!      print*,np, fre, SNR
 
      rate = 7.8d-6*m20*m10**(-2.7)
      N = rate*dtt

      if(MOD(k,10000).eq.0.0) print*,k,np,hcn
      if(SNR.le.SNRcr) N = 0.0
      if(kwx1.le.13.and.kw.eq.14) N = 0.0
      if(kwx1.eq.14.and.kwx2.eq.4) N = 0.0

      mt(k) = log10(fre)
      mt2(k) = log10(hcn)
c      spin(k) = spin2
      Nt(k) = N
c       print*,fre,hcp,Nt(k)
c      if(kwx11.eq.1) Nt(k) = 0.0
c      md(k) = log10(abs(mdacc))
!      mv0(2) = mv0(2) + 5.0*log10(0.1*rd) + rd/1.0d3
!      mV(k) = mv0
      enddo


!      goto 40

      do i = 1, 100
      m1(i+1) = m1(i) + 0.05

       do j = 1, 100
       m2(j+1) = m2(j) + 0.06

      print*,i,j


      rewind(4)
      dt2 = 0      
      do k = 1, 4876629

c      print*,Nt(k),mt(k),mt2(k)
c      Mc = (mx*mx2)**0.6/(mx+mx2)**0.2
c      dt1 = 4.19*rate*10.0*0.000343*(Mc/1.2)**2.5

      dt1 = Nt(k)

      if(mt(k).le.m1(i+1).and.mt(k).gt.m1(i)
     &.and.mt2(k).gt.m2(j).and.mt2(k).le.m2(j+1).and.
     & (kwT(k).eq.14.and.kw2T(k).le.12.or.
     & kwT(k).le.12.and.kw2T(k).eq.14))then

c      if(mt(k).le.m(i+1).and.mt(k).gt.m(i).and.spin(k).gt.0.8
c     &.and.pp(k).gt.p(j).and.pp(k).le.p(j+1))then      

      dt2 = dt2+dt1
      dt3(i,j) = dt2
      endif


      enddo

      write(1001,11)m1(i),m2(j),dt3(i,j)
c      write(1001,11)m1(i),m2(j),dt3(i,j)
11    format(2f10.5,1E12.4,1f8.3)

      enddo
      enddo  
!40    continue    
      end

            
