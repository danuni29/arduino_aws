import serial
import time

def main():
    ser = serial.Serial('COM3', 9600)
    time.sleep(2)
    while True:
        if ser.in_waiting != 0:
            data = ser.readline()
            print(data.decode()[:-2])
            time.sleep(1)



if __name__ == '__main__':
    main()