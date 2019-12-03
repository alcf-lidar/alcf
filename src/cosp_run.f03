module cosp_run_mod
    use mod_cosp_constants
    use mod_cosp_types
    use mod_cosp
    use mod_cosp_io
    implicit none

    type cosp_run_config
        type(cosp_config) output
        integer :: &
            overlap, &
            isccp_topheight, &
            isccp_topheight_direction, &
            npoints_it, &
            ncolumns, &
            nlevels, &
            nprmts_max_hydro, &
            naero, &
            nprmts_max_aero, &
            lidar_ice_type, &
            lidar_wavelength, &
            surface_lidar, &
            nlr, &
            platform, &
            satellite, &
            instrument, &
            nchannels, &
            surface_radar, &
            use_mie_tables, &
            use_gas_abs, &
            do_ray, &
            melt_lay
        logical :: &
            use_vgrid, &
            csat_vgrid, &
            use_precipitation_fluxes, &
            use_reff
        real :: &
            radar_freq, &
            k2, &
            ZenAng, &
            co2, &
            ch4, &
            n2o, &
            co, &
            lidar_max_range
        integer, dimension(RTTOV_MAX_CHANNELS) :: channels
        real, dimension(RTTOV_MAX_CHANNELS) :: surfem
    end type

    type cosp_input_fields
        integer :: npoints
        integer :: ncolumns
        integer :: nlevels
        real :: emsfc_lw
        real :: time
        real, dimension(:), allocatable :: &
            lon, &
            lat, &
            skt, &
            land, &
            u_wind, &
            v_wind, &
            sunlit, &
            orog
        real, dimension(:, :), allocatable :: &
            p, &
            ph, &
            zlev, &
            zlev_half, &
            T, &
            sh, &
            rh, &
            tca, &
            cca, &
            !mr_lsliq, &
            !mr_lsice, &
            !mr_ccliq, &
            !mr_ccice, &
            rain_ls, &
            snow_ls, &
            grpl_ls, &
            rain_cv, &
            snow_cv, &
            dtau_s, &
            dtau_c, &
            dem_s, &
            dem_c, &
            mr_ozone
        real, dimension(:, :, :), allocatable :: &
            mr_hydro, &
            Reff
    end type

    type cosp_output_fields
        type(cosp_subgrid) :: sgx
        type(cosp_sgradar) :: sgradar
        type(cosp_sglidar) :: sglidar
        type(cosp_isccp) :: isccp
        type(cosp_modis) :: modis
        type(cosp_misr) :: misr
        type(cosp_rttov) :: rttov
        type(cosp_vgrid) :: vgrid
        type(cosp_radarstats) :: stradar
        type(cosp_lidarstats) :: stlidar
    end type
