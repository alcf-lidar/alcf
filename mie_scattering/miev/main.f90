program main
    implicit none

    interface
        SUBROUTINE MIEV0( XX, CREFIN, PERFCT, MIMCUT, ANYANG, NUMANG, XMU, &
                          NMOM, IPOLZN, MOMDIM, PRNT, QEXT, QSCA, GQSC, &
                          PMOM, SFORW, SBACK, S1, S2, TFORW, TBACK, &
                          SPIKE )
            LOGICAL  ANYANG, PERFCT, PRNT(*)
            INTEGER  IPOLZN, MOMDIM, NUMANG, NMOM
            REAL     GQSC, MIMCUT, PMOM( 0:MOMDIM, * ), QEXT, QSCA, SPIKE, &
                     XMU(*), XX
            COMPLEX  CREFIN, SFORW, SBACK, S1(*), S2(*), TFORW(*), TBACK(*)
        END SUBROUTINE
    end interface

    integer :: len, n
    integer numang, nmom, ipolzn, momdim
    real, parameter :: r_min=0.1e-6, r_max=100e-6, r_d=0.1e-6
    character(len=:), allocatable :: lambda_s
    integer :: lambda_i
    !real, parameter :: lambda=532e-9
    real :: lambda
    real, parameter :: pi=4*atan(1.0)
    real r
    real xx
    complex crefin
    parameter (momdim = 200)
    real mimcut, qext, qsca, gqsc, spike, pmom(0:momdim, 4), xmu(1), p180
    complex sforw, sback, s1(2), s2(2), tforw(2), tback(2)
    logical perfct, anyang, prnt(2)

    n = command_argument_count()
    if (n /= 1) then
        write(*,*) 'Usage: miev <wavelength_nm>'
        stop 1
    end if

    call get_command_argument(1, lambda_s, len)
    allocate(character(len=len) :: lambda_s)
    call get_command_argument(1, lambda_s, len)
    read(lambda_s,'(I64)') lambda_i
    lambda = lambda_i*1e-9

    xx = 100.0
    crefin = 1.33
    mimcut = 0.0
    perfct = .false.
    anyang = .true.
    numang = 1
    xmu = (/ -1.0 /)
    nmom = 0
    ipolzn = 0
    prnt = (/.false., .false./)

    write(*,*) 'wavelength_nm: ', lambda_i, 'crefin: { ', realpart(crefin), imagpart(crefin), ' }'
    write(*,*) 'r qext qsca p180'

    r = r_min
    do while (r < r_max)
        xx = 2*pi*r/lambda
        call miev0( &
            xx=xx, &
            crefin=crefin, &
            perfct=perfct, &
            mimcut=mimcut, &
            anyang=anyang, &
            numang=numang, &
            xmu=xmu, &
            nmom=nmom, &
            ipolzn=ipolzn, &
            momdim=momdim, &
            prnt=prnt, &
            qext=qext, &
            qsca=qsca, &
            gqsc=gqsc, &
            pmom=pmom, &
            sforw=sforw, &
            sback=sback, &
            s1=s1, &
            s2=s2, &
            tforw=tforw, &
            tback=tback, &
            spike=spike &
        )

        p180 = 4/(xx**2*qsca)*(cabs(s1(1))**2 + cabs(s2(1))**2)/2
        if (spike == 1.0) then
            write(*,*) r*1e6, qext, qsca, p180
        end if

        r = r + r_d
    end do
end program
