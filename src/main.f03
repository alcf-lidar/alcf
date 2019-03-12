module main_module
    use cosp_run
    use nc_utils
    implicit none
contains
    function arg(i)
        integer, intent(in) :: i
        character(len=:), allocatable :: arg
        integer :: len

        call get_command_argument(i, arg, len)
        allocate(character(len=len) :: arg)
        call get_command_argument(i, arg, len)
    end function

    subroutine read_input(file, input, time)
        character(len=*), intent(in) :: file
        type(cosp_input_fields), intent(out) :: input
        real(8), dimension(:), allocatable, intent(out) :: &
            time
        integer :: ncid
        real(8), dimension(:), allocatable :: &
            lon, &
            lat, &
            ps, &
            orog
        real(8), dimension(:,:), allocatable :: &
            zg, &
            ta, &
            pfull, &
            clw, &
            cli, &
            clt
        integer :: &
            nlon, &
            nlat, &
            npoints, &
            nlev, &
            nhydro
        integer, dimension(256) :: shp
        integer :: i
        integer :: ilon, ilat

        call nc_check(nf90_open(file, NF90_NOWRITE, ncid))

        call nc_get_var_1d_real(ncid, 'lon', lon)
        call nc_get_var_1d_real(ncid, 'lat', lat)
        call nc_get_var_1d_real(ncid, 'time', time)
        call nc_get_var_1d_real(ncid, 'ps', ps)
        call nc_get_var_1d_real(ncid, 'orog', orog)
        call nc_get_var_2d_real(ncid, 'zg', zg)
        call nc_get_var_2d_real(ncid, 'ta', ta)
        call nc_get_var_2d_real(ncid, 'pfull', pfull)
        call nc_get_var_2d_real(ncid, 'clw', clw)
        call nc_get_var_2d_real(ncid, 'cli', cli)
        call nc_get_var_2d_real(ncid, 'clt', clt)

        shp(1:2) = shape(ta)
        npoints = shp(2)
        nlev = shp(1)
        nhydro = N_HYDRO

        call allocate_cosp_input_fields(input, npoints, nlev)

        input%npoints = npoints
        input%nlevels = nlev
        input%emsfc_lw = 1.
        input%time = 1.
        input%lon = lon
        input%lat = lat
        input%T = transpose(ta)
        input%p = transpose(pfull)
        input%tca = transpose(clt)*0.01
        input%zlev = transpose(zg)
        do i = 1, npoints
            input%zlev(i,:) = input%zlev(i,:) - orog(i)
        end do
        input%zlev_half(:,2:nlev) = 0.5*(input%zlev(:,1:(nlev-1)) + input%zlev(:,2:nlev))
        input%zlev_half(:,1) = 0
        input%mr_hydro(:,:,1) = transpose(clw)
        input%mr_hydro(:,:,2) = transpose(cli)
        input%ph(:,2:(nlev-1)) = 0.5*(input%p(:,1:(nlev-1)) + input%p(:,2:nlev))
        input%ph(:,1) = ps

        call nc_check(nf90_close(ncid))
    end subroutine

    subroutine write_output(file, input, time, output)
        character(len=*), intent(in) :: file
        type(cosp_input_fields), intent(in) :: input
        real(8), dimension(:), allocatable, intent(in) :: time
        type(cosp_output_fields), intent(in) :: output
        integer :: ncid
        integer :: column_dimid, level_dimid, time_dimid
        integer :: &
            lon_varid, &
            lat_varid, &
            time_varid, &
            zlev_varid, &
            zlev_half_varid, &
            p_varid, &
            ph_varid, &
            beta_mol_varid, &
            beta_tot_varid
        integer :: status
        integer :: npoints, nlevels, ncolumns

        npoints = input%npoints
        nlevels = input%nlevels
        ncolumns = size(output%sglidar%beta_tot, 2)

        call nc_check(nf90_create(file, 0, ncid))
        call nc_check(nf90_def_dim(ncid, 'time', npoints, time_dimid))
        call nc_check(nf90_def_dim(ncid, 'level', nlevels, level_dimid))
        call nc_check(nf90_def_dim(ncid, 'column', ncolumns, column_dimid))
        call nc_check(nf90_def_var(ncid, 'lon', nf90_double, time_dimid, lon_varid))
        call nc_check(nf90_def_var(ncid, 'lat', nf90_double, time_dimid, lat_varid))
        call nc_check(nf90_def_var(ncid, 'zfull', nf90_double, (/time_dimid, level_dimid/), zlev_varid))
        call nc_check(nf90_def_var(ncid, 'zhalf', nf90_double, (/time_dimid, level_dimid/), zlev_half_varid))
        call nc_check(nf90_def_var(ncid, 'pfull', nf90_double, (/time_dimid, level_dimid/), p_varid))
        call nc_check(nf90_def_var(ncid, 'phalf', nf90_double, (/time_dimid, level_dimid/), ph_varid))
        call nc_check(nf90_def_var(ncid, 'backscatter', nf90_double, (/time_dimid, column_dimid, level_dimid/), beta_tot_varid))
        call nc_check(nf90_def_var(ncid, 'backscatter_mol', nf90_double, (/time_dimid, level_dimid/), beta_mol_varid))
        call nc_check(nf90_def_var(ncid, 'time', nf90_double, time_dimid, time_varid))
        call nc_check(nf90_enddef(ncid))
        call nc_check(nf90_put_var(ncid, lon_varid, input%lon))
        call nc_check(nf90_put_var(ncid, lat_varid, input%lat))
        call nc_check(nf90_put_var(ncid, beta_tot_varid, output%sglidar%beta_tot))
        call nc_check(nf90_put_var(ncid, beta_mol_varid, output%sglidar%beta_mol))
        call nc_check(nf90_put_var(ncid, zlev_varid, input%zlev))
        call nc_check(nf90_put_var(ncid, zlev_half_varid, input%zlev_half))
        call nc_check(nf90_put_var(ncid, p_varid, input%p))
        call nc_check(nf90_put_var(ncid, ph_varid, input%ph))
        call nc_check(nf90_put_var(ncid, time_varid, time))
        call nc_check(nf90_close(ncid))
    end subroutine
end module

program main
    use iso_fortran_env
    use cosp_run
    use main_module
    implicit none

    character(len=:), allocatable :: program_name
    character(len=:), allocatable :: input_file
    character(len=:), allocatable :: output_file
    character(len=:), allocatable :: config_file
    integer :: unit
    type(cosp_run_config) :: config
    type(cosp_input_fields) :: input
    type(cosp_output_fields) :: output
    namelist /config_nml/ config
    real(8), dimension(:), allocatable ::  time

    program_name = arg(0)
    if (command_argument_count() /= 3) then
        write(error_unit, "('Usage: ',a,' <config> <input> <output>')") program_name
        stop ''
    end if
    config_file = arg(1)
    input_file = arg(2)
    output_file = arg(3)

    open(newunit=unit, file=config_file, status='old')
    read(unit, nml=config_nml)
    close(unit)

    call read_input(input_file, input, time)
    call cosp_run(config, input, output)
    call write_output(output_file, input, time, output)
end program
