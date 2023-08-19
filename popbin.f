      PROGRAM popbin
      implicit none
      INCLUDE 'const_bse.h'
      integer i,j,k,jj,nm1,kk,unevl,ist,istt,ist1
      integer kw,kw2,kstar(2),timei
      character*15 stime,stime2,stime3
      integer,dimension(8) :: timevalues
      character(8) :: date
      character(6) :: time,timeis
      character(5) :: timezone 
      character*19 tmptxt2(30000)
      real*8 Rsun,CG,sep,Mtotal,sfr,ri,ndt
      real*8 m1,m2
      real*8 mass0(2),mass(2),z,zpars(20)
      real*8 MBOL0(2),mv0(2),sepx
      real*8 epoch(2),tms(2),tphys,tphysf,dtp,pi,a,b,c,lm1,lm2,lsep
      real*8 rad(2),lum(2),ospin(2),LOGL, LOGT, MASS00,MV,BMINV,UMINB
      real*8 massc(2),radc(2),menv(2),renv(2),r0,alpha,rd
      real*8 sep0,tb0,tb,ecc0,ecc,aursun,yeardy,yearsc,tol,z0

      integer iz,kstarz(2)
      real*8 mass0z(2),massz(2),zparsz(20)
      real*8 radz(2),lumz(2),masscz(2),radcz(2)
      real*8 menvz(2),renvz(2),ospinz(2),epochz(2),tmsz(2)
      real*8 tphysz,dtpz,tbz,eccz

      integer izz,kstarzz(2)
      real*8 mass0zz(2),masszz(2),zparszz(20)
      real*8 radzz(2),lumzz(2),massczz(2),radczz(2)
      real*8 menvzz(2),renvzz(2),ospinzz(2),epochzz(2),tmszz(2)
      real*8 tphyszz,dtpzz,tbzz,ecczz

      PARAMETER(aursun=214.95d0,yeardy=365.25d0,yearsc=3.1557d+07)
      PARAMETER(tol=1.d-07)
      real*8 t1,t2,mx,mx2,tbx,eccx,t3

      neta = 0.5
      bwind = 0.0
      hewind = 1.0
      alpha1 = 1.0
      alpha3 = 3.0
      alpha5 = 5.0
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
      tmptxt2 = ""
      
      pi = 3.1415
      z = 0.004
      sfr=0.5




      if(idum.gt.0) idum = -idum
      CALL mvdata
      CALL instar
      nm1 = 1.0d5
      call date_and_time(date,time,timezone,timevalues)
      read(time, *) timei
      timei=timei+1
      write(timeis,'(I6)')timei
      stime=date//"_"//time
      stime2=date//"_"//timeis
      timei=timei+1
      write(timeis,'(I6)')timei
      stime3=date//"_"//timeis

      OPEN(112,file='../data/N'//stime//'s.csv',status='unknown')
      OPEN(113,file='../data/N'//stime//'ss.csv',status='unknown')
      write(112,*)"i,t1,mx,mx2,tbx,kw,kw2,ndt,ces,"
      write(113,*)"i,kw,kw2,ces,"

      OPEN(132,file='../data/N'//stime2//'s.csv',status='unknown')
      OPEN(133,file='../data/N'//stime2//'ss.csv',status='unknown')
      write(132,*)"i,t1,mx,mx2,tbx,kw,kw2,ndt,ces,"
      write(133,*)"i,kw,kw2,ces,"

      OPEN(152,file='../data/N'//stime3//'s.csv',status='unknown')
      OPEN(153,file='../data/N'//stime3//'ss.csv',status='unknown')
      write(152,*)"i,t1,mx,mx2,tbx,kw,kw2,ndt,ces,"
      write(153,*)"i,kw,kw2,ces,"

      OPEN(106,file='../data/rdc.num',status='unknown',
     &POSITION='append')
      do i = 1,nm1
            if(MOD(i,5000).eq.0.0) print*,i,unevl
            call random_number(r0)
            call random_number(alpha)
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
            ist = -1
            ri=sfr*m2*0.15571*0.12328*2.995*5.604*8.1116/nm1/M1**2.7
            if(m1.le.m2)then
                  unevl=unevl+1
                  goto 70
            endif
            CALL zcnsts(z,zpars)
            Rsun = 6.96e8
            CG= 6.67e-11
            Mtotal = 1.99e30*(m1+m2)
            tb = ((sep*Rsun)**3*39.476/(CG*Mtotal))**0.5/8.64e4
            ecc0 = ecc
            sep0 = aursun*(tb0*tb0*(mass(1) + mass(2)))**(1.d0/3.d0)
            sep = sep0
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
            tphysf = 120
            dtp = 0.0

            kstarz   = kstar
            mass0z   = mass0
            massz    = mass
            radz     = rad
            lumz     = lum
            masscz   = massc
            radcz    = radc
            menvz    = menv
            renvz    = renv
            ospinz   = ospin
            epochz   = epoch
            tmsz     = tms
            tphysz   = tphys
            dtpz     = dtp
            zparsz   = zpars
            tbz      = tb
            eccz     = ecc

            kstarzz  = kstar
            mass0zz  = mass0
            masszz   = mass
            radzz    = rad
            lumzz    = lum
            massczz  = massc
            radczz   = radc
            menvzz   = menv
            renvzz   = renv
            ospinzz  = ospin
            epochzz  = epoch
            tmszz    = tms
            tphyszz  = tphys
            dtpzz    = dtp
            zparszz  = zpars
            tbzz     = tb
            ecczz    = ecc

            alpha1 = 1.0
            alpha3 = 3.0
            alpha5 = 5.0
            CALL evolv2(kstar,mass0,mass,rad,lum,massc,radc,menv,
     &renv,ospin,epoch,tms,tphys,tphysf,dtp,z,zpars,tb,ecc)
            alpha1 = 1.0
            alpha3 = 3.0
            alpha5 = 5.0
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
            eccx = bcm(jj,32)
            if(((kw.eq.14).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.((kw.eq.13).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.(((kw2.eq.13).or.(kw2.eq.14)).and.((kw.eq.7).or.(kw2.eq.8)
     &.or.(kw2.eq.9))))then
                  ist = 1
                  istt = 1
                  write(112,*)i,",",t1,",",mx,",",mx2,",",tbx
     &,",",kw,",",kw2,",",ndt,",",bcm(jj,34)
            endif
            if((bcm(jj,2).ne.bcm(jj-1,2)).or.(bcm(jj,16).ne.bcm(jj-1,16)
     &))then
                write(tmptxt2(jj),102)i,kw,kw2,bcm(jj,34)
            endif
      goto 30

 40   do ist1 = 1,30000
            if(LEN_TRIM(tmptxt2(ist1)) > 0)then
                  if(ist.eq.1)then
                        write(113,*)tmptxt2(ist1)
                  endif
            endif
      enddo
      ist = -1
      istt = -1
      tmptxt2 = ""



      CALL evolv23(kstarz,mass0z,massz,radz,lumz,masscz,radcz,
     &menvz,renvz,ospinz,epochz,tmsz,
     &tphysz,tphysf,dtpz,z,zparsz,tbz,eccz)
            jj = 0
            t1 = -1.0
            t2 = -1.0
            t3 = -1.0
            alpha1 = 1.0
            alpha3 = 3.0
            alpha5 = 5.0
 50         jj = jj + 1
            if((bcm(jj,1).lt.0.0).or.((ist.eq.-1).and.(istt.eq.1)))then
                  goto 60
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
            eccx = bcm(jj,32)
            if(((kw.eq.14).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.((kw.eq.13).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.(((kw2.eq.13).or.(kw2.eq.14)).and.((kw.eq.7).or.(kw2.eq.8)
     &.or.(kw2.eq.9))))then
                  ist = 1
                  istt = 1
                  write(132,*)i,",",t1,",",mx,",",mx2,",",tbx
     &,",",kw,",",kw2,",",ndt,",",bcm(jj,34)
            endif
            if((bcm(jj,2).ne.bcm(jj-1,2)).or.(bcm(jj,16).ne.bcm(jj-1,16)
     &))then
                write(tmptxt2(jj),102)i,kw,kw2,bcm(jj,34)
            endif
      goto 50
 60   do ist1 = 1,30000
            if(LEN_TRIM(tmptxt2(ist1)) > 0)then
                  if(ist.eq.1)then
                        write(133,*)tmptxt2(ist1)
                  endif
            endif
      enddo

      ist = -1
      istt = -1
      tmptxt2 = ""

      CALL evolv25(kstarzz,mass0zz,masszz,radzz,lumzz,massczz,
     &radczz,menvzz,renvzz,ospinzz,epochzz,tmszz,
     &tphyszz,tphysf,dtpzz,z,zparszz,tbzz,ecczz)
            jj = 0
            t1 = -1.0
            t2 = -1.0
            t3 = -1.0
            alpha1 = 1.0
            alpha3 = 3.0
            alpha5 = 5.0
 61         jj = jj + 1
            if((bcm(jj,1).lt.0.0).or.((ist.eq.-1).and.(istt.eq.1)))then
                  goto 62
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
            eccx = bcm(jj,32)
            if(((kw.eq.14).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.((kw.eq.13).and.((kw2.eq.7).or.(kw2.eq.8).or.(kw2.eq.9)))
     &.or.(((kw2.eq.13).or.(kw2.eq.14)).and.((kw.eq.7).or.(kw2.eq.8)
     &.or.(kw2.eq.9))))then
                  ist = 1
                  istt = 1
                  write(152,*)i,",",t1,",",mx,",",mx2,",",tbx
     &,",",kw,",",kw2,",",ndt,",",bcm(jj,34)
            endif
            if((bcm(jj,2).ne.bcm(jj-1,2)).or.(bcm(jj,16).ne.bcm(jj-1,16)
     &))then
                write(tmptxt2(jj),102)i,kw,kw2,bcm(jj,34)
            endif
      goto 61
 62   do ist1 = 1,30000
            if(LEN_TRIM(tmptxt2(ist1)) > 0)then
                  if(ist.eq.1)then
                        write(153,*)tmptxt2(ist1)
                  endif
            endif
      enddo
      ist = -1
      istt = -1
      tmptxt2 = ""


 70   continue
      enddo
      WRITE(106,*)stime,"|Total Number:",nm1,
     &", UnenvolvedNumbers:",unevl,",z:",z,",sfr:",sfr,
     &",alpha1:",alpha1,",SNtype:",SNtype,",bwind:",bwind,
     &",hewind:",hewind,",ceflag:",ceflag,
     &",tflag:",tflag,",ifflag:",ifflag,",wdflag:",wdflag,
     &",bhflag:",bhflag,",nsflag:",nsflag,",mxns:",mxns,
     &",sigma:",sigma,",beta:",beta,",xi:",xi,",acc2:",acc2,
     &",epsnov:",epsnov,",eddfac:",eddfac,",gamma:",gamma
      WRITE(106,*)stime2,"|Total Number:",nm1,
     &", UnenvolvedNumbers:",unevl,",z:",z,",sfr:",sfr,
     &",alpha1:",alpha3,",SNtype:",SNtype,",bwind:",bwind,
     &",hewind:",hewind,",ceflag:",ceflag,
     &",tflag:",tflag,",ifflag:",ifflag,",wdflag:",wdflag,
     &",bhflag:",bhflag,",nsflag:",nsflag,",mxns:",mxns,
     &",sigma:",sigma,",beta:",beta,",xi:",xi,",acc2:",acc2,
     &",epsnov:",epsnov,",eddfac:",eddfac,",gamma:",gamma
      WRITE(106,*)stime3,"|Total Number:",nm1,
     &", UnenvolvedNumbers:",unevl,",z:",z,",sfr:",sfr,
     &",alpha1:",alpha5,",SNtype:",SNtype,",bwind:",bwind,
     &",hewind:",hewind,",ceflag:",ceflag,
     &",tflag:",tflag,",ifflag:",ifflag,",wdflag:",wdflag,
     &",bhflag:",bhflag,",nsflag:",nsflag,",mxns:",mxns,
     &",sigma:",sigma,",beta:",beta,",xi:",xi,",acc2:",acc2,
     &",epsnov:",epsnov,",eddfac:",eddfac,",gamma:",gamma

 101  FORMAT(i9,",",F22.16,",",F20.16,",",F20.16,",",F20.10,",",i2,","
     &,i2,",",F17.10,",",F15.8,",",F12.8,",",F12.8,",",
     &F30.20,",",F30.20,",",F3.1)
     
 102  FORMAT(i9,",",i2,",",i2,",",F3.1)
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
