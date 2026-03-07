#!/usr/bin/env python3

import RobotContainer
import commands2


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        """Robot initialization function"""
        self.robotContainer = RobotContainer.RobotContainer()
        self.autonomousCommand = None

    def autonomousInit(self) -> None:
        """This function is run once each time the robot enters autonomous mode."""
        # Note: When you are ready for auto, you would fetch the command from
        # your robotContainer and schedule it here.
        # Example:
        # self.autonomousCommand = self.robotContainer.getAutonomousCommand()
        # if self.autonomousCommand is not None:
        #     self.autonomousCommand.schedule()
        return super().autonomousInit()

    def teleopInit(self) -> None:
        """This function is called once each time the robot enters teleoperated mode."""
        # This makes sure that the autonomous routine stops running when
        # teleop starts. If you want auto to continue until interrupted, 
        # you can remove this block.
        if self.autonomousCommand is not None:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically (every 20ms) during teleoperated mode."""
        # Because you are using a Command-Based robot, the CommandScheduler 
        # automatically runs your swerve's default RunCommand here. 
        # You generally don't need to put anything in this method!
        pass
