import math

vjoy_device_id = 0

def stick_to_pedal(stick_value):
    """Convert stick value (-1 to 1) to pedal value (0 to 1)."""
    return (stick_value + 1) / 2

def stick_to_wheel(stick_value):
    """Convert stick value (-1 to 1) to wheel value (-16384 to 16384)."""
    return int(stick_value * 16384)

def update():
    # Replace these with actual Xbox 360 controller input reading functions
    left_stick_x = filters.deadband(0.05, xbox360[0].leftStickX)
    left_trigger = xbox360[0].LT  # Left trigger value (0 to 1)
    right_trigger = xbox360[0].RT  # Right trigger value (0 to 1)
    
    # Convert inputs to vJoy values
    wheel_value = stick_to_wheel(left_stick_x)
    vJoy[vjoy_device_id].x = wheel_value
    
    # Map the brake to the y-axis
    brake_value = stick_to_pedal(left_trigger)
    vJoy[vjoy_device_id].y = int(brake_value * 32768)  # Using y-axis for brake
    
    # Map the throttle to the z-axis
    throttle_value = stick_to_pedal(right_trigger)
    vJoy[vjoy_device_id].z = int(throttle_value * 32768)  # Using z-axis for throttle

if starting:
    vJoy[vjoy_device_id].x = 0
    vJoy[vjoy_device_id].y = 0  # Initialize brake axis
    vJoy[vjoy_device_id].z = 0  # Initialize throttle axis

diagnostics.watch(vJoy[vjoy_device_id].x)
diagnostics.watch(vJoy[vjoy_device_id].y)  # Watch brake axis
diagnostics.watch(vJoy[vjoy_device_id].z)  # Watch throttle axis
