import serial


def read_weight():
    bal = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
                        )
    bal.reset_output_buffer()
    response = bal.read_until('\r\n')
    bal.reset_output_buffer()
    bal.close()
    return response


if __name__ == '__main__':

    i = 0

    while i < 3:
        i = i + 1
        print(read_weight())

