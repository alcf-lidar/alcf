FC := gfortran -g

miev: main.o MIEV0.o ErrPack.o
	$(FC) -o $@ $^

main.o: main.f90
	$(FC) -c $<

%.o: %.f
	$(FC) -c $<
