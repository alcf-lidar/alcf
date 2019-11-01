module nc_utils
	use netcdf
	implicit none
contains
	subroutine nc_check(status)
		integer, intent(in) :: status

		if(status /= nf90_noerr) then
			print *, trim(nf90_strerror(status))
			stop ''
		end if
	end subroutine

	subroutine nc_inq_var(ncid, name, varid, dims)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		integer, intent(out) :: varid
		integer, dimension(:), allocatable, intent(out) :: dims

		integer :: xtype, ndims
		character(len=NF90_MAX_NAME) :: xname
		integer, dimension(NF90_MAX_VAR_DIMS) :: dimids
		integer :: i
		integer :: status

		status = nf90_inq_varid(ncid, name, varid)
		if(status /= nf90_noerr) then
			write(*, "(a,': ',a)") trim(name), trim(nf90_strerror(status))
			stop ''
		end if

		call nc_check(nf90_inquire_variable(ncid, varid, xname, xtype, ndims, dimids))

		allocate(dims(ndims))
		dims = 0

		do i=1,ndims
			call nc_check(nf90_inquire_dimension(ncid, dimids(i), len=dims(i)))
		end do
	end subroutine

	function nc_count(dims, start, count) result(count_new)
		integer, dimension(:), intent(in) :: dims
		integer, dimension(:), intent(in), optional :: start
		integer, dimension(:), intent(in), optional :: count
		integer, dimension(size(dims)) :: count_new

		if (present(start) .and. present(count)) then
			count_new = count
			where (count == -1)
				count_new = dims - start + 1
			end where
		else
			count_new = dims
		end if
	end function

	subroutine nc_get_var_0d_real(ncid, name, var)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), intent(out) :: var

		integer, dimension(:), allocatable :: dims
		integer :: varid

		call nc_inq_var(ncid, name, varid, dims)
		call nc_check(nf90_get_var(ncid, varid, var))
	end subroutine

	subroutine nc_get_var_1d_real(ncid, name, var, start, count)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:), allocatable, intent(out) :: var
		integer, dimension(:), intent(in), optional :: start, count

		integer, dimension(:), allocatable :: dims
		integer :: varid
		integer, dimension(1) :: count_new

		call nc_inq_var(ncid, name, varid, dims)
		count_new = nc_count(dims, start, count)
		allocate(var(count_new(1)))
		call nc_check(nf90_get_var(ncid, varid, var, start, count_new))
	end subroutine

	subroutine nc_get_var_2d_real(ncid, name, var, start, count)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:, :), allocatable, intent(out) :: var
		integer, dimension(:), intent(in), optional :: start, count

		integer, dimension(:), allocatable :: dims
		integer :: varid
		integer, dimension(2) :: count_new

		call nc_inq_var(ncid, name, varid, dims)
		count_new = nc_count(dims, start, count)
		allocate(var(count_new(1), count_new(2)))
		call nc_check(nf90_get_var(ncid, varid, var, start, count_new))
	end subroutine

	subroutine nc_get_var_3d_real(ncid, name, var, start, count)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:, :, :), allocatable, intent(out) :: var
		integer, dimension(:), intent(in), optional :: start, count

		integer, dimension(:), allocatable :: dims
		integer :: varid
		integer, dimension(3) :: count_new

		call nc_inq_var(ncid, name, varid, dims)
		count_new = nc_count(dims, start, count)
		allocate(var(count_new(1), count_new(2), count_new(3)))
		call nc_check(nf90_get_var(ncid, varid, var))
	end subroutine

	subroutine nc_get_var_4d_real(ncid, name, var, start, count)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:, :, :, :), allocatable, intent(out) :: var
		integer, dimension(:), intent(in), optional :: start, count

		integer, dimension(:), allocatable :: dims
		integer :: varid
		integer, dimension(4) :: count_new

		call nc_inq_var(ncid, name, varid, dims)
		count_new = nc_count(dims, start, count)
		allocate(var(count_new(1), count_new(2), count_new(3), count_new(4)))
		call nc_check(nf90_get_var(ncid, varid, var, start, count_new))
	end subroutine

	subroutine nc_def_var(ncid, name, xtype, dims, varid)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		integer, dimension(:), intent(in) :: dims
		integer, intent(in) :: xtype
		integer, intent(out) :: varid

		character(len=NF90_MAX_NAME) :: dimname
		integer :: status
		integer :: i
		integer, dimension(:), allocatable :: dimids

		allocate(dimids(size(dims)))
		status = nf90_redef(ncid)
		do i = 1, size(dims)
			write(dimname, "(I32)") i
			call nc_check(nf90_def_dim( &
				ncid, &
				name // '_' // adjustl(dimname), &
				dims(i), &
				dimids(i) &
			))
		end do
		call nc_check(nf90_def_var( &
			ncid, &
			name, &
			xtype, &
			dimids, &
			varid &
		))
		call nc_check(nf90_enddef(ncid))
	end subroutine

	subroutine nc_put_var_1d_real(ncid, name, var, dimids)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:), intent(in) :: var
		integer, dimension(1), intent(in), optional :: dimids

		integer :: varid
		character(len=NF90_MAX_NAME) :: dimname
		integer, dimension(1) :: xdimids
		integer :: status

		status = nf90_redef(ncid)
		if (present(dimids)) then
			xdimids = dimids
		else
			write(dimname, "(A,'_',I0)") name, 1
			call nc_check(nf90_def_dim( &
				ncid, &
				dimname, &
				size(var), &
				xdimids(1) &
			))
		end if
		call nc_def_var(ncid, name, nf90_double, xdimids, varid)
		call nc_check(nf90_put_var(ncid, varid, var))
	end subroutine

	subroutine nc_put_var_2d_real(ncid, name, var, dimids)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:, :), intent(in) :: var
		integer, dimension(2), intent(in), optional :: dimids

		character(len=NF90_MAX_NAME) :: dimname
		integer, dimension(2) :: xdimids
		integer :: varid
		integer :: i
		integer :: status

		status = nf90_redef(ncid)
		if (present(dimids)) then
			xdimids = dimids
		else
			do i = 1, 2
				write(dimname, "(A,'_',I0)") name, i
				call nc_check(nf90_def_dim( &
					ncid, &
					dimname, &
					size(var, i), &
					xdimids(i) &
				))
			end do
		end if
		call nc_check(nf90_def_var( &
			ncid, &
			name, &
			nf90_double, &
			xdimids, &
			varid &
		))
		call nc_check(nf90_enddef(ncid))
		call nc_check(nf90_put_var(ncid, varid, var))
	end subroutine

	subroutine nc_put_var_3d_real(ncid, name, var, dimids)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:, :, :), intent(in) :: var
		integer, dimension(3), intent(in), optional :: dimids

		character(len=NF90_MAX_NAME) :: dimname
		integer, dimension(3) :: xdimids
		integer :: varid
		integer :: i
		integer :: status

		status = nf90_redef(ncid)
		if (present(dimids)) then
			xdimids = dimids
		else
			do i = 1, 3
				write(dimname, "(A,'_',I0)") name, i
				call nc_check(nf90_def_dim( &
					ncid, &
					dimname, &
					size(var, i), &
					xdimids(i) &
				))
			end do
		end if
		call nc_check(nf90_def_var( &
			ncid, &
			name, &
			nf90_double, &
			xdimids, &
			varid &
		))
		call nc_check(nf90_enddef(ncid))
		call nc_check(nf90_put_var(ncid, varid, var))
	end subroutine

	subroutine nc_put_var_4d_real(ncid, name, var, dimids)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: name
		real(8), dimension(:,:,:,:), intent(in) :: var
		integer, dimension(4), intent(in), optional :: dimids

		character(len=NF90_MAX_NAME) :: dimname
		integer, dimension(4) :: xdimids
		integer :: varid
		integer :: i
		integer :: status

		status = nf90_redef(ncid)
		if (present(dimids)) then
			xdimids = dimids
		else
			do i = 1, 4
				write(dimname, "(A,'_',I0)") name, i
				call nc_check(nf90_def_dim( &
					ncid, &
					dimname, &
					size(var, i), &
					xdimids(i) &
				))
			end do
		end if
		call nc_check(nf90_def_var( &
			ncid, &
			name, &
			nf90_double, &
			xdimids, &
			varid &
		))
		call nc_check(nf90_enddef(ncid))
		call nc_check(nf90_put_var(ncid, varid, var))
	end subroutine

	subroutine nc_get_att(ncid, varname, name, att)
		integer, intent(in) :: ncid
		character(len=*), intent(in) :: varname
		character(len=*), intent(in) :: name
		character(len=:), allocatable, intent(out) :: att

		integer :: varid
		integer, dimension(:), allocatable :: dims
		integer :: len

		call nc_inq_var(ncid, varname, varid, dims)
		call nc_check(nf90_inquire_attribute(ncid, varid, name, len=len))
		allocate(character(len=len) :: att)
		call nc_check(nf90_get_att(ncid, varid, name, att))
	end subroutine
end module
