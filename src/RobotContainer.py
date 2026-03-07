import wpilib
import wpilib.interfaces

from pathplannerlib.auto import AutoBuilder, NamedCommands, PathPlannerAuto

from subsystems import drivetrain
from constants import Constants
import commands2


class RobotContainer():
    def __init__(self, constants=Constants()):
        self.constants = constants
        self.controller = wpilib.interfaces.GenericHID(0)
        self.Juanita = wpilib.interfaces.GenericHID(1)

        self.swerve = drivetrain.Drivetrain()
        self.swerve.setDefaultCommand(
            commands2.RunCommand(
                lambda: self.swerve.joystickDrive(
                    self.controller.getRawAxis(0) * self.constants.kMaxSpeed,
                    -self.controller.getRawAxis(1) * -self.constants.kMaxSpeed,
                    self.controller.getRawAxis(4) * self.constants.kMaxAngularSpeed,
                    not self.controller.getRawButton(1),
                    self.controller.getRawButton(2),
                    self.controller.getRawButton(6)),
                self.swerve)
        )

    def disable(self):
        # self.elevator.disable()
        self.swerve.disable()
