import math

vjoy_device_id = 0

def stick_to_pedal(stick_value):
    return (stick_value + 1) / 2

def stick_to_wheel(stick_value):
    return int(stick_value * 16384)

def update():
    left_stick_x = filters.deadband(0.05, ds4[0].leftStickX)
    left_trigger = ds4[0].L2
    right_trigger = ds4[0].R2
    
    wheel_value = stick_to_wheel(left_stick_x)
    vJoy[vjoy_device_id].x = wheel_value

    brake_value = stick_to_pedal(left_trigger)
    vJoy[vjoy_device_id].rz = int(brake_value * 32768)
    
    throttle_value = stick_to_pedal(right_trigger)
    vJoy[vjoy_device_id].z = int(throttle_value * 32768)

if starting:
    vJoy[vjoy_device_id].x = 0
    vJoy[vjoy_device_id].rz = 0
    vJoy[vjoy_device_id].z = 0

diagnostics.watch(vJoy[vjoy_device_id].x)
diagnostics.watch(vJoy[vjoy_device_id].rz)
diagnostics.watch(vJoy[vjoy_device_id].z)