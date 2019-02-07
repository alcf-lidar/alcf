module main_module
    use cosp_run
    use nc_utils
    implicit none

    type input_names
        character(len=NF90_MAX_NAME) :: lat = 'lat'
        character(len=NF90_MAX_NAME) :: lon = 'lon'
        character(len=NF90_MAX_NAME) :: skt = 'skt'
        character(len=NF90_MAX_NAME) :: land = 'land'
        character(len=NF90_MAX_NAME) :: u_wind = 'u_wind'
        character(len=NF90_MAX_NAME) :: v_wind = 'v_wind'
        character(len=NF90_MAX_NAME) :: sunlit = 'sunlit'
        character(len=NF90_MAX_NAME) :: p = 'p'
        character(len=NF90_MAX_NAME) :: ph = 'ph'
        character(len=NF90_MAX_NAME) :: zlev = 'zlev'
        character(len=NF90_MAX_NAME) :: zlev_half = 'zlev_half'
        character(len=NF90_MAX_NAME) :: T = 'T'
        character(len=NF90_MAX_NAME) :: sh = 'sh'
        character(len=NF90_MAX_NAME) :: rh = 'rh'
        character(len=NF90_MAX_NAME) :: tca = 'tca'
        character(len=NF90_MAX_NAME) :: cca = 'cca'
        character(len=NF90_MAX_NAME) :: mr_hydro = 'mr_hydro'
        !character(len=NF90_MAX_NAME) :: mr_lsliq = 'mr_lsliq'
        !character(len=NF90_MAX_NAME) :: mr_lsice = 'mr_lsice'
        !character(len=NF90_MAX_NAME) :: mr_ccliq = 'mr_ccliq'
        !character(len=NF90_MAX_NAME) :: mr_ccice = 'mr_ccice'
        character(len=NF90_MAX_NAME) :: rain_ls = 'rain_ls'
        character(len=NF90_MAX_NAME) :: snow_ls = 'snow_ls'
        character(len=NF90_MAX_NAME) :: grpl_ls = 'grpl_ls'
        character(len=NF90_MAX_NAME) :: rain_cv = 'rain_cv'
        character(len=NF90_MAX_NAME) :: snow_cv = 'snow_cv'
        character(len=NF90_MAX_NAME) :: dtau_s = 'dtau_s'
        character(len=NF90_MAX_NAME) :: dtau_c = 'dtau_c'
        character(len=NF90_MAX_NAME) :: dem_s = 'dem_s'
        character(len=NF90_MAX_NAME) :: dem_c = 'dem_c'
        character(len=NF90_MAX_NAME) :: mr_ozone = 'mr_ozone'
        character(len=NF90_MAX_NAME) :: Reff = 'Reff'
        character(len=NF90_MAX_NAME) :: emsfc_lw = 'emsfc_lw'
    end type
