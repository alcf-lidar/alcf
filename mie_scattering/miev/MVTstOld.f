
      PROGRAM TSTMIV

c         Test cases for MIEV0 from NCAR Tech Note, with, in addition,
c         calculations of Legendre coefficients

c     NOTE:  set NoPMOM = True if using NoPMOM version of MIEV0


      IMPLICIT  NONE

c ----------------------------------------------------------------------
c --------  I / O SPECIFICATIONS FOR SUBROUTINE MIEV0  -----------------
c ----------------------------------------------------------------------
      INTEGER  MAXANG, MOMDIM
      PARAMETER  ( MAXANG = 40, MOMDIM = 10 )
      LOGICAL  ANYANG, PERFCT, PRNT(2)
      INTEGER  IPOLZN( 4,2 ), NUMANG, NMOM
      REAL     GQSC, MIMCUT, PMOM( 0:MOMDIM, 4 ), QEXT, QSCA, SPIKE,
     $         XMU(MAXANG), XX(4)
      COMPLEX  CREFIN( 2 ), SFORW, SBACK, S1( MAXANG ), S2( MAXANG ),
     $         TFORW( 2 ), TBACK( 2 )
c ----------------------------------------------------------------------

c     .. Local Scalars ..

      LOGICAL   NOPMOM
      INTEGER   I, NIOR, NXX
      REAL      PI
c     ..
c     .. External Subroutines ..

      EXTERNAL  MIEV0
c     ..
c     .. Intrinsic Functions ..

      INTRINSIC ASIN, COS
c     ..
      DATA  CREFIN / (1.5,0.0), (1.5,-0.1) /,
     $      XX / 10., 100., 1000., 5000. /,
     $      IPOLZN / 13, 24, 1234, 0, -13, -24, -1234, 0 /,
     $      PRNT / 2*.TRUE. /,
     $      PERFCT /.FALSE./,
     $      MIMCUT / 1.E-6 /,
     $      ANYANG /.TRUE./,
     $      NUMANG / 19 /


      NOPMOM = .False.
      PI     = 2.*ASIN( 1.0 )

      IF( NUMANG.GT.MAXANG ) STOP 'numang'

      DO 10 I = 1, NUMANG
         XMU( I ) = COS( (I-1)*PI / ( NUMANG - 1 ) )
   10 CONTINUE

      XMU( NUMANG ) = -1.0


      DO 30 NIOR = 1, 2

         DO 20 NXX = 1, 4

            NMOM = 10
            IF( NOPMOM .OR. NXX.EQ.4 ) NMOM = 0

            CALL MIEV0( XX( NXX ), CREFIN( NIOR ), PERFCT, MIMCUT,
     &                  ANYANG, NUMANG, XMU, NMOM, IPOLZN( NXX,NIOR ),
     &                  MOMDIM, PRNT, QEXT, QSCA, GQSC, PMOM, SFORW,
     &                  SBACK, S1, S2, TFORW, TBACK, SPIKE )

   20    CONTINUE

   30 CONTINUE


      STOP

      END

