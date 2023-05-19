import serial
import struct

def parse_data(data):
    # 解析數據
    distance = struct.unpack('>H', bytes(data[0:2]))[0]
    if distance > 32767: # 將大於32767的數據轉換為負數
        distance -= 65536
    x = struct.unpack('>H', bytes(data[2:4]))[0]
    if x > 32767: # 將大於32767的數據轉換為負數
        x -= 65536
    y = struct.unpack('>H', bytes(data[4:6]))[0]
    if y > 32767: # 將大於32767的數據轉換為負數
        y -= 65536
    return distance, x, y



def check_sum(data):
    # 计算并检查校验和
    #print("check_sum",data[:-1])
    checksum = sum(data[:-1]) % 256
    #print("Ans",checksum)

    return checksum 


def read_from_port(port):
    with serial.Serial(port, baudrate=115200, timeout=1) as ser:
        data = []
        while True:
            byte = ser.read(1)
            if byte == b'\x53':
                next_byte = ser.read(1)
                if next_byte == b'\x59':
                    print("Start frame detected")
                    data = [0x53, 0x59]
                    continue
                    
            data.append(ord(byte))
            #print(f"Received byte: {ord(byte):02x}")
            #print("data",data)
            #print("data:", [hex(d) for d in data])
            if len(data) == 14:
                #if data[-2:] == [0x53, 0x43] and check_sum(data[:-2]):
                if data[-2:] == [84,67] and check_sum(data[:-2])==data[-3]:
                    print("End frame detected, checksum passed")
                    #print(data[5:11])
                    print("data:", [hex(d) for d in data])
                    distance, x, y = parse_data(data[5:11])
                    print(f'Distance: {distance} cm, X: {x} cm, Y: {y} cm')
                else:
                    #print(data[-2:])
                    print("End frame detected, checksum failed")
                data = []

if __name__ == "__main__":
    # 用您的串口替換'/dev/cu.usbserial-1442210'
    read_from_port('/dev/cu.usbserial-1442210')