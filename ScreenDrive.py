import cv2
import numpy as np
import vgamepad as vg
from PIL import ImageGrab

gamepad = vg.VX360Gamepad()

RacingLineColor = (96, 168, 198)
BlueErrorCorrection = 20
SkipPixel = 2

#700 500
#700+500 575
ScreenGap = (650, 410)
ScreenSize = (1350, 550)

font = cv2.FONT_HERSHEY_SIMPLEX
TurnAngle = 0

CountX = 0

while True:
    screen = np.array(ImageGrab.grab(bbox=(ScreenGap[0], ScreenGap[1], ScreenSize[0], ScreenSize[1])))

    LowerGoColor = (RacingLineColor[0] - round(BlueErrorCorrection), RacingLineColor[1] - round(BlueErrorCorrection), RacingLineColor[2] - round(BlueErrorCorrection))
    UpperGoColor = (RacingLineColor[0] + round(BlueErrorCorrection), RacingLineColor[1] + round(BlueErrorCorrection), RacingLineColor[2] + round(BlueErrorCorrection))

    for x in range(1, ScreenSize[0]-ScreenGap[0], SkipPixel):
        for y in range(1, ScreenSize[1]-ScreenGap[1], SkipPixel):
            if LowerGoColor[0] < screen[y, x, 0] < UpperGoColor[0] and LowerGoColor[1] < screen[y, x, 1] < UpperGoColor[1] and LowerGoColor[2] < screen[y, x, 2] < UpperGoColor[2]:
                img = cv2.rectangle(screen, (x, y), (x+5, y+5), (255, 0, 255), 2)
                TurnAngle = x
                CountX += 1
            else:
                img = screen

    if CountX < 12:
        BlueErrorCorrection += 1
    if CountX > 12:
        BlueErrorCorrection -= 1

    Text1 = cv2.putText(screen, 'X: {}'.format(CountX), (10, 40), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    CountX = 0


    Text = cv2.putText(screen, 'ErrCorr: {}'.format(round(BlueErrorCorrection)), (10, 20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


    cv2.imshow('window', img)

    gamepad.left_joystick(x_value=150 * (-300 + TurnAngle), y_value=0)  # values between -32768 and 32767

    gamepad.right_trigger(value=150)  # value between 0 and 255

    gamepad.update()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break