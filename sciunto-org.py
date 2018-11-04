# Parameters for the Mettler Toledo XS105 scale:
# 9600
# 8/No
# 1 stopbit
# Xon/Xoff
# <CR><LF>
# Ansi/win
# Off

import serial
import time
import re


def read_weight(socket, timelapse=1):
    """
    Returns the weight in gram and the stability.

    :param socket: serial socket
    :param timelapse: timelapse between each measurement
    :returns: tuple (weight, stability)
    """
    ser.write(b'\nSI\n')
    time.sleep(1)
    #TODO check inWaiting length
    value = ser.read(ser.inWaiting())
    value = value.decode('utf-8')
    value = value.split('\n')[1][:-1]
    if value[3] == 'S':
        stability = True
    else:
        stability = False
    weight = value[4:-1].strip(' ')
    return (weight, stability)


if __name__ == '__main__':

    ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
    )

    if not ser.isOpen():
        ser.open()
    with open('data.dat', 'w') as fh:
        fh.write('# Time (s) | Weight (g) | Stability')
        zerotimer = time.time()  # perf_counter might be better py3
        try:
            while True:
                try:
                    weight, stability = read_weight(ser)
                    timer = time.time() - zerotimer
                    print('t = ' + str(timer) + 's | M = ' + str(weight) + ' g')
                    fh.write(str(timer) + ' ' + weight + ' ' + str(stability) +'\n')
                except IndexError:
                    time.sleep(1)
        except KeyboardInterrupt:
            fh.close()
            ser.close()