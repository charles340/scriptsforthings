import math

# Configuration parameters
HANDBRAKE_CLUTCH_LINK = 1
STEER_INPUT_SPEED_MIN = 0.035
STEER_INPUT_SPEED_MAX = 0.035
STEER_INPUT_VELOCITY_THRESHOLD = 40
STEER_POWER = 0.5
FFB_POWER = 0.004
PHYSICS_VELOCITY_THRESHOLD = 5
UNDERSTEER_TOLERANCE_MIN = 0.9
UNDERSTEER_TOLERANCE_MAX = 0.4
UNDERSTEER_TOLERANCE_VELOCITY_THRESHOLD = 100
MAX_ANGULAR_VELOCITY = 3
STEER_INFLUENCE_AT_SLIP_ANGLE = 0
STEER_INFLUENCE_AT_ANGULAR_VELOCITY = 1
HOLD_POWER = 0.150
CENTER_STABILITY = 0.1

steerInputPrevious = 0
steerMainPrevious = 0

def r360(r):
    m = math.pi * 2
    v = abs(r)
    sg = math.copysign(1, r)
    n = int(v // m)
    r = v - (n * m)
    if sg < 0:
        r = m - r
    return r

def rDiff(a, b):
    pi2 = math.pi * 2
    v1, v2 = (b - a, a + (pi2 - b)) if a < b else (b + (pi2 - a), a - b)
    return v1 if abs(v1) < abs(v2) else -abs(v2)

def lerp(a, b, t):
    return (1 - t) * a + t * b

def inverseLerp(t, a, b):
    return (t - a) / (b - a)

def remap(value, minFrom, maxFrom, minTo, maxTo):
    return lerp(minTo, maxTo, inverseLerp(value, minFrom, maxFrom))

def clamp(value, min, max):
    return max if value > max else min if value < min else value

def clamp01(value):
    return clamp(value, 0, 1)

def deadzone(value, deadzone):
    return math.copysign(max(abs(value) - deadzone, 0) / (1 - deadzone), value)

def linearity(value, linearity):
    return math.copysign(abs(value) ** linearity, value)

def update():
    global steerInputPrevious, steerMainPrevious

    # Replace `ds4` with the correct device name from the device recognition script
    state = ds4[0]
    
    localVelocityX = state.localVelocity.x
    localVelocityZ = state.localVelocity.z
    localAngularVelocityY = state.localAngularVelocity.y

    angularVelocityAbs = abs(localAngularVelocityY)
    angularVelocityFraction = clamp(angularVelocityAbs, 0, MAX_ANGULAR_VELOCITY) / MAX_ANGULAR_VELOCITY

    stickInput = state.stickX

    steerInput = deadzone(stickInput, state.steeringDeadzone)
    steerInput = linearity(steerInput, state.steeringGamma)

    steerInputSpeedFactor = clamp(abs(localVelocityZ), 0, STEER_INPUT_VELOCITY_THRESHOLD) / STEER_INPUT_VELOCITY_THRESHOLD
    steerInputDeltaMax = lerp(STEER_INPUT_SPEED_MIN, STEER_INPUT_SPEED_MAX, steerInputSpeedFactor)

    steerInputDelta = steerInput - steerInputPrevious
    steerInputDeltaNew = clamp(steerInputDelta, -steerInputDeltaMax, steerInputDeltaMax)

    steerInput = steerInputPrevious + steerInputDeltaNew
    steerInput = clamp(steerInput, -1, 1)
    steerInputPrevious = steerInput

    physicsSpeedFactor = clamp(abs(localVelocityZ), 0, PHYSICS_VELOCITY_THRESHOLD) / PHYSICS_VELOCITY_THRESHOLD
    driftR = math.atan2(localVelocityX, abs(localVelocityZ)) * physicsSpeedFactor

    slipAngle = -driftR * math.copysign(1, localVelocityZ)
    slipAngleAbs = abs(slipAngle)
    slipAngleFraction = 1 - clamp01(slipAngleAbs - 1) if slipAngleAbs > 1 else slipAngleAbs

    slipAngle = slipAngleFraction * math.copysign(1, slipAngle)
    slipAngle = lerp(slipAngle, slipAngle * (1 - clamp01(STEER_INFLUENCE_AT_SLIP_ANGLE)), slipAngleFraction)
    slipAngle = lerp(slipAngle, slipAngle * (1 - clamp01(STEER_INFLUENCE_AT_ANGULAR_VELOCITY)), angularVelocityFraction)

    understeerToleranceSpeedFactor = clamp(abs(localVelocityZ), 0, UNDERSTEER_TOLERANCE_VELOCITY_THRESHOLD) / UNDERSTEER_TOLERANCE_VELOCITY_THRESHOLD
    understeerTolerance = lerp(UNDERSTEER_TOLERANCE_MIN, UNDERSTEER_TOLERANCE_MAX, understeerToleranceSpeedFactor)
    understeerTolerance = clamp(understeerTolerance, -1, 1)

    slipAngleRto = lerp(1, understeerTolerance, steerInputSpeedFactor)
    inSlipAngle = steerInput * slipAngleRto

    diffR = (slipAngle + inSlipAngle)

    steerMainPreviousFraction = abs(steerMainPrevious)
    steerPower = lerp(1, STEER_POWER, steerInputSpeedFactor)
    steerForce = math.sin(diffR) * steerPower - (state.ffb * FFB_POWER)
    steerForce = lerp(steerForce, 0, steerMainPreviousFraction)

    steerMain = clamp(steerForce, -1, 1)
    state.steer = steerMain

    steerMainPrevious = steerMain

    if HANDBRAKE_CLUTCH_LINK != 0 and state.handbrake > 0:
        state.clutch = 1 - state.handbrake

if starting:
    centreX = 0.00
    centreY = 0.00
    sensX = 3.5
    sensY = -40.0
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 20
    x = 0
    y = 0
    moveLatch = False

if starting:
    update()
