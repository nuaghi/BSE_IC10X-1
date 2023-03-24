      SUBROUTINE LT2UBV ( LOGL, LOGT, MASS00, MV, BMINV, UMINB )
      COMMON /UBVDAT/ TGR(34), GGR(13), TAB(5,13,34)
      COMMON /HERE05/ LOGG, LOGG1, LOGG2, LOGM, LOGT1, LOGT2, MBOL, 
     : BC1, BC2, BCX, BV1, BV2, BVX, DG1, DG2, DT1, DT2, UB1, UB2, UBX,
     : BC(4), UB(4), BV(4), VR(4), RI(4), I, ING1, ING2, INT1, INT2, 
     : J, K, K0, K1, K2 
      real*8  LOGL, LOGT, MASS00, MV, BMINV, UMINB ,LOGG, LOGG1, LOGG2, MBOL, 
     : BC1, BC2, BCX, BV1, BV2, BVX, DG1, DG2, DT1, DT2, UB1, UB2, UBX
      LOGM = log10(MASS00)
      LOGG = LOGM + 4.0D0*LOGT - LOGL - 10.6071D0
c determine values of log g to interpolate between
      ING1 = 1
      ING2 = 13
c      print*,TGR(1),GGR(1),TAB(1,1,1)
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
      print*,LOGL,LOGT, MASS00
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
