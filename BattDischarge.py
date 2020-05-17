import u3


class BattDischarge:
    def __init__(self, channels, ser_num=None):
        self.channel = []
        for i, dic in enumerate(channels):
            self.channel[i] = {
                'adc': dic['adc_in'], 'load_en': dic['load_enable'], 'load': dic['load_ohms']
            }
        self.d = u3.U3(debug=True)
        self.d.open(serial=ser_num)
        # make sure there is an extender attached; need to use special mode ADC if LV model
        self.d.configU3(FIOAnalog=0xFF, EIODirection=0xFF, EIOState=0x00)

    def _ctrl_load(self, chan, level):
        if chan < len(self.channel):
            self.d.setDOState(self.channel[chan].get('load_en'), level)
        else:
            print("unable to affect load for channel {}".format(chan))

    def enable_load(self, chan):
        self._ctrl_load(chan, 0)

    def disable_load(self, chan):
        self._ctrl_load(chan, 1)

    def disable_all_loads(self):
        for dic in self.channel:
            self.d.setDOState(dic['load_en'], 0)

    def measure_channel(self, chan, avgs=0, msec_delay=50):
        if chan < len(self.channel):
            v = self.d.getAIN(self.channel[chan].get('adc'))
            i = v / self.channel[chan].get('load')
            return v, i
        else:
            return 0, 0


if __name__ == '___main__':
    c = [
        {'adc_in': 0, 'load_enable': 8, 'load_ohms': 751},
        {'adc_in': 1, 'load_enable': 9, 'load_ohms': 744},
        {'adc_in': 2, "load_enable": 10, 'load_ohms': 751}
    ]
    bd = BattDischarge(c)
    print(bd)
    bd.disable_all_loads()
    for idx in range(len(c)):
        volts, current = bd.measure_channel(idx)
        print('chan {}: v={} i={}'.format(idx, volts, current))

