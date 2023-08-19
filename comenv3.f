***
      SUBROUTINE COMENV3(M01,M1,MC1,AJ1,JSPIN1,KW1,
     &                  M02,M2,MC2,AJ2,JSPIN2,KW2,
     &                  ZPARS,ECC,SEP,JORB,COEL,z)
*
* Common Envelope Evolution.
*
*     Author : C. A. Tout
*     Date :   18th September 1996
*
*     Redone : J. R. Hurley
*     Date :   7th July 1998
*
      IMPLICIT NONE
*
      INTEGER KW1,KW2,KW,I,J
      INTEGER KTYPE(0:14,0:14)
      COMMON /TYPES/ KTYPE
      INTEGER ceflag,tflag,ifflag,nsflag,wdflag
      COMMON /FLAGS/ ceflag,tflag,ifflag,nsflag,wdflag
*
      real*8 d(11,15),LEB(20,20),LEB1,FENV,ETA1
*
      REAL*8 M01,M1,MC1,AJ1,JSPIN1,R1,L1,K21
      REAL*8 M02,M2,MC2,AJ2,JSPIN2,R2,L2,K22,MC22
      REAL*8 TSCLS1(20),TSCLS2(20),LUMS(10),GB(10),TM1,TM2,TN,ZPARS(20)
      REAL*8 EBINDI,EBINDF,EORBI,EORBF,ECIRC,SEPF,SEPL,MF,XX
      REAL*8 CONST,DELY,DERI,DELMF,MC3,FAGE1,FAGE2,z
      REAL*8 ECC,SEP,JORB,TB,OORB,OSPIN1,OSPIN2,TWOPI
      REAL*8 RC1,RC2,Q1,Q2,RL1,RL2,LAMB1,LAMB2
      REAL*8 MENV,RENV,MENVD,RZAMS,VS(3)
      REAL*8 AURSUN,K3,ALPHA3,LAMBDA,LAMBDA1,LAMBDA2,LAMBDA3,sss
      REAL*8 R11(2000),lg1(2000),lb1(2000)
      REAL*8 R12(2000),lg2(2000),lb2(2000),R13(2000),lg3(2000),lb3(2000)
      PARAMETER (AURSUN = 214.95D0,K3 = 0.21D0) 
      COMMON /VALUE2/ ALPHA3,LAMBDA
      LOGICAL COEL
      REAL bcm(50000,34),bpp(80,10)
      COMMON /BINARY/ bcm,bpp
      REAL*8 CELAMF,RL,RZAMSF
      EXTERNAL CELAMF,RL,RZAMSF
      alpha3 = 3.0
*
* Common envelope evolution - entered only when KW1 = 2, 3, 4, 5, 6, 8 or 9.
*
* For simplicity energies are divided by -G.
*
      TWOPI = 2.D0*ACOS(-1.D0)
      COEL = .FALSE.