contains
    subroutine cosp_run(config, input, output)
        type(cosp_run_config), intent(in) :: config
        type(cosp_input_fields), intent(in) :: input
        type(cosp_output_fields), intent(inout) :: output
        type(cosp_gridbox) :: gbx

        integer :: k
        double precision :: time, time_bnds(2), time_step
        real :: toffset_step, half_time_step

        time_step      = 3.D0/24.D0
        time           = 8*1.D0/8.D0
        toffset_step   = time_step/input%npoints
        half_time_step = 0.5*time_step

        call construct_cosp_gridbox( &
            time=time, &
            time_bnds=time_bnds, &
            radar_freq=config%radar_freq, &
            surface_radar=config%surface_radar, &
            use_mie_tables=config%use_mie_tables, &
            use_gas_abs=config%use_gas_abs, &
            do_ray=config%do_ray, &
            melt_lay=config%melt_lay, &
            k2=config%k2, &
            Npoints=input%npoints, &
            Nlevels=input%nlevels, &
            Ncolumns=config%ncolumns, &
            Nhydro=N_HYDRO, &
            Nprmts_max_hydro=config%Nprmts_max_hydro, &
            Naero=config%naero, &
            Nprmts_max_aero=config%nprmts_max_aero, &
            Npoints_it=config%npoints_it, &
            lidar_ice_type=config%lidar_ice_type, &
            lidar_wavelength=config%lidar_wavelength, &
            surface_lidar=config%surface_lidar, &
            isccp_top_height=config%isccp_topheight, &
            isccp_top_height_direction=config%isccp_topheight_direction, &
            isccp_overlap=config%overlap, &
            isccp_emsfc_lw=input%emsfc_lw, &
            use_precipitation_fluxes=config%use_precipitation_fluxes, &
            use_reff=config%use_reff, &
            plat=config%platform, &
            sat=config%satellite, &
            inst=config%instrument, &
            nchan=config%nchannels, &
            zenang=config%zenang, &
            ichan=config%channels(1:config%nchannels), &
            surfem=config%surfem(1:config%nchannels), &
            co2=config%co2, &
            ch4=config%ch4, &
            n2o=config%n2o, &
            co=config%co, &
            y=gbx &
        )

        gbx%longitude = input%lon
        gbx%latitude = input%lat
        ! Toffset. This assumes that time is the mid-point of the interval.

        do k=1,input%npoints
            gbx%toffset(k) = -half_time_step + toffset_step*(k - 0.5)
        end do

        gbx%p = input%p
        gbx%ph = input%ph
        gbx%zlev = input%zlev
        gbx%zlev_half = input%zlev_half
        gbx%T = input%T
        gbx%q = input%rh
        gbx%sh = input%sh
        gbx%cca = input%cca
        gbx%tca = input%tca
        gbx%psfc = input%ph(:,1)
        gbx%skt = input%skt
        gbx%land = input%land
        gbx%mr_ozone = input%mr_ozone
        gbx%u_wind = input%u_wind
        gbx%v_wind = input%v_wind
        gbx%sunlit = input%sunlit
        gbx%mr_hydro = input%mr_hydro
        ! gbx%mr_hydro(:,:,I_LSCLIQ) = input%mr_lsliq
        ! gbx%mr_hydro(:,:,I_LSCICE) = input%mr_lsice
        ! gbx%mr_hydro(:,:,I_CVCLIQ) = input%mr_ccliq
        ! gbx%mr_hydro(:,:,I_CVCICE) = input%mr_ccice
        gbx%rain_ls = input%rain_ls
        gbx%snow_ls = input%snow_ls
        gbx%grpl_ls = input%grpl_ls
        gbx%rain_cv = input%rain_cv
        gbx%snow_cv = input%snow_cv
        gbx%Reff = input%Reff
        gbx%Reff(:,:,I_LSRAIN) = 0.0
        gbx%dtau_s = input%dtau_s
        gbx%dtau_c = input%dtau_c
        gbx%dem_s = input%dem_s
        gbx%dem_c = input%dem_c

        call construct_cosp_vgrid( &
            gbx, &
            config%nlr, &
            config%use_vgrid, &
            config%csat_vgrid, &
            output%vgrid &
        )
        call construct_cosp_subgrid( &
            input%npoints, &
            config%ncolumns, &
            input%nlevels, &
            output%sgx &
        )
        call construct_cosp_sgradar( &
            config%output, &
            input%npoints, &
            config%ncolumns, &
            input%nlevels, &
            N_HYDRO, &
            output%sgradar &
        )
        call construct_cosp_radarstats( &
            config%output, &
            input%npoints, &
            config%ncolumns, &
            output%vgrid%nlvgrid, &
            N_HYDRO, &
            output%stradar &
        )
        call construct_cosp_sglidar( &
            config%output, &
            input%npoints, &
            config%ncolumns, &
            input%nlevels, &
            N_HYDRO, &
            PARASOL_NREFL, &
            output%sglidar &
        )
        call construct_cosp_lidarstats( &
            config%output, &
            input%npoints, &
            config%ncolumns, &
            output%vgrid%nlvgrid, &
            N_HYDRO, &
            PARASOL_NREFL, &
            output%stlidar &
        )
        call construct_cosp_isccp( &
            config%output, &
            input%npoints, &
            config%ncolumns, &
            input%nlevels, &
            output%isccp &
        )
        call construct_cosp_modis( &
            config%output, &
            input%npoints, &
            output%modis &
        )
        call construct_cosp_misr( &
            config%output, &
            input%npoints, &
            output%misr &
        )
        call construct_cosp_rttov( &
            config%output, &
            input%npoints, &
            config%nchannels, &
            output%rttov &
        )

        call cosp( &
            config%overlap, &
            config%ncolumns, &
            config%output, &
            output%vgrid, &
            gbx, &
            output%sgx, &
            output%sgradar, &
            output%sglidar, &
            output%isccp, &
            output%misr, &
            output%modis, &
            output%stradar, &
            output%stlidar &
        )

        gbx%time = time
    end subroutine

    subroutine cosp_run_free_output(output)
        type(cosp_output_fields), intent(inout) :: output

        !call free_cosp_gridbox(output%gbx)
        call free_cosp_subgrid(output%sgx)
        call free_cosp_sgradar(output%sgradar)
        call free_cosp_radarstats(output%stradar)
        call free_cosp_sglidar(output%sglidar)
        call free_cosp_lidarstats(output%stlidar)
        call free_cosp_isccp(output%isccp)
        call free_cosp_misr(output%misr)
        call free_cosp_modis(output%modis)
        call free_cosp_rttov(output%rttov)
        call free_cosp_vgrid(output%vgrid)
    end subroutine

    subroutine allocate_cosp_input_fields(fields, npoints, nlevels)
        type(cosp_input_fields), intent(inout) :: fields
        integer, intent(in) :: &
            npoints, &
            nlevels

        integer, parameter :: nhydro = N_HYDRO

        allocate( &
            fields%lon(npoints), &
            fields%lat(npoints), &
            fields%skt(npoints), &
            fields%land(npoints), &
            fields%u_wind(npoints), &
            fields%v_wind(npoints), &
            fields%sunlit(npoints), &
            fields%orog(npoints), &
            fields%p(npoints, nlevels), &
            fields%ph(npoints, nlevels), &
            fields%zlev(npoints, nlevels), &
            fields%zlev_half(npoints, nlevels), &
            fields%T(npoints, nlevels), &
            fields%sh(npoints, nlevels), &
            fields%rh(npoints, nlevels), &
            fields%tca(npoints, nlevels), &
            fields%cca(npoints, nlevels), &
            fields%rain_ls(npoints, nlevels), &
            fields%snow_ls(npoints, nlevels), &
            fields%grpl_ls(npoints, nlevels), &
            fields%rain_cv(npoints, nlevels), &
            fields%snow_cv(npoints, nlevels), &
            fields%dtau_s(npoints, nlevels), &
            fields%dtau_c(npoints, nlevels), &
            fields%dem_s(npoints, nlevels), &
            fields%dem_c(npoints, nlevels), &
            fields%mr_ozone(npoints, nlevels), &
            fields%mr_hydro(npoints, nlevels, nhydro), &
            fields%Reff(npoints, nlevels, nhydro) &
        )

        fields%lon = 0
        fields%lat = 0
        fields%skt = 0
        fields%land = 0
        fields%u_wind  = 0
        fields%v_wind = 0
        fields%sunlit = 0
        fields%orog = 0
        fields%p = 0
        fields%ph = 0
        fields%zlev = 0
        fields%zlev_half = 0
        fields%T = 0
        fields%sh = 0
        fields%rh = 0
        fields%tca = 0
        fields%cca = 0
        fields%rain_ls = 0
        fields%snow_ls = 0
        fields%grpl_ls = 0
        fields%rain_cv = 0
        fields%snow_cv = 0
        fields%dtau_s = 0
        fields%dtau_c = 0
        fields%dem_s = 0
        fields%dem_c = 0
        fields%mr_ozone = 0
        fields%mr_hydro = 0
        fields%Reff = 0
    end subroutine

    subroutine deallocate_cosp_input_fields(fields, npoints, nlevels)
        type(cosp_input_fields), intent(inout) :: fields
        integer, intent(in) :: &
            npoints, &
            nlevels

        integer, parameter :: nhydro = 4

        deallocate( &
            fields%lon, &
            fields%lat, &
            fields%skt, &
            fields%land, &
            fields%u_wind, &
            fields%v_wind, &
            fields%sunlit, &
            fields%p, &
            fields%ph, &
            fields%zlev, &
            fields%zlev_half, &
            fields%T, &
            fields%sh, &
            fields%rh, &
            fields%tca, &
            fields%cca, &
            fields%rain_ls, &
            fields%snow_ls, &
            fields%grpl_ls, &
            fields%rain_cv, &
            fields%snow_cv, &
            fields%dtau_s, &
            fields%dtau_c, &
            fields%dem_s, &
            fields%dem_c, &
            fields%mr_ozone, &
            fields%mr_hydro, &
            fields%Reff &
        )
    end subroutine
end module
