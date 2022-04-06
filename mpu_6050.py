from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    acel_data = mpu.get_accel_data()
    print("Acc X : "+str(round(acel_data['x'],3)))
    print("Acc Y : "+str(round(acel_data['y'],3)))
    print("Acc Z : "+str(round(acel_data['z'],3)))
    print()

    gyro_data = mpu.get_gyro_data()
    print("Gyro X : "+str(round(gyro_data['x'],3)))
    print("Gyro Y : "+str(round(gyro_data['y'],3)))
    print("Gyro Z : "+str(round(gyro_data['z'],3)))
    print()
    print("-------------------------------")
    time.sleep(1)

