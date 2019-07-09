
      PROGRAM LPTEST

c      Compute the coefficients in the Legendre polynomial expansions
c      of the phase matrix elements.  Compare values from angular
c      integration with values computed directly by MIEV0.

c      NOTES:

c       (0) Do NOT use the NoPMOM version of MIEV0 here.

c       (1) In MIEV0, set the PARAMETER MAXANG to 10001 (in order
c           to do the angular integrations) and set MAXTRM to 150
c           or so (ALL occurrences; to save storage).

c       (2) Large differences between the exact and quadrature
c           values can appear, but these are invariably in cases
c           where the Legendre coefficients are many orders of
c           magnitude down from their maximum values.  These
c           differences can be seen to be mainly due to quadrature
c           error, by comparing the 1001-point to the immediately
c           following 100001-point quadrature (which also shows
c           how hard it would be to get Legendre coefficients by
c           quadrature in some cases).

c       (3) Because of the size of the output, only a few cases
c           are sampled here.  The user is urged to try cases
c           corresponding to his own interests; but remember that
c           computer time escalates rapidly for size parameters
c           over 100 or so.


c      CALLING TREE:

c         LPTEST
c            ERRMSG
c            MIEV0
c            SIMPSO
c               ERRMSG

c ----------------------------------------------------------------------
c ------------  I/O SPECIFICATIONS FOR SUBROUTINE  MIEV0  --------------
c ----------------------------------------------------------------------
      PARAMETER  ( MAXANG = 10001, MOMDIM = 250 )
      LOGICAL  ANYANG, PERFCT, PRNT( 2 )
      INTEGER  IPOLZN, NUMANG, NMOM
      REAL     GQSC, MIMCUT, PMOM( 0:MOMDIM, 4 ), QEXT, QSCA, SPIKE,
     $         XMU( MAXANG ), XX
      COMPLEX  CREFIN, SFORW, SBACK, S1( MAXANG ), S2( MAXANG ),
     $         TFORW( 2 ), TBACK( 2 )
c ----------------------------------------------------------------------

c         *** Definitions of local variables ***

c   PROD      : Product of a Legendre polynomial and a phase quantity

c   PMOMAP    : Moments calculated by angular integration

c   PQ( I,N ) : I-th phase quantity at N-th angle

c   PL( N )   : Legendre polynomial P-sub-MOM  of argument  XMU(N)
c   PLm1( N ) : Legendre Polynomial P-sub-(MOM-1)  of argument  XMU(N)

c   STEP      : Size of integration interval in Simpson quadrature

c     .. Local Scalars ..

      CHARACTER PMINDX*6
      INTEGER   IANG, IPOL, ISZPAR, J, MOM, N, NREFIN
      REAL      FNORM, PMOMAP, POL, STEP
      COMPLEX   CTMP
c     ..
c     .. Local Arrays ..

      REAL      PL( MAXANG ), PLM1( MAXANG ),
     &          PQ( 4, MAXANG ), PROD( MAXANG )
c     ..
c     .. External Functions ..

      REAL      SIMPSO
      EXTERNAL  SIMPSO
c     ..
c     .. External Subroutines ..

      EXTERNAL  ERRMSG, MIEV0
c     ..
c     .. Intrinsic Functions ..

      INTRINSIC ABS, AIMAG, CONJG, REAL
c     ..
c     .. Statement Functions ..

      REAL      SQ
c     ..
c     .. Statement Function definitions ..

      SQ( CTMP ) = REAL( CTMP )**2 + AIMAG( CTMP )**2
c     ..

c                      ** Set some input variables to MIEV0
      PRNT(1) = .FALSE.
      PRNT(2) = .FALSE.
      PERFCT = .FALSE.
      ANYANG = .FALSE.
      MIMCUT = 1.E-6


      WRITE( *, 9000 )

c          ** Loop over values of IPOLZN, CREFIN, XX, and NUMANG

      DO 130 IPOL = 1, 2

         IF( IPOL.EQ.1 ) IPOLZN = -1234
         IF( IPOL.EQ.2 ) IPOLZN = +1234


         DO 120 NREFIN = 1, 2

            IF( NREFIN.EQ.1 ) CREFIN = ( 1.342, 0.0 )
            IF( NREFIN.EQ.2 ) CREFIN = ( 1.342, -1.0 )


            DO 110 ISZPAR = 1, 3

               IF( ISZPAR.EQ.1 ) XX = 1.E-4
               IF( ISZPAR.EQ.2 ) XX = 1.0
               IF( ISZPAR.EQ.3 ) XX = 100.0

c                                           ** Calculate max. possible
c                                           ** no. of Legendre coeffs.
c                                           ** (twice Mie series length)

               NMOM = 2.*( XX + 4.*XX**(1./3.) + 2.)


               DO 100 IANG = 1, 2
c                                             ** WARNING -- NUMANG must
c                                             ** be odd for Simpson Rule
                  IF( IANG.EQ.1 ) NUMANG = 1001
                  IF( IANG.EQ.2 ) NUMANG = 10001

                  IF( NUMANG.GT.MAXANG ) CALL ERRMSG
     &                ( 'PMOMTEST--MAXANG too small', .TRUE.)

                  WRITE( *, 9001 ) NUMANG, XX, IPOLZN, CREFIN

                  STEP   = 2./ ( NUMANG - 1 )

                  DO 10 N = 1, NUMANG
                     XMU( N ) = 1. - ( N - 1 )*STEP
   10             CONTINUE


                  CALL MIEV0( XX, CREFIN, PERFCT, MIMCUT, ANYANG,
     &                        NUMANG, XMU, NMOM, IPOLZN, MOMDIM, PRNT,
     &                        QEXT, QSCA, GQSC, PMOM, SFORW, SBACK, S1,
     &                        S2, TFORW, TBACK, SPIKE )


                  IF( IPOLZN.LT.0 ) THEN
