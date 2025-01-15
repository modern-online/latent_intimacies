import smbus2 as smbus
import time 

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x53
POWER_CTL = 0x2D
DATAX0 = 0x32

bus.write_byte_data(DEVICE_ADDRESS, POWER_CTL, 0x08)
global prevY
prevY = 0

def read_raw_values():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, DATAX0, 6)
    #x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]

    #if x > 32767:
    #    x -= 65536
    if y > 32767:
        y -= 65536

    return y

def is_moving(nullify_sensor):
    # ADJUST THIS BASED ON REALITY
    global prevY
    y = abs(read_raw_values())
    print(f"accellerometer: {y}")
    difference = abs(y-prevY)
    print("y_difference: " + str(difference))
    if y > 30 or difference >= 10 and difference != y:
        prevY = y
        #print(abs(x))
        #print(abs(y))
        if not nullify_sensor:
        	return True
        else:
        	return False
    return False

#while True:
#    y = read_raw_values()
#    print(f"x: {x}, y: {y}")
#    #if is_moving(x , y):
#    #    print("moving!")
#    time.sleep(.5)
