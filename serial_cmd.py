import serial
import serial.tools.list_ports as list_ports
import string, array

class Serial_cmd:

    Arduino_IDs = ((0x2341, 0x0043), (0x2341, 0x0001),
                   (0x2A03, 0x0043), (0x2341, 0x0243),
                   (0x0403, 0x6001), (0x1A86, 0x7523))

    def __init__(self, port = ''):
        if port == '':
            self.dev = None
            self.connected = False
            devices = list_ports.comports()
            for device in devices:
                if (device.vid, device.pid) in Serial_cmd.Arduino_IDs:
                    try:
                        self.dev = serial.Serial(device.device, 115200)
                        self.connected = True
                        print('Connected to {!s}...'.format(device.device))
                    except:
                        pass
                if self.connected:
                    break
        else:
            try:
                self.dev = serial.Serial(port, 115200)
                self.connected = True
            except:
                self.dev = None
                self.connected = False

    def write(self, command):
        if self.connected:
            self.dev.write('{!s}\r'.format(command).encode())

    def read(self):
        if self.connected:
            return self.dev.readline().decode()

    def get_rSensor(self):
        if self.connected:
            self.write('RSENSOR?')
            return int(self.read(), 16)

    def get_lSensor(self):
        if self.connected:
            self.write('LSENSOR?')
            return int(self.read(), 16)

    def set_rMotor(self, val):
        if self.connected:
            self.write('RMOTOR!{:X}'.format(int(val)))

    def set_lMotor(self, val):
        if self.connected:
            self.write('LMOTOR!{:X}'.format(int(val)))
