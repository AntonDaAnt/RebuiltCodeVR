#import commands2
#import wpimath.controller
#import math
#from rev import SparkFlex, SparkLowLevel, SparkBaseConfig, SparkMax, SparkMaxConfig
#
#class IntakeSubsystem(commands2.Subsystem):
#    def __init__(self, constants, network):
#        super().__init__()
#        self.constants = constants
#        self.nt = network
#
#        # 1. HARDWARE INITIALIZATION
#        self.left_motor = SparkFlex(self.constants.BallIntakeMotorChannelLeft, SparkLowLevel.MotorType.kBrushless)
#        self.right_motor = SparkFlex(self.constants.BallIntakeMotorChannelRight, SparkLowLevel.MotorType.kBrushless)
#
#        # 2. MOTOR CONFIGURATION
#        leader_config = SparkMaxConfig()
#        leader_config.smartCurrentLimit(40)
#        leader_config.voltageCompensation(12.0)
#        leader_config.setIdleMode(SparkMaxConfig.IdleMode.kCoast)
#        follower_config = SparkMaxConfig()
#        follower_config.apply(leader_config)
#        follower_config.follow(leader_config, True)
#
#        self.left_motor.configure(leader_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
#        self.right_motor.configure(leader_config, SparkMax.Resetmode.kResetSafeParameters, SparkMax.persistMode.kPresistParameters)
#
#    # 4. SUBSYSTEM METHODS
#    def run_intake(self, speed: float = 0.5):
#        """Spins the intake inward to collect balls."""
#        self.left_motor.set(speed)
#        
#        # TODO: Log the state to the network table using self.nt.setValue("Intake/State", "Running")
#        pass
#
#    def run_outtake(self, speed: float = -0.5):
#        """Spins the intake outward to reject balls."""
#        # TODO: Set the leader motor to the requested speed (it should be negative!).
#        pass
#
#    def stop(self):
#        """Stops the intake entirely."""
#        # TODO: Set the leader motor speed to 0.
#        pass
#
#    # ==========================================
#    # 5. PERIODIC (Runs every 20ms)
#    # ==========================================
#    def periodic(self):
#        """This runs automatically over and over. Great for updating the dashboard."""
#        # TODO: Use self.nt.setValue() to log the current draw of the leader motor.
#        # Hint: Use self.left_motor.getOutputCurrent()
#        pass
#