"""
Interface to weeebot bluetooth

See: 
https://github.com/WEEEMAKE/
Weeemake_Libraries_for_Arduino: Weeemake/src/WeInfraredReceiver.h
Weeemake_Factory_Firmware/twelve_in_one/twelve_in_one.ino

TODO: check speed control
"""
import asyncio
from bleak import BleakClient, BleakError

DEVICE_ADDRESS = "35B598CA-A4A0-5B38-F1CF-4C00EB006299"
WRITE_CHAR_UUID = "0000f101-0000-1000-8000-00805f9b34fb"

# IR Command Mappings (Hex -> Decimal)
IR_COMMANDS = {
    "MODE_A": "IR69\n",  # 0x45 = 69 decimal
    "FORWARD": "IR64\n",  # 0x40 = 64 decimal
    "BACKWARD": "IR25\n",  # 0x19 = 25 decimal
    "LEFT": "IR7\n",  # 0x07 = 7 decimal
    "RIGHT": "IR9\n",  # 0x09 = 9 decimal
    "BEEP": "BZ 440 300\n",
    "SPEED_UP": "IR28\n",  # 0x1C = 28 decimal
    "SLOW_DOWN": "IR8\n",  # 0x08 = 8 decimal
    "STOP": "IR69\n",  # Mode A = Stop
    "RGB": "RGB 1 255 0 0\n",  # Example RGB Command
}

class WeeecodeRobot:
    """BLE Interface for Weeecode Robot with Turtle-style commands."""
    
    def __init__(self, address=DEVICE_ADDRESS, command_delay=0.05):
        self.address = address
        self.client = None
        self.speed_level = 3  # Default speed level
        self.command_delay = command_delay  # Delay between repeated commands (default: 50ms)

    async def connect(self):
        """Connects to the BLE device."""
        try:
            self.client = BleakClient(self.address)
            await self.client.connect()
            print(f"Connected to {self.address}")
        except BleakError as e:
            print(f"BLE Connection Error: {e}")

    async def disconnect(self):
        """Disconnects from the BLE device."""
        if self.client:
            await self.client.disconnect()
            print("Disconnected.")

    async def send_command(self, command):
        """Sends a command to the robot over BLE."""
        if self.client:
            try:
                print(f"Sending: {command.strip()}")
                await self.client.write_gatt_char(WRITE_CHAR_UUID, command.encode('utf-8'))
                await asyncio.sleep(self.command_delay)  # Adjusted for smoother motion
            except BleakError as e:
                print(f"BLE Write Error: {e}")

    def set_command_delay(self, delay):
        """Adjusts the command delay for smoother or more responsive motion."""
        self.command_delay = delay
        print(f"Command delay set to {delay} seconds")

    async def move_forward(self, duration=2.0):
        """Moves forward for a set duration."""
        print("Moving Forward")
        for _ in range(int(duration / self.command_delay)):
            await self.send_command(IR_COMMANDS["FORWARD"])

    async def move_backward(self, duration=2.0):
        """Moves backward for a set duration."""
        print("Moving Backward")
        for _ in range(int(duration / self.command_delay)):
            await self.send_command(IR_COMMANDS["BACKWARD"])

    async def turn_left(self, duration=1.0):
        """Turns left for a set duration."""
        print("Turning Left")
        for _ in range(int(duration / self.command_delay)):
            await self.send_command(IR_COMMANDS["LEFT"])

    async def turn_right(self, duration=1.0):
        """Turns right for a set duration."""
        print("Turning Right")
        for _ in range(int(duration / self.command_delay)):
            await self.send_command(IR_COMMANDS["RIGHT"])

    async def stop(self):
        """Stops all movement."""
        print("Stopping")
        await self.send_command(IR_COMMANDS["STOP"])

    async def speed_up(self):
        """Increases speed."""
        if self.speed_level < 5:
            self.speed_level += 1
            print(f"Increasing Speed: Level {self.speed_level}")
            await self.send_command(IR_COMMANDS["SPEED_UP"])

    async def slow_down(self):
        """Decreases speed."""
        if self.speed_level > 1:
            self.speed_level -= 1
            print(f"Decreasing Speed: Level {self.speed_level}")
            await self.send_command(IR_COMMANDS["SLOW_DOWN"])

    async def beep(self, frequency=440, duration=500):
        """Beep at a certain frequency and duration."""
        cmd = f"BZ {frequency} {duration}\n"
        print(f"Beeping: {frequency}Hz for {duration}ms")
        await self.send_command(cmd)

    async def set_rgb(self, idx, r, g, b):
        """Sets the RGB LED to a color."""
        cmd = f"RGB {idx} {r} {g} {b}\n"
        print(f"Setting RGB LED {idx} to ({r}, {g}, {b})")
        await self.send_command(cmd)

    async def run_demo(self):
        """Demonstrates motor control."""
        await self.connect()
        
        self.set_command_delay(0.05)  # Faster commands for smoother motion

        await self.move_forward(1.0)
        await self.turn_left(0.5)
        await self.move_forward(1.0)
        await self.turn_left(0.5)
        await self.move_forward(1.0)
        await self.turn_left(0.5)
        await self.move_forward(1.0)
        await self.turn_left(0.5)

        #await self.move_backward(1.5)
        #await self.slow_down()
        #await self.speed_up()
        #await self.stop()

        #await self.beep(600, 300)
        await self.set_rgb(1, 255, 0, 0)  # Red
        await self.set_rgb(1, 0, 255, 0)  # Green
        await self.set_rgb(1, 0, 0, 255)  # Blue
        
        await self.disconnect()

# Run Demo
if __name__ == "__main__":
    robot = WeeecodeRobot()
    asyncio.run(robot.run_demo())

