import threading

import pypot.dynamixel



class Primitive(object):
    def __init__(self, robot, *args, **kwargs):
        self.robot = MockupRobot(robot)
        self.robot._primitive_manager.add(self)
        
        self.args = args
        self.kwargs = kwargs
        
        self._thread = threading.Thread(target=self._wrapped_run)
        self._thread.daemon = True
    
    def run(self, *args, **kwargs):
        pass
    
    def start(self):
        self._thread.start()

    def _wrapped_run(self):
        self.on_start()
        self.run(*self.args, **self.kwargs)
        self.on_stop()

    def on_start(self):
        pass

    def on_stop(self):
        self.robot._primitive_manager.remove(self)


class MockupRobot(object):
    def __init__(self, robot):
        self._robot = robot
        self._motors = []
        
        for m in robot.motors:
            mockup_motor = MockupMotor(m)
            self._motors.append(mockup_motor)
            setattr(self, m.name, mockup_motor)
    
    def __getattr__(self, attr):
        return getattr(self._robot, attr)
    
    @property
    def motors(self):
        return self._motors


class MockupMotor(pypot.dynamixel.DxlMotor):
    def __init__(self, m):
        pypot.dynamixel.DxlMotor.__init__(self, m.id, m.name, m.direct, m.offset)
        self._values = m._values
        self.to_set = {}
    
    @property
    def goal_position(self):
        return pypot.dynamixel.DxlMotor.goal_position.fget(self)
    
    @goal_position.setter
    def goal_position(self, value):
        self.to_set['goal_position'] = value
    
    @property
    def moving_speed(self):
        return pypot.dynamixel.DxlMotor.moving_speed.fget(self)
    
    @moving_speed.setter
    def moving_speed(self, value):
        self.to_set['moving_speed'] = value
    
    @property
    def torque_limit(self):
        return pypot.dynamixel.DxlMotor.torque_limit.fget(self)
    
    @torque_limit.setter
    def torque_limit(self, value):
        self.to_set['torque_limit'] = value
    
    @property
    def pid(self):
        return pypot.dynamixel.DxlMotor.pid.fget(self)
    
    @pid.setter
    def pid(self, value):
        self.to_set['pid'] = pid