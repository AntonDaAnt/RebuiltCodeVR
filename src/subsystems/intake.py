import commands2
from rev import SparkMax, SparkLowLevel, SparkMaxConfig

class IntakeSubsystem(commands2.Subsystem):
    def __init__(self, constants, network):
        super().__init__()
        self.constants = constants
        self.nt = network

        # ==========================================
        # 1. HARDWARE INITIALIZATION
        # ==========================================
        # TODO: Initialize self.left_motor and self.right_motor using SparkMax.
        # Hint: Use self.constants.IntakeMotorLeft and SparkLowLevel.MotorType.kBrushless
        self.left_motor = None  
        self.right_motor = None 

        # ==========================================
        # 2. MOTOR CONFIGURATION (The "Brain" Settings)
        # ==========================================
        # We use SparkMaxConfig() to safely apply settings to the motors.
        leader_config = SparkMaxConfig()
        follower_config = SparkMaxConfig()

        # --- Safety & Consistency ---

        # TODO: Set a Smart Current Limit on the leader_config to 30 Amps.
        # Why? If a ball gets stuck, the motor will stall and draw massive current. 30A protects the NEO.
        # Hint: leader_config.smartCurrentLimit(30)

        # TODO: Enable Voltage Compensation on the leader_config at 12.0 Volts.
        # Why? A battery drops from 12.8V to 11.5V during a match. This ensures 50% speed is ALWAYS 6 Volts.
        # Hint: leader_config.voltageCompensation(12.0)

        # TODO: Set the Idle Mode to Coast so the intake rollers spin freely when stopped.
        # Hint: leader_config.setIdleMode(SparkMaxConfig.IdleMode.kCoast)

        # --- Follower Setup ---

        # TODO: Make the follower_config copy all the leader_config's safety settings.
        # Hint: follower_config.apply(leader_config)

        # TODO: Tell the follower_config to follow the leader motor.
        # Hint: Check if the motors face opposite directions! If they do, set invert=True in the follow() method.

        # ==========================================
        # 3. APPLY CONFIGURATION
        # ==========================================
        # TODO: Apply the leader_config to self.left_motor using .configure()
        # Hint: self.left_motor.configure(leader_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        
        # TODO: Apply the follower_config to self.right_motor using .configure()

    # ==========================================
    # 4. SUBSYSTEM METHODS (The "Actions")
    # ==========================================
    def run_intake(self, speed: float = 0.5):
        """Spins the intake inward to collect balls."""
        # TODO: Set the leader motor to the requested speed.
        # Hint: self.left_motor.set(speed)
        
        # TODO: Log the state to the network table using self.nt.setValue("Intake/State", "Running")
        pass

    def run_outtake(self, speed: float = -0.5):
        """Spins the intake outward to reject balls."""
        # TODO: Set the leader motor to the requested speed (it should be negative!).
        pass

    def stop(self):
        """Stops the intake entirely."""
        # TODO: Set the leader motor speed to 0.
        pass

    # ==========================================
    # 5. PERIODIC (Runs every 20ms)
    # ==========================================
    def periodic(self):
        """This runs automatically over and over. Great for updating the dashboard."""
        # TODO: Use self.nt.setValue() to log the current draw of the leader motor.
        # Hint: Use self.left_motor.getOutputCurrent()
        pass