*
* Obtain the core masses and radii.
*
      KW = KW1
      CALL star(KW1,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
      CALL hrdiag(M01,AJ1,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS,
     &            R1,L1,KW1,MC1,RC1,MENV,RENV,K21)
      OSPIN1 = JSPIN1/(K21*R1*R1*(M1-MC1)+K3*RC1*RC1*MC1)
      MENVD = MENV/(M1-MC1)
      RZAMS = RZAMSF(M01)
c      LAMB1 = CELAMF(KW,M01,L1,R1,RZAMS,MENVD,LAMBDA)
      KW = KW2
      CALL star(KW2,M02,M2,TM2,TN,TSCLS2,LUMS,GB,ZPARS)
      CALL hrdiag(M02,AJ2,M2,TM2,TN,TSCLS2,LUMS,GB,ZPARS,
     &            R2,L2,KW2,MC2,RC2,MENV,RENV,K22)
      OSPIN2 = JSPIN2/(K22*R2*R2*(M2-MC2)+K3*RC2*RC2*MC2)
*
* Calculate the binding energy of the giant envelope (multiplied by lambda).
*



      IF(m01.Ge.0.8.and.m01.lt.1.5)THEN
        open(1,file='./z=0.02/m=1/M1.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.1.5.and.m01.lt.3.0)THEN
        open(1,file='./z=0.02/m=2/M2.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.3.0.and.m01.lt.5.0)THEN
        open(1,file='./z=0.02/m=4/M4.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.5.0.and.m01.lt.7.0)THEN
        open(1,file='./z=0.02/m=6/M6.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.7.0.and.m01.lt.9.0)THEN
        open(1,file='./z=0.02/m=8/M8.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.11.0)THEN
        open(1,file='./z=0.02/m=10/M10.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.15.0)THEN
        open(1,file='./z=0.02/m=10/M10.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.15.0.and.m01.lt.25.0)THEN
        open(1,file='./z=0.02/m=20/M20.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.25.0.and.m01.lt.35.0)THEN
        open(1,file='./z=0.02/m=30/M30.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.35.0.and.m01.lt.50.0)THEN
        open(1,file='./z=0.02/m=40/M40.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ELSEIF(m01.Ge.50.0.and.m01.lt.100.0)THEN
        open(1,file='./z=0.02/m=60/M60.dat',status='unknown')
        rewind(1)
        do i = 1,2000
        read(1,*)R11(i),lg1(i),lb1(i)
        enddo
      ENDIF

      DO j = 1,1999
      if(R1.le.R11(j+1).and.R1.gt.R11(j))then
      LAMBDA1 = lb1(j)
      elseif(R1.gt.R11(1999))then
      LAMBDA1 = lb1(1999)
      elseif(R1.le.R11(1))then
      LAMBDA1 = lb1(1)
      endif
      enddo

      IF(m01.Ge.0.8.and.m01.lt.1.5)THEN
        open(2,file='./z=0.001/m=1/M1.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.1.5.and.m01.lt.3.0)THEN
        open(2,file='./z=0.001/m=2/M2.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.3.0.and.m01.lt.5.0)THEN
        open(2,file='./z=0.001/m=4/M4.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.5.0.and.m01.lt.7.0)THEN
        open(2,file='./z=0.001/m=6/M6.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.7.0.and.m01.lt.9.0)THEN
        open(2,file='./z=0.001/m=8/M8.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.11.0)THEN
        open(2,file='./z=0.001/m=10/M10.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.15.0)THEN
        open(2,file='./z=0.001/m=10/M10.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.15.0.and.m01.lt.25.0)THEN
        open(2,file='./z=0.001/m=20/M20.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.25.0.and.m01.lt.35.0)THEN
        open(2,file='./z=0.001/m=30/M30.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.35.0.and.m01.lt.50.0)THEN
        open(2,file='./z=0.001/m=40/M40.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ELSEIF(m01.Ge.50.0.and.m01.lt.100.0)THEN
        open(2,file='./z=0.001/m=60/M60.dat',status='unknown')
        rewind(2)
        do i = 1,2000
        read(2,*)R12(i),lg2(i),lb2(i)
        enddo
      ENDIF

      DO j = 1,1999
      if(R1.le.R12(j+1).and.R1.gt.R12(j))then
      LAMBDA2 = lb2(j)
      elseif(R1.gt.R12(1999))then
      LAMBDA2 = lb2(1999)
      elseif(R1.le.R12(1))then
      LAMBDA2 = lb2(1)
      endif
      enddo

      IF(m01.Ge.0.8.and.m01.lt.1.5)THEN
        open(3,file='./z=0.0001/m=1/M1.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.1.5.and.m01.lt.3.0)THEN
        open(3,file='./z=0.0001/m=2/M2.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.3.0.and.m01.lt.5.0)THEN
        open(3,file='./z=0.0001/m=4/M4.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.5.0.and.m01.lt.7.0)THEN
        open(3,file='./z=0.0001/m=6/M6.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.7.0.and.m01.lt.9.0)THEN
        open(3,file='./z=0.0001/m=8/M8.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.11.0)THEN
        open(3,file='./z=0.0001/m=10/M10.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.9.0.and.m01.lt.15.0)THEN
        open(3,file='./z=0.0001/m=10/M10.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.15.0.and.m01.lt.25.0)THEN
        open(3,file='./z=0.0001/m=20/M20.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.25.0.and.m01.lt.35.0)THEN
        open(3,file='./z=0.0001/m=30/M30.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.35.0.and.m01.lt.50.0)THEN
        open(3,file='./z=0.0001/m=40/M40.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ELSEIF(m01.Ge.50.0.and.m01.lt.100.0)THEN
        open(3,file='./z=0.0001/m=60/M60.dat',status='unknown')
        rewind(3)
        do i = 1,2000
        read(3,*)R13(i),lg3(i),lb3(i)
        enddo
      ENDIF

      DO j = 1,1999
      if(R1.le.R13(j+1).and.R1.gt.R13(j))then
      LAMBDA3 = lb3(j)
      elseif(R1.gt.R13(1999))then
      LAMBDA3 = lb3(1999)
      elseif(R1.le.R13(1))then
      LAMBDA3 = lb3(1)
      endif
      enddo

      IF(z.gt.0.02)then
      LAMBDA = LAMBDA1
      ELSEIF(z.le.0.02.and.z.gt.0.001)then
      LAMBDA = LAMBDA1+(0.02-z)/(0.02-0.001)*(LAMBDA2-LAMBDA1)
      ELSEIF(z.le.0.001.and.z.gt.0.0001)then
      LAMBDA = LAMBDA2+(0.001-z)/(0.001-0.0001)*(LAMBDA3-LAMBDA2)
      ENDIF

      call random_number(sss) 
c        print*,sss,R1,LAMBDA
c      sss = 0.5+sss*2.5
       sss = 1.0
       EBINDI = M1*(M1-MC1)/(sss*LAMBDA*R1)
c      enddo
c      endif
c       EBINDI = M1*(M1-MC1)/(1.0d-5*R1)
c      print*,LAMBDA,R1
*
* If the secondary star is also giant-like add its envelopes's energy.
*
      EORBI = M1*M2/(2.D0*SEP)
      IF(KW2.GE.2.AND.KW2.LE.9.AND.KW2.NE.7)THEN
         MENVD = MENV/(M2-MC2)
         RZAMS = RZAMSF(M02)
c         LAMB2 = CELAMF(KW,M02,L2,R2,RZAMS,MENVD,LAMBDA)
         LAMB2 = LAMBDA                                 !......
         EBINDI = EBINDI + M2*(M2-MC2)/(LAMB2*R2)
*
* Calculate the initial orbital energy
*
         IF(CEFLAG.NE.3) EORBI = MC1*MC2/(2.D0*SEP)
      ELSE
         IF(CEFLAG.NE.3) EORBI = MC1*M2/(2.D0*SEP)
      ENDIF
*
* Allow for an eccentric orbit.
*
      ECIRC = EORBI/(1.D0 - ECC*ECC)
*
* Calculate the final orbital energy without coalescence.
*
      EORBF = EORBI + EBINDI/ALPHA3
*
* If the secondary is on the main sequence see if it fills its Roche lobe.
*
      IF(KW2.LE.1.OR.KW2.EQ.7)THEN
         SEPF = MC1*M2/(2.D0*EORBF)
         Q1 = MC1/M2
         Q2 = 1.D0/Q1
         RL1 = RL(Q1)
         RL2 = RL(Q2)
         IF(RC1/RL1.GE.R2/RL2)THEN
*
* The helium core of a very massive star of type 4 may actually fill
* its Roche lobe in a wider orbit with a very low-mass secondary.
*
            IF(RC1.GT.RL1*SEPF)THEN
               COEL = .TRUE.
               SEPL = RC1/RL1
            ENDIF
         ELSE
            IF(R2.GT.RL2*SEPF)THEN
               COEL = .TRUE.
               SEPL = R2/RL2
            ENDIF
         ENDIF
         IF(COEL)THEN
*
            KW = KTYPE(KW1,KW2) - 100
            MC3 = MC1
            IF(KW2.EQ.7.AND.KW.EQ.4) MC3 = MC3 + M2
*
* Coalescence - calculate final binding energy.
*
            EORBF = MAX(MC1*M2/(2.D0*SEPL),EORBI)
            EBINDF = EBINDI - ALPHA3*(EORBF - EORBI)
         ELSE
*
* Primary becomes a black hole, neutron star, white dwarf or helium star.
*
            MF = M1
            M1 = MC1
            CALL star(KW1,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
            CALL hrdiag(M01,AJ1,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS,
     &                  R1,L1,KW1,MC1,RC1,MENV,RENV,K21)
            IF(KW1.GE.13)THEN
               CALL kick(KW1,MF,M1,M2,ECC,SEPF,JORB,VS)
               IF(ECC.GT.1.D0) GOTO 30
            ENDIF
         ENDIF
      ELSE
*
* Degenerate or giant secondary. Check if the least massive core fills its
* Roche lobe.
*
         SEPF = MC1*MC2/(2.D0*EORBF)
         Q1 = MC1/MC2
         Q2 = 1.D0/Q1
         RL1 = RL(Q1)
         RL2 = RL(Q2)
         IF(RC1/RL1.GE.RC2/RL2)THEN
            IF(RC1.GT.RL1*SEPF)THEN
               COEL = .TRUE.
               SEPL = RC1/RL1
            ENDIF
         ELSE
            IF(RC2.GT.RL2*SEPF)THEN
               COEL = .TRUE.
               SEPL = RC2/RL2
            ENDIF
         ENDIF
*
         IF(COEL)THEN
*
* If the secondary was a neutron star or black hole the outcome
* is an unstable Thorne-Zytkow object that leaves only the core.
*
            SEPF = 0.D0
            IF(KW2.GE.13)THEN
               MC1 = MC2
               M1 = MC1
               MC2 = 0.D0
               M2 = 0.D0
               KW1 = KW2
               KW2 = 15
               AJ1 = 0.D0
*
* The envelope mass is not required in this case.
*
               GOTO 30
            ENDIF
*
            KW = KTYPE(KW1,KW2) - 100
            MC3 = MC1 + MC2
*
* Calculate the final envelope binding energy.
*
            EORBF = MAX(MC1*MC2/(2.D0*SEPL),EORBI)
            EBINDF = EBINDI - ALPHA3*(EORBF - EORBI)
*
* Check if we have the merging of two degenerate cores and if so
* then see if the resulting core will survive or change form.
*
            IF(KW1.EQ.6.AND.(KW2.EQ.6.OR.KW2.GE.11))THEN
               CALL dgcore(KW1,KW2,KW,MC1,MC2,MC3,EBINDF)
            ENDIF
            IF(KW1.LE.3.AND.M01.LE.ZPARS(2))THEN
               IF((KW2.GE.2.AND.KW2.LE.3.AND.M02.LE.ZPARS(2)).OR.
     &             KW2.EQ.10)THEN
                  CALL dgcore(KW1,KW2,KW,MC1,MC2,MC3,EBINDF)
                  IF(KW.GE.10)THEN
                     KW1 = KW
                     M1 = MC3
                     MC1 = MC3
                     IF(KW.LT.15) M01 = MC3
                     AJ1 = 0.D0
                     MC2 = 0.D0
                     M2 = 0.D0
                     KW2 = 15
                     GOTO 30
                  ENDIF
               ENDIF
            ENDIF
*
         ELSE
*
* The cores do not coalesce - assign the correct masses and ages.
*
            MF = M1
            M1 = MC1
            CALL star(KW1,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
            CALL hrdiag(M01,AJ1,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS,
     &                  R1,L1,KW1,MC1,RC1,MENV,RENV,K21)
            IF(KW1.GE.13)THEN
               CALL kick(KW1,MF,M1,M2,ECC,SEPF,JORB,VS)
               IF(ECC.GT.1.D0) GOTO 30
            ENDIF
            MF = M2
            KW = KW2
            M2 = MC2
            CALL star(KW2,M02,M2,TM2,TN,TSCLS2,LUMS,GB,ZPARS)
            CALL hrdiag(M02,AJ2,M2,TM2,TN,TSCLS2,LUMS,GB,ZPARS,
     &                  R2,L2,KW2,MC2,RC2,MENV,RENV,K22)
            IF(KW2.GE.13.AND.KW.LT.13)THEN
               CALL kick(KW2,MF,M2,M1,ECC,SEPF,JORB,VS)
               IF(ECC.GT.1.D0) GOTO 30
            ENDIF
         ENDIF
      ENDIF
*
      IF(COEL)THEN
         MC22 = MC2
         IF(KW.EQ.4.OR.KW.EQ.7)THEN
* If making a helium burning star calculate the fractional age 
* depending on the amount of helium that has burnt.
            IF(KW1.LE.3)THEN
               FAGE1 = 0.D0
            ELSEIF(KW1.GE.6)THEN
               FAGE1 = 1.D0
            ELSE
               FAGE1 = (AJ1 - TSCLS1(2))/(TSCLS1(13) - TSCLS1(2))
            ENDIF
            IF(KW2.LE.3.OR.KW2.EQ.10)THEN
               FAGE2 = 0.D0
            ELSEIF(KW2.EQ.7)THEN
               FAGE2 = AJ2/TM2
               MC22 = M2
            ELSEIF(KW2.GE.6)THEN
               FAGE2 = 1.D0
            ELSE
               FAGE2 = (AJ2 - TSCLS2(2))/(TSCLS2(13) - TSCLS2(2))
            ENDIF
         ENDIF
      ENDIF
*
* Now calculate the final mass following coelescence.  This requires a
* Newton-Raphson iteration.
*
      IF(COEL)THEN
*
* Calculate the orbital spin just before coalescence. 
*
         TB = (SEPL/AURSUN)*SQRT(SEPL/(AURSUN*(MC1+MC2)))
         OORB = TWOPI/TB
*
         XX = 1.D0 + ZPARS(7)
         IF(EBINDF.LE.0.D0)THEN
            MF = MC3
            GOTO 20
         ELSE
            CONST = ((M1+M2)**XX)*(M1-MC1+M2-MC22)*EBINDF/EBINDI
         ENDIF
*
* Initial Guess.
*
         MF = MAX(MC1 + MC22,(M1 + M2)*(EBINDF/EBINDI)**(1.D0/XX))
   10    DELY = (MF**XX)*(MF - MC1 - MC22) - CONST
*        IF(ABS(DELY/MF**(1.D0+XX)).LE.1.0D-02) GOTO 20
         IF(ABS(DELY/MF).LE.1.0D-03) GOTO 20
         DERI = MF**ZPARS(7)*((1.D0+XX)*MF - XX*(MC1 + MC22))
         DELMF = DELY/DERI
         MF = MF - DELMF
         GOTO 10
*
* Set the masses and separation.
*
   20    IF(MC22.EQ.0.D0) MF = MAX(MF,MC1+M2)
         M2 = 0.D0
         M1 = MF
         KW2 = 15
*
* Combine the core masses.
*
         IF(KW.EQ.2)THEN
            CALL star(KW,M1,M1,TM2,TN,TSCLS2,LUMS,GB,ZPARS)
            IF(GB(9).GE.MC1)THEN
               M01 = M1
               AJ1 = TM2 + (TSCLS2(1) - TM2)*(AJ1-TM1)/(TSCLS1(1) - TM1)
               CALL star(KW,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
            ENDIF
         ELSEIF(KW.EQ.7)THEN
            M01 = M1
            CALL star(KW,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
            AJ1 = TM1*(FAGE1*MC1 + FAGE2*MC22)/(MC1 + MC22)
         ELSEIF(KW.EQ.4.OR.MC2.GT.0.D0.OR.KW.NE.KW1)THEN
            IF(KW.EQ.4) AJ1 = (FAGE1*MC1 + FAGE2*MC22)/(MC1 + MC22)
            MC1 = MC1 + MC2
            MC2 = 0.D0
*
* Obtain a new age for the giant.
*
            CALL gntage(MC1,M1,KW,ZPARS,M01,AJ1)
            CALL star(KW,M01,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS)
         ENDIF
         CALL hrdiag(M01,AJ1,M1,TM1,TN,TSCLS1,LUMS,GB,ZPARS,
     &               R1,L1,KW,MC1,RC1,MENV,RENV,K21)
         JSPIN1 = OORB*(K21*R1*R1*(M1-MC1)+K3*RC1*RC1*MC1)
         KW1 = KW
         ECC = 0.D0
      ELSE
*
* Check if any eccentricity remains in the orbit by first using 
* energy to circularise the orbit before removing angular momentum. 
* (note this should not be done in case of CE SN ... fix).  
*
         IF(EORBF.LT.ECIRC)THEN
            ECC = SQRT(1.D0 - EORBF/ECIRC)
         ELSE
            ECC = 0.D0
         ENDIF
*
* Set both cores in co-rotation with the orbit on exit of CE, 
*
         TB = (SEPF/AURSUN)*SQRT(SEPF/(AURSUN*(M1+M2)))
         OORB = TWOPI/TB
         JORB = M1*M2/(M1+M2)*SQRT(1.D0-ECC*ECC)*SEPF*SEPF*OORB
*        JSPIN1 = OORB*(K21*R1*R1*(M1-MC1)+K3*RC1*RC1*MC1)
*        JSPIN2 = OORB*(K22*R2*R2*(M2-MC2)+K3*RC2*RC2*MC2)
*
* or, leave the spins of the cores as they were on entry.
* Tides will deal with any synchronization later.
*
         JSPIN1 = OSPIN1*(K21*R1*R1*(M1-MC1)+K3*RC1*RC1*MC1)
         JSPIN2 = OSPIN2*(K22*R2*R2*(M2-MC2)+K3*RC2*RC2*MC2)
      ENDIF
   30 SEP = SEPF
      RETURN
      END
***
