import commands2
import wpimath.controller
import math
from rev import SparkMax, SparkLowLevel, SparkMaxConfig

class ArmSubsystem(commands2.Subsystem):
    def __init__(self, constants, network):
        super().__init__()
        self.constants = constants
        self.nt = network

        # ==========================================
        # 1. HARDWARE INITIALIZATION
        # ==========================================
        self.left_motor = None  
        self.right_motor = None 
        self.encoder = None

        # --- Limit Switches ---
        # TODO: Initialize the forward and reverse limit switches from the leader motor.
        # Why? We wire them directly to the Spark MAX so it auto-stops the motor instantly.
        # Hint: self.reverse_limit = self.left_motor.getReverseLimitSwitch(SparkLowLevel.SparkLimitSwitch.Type.kNormallyOpen)
        self.forward_limit = None
        self.reverse_limit = None

        # ==========================================
        # 2. MOTOR CONFIGURATION
        # ==========================================
        leader_config = SparkMaxConfig()
        follower_config = SparkMaxConfig()

        # --- Safety & Consistency ---
        # TODO: Set 40A smart current limit, 12V voltage compensation, and Brake mode.
        
        # --- Limit Switch Config ---
        # TODO: Enable the limit switches in the configuration so the hardware knows to use them!
        # Hint: leader_config.limitSwitch.forwardLimitSwitchEnabled(True)
        # Hint: leader_config.limitSwitch.reverseLimitSwitchEnabled(True)

        # --- Follower Setup ---
        # TODO: Apply leader_config to follower_config, then make the right motor follow the left (inverted).

        # ==========================================
        # 3. APPLY CONFIGURATION
        # ==========================================
        # TODO: Apply the configs to both motors using .configure(...)

        # ==========================================
        # 4. MATH & CONTROLLERS
        # ==========================================
        self.target_angle_rads = 0.0

        # TODO: Initialize the PID Controller and ArmFeedforward controller.
        self.pid = None
        self.feedforward = None

    # ==========================================
    # 5. SUBSYSTEM METHODS
    # ==========================================
    def set_target_angle(self, angle_radians: float):
        self.target_angle_rads = angle_radians
        self.nt.setValue("Arm/TargetAngle", angle_radians)

    def stop(self):
        # TODO: Set the leader motor voltage to 0.
        pass

    # ==========================================
    # 6. PERIODIC (The Control Loop)
    # ==========================================
    def periodic(self):
        # 1. Read Encoders
        current_angle_rads = 0.0 # TODO: Get actual encoder value

        # --- Limit Switch Auto-Zeroing ---
        # If the arm hits the bottom limit switch, we know exactly where it is!
        # This fixes any "drift" in the encoder over the course of a match.
        # TODO: Check if the reverse limit switch is pressed. If it is, reset the encoder position to your "stowed" angle.
        # Hint: if self.reverse_limit.get(): 
        #           self.encoder.setPosition(self.constants.armStowedAngleRads)
        
        # 2. Calculate Feedforward (Gravity + Friction)
        # TODO: ff_voltage = self.feedforward.calculate(current_angle_rads, 0)
        ff_voltage = 0.0

        # 3. Calculate PID (Correction)
        # TODO: pid_voltage = self.pid.calculate(current_angle_rads, self.target_angle_rads)
        pid_voltage = 0.0

        # 4. Combine and Apply
        # TODO: total_voltage = ff_voltage + pid_voltage
        # TODO: Apply to left motor UNLESS you want it stopped.
        
        # 5. Telemetry
        # TODO: Log the limit switch states to the dashboard so drivers know if they are jammed!
        # Hint: self.nt.setValue("Arm/AtBottomLimit", self.reverse_limit.get())
        pass
