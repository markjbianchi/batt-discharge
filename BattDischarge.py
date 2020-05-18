import u3


class BattDischarge:
    def __init__(self, chan, ser_num=None):
        try:
            u3.U3().close()
        except u3.LabJackException:
            print('caught LJ exception on close()')
        self.channels = []
        for dic in chan:
            self.channels.append({
                'adc_pin': dic['adc_in'], 'load_pin': dic['load_enable'],
                'load': dic['load_ohms'], 'enabled': False
            })
        self.dacq = u3.U3()
        #self.dacq.open(serial=ser_num)
        self.dacq.configU3(FIOAnalog=0xFF, EIODirection=0xFF, EIOState=0x00)
        self.dacq.configIO(FIOAnalog=0xFF, EIOAnalog=0)

    def _handle_led(self):
        # LED is on when any battery is being discharged
        any_enabled = False
        for dic in self.channels:
            if dic.get('enabled'):
                any_enabled = True
        self.dacq.getFeedback(u3.LED(State=any_enabled))

    def _ctrl_load(self, chan, level):
        self.dacq.setDOState(self.channels[chan].get('load_pin'), level)
        self.channels[chan].update({'enabled': bool(level)})
        self._handle_led()

    def close(self):
        self.dacq.close()

    def enable_load(self, chan):
        self._ctrl_load(chan, 1)

    def disable_load(self, chan):
        self._ctrl_load(chan, 0)

    def disable_all_loads(self):
        for i, dic in enumerate(self.channels):
            self.dacq.setDOState(dic['load_pin'], 0)
            self.channels[i].update({'enabled': False})
        self._handle_led()

    def measure_channel(self, chan):
        neg_chan = 31 if chan < 4 else 32
        v = self.dacq.getAIN(self.channels[chan].get('adc_pin'), negChannel=neg_chan)
        if self.channels[chan].get('enabled'):
            i = v / self.channels[chan].get('load')
        else:
            i = 0
        return v, i


if __name__ == '___main__':
    ch = [
        {'adc_in': 0, 'load_enable': 8, 'load_ohms': 751},
        {'adc_in': 1, 'load_enable': 9, 'load_ohms': 744},
        {'adc_in': 2, "load_enable": 10, 'load_ohms': 751}
    ]
    bd = BattDischarge(ch)
    print(bd)
    bd.disable_all_loads()
    for idx in range(len(ch)):
        volts, current = bd.measure_channel(idx)
        print('chan {}: v={:.3f} i={:.3f}'.format(idx, volts, current))
    bd.close()
