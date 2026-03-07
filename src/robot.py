#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import commands2
import RobotContainer

class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        """Robot initialization function"""
        self.robotContainer = RobotContainer.RobotContainer()
        self.autonomousCommand = None

    def autonomousInit(self) -> None:
        """This function is run once each time the robot enters autonomous mode."""
        return super().autonomousInit()

    def teleopInit(self) -> None:
        """This function is called once each time the robot enters teleoperated mode."""
        # This makes sure that the autonomous routine stops running when
        # teleop starts.
        if self.autonomousCommand is not None:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically (every 20ms) during teleoperated mode."""
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)