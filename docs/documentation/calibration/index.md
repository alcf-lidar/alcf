---
title: Calibration
layout: default
---

### [Documentation](../)
## Calibration

Depending on the instrument, calibration in ALCF may be an essential part of
processing ALC data. Ceilometers often report backscatter values in
"arbitrary units" which need to be converted to m^-1.sr^-1 for a reliable
comparison with the COSP simulator. The recommended calibration method of
calibration in ALCF is [O'Connor et al. (2004)](https://journals.ametsoc.org/doi/abs/10.1175/1520-0426(2004)021%3C0777%3AATFAOC%3E2.0.CO%3B2) for its universality.
The method is based on the fact that the lidar ratio of fully opaque
stratocumulus scenes tends to a constant.

1. Plot daily uncalibrated ALC data by:

        alcf lidar <type> <raw-dir> <lidar-dir>
        alcf plot lidar --lr <lidar-dir> <plot-dir>

2. Identify visually sections of the plots which contain fully attenuating
stratocumulus clouds, and note their time intervals.

TODO:

3. Supply the time intervals to alcf calibrate:

        alcf calibrate { <start> <end> }...

    where `<start>` and `<end>` are the start time and end time of each interval
    in the ISO format (`<year>-<month>-<day>T<hour>:<minute>`). The command
    will output the calibration coefficient to be used with the `alcf lidar`
    command:

        alcf lidar <type> --calibration_coeff: <coeff> <input> <output>

    where `<coeff>` is the calibration coefficient.