contains
    function arg(i)
        integer, intent(in) :: i
        character(len=:), allocatable :: arg

        integer :: len

        call get_command_argument(i, arg, len)
        allocate(character(len=len) :: arg)
        call get_command_argument(i, arg, len)
    end function

    subroutine read_input(file, names, input)
        character(len=*) :: file
        type(input_names) :: names
        type(cosp_input_fields) :: input

        integer :: ncid

        call nc_check(nf90_open(file, NF90_NOWRITE, ncid))
        call nc_get_var_0d_real(ncid, names%emsfc_lw, input%emsfc_lw)
        call nc_get_var_1d_real(ncid, names%lat, input%lat)
        call nc_get_var_1d_real(ncid, names%lon, input%lon)
        call nc_get_var_1d_real(ncid, names%skt, input%skt)
        call nc_get_var_1d_real(ncid, names%land, input%land)
        call nc_get_var_1d_real(ncid, names%u_wind, input%u_wind)
        call nc_get_var_1d_real(ncid, names%v_wind, input%v_wind)
        call nc_get_var_1d_real(ncid, names%sunlit, input%sunlit)
        call nc_get_var_2d_real(ncid, names%p, input%p)
        call nc_get_var_2d_real(ncid, names%ph, input%ph)
        call nc_get_var_2d_real(ncid, names%zlev, input%zlev)
        call nc_get_var_2d_real(ncid, names%zlev_half, input%zlev_half)
        call nc_get_var_2d_real(ncid, names%T, input%T)
        call nc_get_var_2d_real(ncid, names%sh, input%sh)
        call nc_get_var_2d_real(ncid, names%rh, input%rh)
        call nc_get_var_2d_real(ncid, names%tca, input%tca)
        call nc_get_var_2d_real(ncid, names%cca, input%cca)
        call nc_get_var_3d_real(ncid, names%mr_hydro, input%mr_hydro)
        !call nc_get_var_2d_real(ncid, names%mr_lsliq, input%mr_lsliq)
        !call nc_get_var_2d_real(ncid, names%mr_lsice, input%mr_lsice)
        !call nc_get_var_2d_real(ncid, names%mr_ccliq, input%mr_ccliq)
        !call nc_get_var_2d_real(ncid, names%mr_ccice, input%mr_ccice)
        call nc_get_var_2d_real(ncid, names%rain_cv, input%rain_cv)
        call nc_get_var_2d_real(ncid, names%snow_ls, input%snow_ls)
        call nc_get_var_2d_real(ncid, names%grpl_ls, input%grpl_ls)
        call nc_get_var_2d_real(ncid, names%rain_ls, input%rain_ls)
        call nc_get_var_2d_real(ncid, names%snow_cv, input%snow_cv)
        call nc_get_var_2d_real(ncid, names%dtau_s, input%dtau_s)
        call nc_get_var_2d_real(ncid, names%dtau_c, input%dtau_c)
        call nc_get_var_2d_real(ncid, names%dem_s, input%dem_s)
        call nc_get_var_2d_real(ncid, names%dem_c, input%dem_c)
        call nc_get_var_2d_real(ncid, names%mr_ozone, input%mr_ozone)
        call nc_get_var_3d_real(ncid, names%Reff, input%Reff)

        input%npoints = size(input%lon)
        !input%nlevels = size(input%zlev, 2)
        input%nlevels = 50

       call nc_check(nf90_close(ncid))
    end subroutine

    subroutine write_output(file, input, output)
        character(len=*) :: file
        type(cosp_input_fields) :: input
        type(cosp_output_fields) :: output

        integer :: ncid
        integer :: point_dimid, subcol_dimid, level_dimid

        call nc_check(nf90_create(file, 0, ncid))
        call nc_check(nf90_def_dim(ncid, 'point', size(input%lon), point_dimid))
        call nc_check(nf90_def_dim(ncid, 'subcol', size(output%sglidar%beta_tot, 2), subcol_dimid))
        call nc_check(nf90_def_dim(ncid, 'level', size(output%sglidar%beta_tot, 3), level_dimid))
        call nc_put_var_3d_real(ncid, 'beta_tot', output%sglidar%beta_tot, (/ point_dimid, subcol_dimid, level_dimid /))
        call nc_put_var_2d_real(ncid, 'beta_mol', output%sglidar%beta_mol, (/ point_dimid, level_dimid /))
        call nc_put_var_1d_real(ncid, 'lon', input%lon, (/ point_dimid /))
        call nc_put_var_1d_real(ncid, 'lat', input%lat, (/ point_dimid /))
        call nc_put_var_2d_real(ncid, 'zlev', input%zlev, (/ level_dimid /))
        call nc_put_var_2d_real(ncid, 'zlev_half', input%zlev_half, (/ level_dimid /))
        call nc_put_var_2d_real(ncid, 'p', input%p, (/ point_dimid, level_dimid /))
        call nc_put_var_2d_real(ncid, 'ph', input%ph, (/ point_dimid, level_dimid /))
        call nc_check(nf90_close(ncid))
    end subroutine
end module

program main
    use iso_fortran_env
    use cosp_run
    use mod_cosp_constants
    use mod_cosp_types
    use mod_cosp
    use mod_cosp_io
    use netcdf
    use nc_utils
    use main_module
    implicit none

    character(len=:), allocatable :: program_name
    character(len=:), allocatable :: input_file
    character(len=:), allocatable :: output_file
    character(len=:), allocatable :: config_file
    integer :: unit
    type(input_names) :: names
    type(cosp_run_config) :: config
    type(cosp_input_fields) :: input
    type(cosp_output_fields) :: output
    namelist /config_nml/ names, config

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

    call read_input(input_file, names, input)

    call cosp_run(config, input, output)

    !write(*, *) output%sglidar%beta_tot

    !write(*, *) output%sglidar%beta_tot(:, 1, :) - output%sglidar%beta_mol

    call write_output(output_file, input, output)

!    ! Example that processes ntsteps. It always uses the same input data
!    time_step      = 3.D0/24.D0
!    time           = 8*1.D0/8.D0 ! First time step
!    toffset_step   = time_step/Npoints
!    half_time_step = 0.5*time_step
!
!    time_bnds = (/time-half_time_step,time+half_time_step/) ! This may need to be adjusted,
!                                                           ! depending on the approx_interval in the MIP table
end program
