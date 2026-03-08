import math
import phoenix6
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics
import wpimath.units

kWheelRadius = wpimath.units.inchesToMeters(2)

class SwerveModule:
    def __init__(
        self,
        driveMotorChannel: int,
        turningMotorChannel: int,
        turningEncoderChannel: int,
        offset: float, # Expected in Degrees
        invertModule: bool = False
    ) -> None:
        self.offset = wpimath.units.degreesToRadians(offset)
        
        # Hardware Initialization
        self.driveMotor = phoenix6.hardware.TalonFX(driveMotorChannel)
        self.turningMotor = phoenix6.hardware.TalonFX(turningMotorChannel)
        self.turningEncoder = phoenix6.hardware.CANcoder(turningEncoderChannel)

        if invertModule:
            # --- NEW: PHOENIX 6 CONFIGURATION ---
            turn_config = phoenix6.configs.TalonFXConfiguration()

            # This flips the motor's definition of "forward" vs "reverse". 
            # If CLOCKWISE_POSITIVE doesn't fix the runaway motor, change it to COUNTER_CLOCKWISE_POSITIVE
            turn_config.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE

            # Apply the configuration to the TalonFX
            self.turningMotor.configurator.apply(turn_config)
            # ------------------------------------

        # Control objects
        self.driveControl = phoenix6.controls.DutyCycleOut(0)
        self.turnControl = phoenix6.controls.DutyCycleOut(0)

        # PID for turning
        self.turningPIDController = wpimath.controller.PIDController(0.05, 0, 0) 
        self.turningPIDController.enableContinuousInput(-math.pi, math.pi)

        # Zero the drive motor on boot
        self.driveMotor.set_position(0)
    
    def getTurningPosition(self) -> float:
        """
        Reads the absolute position of the CANcoder, converts to radians, 
        and APPLIES THE OFFSET so 0 is always true forward.
        """
        absolute_pos_rad = wpimath.units.rotationsToRadians(
            self.turningEncoder.get_absolute_position().value
        )
        return absolute_pos_rad - self.offset

    def getDrivePosition(self) -> float:
        """Returns the total distance the drive wheel has traveled in meters."""
        # Phoenix 6 get_position() returns rotations
        return self.driveMotor.get_position().value * (2 * math.pi * kWheelRadius)

    def getPosition(self) -> wpimath.kinematics.SwerveModulePosition:
        """Required for Odometry: Returns the distance traveled and current angle."""
        return wpimath.kinematics.SwerveModulePosition(
            self.getDrivePosition(),
            wpimath.geometry.Rotation2d(self.getTurningPosition())
        )

    def getState(self) -> wpimath.kinematics.SwerveModuleState:
        """Required for Kinematics: Returns the current velocity and angle."""
        velocity = self.driveMotor.get_velocity().value * (2 * math.pi * kWheelRadius)
        return wpimath.kinematics.SwerveModuleState(
            velocity, 
            wpimath.geometry.Rotation2d(self.getTurningPosition())
        )

    def setDesiredState(self, desiredState: wpimath.kinematics.SwerveModuleState):
        current_rotation = wpimath.geometry.Rotation2d(self.getTurningPosition())
        
        # 1. Optimize state IN-PLACE (Modern WPILib standard)
        desiredState.optimize(current_rotation)

        # 2. Prevent wheel 'jitter' at low joystick inputs
        if abs(desiredState.speed) < 0.01:
            self.stop()
            return

        # 3. Calculate Turn Output (PID)
        turn_output = self.turningPIDController.calculate(
            self.getTurningPosition(), 
            desiredState.angle.radians()
        )

        # TODO: Delete this later (it is for testing)
        turn_output = max(-0.2, min(0.2, turn_output))

        # 4. Calculate Drive Output
        max_speed = 1 # TODO: Set this to your robot's actual max physical m/s
        drive_output = desiredState.speed / max_speed

        # 5. Apply outputs
        self.driveMotor.set_control(self.driveControl.with_output(drive_output))
        self.turningMotor.set_control(self.turnControl.with_output(turn_output))

    def stop(self):
        self.driveMotor.set_control(self.driveControl.with_output(0))
        self.turningMotor.set_control(self.turnControl.with_output(0))
