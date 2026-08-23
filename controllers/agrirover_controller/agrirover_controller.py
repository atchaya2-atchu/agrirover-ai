from controller import Robot

robot = Robot()

TIME_STEP = 32

left_front = robot.getDevice("left_front_motor")
right_front = robot.getDevice("right_front_motor")
left_rear = robot.getDevice("left_rear_motor")
right_rear = robot.getDevice("right_rear_motor")

motors = [left_front, right_front, left_rear, right_rear]

for motor in motors:
    motor.setPosition(float("inf"))
    motor.setVelocity(0.0)

left_sensor = robot.getDevice("front_left_sensor")
right_sensor = robot.getDevice("front_right_sensor")

left_sensor.enable(TIME_STEP)
right_sensor.enable(TIME_STEP)

speed = 4.0

while robot.step(TIME_STEP) != -1:

    left_distance = left_sensor.getValue()
    right_distance = right_sensor.getValue()

    if left_distance < 800 or right_distance < 800:
        left_front.setVelocity(0.0)
        right_front.setVelocity(0.0)
        left_rear.setVelocity(0.0)
        right_rear.setVelocity(0.0)

    else:
        left_front.setVelocity(speed)
        right_front.setVelocity(speed)
        left_rear.setVelocity(speed)
        right_rear.setVelocity(speed)
