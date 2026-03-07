#import commands2
#import wpimath.controller
#import math
#from rev import SparkFlex, SparkLowLevel, SparkBaseConfig
#
#class Shooter(commands2.Subsystem):
#    def __init__(self, constants, network):
#        super().__init__()
#        self.constants = constants
#        self.nt = network 
#
#        # 1. Hardware Initialization
#        self.left_motor = SparkFlex(self.constants.ShooterMotorChannelLeft, SparkLowLevel.MotorType.kBrushless)
#        self.right_motor = SparkFlex(self.constants.ShooterMotorChannelRight, SparkLowLevel.MotorType.kBrushless)
#
#        # 2. Create Global Configuration
#        shooter_config = SparkBaseConfig()
#        shooter_config.smartCurrentLimit(40)
#        shooter_config.voltageCompensation(12.0)
#        shooter_config.openLoopRampRate(0.25)
#        shooter_config.closedLoopRampRate(0.25)
#
#        # 3. Apply Config to Leader (Left)
#        self.left_motor.configure(
#            shooter_config,
#            SparkFlex.ResetMode.kResetSafeParameters,
#            SparkFlex.PersistMode.kPersistParameters
#        )
#
#        # 4. Apply Config to Follower (Right) with Inversion
#        right_config = SparkBaseConfig()
#        right_config.apply(shooter_config) 
#        right_config.follow(self.left_motor, True) 
#        
#        self.right_motor.configure(
#            right_config,
#            SparkFlex.ResetMode.kResetSafeParameters,
#            SparkFlex.PersistMode.kPersistParameters
#        )
#
#        self.encoder = self.left_motor.getEncoder()
#
#        # 5. Conversion Factor: RPM to Rad/S
#        self.rpm_to_rads = (2 * math.pi) / 60.0
#
#        # 6. Push initial default values to the Dashboard via your Network class
#        self.nt.setValue("Shooter/kP", self.constants.shooterKP)
#        self.nt.setValue("Shooter/kS", self.constants.shooterKS)
#        self.nt.setValue("Shooter/kV", self.constants.shooterKV)
#        self.nt.setValue("Shooter/TargetRPM", 0.0)
#
#        # 7. Controllers
#        self.pid = wpimath.controller.PIDController(self.constants.shooterKP, 0, 0)
#        self.feedforward = wpimath.controller.SimpleMotorFeedforwardRadians(
#            self.constants.shooterKS,
#            self.constants.shooterKV,  
#            self.constants.shooterKA   
#        )
#
#        self.target_rpm = 0.0
#
#    def periodic(self):
#        # 1. Update from Network (Live Tuning)
#        # Using your getValue with a default fallback just in case
#        new_kP = self.nt.getValue("Shooter/kP", self.constants.shooterKP)
#        new_kS = self.nt.getValue("Shooter/kS", self.constants.shooterKS)
#        new_kV = self.nt.getValue("Shooter/kV", self.constants.shooterKV)
#        self.target_rpm = self.nt.getValue("Shooter/TargetRPM", 0.0)
#
#        if new_kP != self.pid.getP():
#            self.pid.setP(new_kP)
#
#        # Rebuild FF if constants change (passing kA so it doesn't crash)
#        self.feedforward = wpimath.controller.SimpleMotorFeedforwardRadians(
#            new_kS, new_kV, self.constants.shooterKA
#        )
#
#        # 2. Velocity Conversions
#        current_rpm = self.encoder.getVelocity()
#        current_rads = current_rpm * self.rpm_to_rads
#        target_rads = self.target_rpm * self.rpm_to_rads
#
#        # 3. Control Loop
#        if self.target_rpm > 100: 
#            pid_out = self.pid.calculate(current_rads, target_rads)
#            ff_out = self.feedforward.calculate(target_rads)
#            
#            # Since the right motor is following, we only command the left
#            self.left_motor.setVoltage(pid_out + ff_out)
#        else:
#            self.left_motor.set(0)
#
#        # 4. Telemetry back to the Dashboard
#        self.nt.setValue("Shooter/ActualRPM", current_rpm)
#
#    def at_setpoint(self) -> bool:
#        return abs(self.target_rpm - self.encoder.getVelocity()) < 50
#