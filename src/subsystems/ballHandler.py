import commands2
from enum import Enum

class RobotState(Enum):
    IDLE = 0
    INTAKING = 1
    SPINNING_UP = 2
    SHOOTING_SINGLE = 3
    MACHINE_GUN = 4

class Superstructure(commands2.Subsystem):
    # TODO: Notice we added 'arm' to the list of required subsystems!
    def __init__(self, shooter, elevator, intake, arm, network, constants):
        super().__init__()
        self.shooter = shooter
        self.elevator = elevator
        self.intake = intake
        self.arm = arm
        self.nt = network
        self.constants = constants

        self.current_state = RobotState.IDLE
        self.target_rpm = 0.0
        
        # New: Track if the driver wants the arm out or in
        self.arm_wants_out = False

        self.timer = commands2.Timer()

    # ==========================================
    # 2. THE CONTROLLER LOGIC
    # ==========================================
    # TODO: We added btn_y to the inputs so we can read the Y button.
    def controllerDrive(self, rt_value: float, btn_a: bool, btn_b: bool, btn_x: bool, btn_y: bool):
        """Reads the controller and determines the robot's state."""
        
        self.target_rpm = rt_value * self.constants.MaxShooterRPM

        # --- ARM LOGIC (Parallel) ---
        # The arm does its own thing regardless of what the shooter is doing.
        # If Y is held down, it's True. If let go, it's False.
        self.arm_wants_out = btn_y

        # --- ROLLER/SHOOTER LOGIC (Sequential) ---
        if btn_x:
            self.current_state = RobotState.INTAKING
        elif btn_b:
            self.current_state = RobotState.MACHINE_GUN
        elif btn_a:
            if self.current_state not in [RobotState.SHOOTING_SINGLE, RobotState.SPINNING_UP]:
                self.current_state = RobotState.SPINNING_UP
        else:
            if self.current_state != RobotState.SHOOTING_SINGLE:
                self.current_state = RobotState.IDLE

    # ==========================================
    # 3. THE STATE MACHINE (Runs every 20ms)
    # ==========================================
    def periodic(self):
        self.nt.setValue("Superstructure/State", self.current_state.name)
        self.nt.setValue("Superstructure/ArmOut", self.arm_wants_out)

        # --- 1. EXECUTE ARM COMMANDS ---
        # TODO: Tell the arm where to go based on the boolean flag.
        # Hint: if self.arm_wants_out:
        #           self.arm.set_target_angle(self.constants.ArmOutAngle)
        #       else:
        #           self.arm.set_target_angle(self.constants.ArmInAngle)

        # --- 2. EXECUTE ROLLER COMMANDS ---
        if self.current_state == RobotState.IDLE:
            # TODO: Tell the intake, elevator, and shooter to stop().
            self.timer.stop()
            self.timer.reset()

        elif self.current_state == RobotState.INTAKING:
            # TODO: Tell the intake to run_intake().
            # TODO: Tell the elevator to reverse slowly.
            pass

        elif self.current_state == RobotState.MACHINE_GUN:
            # TODO: self.shooter.set_target_rpm(self.target_rpm)
            # TODO: if self.shooter.at_setpoint(): self.elevator.feed() else: self.elevator.stop()
            pass

        elif self.current_state == RobotState.SPINNING_UP:
            # TODO: self.shooter.set_target_rpm(self.target_rpm)
            # TODO: self.elevator.stop()
            # TODO: if self.shooter.at_setpoint(): change state to SHOOTING_SINGLE and start timer.
            pass

        elif self.current_state == RobotState.SHOOTING_SINGLE:
            # TODO: Keep shooter spinning.
            # TODO: Tell elevator to feed().
            # TODO: if self.timer.hasElapsed(0.5): change state back to IDLE.
            pass
