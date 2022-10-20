## Calibration

Depending on the instrument, calibration in the ALCF may be an essential part of
processing ALC data. Ceilometers often report backscatter values in arbitrary
units which need to be converted to m<sup>-1</sup>.sr<sup>-1</sup> for a
reliable comparison with the COSP simulator. The recommended calibration method
in the ALCF is [O'Connor et al. (2004)](https://journals.ametsoc.org/doi/abs/10.1175/1520-0426(2004)021%3C0777%3AATFAOC%3E2.0.CO%3B2).
The method is based on the fact that the lidar ratio in fully opaque liquid
stratocumulus profiles is approximately constant, depending only on the
wavelength of the lidar, assuming the cloud droplet size of the stratocumulus
cloud is within a certain typical range.

The calibration steps are outlined below:

1. Process and plot backscatter profiles with the lidar ratio, assuming the
default calibration coefficient.

	`alcf auto lidar <type> <input> <output> --lr`

2. Identify time periods with stratocumulus cloud.

	Go through the backscatter profile plots in `<output>/plot/backscatter/`
	and note the time periods with stratocumulus cloud in a text file
	`calibration_time_periods.txt` in the format:

	```
	<start> <end>
	<start> <end>
	...
	```

	where `start` and `end` are in the format `YYYY-MM-DDTHH:MM`.
	Avoid profiles with multiple layers or cloud close to the surface.
	See [O'Connor et al. (2014)](https://journals.ametsoc.org/doi/abs/10.1175/1520-0426(2004)021%3C0777%3AATFAOC%3E2.0.CO%3B2)
	or [Hopkin et al. (2019)](https://www.atmos-meas-tech.net/12/4131/2019/) for more
	information.

	Figure 1 shows an example of a stratocumulus cloud in the time period:

	```
	2018-02-18T13:00 2018-02-18T15:00
	```

	<figure><a href="2018-02-18T000000.png"><img src="2018-02-18T000000.png" width="600" /></a><br /><strong>Figure 1:</strong> Stratocumulus layer between 13:00 and 15:00 UTC suitable for calibration.</figure>

3. Run `alcf calibrate` with a file listing the time periods to calculate
the calibration coefficient.

	`alcf calibrate <type> <input> calibration.txt calibration_time_periods.txt`

	The coefficient is saved in `calibration_time_periods.txt`.

4. Process and plot backscatter profiles with the calculated calibration
coefficient.

	`alcf auto lidar <type> <input> <output> --lr calibration_file: calibration.txt`

5. Check that the plotted lidar ratio in the stratocumulus profiles is
	approximatly 18.8 sr.
