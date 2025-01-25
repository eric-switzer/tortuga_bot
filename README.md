# Control for WEEEbot robot interfaces

Initial command assignments

| **Command Name**     | **IR Hex Code** | **Effect**                                                                                   | **Notes**                                              |
|----------------------|----------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------|
| **Mode A**          | `0x45`          | Stop, set `moveSpeed = 150`, beep `NTD1` (294 Hz), RGB (10,0,0)                             | Basic mode.                                           |
| **Mode B**          | `0x46`          | Stop, set `moveSpeed = 100`, beep `NTD2` (330 Hz), RGB (0,10,0)                             | "Wander" mode.                                        |
| **Mode C**          | `0x47`          | Stop, set `moveSpeed = 100`, beep `NTD3` (350 Hz), RGB (0,0,10)                             | "Line-following" mode.                                |
| **Mode D**          | `0x44`          | Enter gyro balancing mode, beep `NTD4` (393 Hz), RGB (0,10,10)                              | Self-balancing mode.                                  |
| **Increase Speed**  | `0x1C`          | `setMoveSpeed(NTD5, 5)`, beep `NTD5` (441 Hz), speed = 210                                  | Speed 210.                                            |
| **Decrease Speed**  | `0x08`          | `setMoveSpeed(NTD4, 4)`, beep `NTD4` (393 Hz), speed = 174                                  | Speed 174.                                            |
| **Forward**         | `0x40`          | `motor_sta = RUN_F`, `PID_speed.Setpoint = 80`, `move_flag = true`                          | Moves forward.                                        |
| **Backward**        | `0x19`          | `motor_sta = RUN_B`, `PID_speed.Setpoint = -80`, `move_flag = true`                         | Moves backward.                                       |
| **Turn Left**       | `0x07`          | `motor_sta = RUN_L`, `PID_turn.Setpoint = -100`, `move_flag = true`                         | Rotates left.                                         |
| **Turn Right**      | `0x09`          | `motor_sta = RUN_R`, `PID_turn.Setpoint = 100`, `move_flag = true`                          | Rotates right.                                        |
| **OK** (RGB Toggle) | `0x15`          | Toggles `RGBUlt_flag` (0 → 1 → 2 → 0), beep `NTD6` (495 Hz)                                 | Affects ultrasonic sensor LEDs.                       |
| **RGB Control**     | `0x0D`          | Toggles `RGB8_flag` (0 → 1 → 2 → 0), beep `NTD6` (495 Hz)                                   | Controls external RGB LED ring.                       |
| **Motor1 Left**     | `0x5A`          | Runs `Motor1` counterclockwise (`motor_sta = MOTOR1_L`)                                    | Moves one specific motor left.                        |
| **Motor1 Right**    | `0x42`          | Runs `Motor1` clockwise (`motor_sta = MOTOR1_R`)                                           | Moves one specific motor right.                       |
| **Motor2 Left**     | `0x52`          | Runs `Motor2` counterclockwise (`motor_sta = MOTOR2_L`)                                    | Moves another specific motor left.                    |
| **Motor2 Right**    | `0x4A`          | Runs `Motor2` clockwise (`motor_sta = MOTOR2_R`)                                           | Moves another specific motor right.                   |