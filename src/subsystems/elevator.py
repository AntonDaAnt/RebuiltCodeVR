import commands2
from rev import SparkMax, SparkLowLevel
from rev import SparkMaxConfig 

class ElevatorSubsystem(commands2.Subsystem):
    def __init__(self, constants, network):
        super().__init__()
        self.constants = constants
        self.nt = network

        # 1. Hardware Initialization (Spark MAX + NEO)
        self.motor = SparkMax(self.constants.ElevatorMotorChannel, SparkLowLevel.MotorType.kBrushless)

       # 2. Motor Configuration
        elevator_config = SparkMaxConfig()
        
        # Safety: 30A limit. 
        elevator_config.smartCurrentLimit(30)
        
        # Idle Mode: BRAKE.
        # This is important for elevators to prevent them from back-driving downwards when you stop applying power.
        elevator_config.setIdleMode(SparkMaxConfig.IdleMode.kBrake)
        
        # 3. Apply Config
        self.motor.configure(
            elevator_config,
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters
        )

    def feed(self):
        """Runs the elevator upwards to feed balls into the shooter."""
        self.motor.set(self.constants.ElevatorSpeedPercentage)
        self.nt.setValue("Elevator/State", "Feeding")

    def reverse(self):
        """Runs the elevator backwards. Great for unjamming balls."""
        self.motor.set(-self.constants.ElevatorSpeedPercentage)
        self.nt.setValue("Elevator/State", "Reversing")

    def stop(self):
        """Stops the elevator."""
        self.motor.set(0)
        self.nt.setValue("Elevator/State", "Stopped")

    def periodic(self):
        # Optional: Log the current draw. 
        # If this spikes to 30A while feeding, you know a ball is jammed!
        self.nt.setValue("Elevator/CurrentDraw", self.motor.getOutputCurrent())
