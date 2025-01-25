"""
Interface to Weeecode Robot over BLE, fully synchronous in user-facing API.
See: 
https://github.com/WEEEMAKE/
Weeemake_Libraries_for_Arduino: Weeemake/src/WeInfraredReceiver.h
Weeemake_Factory_Firmware/twelve_in_one/twelve_in_one.ino
"""
import asyncio
import nest_asyncio
from bleak import BleakClient, BleakError, BleakScanner

# Apply nest_asyncio to allow nested event loops in Jupyter
nest_asyncio.apply()

DEVICE_ADDRESS = "35B598CA-A4A0-5B38-F1CF-4C00EB006299"  # Replace if needed
WRITE_CHAR_UUID = "0000f101-0000-1000-8000-00805f9b34fb"

# IR Command Mappings
IR_COMMANDS = {
    "FORWARD":   "IR64\n",
    "BACKWARD":  "IR25\n",
    "LEFT":      "IR7\n",
    "RIGHT":     "IR9\n",
    "STOP":      "IR69\n",
    "SPEED_UP":  "IR28\n",
    "SLOW_DOWN": "IR8\n",
    "BEEP":      "BZ 440 300\n",
}

class WeeecodeRobot:
    """Synchronous BLE interface for Weeecode Robot."""

    def __init__(self, address=DEVICE_ADDRESS, command_delay=0.05):
        self.address = address
        self.command_delay = command_delay
        self.speed_level = 3

        # Get or create an event loop
        self.loop = self.get_event_loop()
        self.client = BleakClient(self.address, loop=self.loop)

    def get_event_loop(self):
        """Ensures all async operations run on the same event loop, even in Jupyter."""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.new_event_loop()

    def _run(self, coro):
        """Runs an async function in the correct event loop."""
        return asyncio.run(coro) if not self.loop.is_running() else asyncio.ensure_future(coro)

    def connect(self):
        """Synchronously connects to the BLE device."""
        return self._run(self._connect())

    async def _connect(self):
        try:
            await self.client.connect()
            print(f"Connected to {self.address}")
        except BleakError as e:
            print(f"Connection failed: {e}")

    def disconnect(self):
        """Synchronously disconnects from the BLE device."""
        return self._run(self._disconnect())

    async def _disconnect(self):
        if self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected.")

    def send_command(self, cmd: str):
        """Send a single command synchronously."""
        return self._run(self._send_command(cmd))

    async def _send_command(self, cmd: str):
        if self.client.is_connected:
            try:
                print(f"Sending: {cmd.strip()}")
                await self.client.write_gatt_char(WRITE_CHAR_UUID, cmd.encode('utf-8'))
                await asyncio.sleep(self.command_delay)
            except BleakError as e:
                print(f"BLE Write Error: {e}")

    def move_forward(self, duration=2.0):
        """Move forward for `duration` seconds."""
        print("Moving forward...")
        for _ in range(int(duration / self.command_delay)):
            self.send_command(IR_COMMANDS["FORWARD"])

    def move_backward(self, duration=2.0):
        """Move backward for `duration` seconds."""
        print("Moving backward...")
        for _ in range(int(duration / self.command_delay)):
            self.send_command(IR_COMMANDS["BACKWARD"])

    def turn_left(self, duration=1.0):
        """Turn left for `duration` seconds."""
        print("Turning left...")
        for _ in range(int(duration / self.command_delay)):
            self.send_command(IR_COMMANDS["LEFT"])

    def turn_right(self, duration=1.0):
        """Turn right for `duration` seconds."""
        print("Turning right...")
        for _ in range(int(duration / self.command_delay)):
            self.send_command(IR_COMMANDS["RIGHT"])

    def stop(self):
        """Stop all motion."""
        print("Stopping...")
        self.send_command(IR_COMMANDS["STOP"])

    def speed_up(self):
        """Increase speed one level."""
        if self.speed_level < 5:
            self.speed_level += 1
            print(f"Speed up -> level {self.speed_level}")
            self.send_command(IR_COMMANDS["SPEED_UP"])

    def slow_down(self):
        """Decrease speed one level."""
        if self.speed_level > 1:
            self.speed_level -= 1
            print(f"Slow down -> level {self.speed_level}")
            self.send_command(IR_COMMANDS["SLOW_DOWN"])

    def beep(self, frequency=440, duration=500):
        """Play a beep at `frequency` Hz for `duration` ms."""
        cmd = f"BZ {frequency} {duration}\n"
        print(f"Beeping {frequency} Hz for {duration} ms...")
        self.send_command(cmd)

    def set_command_delay(self, delay):
        """Adjust the delay between IR commands for smoother/faster motion."""
        self.command_delay = delay
        print(f"Command delay set to {delay}s")

def find_devices():
    """Synchronous BLE scanning; prints discovered devices."""
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(_async_find_devices())

async def _async_find_devices():
    print("Scanning for BLE devices (5 seconds)...")
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        print(f"- Name: {d.name}, Address: {d.address}, RSSI: {d.rssi}")

# ----- Example usage -----
if __name__ == "__main__":
    # 1) Scan for devices (if needed) to find correct address
    find_devices()

    # 2) Instantiate the robot
    bot = WeeecodeRobot()

    # 3) Connect
    bot.connect()

    # 4) Simple moves
    bot.move_forward(1.5)
    bot.turn_left(0.75)
    bot.slow_down()
    bot.move_forward(1.0)
    bot.stop()

    # 5) Beep
    bot.beep(600, 300)

    # 6) Disconnect
    bot.disconnect()

