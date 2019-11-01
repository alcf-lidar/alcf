COSP_PATH := build/COSPv1-master
INCLUDEPATH := build/opt/include
LIBPATH := build/opt/lib

LIBS := $(LIBPATH)/libcmor.a -lnetcdff -lnetcdf -ludunits2 -luuid

FC := gfortran -fPIC -ffree-line-length-512 -Isrc -I$(COSP_PATH) -I$(INCLUDEPATH) -L$(LIBPATH)

COSP_OBJ_FILES := cosp_radar.o cosp_types.o cosp_constants.o cosp_simulator.o \
        cosp_utils.o scops.o prec_scops.o cosp.o cosp_stats.o \
        pf_to_mr.o \
        cosp_lidar.o radar_simulator_types.o zeff.o \
        array_lib.o atmos_lib.o dsd.o calc_Re.o format_input.o \
        gases.o scale_LUTs_io.o radar_simulator_init.o \
        math_lib.o mrgrnk.o optics_lib.o radar_simulator.o \
        lidar_simulator.o cosp_io.o llnl_stats.o lmd_ipsl_stats.o \
        cosp_isccp_simulator.o icarus.o \
        cosp_misr_simulator.o MISR_simulator.o \
        cosp_modis_simulator.o modis_simulator.o \
        cosp_rttov_simulator.o

COSP_OBJS := $(foreach obj,$(COSP_OBJ_FILES),$(COSP_PATH)/$(obj))

OBJS := src/cosp_run.o src/nc_utils.o $(COSP_OBJS)

TARGETS := alcf/opt/bin/cosp_alcf

all: $(TARGETS)

alcf/opt/bin/cosp_alcf: src/main.o $(OBJS)
	$(FC) -o $@ $^ $(LIBS)

src/main.o: src/main.f03 src/nc_utils.o src/cosp_run.o

%.o: %.f03
	$(FC) -c -o $@ $<

.PHONY: clean
clean:
	rm -rf src/*.o src/*.mod $(TARGETS)
