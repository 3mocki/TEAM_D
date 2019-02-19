import threading
import math
from neo import Gpio


class Reader:
    # S0,S1,S2,S3
    selector_pins = [16, 17, 18, 19]

    # Number of connected to MUX Board
    mux_channel = {
        'temp1': 1,
        'no2': {'we': 2, 'ae': 3},
        'o3': {'we': 4, 'ae': 5},
        'co': {'we': 6, 'ae': 7},
        'so2': {'we': 8, 'ae': 9},
        'pm2_5': 10,
    }

    # Refer to Calibration Certificates
    calibration = {
        'no2': {
            'n': [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00],
            'we_zero': 215,
            'ae_zero': 246,
            'sensitivity': 0.258
        },
        'o3': {
            'n': [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18],
            'we_zero': 390,
            'ae_zero': 393,
            'sensitivity': 0.379
        },
        'co': {
            'n': [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48],
            'we_zero': 326,
            'ae_zero': 280,
            'sensitivity': 0.333
        },
        'so2': {
            'n': [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75],
            'we_zero': 380,
            'ae_zero': 306,
            'sensitivity': 0.371
        }
    }

    def __init__(self):

        self.lock = threading.Lock()
        self.gpio = Gpio()

        # init to LOW
        self.lock.acquire()
        for pin in Reader.selector_pins:
            self.gpio.pinMode(pin, self.gpio.OUTPUT)
            self.gpio.digitalWrite(pin, self.gpio.LOW)
        self.lock.release()

    # Read NO2, SO2, O3, CO, PM2.5, TEMP
    def read_no2(self):  # Had a problem on sensors
        return round(self.__calibrate('no2') * 1000, 2)

    def read_o3(self):
        o3 = round(self.__calibrate('o3') * 100, 2)  # Had a problem on sensors
        if o3 < 0:
            return 0
        else:
            return o3

    def read_co(self):
        return round(self.__calibrate('co'), 2)

    def read_so2(self):
        return round(self.__calibrate('so2') * 1000, 2)  # Had a problem on sensors

    def read_temp(self):
        mV = self.__read_adc(Reader.mux_channel['temp1'])
        temp = (mV - 500) / 10  # Celcius Value
        ftemp = (temp * 1.8) + 32  # Celcius to Fahrenheit
        return round(ftemp - 30, 2)

    def read_pm(self):
        mV = self.__read_adc(Reader.mux_channel['pm2_5'])
        v = mV / 1000

        hppcf = 240 * (v ** 6) - 2491.3 * (v ** 5) + 9448.7 * (v ** 4) - 14840 * (v ** 3) + 10684 * (
                    v ** 2) + 2211.8 * v + 7.9623
        ugm3 = .518 + .00274 * hppcf
        return round(ugm3, 2)

    def __read_adc(self, channel):
        s_bin = self.__dec_to_bin(channel)

        self.lock.acquire()

        # write
        for i in range(4):
            self.gpio.digitalWrite(Reader.selector_pins[i], s_bin[i])

        # read
        raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
        scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

        self.lock.release()

        return raw * scale

    def __calibrate(self, name):

        we = self.__read_adc(Reader.mux_channel[name]['we'])
        ae = self.__read_adc(Reader.mux_channel[name]['ae'])

        # Fahrenheit to Celcius ; There is a probelm if your Faherenheit temperature value is over 60
        temperature = (self.read_temp() - 32) / 1.8
        calibration = Reader.calibration[name]
        we = we - calibration['we_zero']
        ae = ae - calibration['ae_zero']
        temp = int(temperature / 10) + 3
        if temp > 7:
            temp = 7
        ae = (calibration['n'][temp]) * ae
        we = (we - ae) / calibration['sensitivity']
        if we / 1000 > 0:
            return we / 1000
        else:
            return 0

    def __dec_to_bin(self, n):
        num = [0, 0, 0, 0]

        if n == 0:
            return num
        else:
            for x in range(n):
                t = x + 1
                for y in range(4):
                    num[y] = t % 2
                    t = t / 2
            return num