c                                          ** Use S1,S2 to store T1,T2
c                                          ** (see MIEV0 doc for defns)

                     DO 20 N = 2, NUMANG - 1
                        CTMP   = S1( N )
                        S1( N ) = ( S2( N ) - XMU( N )*S1( N ) ) /
     &                            ( 1. - XMU( N )**2 )
                        S2( N ) = ( CTMP - XMU( N )*S2( N ) ) /
     &                            ( 1. - XMU( N )**2 )
   20                CONTINUE

                     S1( 1 ) = TFORW( 1 )
                     S2( 1 ) = TFORW( 2 )
                     S1( NUMANG ) = TBACK( 1 )
                     S2( NUMANG ) = TBACK( 2 )

                  END IF
c                                       ** Calculate phase quantities

                  DO 30 N = 1, NUMANG
                     PQ( 1, N ) = SQ( S1( N ) )
                     PQ( 2, N ) = SQ( S2( N ) )
                     PQ( 3, N ) =  REAL(  S1( N )*CONJG( S2( N ) ) )
                     PQ( 4, N ) = -AIMAG( S1( N )*CONJG( S2( N ) ) )
   30             CONTINUE


                  FNORM  = 4./ ( XX**2 * QSCA )

                  DO 90 MOM = 0, NMOM
c                                         ** Calculate Legendre polys.
                     IF( MOM.EQ.0 ) THEN

                        DO 40 N = 1, NUMANG
                           PL( N ) = 1.0
   40                   CONTINUE

                     ELSE IF( MOM.EQ.1 ) THEN

                        DO 50 N = 1, NUMANG
                           PLM1( N ) = 1.0
                           PL( N ) = XMU( N )
   50                   CONTINUE

                     ELSE

                        DO 60 N = 1, NUMANG
                           POL    = ( ( 2*MOM - 1 )*XMU( N )*PL( N ) -
     &                              ( MOM - 1 )*PLM1( N ) ) / MOM
                           PLM1( N ) = PL( N )
                           PL( N ) = POL
   60                   CONTINUE

                     END IF


                     DO 80 J = 1, 4

                        DO 70 N = 1, NUMANG
                           PROD( N ) = PL( N )*PQ( J, N )
   70                   CONTINUE
c                                            ** Legendre moments by
c                                               angular quadrature

                        PMOMAP = 0.5 * SIMPSO( PROD, NUMANG, STEP )

c                                        ** Put moment number and polar-
c                                           ization flag into a string

                        IF(J.EQ.1) WRITE( PMINDX,'(I4,A,I1)') MOM,',',J
                        IF(J.NE.1) WRITE( PMINDX,'(I6)') J

                        IF( PMOM(MOM,J).NE.0.) THEN

                           WRITE(*,'(A,1P,2E20.5,0P,F24.5)')
     &                           PMINDX, PMOM(MOM,J),
     &                           ( 2*MOM + 1 ) * FNORM * PMOM(MOM,J),
     &                           PMOMAP / PMOM(MOM,J) - 1.

                        ELSE

                           WRITE(*,'(A,F20.1)') PMINDX, 0.0

                        END IF


   80                CONTINUE

   90             CONTINUE

  100          CONTINUE

  110       CONTINUE

  120    CONTINUE

  130 CONTINUE


      STOP

 9000 FORMAT( ////, 30X, '************************************',/,
     &              30X, '* L E G E N D R E    M O M E N T S *',/,
     &              30X, '************************************' )
 9001 FORMAT( //, ' No. Quad Angs=', I5, '   Size Param=', F8.4,
     &  '  IPOLZN=', I6, '   Refr Index=', F6.3, 1P,E9.1, /,'  PMOM',8X,
     &  'unnormalized     Dave normalized    quadrature/exact - 1')
      END

      REAL FUNCTION SIMPSO( F, N, H )

c         Quadrature by Simpsons Rule

c     I N P U T

c          F(I), I=1 TO N : Values of the function being integrated
c          N :  No. of function values (**MUST BE ODD**)
c          H :  Step (in variable of integration) between values of F

c     O U T P U T

c          SIMPSO :  Approximate value of integral  ( H/3 * ( F(1) +
c                        4F(2) + 2F(3) +...+ 4F(N-1) + F(N)) )

c ----------------------------------------------------------------------

c     .. Scalar Arguments ..

      INTEGER   N
      REAL      H
c     ..
c     .. Array Arguments ..

      REAL      F( * )
c     ..
c     .. Local Scalars ..

      INTEGER   I
c     ..
c     .. External Subroutines ..

      EXTERNAL  ERRMSG
c     ..
c     .. Intrinsic Functions ..

      INTRINSIC MOD
c     ..

      IF( N.LT.3 .OR. MOD( N,2 ).NE.1 .OR. H.LE.0.0 )
     &    CALL ERRMSG( 'SIMPSO--Bad input arguments',.TRUE. )


      SIMPSO = F( 1 ) + F( N )

      DO 10 I = 2, N - 1
         SIMPSO = SIMPSO + 2.*( 2 - MOD( I,2 ) ) * F( I )
   10 CONTINUE

      SIMPSO = ( H / 3.) * SIMPSO

      RETURN
      END

