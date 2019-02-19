def adc():
	raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
	scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

	return raw*scale
