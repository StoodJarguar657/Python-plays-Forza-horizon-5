import vgamepad as vg

gamepad = vg.VX360Gamepad()

while True:
    gamepad.right_trigger(value=255)

    gamepad.update()