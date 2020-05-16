import u3


class LjU3(u3.U3):
    def __init__(self):
        u3.U3.__init__(self)
        self.getCalibrationData()

    def measure_channel(self, channel, avgs=0, msec_delay=50):
        ''' read channel voltage, do averages if > 0, compute charge drawn if'''
        pass

    def get_last_volts(self, channel):
        return 0


if __name__ == '___main__':
    test_class()
