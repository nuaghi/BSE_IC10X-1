      PROGRAM popbin
      implicit none
      INCLUDE 'const_bse.h'
      integer i,j,k,jj,nm1,Kstage,kk,unevl,ii,ist,istt,ist1
      integer kw,kw2,kwx,kwx2,kstar(2),kwx1,kwx11,kwx22
      integer i1,i2,kdum,tnum,dtime(8)
      character*8 detime(3),cdetime
      character*6 ddetime
      character*15 stime
      character*180 tmptxt(20000)
      real*8 Rsun,CG,sep,Mtotal,spin,mx11,mx22,sfr,ri,ndt
      real*8 m1,m2,tmax,radius,twopi,radius2,spin2,arr(8),perd
      real*8 mass0(2),mass(2),z,zpars(20),ospbru(50000),omega(50000)
      real*8 ospbru2(50000),omega2(50000),MBOL0(2),mv0(2),sepx
      real*8 epoch(2),tms(2),tphys,tphysf,dtp,pi,a,b,c,lm1,lm2,lsep
      real*8 rad(2),lum(2),ospin(2),LOGL, LOGT, MASS00,MV,BMINV,UMINB
      real*8 massc(2),radc(2),menv(2),renv(2),r0,alpha,rd
      real*8 sep0,tb0,tb,ecc0,ecc,aursun,yeardy,yearsc,tol,z0
      PARAMETER(aursun=214.95d0,yeardy=365.25d0,yearsc=3.1557d+07)
      PARAMETER(tol=1.d-07)
      real*8 t1,t2,mx,mx2,tbx,eccx,t3,q,r,tau,a1,a2,a3,a4,a5,tbx1,eccx1
      neta = 0.5
      bwind = 0.0
      hewind = 1.0
      alpha1 = 1.0
      ceflag = 3
      tflag = 1
      ifflag = 0 
      wdflag = 0 
      bhflag = 1
      nsflag = 1
      mxns = 2.5
      pts1 = 0.05
      pts2 = 0.01
      pts3 = 0.02
      sigma = 265.0
      beta = 0.125
      xi = 1.0 
      acc2 = 1.5
      epsnov = 0.001
      eddfac = 1.0
      gamma = -2.0
      SNtype = 2.0
      idum = 3234
      unevl = 0
      tmptxt = ""
      if(idum.gt.0) idum = -idum
      CALL mvdata
      CALL instar
      nm1 = 1.0d4
      call date_and_time(detime(1), detime(2), detime(3), dtime)
      read(detime(1),*)cdetime
      read(detime(2),*)ddetime
      stime=cdetime//"_"//ddetime
      OPEN(104,file='../data/N'//stime//'.csv',status='unknown')
      OPEN(106,file='../data/rdc.num',status='unknown',
     &POSITION='append')
      write(104,*)'i,t1,mx,mx2,tbx,kw,kw2,sepx,ndt,'
      do i = 1,nm1
            if(MOD(i,1000).eq.0.0) print*,i
            call random_number(r0)
            call random_number(alpha)
            pi = 3.1415
            r0 = 15.0*r0
            alpha = 2.0*pi*alpha
            rd =1.0d3*sqrt(64.0+r0**2-16.0*r0*cos(alpha))
            call random_number(a)
            lm1 = 1.609+2.995*a
            m1 = 2.7183**lm1
            call random_number(b)
            lm2 = -1.0+5.604*b
            m2 = 2.7183**lm2
            call random_number(c)
            LSEP = 1.0987+8.1116*c
            sep = 2.7183**lsep
            ecc = 0.0
            z = 0.004
            sfr=0.5
            ist = -1
            ri=sfr*m2*0.15571*0.12328*2.995*5.604*8.1116/nm1/M1**2.7
            if(m1.le.m2)then
                  unevl=unevl+1
                  goto 40
            endif
            CALL zcnsts(z,zpars)
            Rsun = 6.96e8
            CG= 6.67e-11
            Mtotal = 1.99e30*(m1+m2)
            tb = ((sep*Rsun)**3*39.476/(CG*Mtotal))**0.5/8.64e4
            ecc0 = ecc
            tb0 = tb
            z0 = z
            kstar(1) = 1
            mass0(1) = m1
            mass(1) = m1
            massc(1) = 0.0
            ospin(1) = 0.0
            epoch(1) = 0.0
            kstar(2) = 1
            mass0(2) = m2
            mass(2) = m2
            massc(2) = 0.0
            ospin(2) = 0.0
            epoch(2) = 0.0
            tphys = 0.0
            tphysf = 10000
            dtp = 0.0
            CALL evolv2(kstar,mass0,mass,rad,lum,massc,radc,
     &menv,renv,ospin,epoch,tms,
     &tphys,tphysf,dtp,z,zpars,tb,ecc)
            jj = 0
            t1 = -1.0
            t2 = -1.0
            t3 = -1.0
 30         jj = jj + 1
            if((bcm(jj,1).lt.0.0).or.((ist.eq.-1).and.(istt.eq.1)))then
                  goto 40
            endif
            kw = INT(bcm(jj,2))
            kw2 = INT(bcm(jj,16))
            bcm(jj,30) = yeardy*bcm(jj,30)
            do kk = 0 , 1
                  LOGL = bcm(jj,5+14*kk)
                  LOGT = bcm(jj,7+14*kk)
                  MASS00 = bcm(jj,4+14*kk)
                  CALL LT2UBV(LOGL,LOGT,MASS00,MV,BMINV,UMINB)
                  mv0(kk+1) = MV
                  MBOL0(kk+1) = 4.75D0 - 2.5D0*LOGL
            enddo
            t1 = bcm(jj,1)
            mx = bcm(jj,4)
            mx2 = bcm(jj,18)
            tbx = bcm(jj,30)
            sepx = bcm(jj,31)
            ndt = ri*1.0d6*(bcm(jj,1) - bcm(jj-1,1))
            ecc = bcm(jj,32)
            if((kw.eq.13.and.kw2.eq.7).or.(kw.eq.14.and.kw2
     &.eq.7).or.(kw.eq.13.and.kw2.eq.8).or.(kw.eq.14.and.kw2.eq.8).or
     &.(kw.eq.13.and.kw2.eq.9).or.(kw.eq.14.and.kw2.eq.9))then
                  ist = 1
                  istt = 1
            endif
            write(tmptxt(jj),111)i,t1,mx,mx2,tbx,kw,kw2,sepx,ecc,ndt
      goto 30
 40   if(ist.eq.1)then
            do ist1 = 1,20000
                  if(LEN_TRIM(tmptxt(ist1)) > 0)then
                        write(104,*)tmptxt(ist1)
                        tmptxt(ist1) = ""
                  endif
            enddo
      else
            do ist1 = 1,20000
                  if(LEN_TRIM(tmptxt(ist1)) > 0)then
                        tmptxt(ist1) = ""
                  endif
            enddo
      endif
      ist = -1
      istt = -1
      continue
      enddo
      WRITE(106,*)cdetime//"_"//ddetime,"| Total Number: ",nm1,
     &", Unenvolved binary numbers:",unevl

 111  FORMAT(i9,",",F22.16,",",F20.16,",",F20.16,",",F20.10,",",i2
     &,",",i2,",",F23.16,",",F15.8,",",F23.16)
      STOP
      END

************************************************************************
      SUBROUTINE mvdata
      COMMON /UBVDAT/ TGR(34), GGR(13), TAB(5,13,34)
      READ (21,*) TGR, GGR, TAB
      RETURN
      END
************************************************************************
      SUBROUTINE LT2UBV ( LOGL, LOGT, MASS00, MV, BMINV, UMINB)
      COMMON /UBVDAT/ TGR(34), GGR(13), TAB(5,13,34)
      COMMON /HERE05/ LOGG, LOGG1, LOGG2, LOGM, LOGT1, LOGT2, MBOL, 
     : BC1, BC2, BCX, BV1, BV2, BVX, DG1, DG2, DT1, DT2, UB1, UB2, UBX,
     : BC(4), UB(4), BV(4), VR(4), RI(4), I, ING1, ING2, INT1, INT2, 
     : J, K, K0, K1, K2 
      real*8  LOGL, LOGT, MASS00, MV, BMINV, UMINB ,
     : LOGG, LOGG1, LOGG2, LOGM, LOGT1, LOGT2, MBOL, 
     : BC1, BC2, BCX, BV1, BV2, BVX, DG1, DG2,DT1, DT2, UB1, UB2, UBX
      integer I, ING1, ING2, INT1, INT2, J, K, K0, K1, K2 
      LOGM = log10(MASS00)
      LOGG = LOGM + 4.0D0*LOGT - LOGL - 10.6071D0
c determine values of log g to interpolate between
      ING1 = 1
      ING2 = 13
 1    IF ( ING2 - ING1.GT.1 ) THEN
       I = (ING1 + ING2)/2
       IF ( GGR(I).GT.LOGG ) THEN
        ING2 = I
       ELSE
        ING1 = I
       END IF
       GO TO 1
      END IF
      LOGG1 = GGR(ING1)
      LOGG2 = GGR(ING2)
c determine values of log T to interpolate between
      INT1 = 1
      INT2 = 34
 2    IF ( INT2 - INT1.GT.1 ) THEN
       I = (INT1 + INT2)/2
       IF ( TGR(I).GT.LOGT ) THEN
        INT2 = I
       ELSE
        INT1 = I
       END IF
       GO TO 2
      END IF
      LOGT1 = TGR(INT1)
      LOGT2 = TGR(INT2)
      DO 3 K = 1, 2
       DO 3 J = 1, 2
        K0 = (K - 1)*2 + J
        K1 = INT1 - 1 + K
        K2 = ING1 - 1 + J
        BC(K0) = TAB(1, K2, K1)
        UB(K0) = TAB(2, K2, K1)
        BV(K0) = TAB(3, K2, K1)
        VR(K0) = TAB(4, K2, K1)
    3   RI(K0) = TAB(5, K2, K1)
      DG1 = (LOGG - LOGG1)/(LOGG2 - LOGG1)
      DG2 = 1.0D0 - DG1
      BC1 = BC(2)*DG1 + BC(1)*DG2
      UB1 = UB(2)*DG1 + UB(1)*DG2
      BV1 = BV(2)*DG1 + BV(1)*DG2
      BC2 = BC(4)*DG1 + BC(3)*DG2
      UB2 = UB(4)*DG1 + UB(3)*DG2
      BV2 = BV(4)*DG1 + BV(3)*DG2
      DT1 = (LOGT - LOGT1)/(LOGT2 - LOGT1)
      DT2 = 1.0D0 - DT1
      BCX = BC2*DT1 + BC1*DT2
      UBX = UB2*DT1 + UB1*DT2
      BVX = BV2*DT1 + BV1*DT2
      MBOL = 4.75D0 - 2.5D0*LOGL
      MV = MBOL - BCX
      BMINV = BVX
      UMINB = UBX
      RETURN
      END
