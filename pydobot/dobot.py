import struct
import threading
import time
import serial

from pydobot.message import Message

class Dobot(threading.Thread):
    on = True
    x = 0.0
    y = 0.0
    z = 0.0
    r = 0.0
    j1 = 0.0
    j2 = 0.0
    j3 = 0.0
    j4 = 0.0

    def __init__(self, port, verbose=True):
        threading.Thread.__init__(self)
        self.verbose = verbose
        self.lock = threading.Lock()
        self.ser = serial.Serial(port,
                                 baudrate=115200,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)
        is_open = self.ser.isOpen()
        # if self.verbose:
            # print('pydobot: %s open' % self.ser.name if is_open else 'failed to open serial port')
        self._set_home_params(x=250, y=0, z=50, r=0)
        self.start()

    def run(self):
        listj = self._get_pose()
        type(listj[1])
        return listj

    def close(self):
        self.on = False
        self.lock.acquire()
        self.ser.close()
        if self.verbose:
            print('pydobot: %s closed' % self.ser.name)
        self.lock.release()

    def _send_command(self, msg):
        self.lock.acquire()
        self._send_message(msg)
        response = self._read_message()
        self.lock.release()
        return response

    def _send_message(self, msg):
        time.sleep(0.1)
        # if self.verbose:
        #     print('pydobot: >>', msg)
        self.ser.write(msg.bytes())

    def _read_message(self):
        time.sleep(0.1)
        b = self.ser.read_all()
        if len(b) > 0:
            msg = Message(b)
            # if self.verbose:
            #     print('pydobot: <<', msg)
            return msg
        return

    def _get_pose(self):
        msg = Message()
        msg.id = 10
        response = self._send_command(msg)
        self.x = struct.unpack_from('f', response.params, 0)[0]
        self.y = struct.unpack_from('f', response.params, 4)[0]
        self.z = struct.unpack_from('f', response.params, 8)[0]
        self.r = struct.unpack_from('f', response.params, 12)[0]
        self.j1 = struct.unpack_from('f', response.params, 16)[0]
        self.j2 = struct.unpack_from('f', response.params, 20)[0]
        self.j3 = struct.unpack_from('f', response.params, 24)[0]
        self.j4 = struct.unpack_from('f', response.params, 28)[0]

        self.xn = '{:03.1f}'.format(self.x)
        self.yn = '{:03.1f}'.format(self.y)
        self.zn = '{:03.1f}'.format(self.z)
        self.rn = '{:03.1f}'.format(self.r)
        self.j1n = '{:03.1f}'.format(self.j1)
        self.j2n = '{:03.1f}'.format(self.j2)
        self.j3n = '{:03.1f}'.format(self.j3)
        self.j4n = '{:03.1f}'.format(self.j4)
        
        joint = ['0',self.j1n,self.j2n,self.j3n,self.j4n,self.xn,self.yn,self.zn,self.rn] 
        return joint

    def _set_end_effector_suction_cup(self, suck=False):
        msg = Message()
        msg.id = 62
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([0x01]))
        if suck is True:
            msg.params.extend(bytearray([0x01]))
        else:
            msg.params.extend(bytearray([0x00]))
        return self._send_command(msg)

    #HOME FUNCTION    
    def _set_home_params(self, x, y, z, r):
        msg = Message()
        msg.id = 30
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', x)))
        msg.params.extend(bytearray(struct.pack('f', y)))
        msg.params.extend(bytearray(struct.pack('f', z)))
        msg.params.extend(bytearray(struct.pack('f', r)))
        return self._send_command(msg)
        
    def _set_home_cmd(self, temp):
        msg = Message()
        msg.id = 31
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('i', temp)))
        return self._send_command(msg)

    def suck(self, suck):
        self._set_end_effector_suction_cup(suck)

    def home(self, status):
        if status==True:
            temp=1
            self._set_home_cmd(temp)
        else:
            print("HOMING FUNCTION NOT ACTIVED")

    def start(self):
        msg = Message()
        msg.id = 240
        msg.ctrl = 0x01
        return self._send_command(msg)

    def stop(self):
        msg = Message()
        msg.id = 241
        msg.ctrl = 0x01
        return self._send_command(msg)

    def force(self):
        msg = Message()
        msg.id = 242
        msg.ctrl = 0x01
        return self._send_command(msg)    
    
    def clear(self):
        msg = Message()
        msg.id = 245
        msg.ctrl = 0x01
        return self._send_command(msg)
    
    def index(self):
        msg = Message()
        msg.id = 246
        msg.ctrl = 0x00
        self.i = struct.unpack_from('i', response.params, 0)[0]
        return self._send_command(msg)
        if self.verbose:
            print("index: %i" %(self.i))
            
            
