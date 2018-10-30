import serial


def read_weight(socket):
    # bal = serial.Serial(port='/dev/ttyUSB0',
    #                     baudrate=9600,
    #                     parity=serial.PARITY_NONE,
    #                     stopbits=serial.STOPBITS_ONE,
    #                     bytesize=serial.EIGHTBITS
    #                     )
    socket.reset_output_buffer()
    print('On attend que la balance envoie le poids')
    response = socket.read_until('\r\n')
    socket.reset_output_buffer()
    #bal.close()
    return response


if __name__ == '__main__':

    ser = serial.Serial(port='/dev/ttyUSB0',
                         baudrate=9600,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS
                        )
    if not ser.isOpen():
        ser.open()

    try:
        while True:
            print(read_weight(ser))
    except KeyboardInterrupt:
        ser.close()
        pass





    # i = 0
    #
    # while i < 3:
    #     i = i + 1
    #     print(read_weight())

