if starting:
	centreX = 0.00
	centreY = 0.00
	sensX = 3.5
	sensY = -40.0
	viewSensX = 10
	viewSensY = 10
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 1
	x = 0
	y = 0
	rx = 0
	ry = 0
	freelook = False
	viewLatch = False
	moveLatch = False

if mouse.deltaX:
	if freelook:
		rx += mouse.deltaX * viewSensX
	else:
		moveLatch = True
		x += mouse.deltaX * sensX
		if abs(x) > vJoy[0].axisMax:
			x = vJoy[0].axisMax * x / abs(x)
else:
	x /= (1.0 + centreX)

if mouse.deltaY:
	if freelook:
		ry += mouse.deltaY * viewSensY
	else:
		moveLatch = True
		y += mouse.deltaY * sensY
		if abs(y) > vJoy[0].axisMax:
			y = vJoy[0].axisMax * y / abs(y)
else:
	y /= (1.0 + centreY)

# recenter
if (not freelook and viewLatch):
	rx = 0
	ry = 0
	viewLatch = False


if (moveLatch and keyboard.getPressed(Key.Space) or keyboard.getPressed(Key.P)):
	x = 0
	y = 0
	moveLatch = False

freelook = mouse.getButton(3) or mouse.middleButton
if (mouse.getPressed(3)):
	viewLatch = True

vJoy[0].rx = rx
vJoy[0].ry = ry
vJoy[0].x = x
vJoy[0].y = y
# vJoy[0].setButton(1,int(mouse.leftButton)) 
# vJoy[0].setButton(2,int(mouse.rightButton)) 
# vJoy[0].setButton(3,int(mouse.middleButton)) 
# vJoy[0].setButton(4,int(keyboard.getKeyDown(Key.E))) 
# vJoy[0].setButton(5,int(keyboard.getKeyDown(Key.R))) 
# vJoy[0].setButton(6,int(keyboard.getKeyDown(Key.T))) 
# vJoy[0].setButton(7,int(keyboard.getKeyDown(Key.Y))) 


diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
diagnostics.watch(vJoy[0].rx)
diagnostics.watch(vJoy[0].ry)
diagnostics.watch(freelook)
diagnostics.watch(moveLatch)
diagnostics.watch(mouse.getButton(3))