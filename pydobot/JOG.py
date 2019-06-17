import struct
import time
import serial

from pydobot.dobot import Dobot
from pydobot.message import Message

##--------------DEFINISI GERAK JOG--------------##
IDLE    = 0x00
AP_DOWN = 0x01
AN_DOWN = 0x02
BP_DOWN = 0x03
BN_DOWN = 0x04
CP_DOWN = 0x05
CN_DOWN = 0x06
DP_DOWN = 0x07
DN_DOWN = 0x08

class JOG(Dobot):
    def __init__(self, port, verbose=True):
        Dobot.__init__(self, port, verbose=True)

##--------------FUNGSI SETTING VELOCITY--------------##     
    def _set_jog_coordinate_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 71
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)
    
    def _set_jog_common_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 72
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)        

##--------------FUNGSI EKSEKUSI JOG--------------##
    def _set_jog_cmd(self, isJoint, cmd):
        msg = Message()
        msg.id = 73
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([isJoint]))
        msg.params.extend(bytearray(struct.pack('i', cmd)))
        return self._send_command(msg)

##--------------EXECUTING IDLE/DIAM on JOG--------------##
    def idle(self):
        self._set_jog_cmd(isJoint=1, cmd=IDLE)

##--------------EXECUTING CARTESIAN JOG---------------##
    def xplus(self):
        self._set_jog_cmd(isJoint=0, cmd=AP_DOWN)
    
    def xmin(self):
        self._set_jog_cmd(isJoint=0, cmd=AN_DOWN)
    
    def yplus(self):
        self._set_jog_cmd(isJoint=0, cmd=BP_DOWN)

    def ymin(self):
        self._set_jog_cmd(isJoint=0, cmd=BN_DOWN)

    def zplus(self):
        self._set_jog_cmd(isJoint=0, cmd=CP_DOWN)

    def zmin(self):
        self._set_jog_cmd(isJoint=0, cmd=CN_DOWN)
    
    def rplus(self):
        self._set_jog_cmd(isJoint=0, cmd=DP_DOWN)

    def rmin(self):
        self._set_jog_cmd(isJoint=0, cmd=DN_DOWN)

##--------------EXECUTING SPEED---------------##
    def jspeed(self, velocity=100., acceleration=100.):
        self._set_jog_common_params(velocity,acceleration)
        self._set_jog_coordinate_params(velocity,acceleration)

##--------------EXECUTING JOINT---------------##
    def joint1pos(self):
        self._set_jog_cmd(isJoint=1, cmd=AP_DOWN)
        print("Joint 1+")
    
    def joint1min(self):
        self._set_jog_cmd(isJoint=1, cmd=AN_DOWN)
        print("Joint 1-")
    
    def joint2pos(self):
        self._set_jog_cmd(isJoint=1, cmd=BP_DOWN)
        print("Joint 2+")
    
    def joint2min(self):
        self._set_jog_cmd(isJoint=1, cmd=BN_DOWN)
        print("Joint 2-")

    def joint3pos(self):
        self._set_jog_cmd(isJoint=1, cmd=CP_DOWN)
        print("Joint 3+")
    
    def joint3min(self):
        self._set_jog_cmd(isJoint=1, cmd=CN_DOWN)
        print("Joint 3-")
    
    def joint4pos(self):
        self._set_jog_cmd(isJoint=1, cmd=DP_DOWN)
        print("Joint 4+")
    
    def joint4min(self):
        self._set_jog_cmd(isJoint=1, cmd=DN_DOWN)
        print("Joint 4-")
