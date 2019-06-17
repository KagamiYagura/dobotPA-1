import struct
import threading
import time
import serial

from pydobot.message import Message
from pydobot.dobot import Dobot

MODE_PTP_JUMP_XYZ = 0x00
MODE_PTP_MOVJ_XYZ = 0x01
MODE_PTP_MOVL_XYZ = 0x02
MODE_PTP_JUMP_ANGLE = 0x03
MODE_PTP_MOVJ_ANGLE = 0x04
MODE_PTP_MOVL_ANGLE = 0x05
MODE_PTP_MOVJ_INC = 0x06
MODE_PTP_MOVL_INC = 0x07
MODE_PTP_MOVJ_XYZ_INC = 0x08
MODE_PTP_JUMP_MOVL_XYZ = 0x09


class PTP(Dobot):
    def __init__(self, port, verbose=True):
        Dobot.__init__(self, port, verbose=True)
        self._set_ptp_coordinate_params(velocity=200.0, acceleration=200.0)
        self._set_ptp_common_params(velocity=70.0, acceleration=70.0)       

    def _set_ptp_coordinate_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 81
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)

    def _set_ptp_common_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 83
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)

    def _set_ptp_cmd(self, x, y, z, r, mode):
        msg = Message()
        msg.id = 84
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([mode]))
        msg.params.extend(bytearray(struct.pack('f', x)))
        msg.params.extend(bytearray(struct.pack('f', y)))
        msg.params.extend(bytearray(struct.pack('f', z)))
        msg.params.extend(bytearray(struct.pack('f', r)))
        return self._send_command(msg)

    def SPEED(self, velocity, acceleration):
        self._set_ptp_common_params(velocity, acceleration)
        self._set_ptp_coordinate_params(velocity, acceleration)
    
    def JUMP_XYZ(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_JUMP_XYZ)

    def MOVJ_XYZ(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVJ_XYZ)
    
    def MOVL_XYZ(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVL_XYZ)
    
    def JUMP_ANGLE(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_JUMP_ANGLE)

    def MOVJ_ANGLE(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVJ_ANGLE)

    def MOVL_ANGLE(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVL_ANGLE)

    def MOVJ_INC(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVJ_INC)

    def MOVL_INC(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVL_INC)
    
    def MOVJ_XYZ_INC(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_MOVJ_INC)
    
    def JUMP_MOVL_XYZ(self, x, y, z, r=0.):
        self._set_ptp_cmd(x, y, z, r, mode=MODE_PTP_JUMP_MOVL_XYZ)
