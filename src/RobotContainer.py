import wpilib
import wpilib.interfaces

from pathplannerlib.auto import AutoBuilder, NamedCommands, PathPlannerAuto

from subsystems import drivetrain, shooter, elevator
from subsystems.networking import Network
from constants import Constants
import commands2


class RobotContainer():
    def __init__(self):
        # Get constants and network
        self.constants = Constants()
        self.network = Network()

        # Set controllers
        self.swerveController = wpilib.interfaces.GenericHID(self.constants.swerveController)
        self.shooterController = wpilib.interfaces.GenericHID(self.constants.shooterController)

        ## Create Shooter Object
        #self.shooter = shooter.Shooter(self.constants, self.network)
        #self.shooter.setDefaultCommand(
        #    commands2.RunCommand(
        #        lambda: self.shooter.periodic(),
        #        self.shooter
        #    )
        #)

        # Create swerve object
        self.swerve = drivetrain.Drivetrain()
        self.swerve.setDefaultCommand(
            commands2.RunCommand(
                lambda: self.swerve.joystickDrive(
                    self.swerveController.getRawAxis(0) * self.constants.kMaxSpeed,
                    -self.swerveController.getRawAxis(1) * -self.constants.kMaxSpeed,
                    self.swerveController.getRawAxis(4) * self.constants.kMaxAngularSpeed,
                    not self.swerveController.getRawButton(1),
                    self.swerveController.getRawButton(2),
                    self.swerveController.getRawButton(6)),
                self.swerve)
        )

    def disable(self):
        self.shooter.disable()
        self.swerve.disable()