import cv2
import numpy as np
import vgamepad as vg
from PIL import ImageGrab

gamepad = vg.VX360Gamepad()

MapDirColor = (62, 237, 255)
Correction = 10
SkipPixel = 3


ScreenGap = (120, 880)
ScreenSize = (250, 940)

font = cv2.FONT_HERSHEY_SIMPLEX
TurnAngle = 0

CountX = 0



def clamp(Value, Min, Max):
    if Value > Min and Value < Max:
        return Value
    if Value > Min and Value > Max:
        return Max
    if Value < Min and Value < Max:
        return Min


UsedTurnAngle = 0

while True:
    screen = np.array(ImageGrab.grab(bbox=(ScreenGap[0], ScreenGap[1], ScreenSize[0], ScreenSize[1])))

    LowerGoColor = (MapDirColor[0] - round(Correction), MapDirColor[1] - round(Correction), MapDirColor[2] - round(Correction))
    UpperGoColor = (MapDirColor[0] + round(Correction), MapDirColor[1] + round(Correction), MapDirColor[2] + round(Correction))

    YVal = ScreenSize[1]-ScreenGap[1]

    for x in range(1, ScreenSize[0]-ScreenGap[0], SkipPixel):
        for y in range(1, ScreenSize[1]-ScreenGap[1], SkipPixel):
            if LowerGoColor[0] < screen[YVal-y, x, 0] < UpperGoColor[0] and LowerGoColor[1] < screen[YVal-y, x, 1] < UpperGoColor[1] and LowerGoColor[2] < screen[YVal-y, x, 2] < UpperGoColor[2]:
                img = cv2.rectangle(screen, (x, YVal-y), (x + 1, YVal-y + 1), (255, 0, 0), 1)
                TurnAngle = x
                CountX += 1
            else:
                img = screen



    if CountX < 40:
        Correction = Correction + 0.5 + CountX / 16
    if CountX > 20:
        Correction = Correction - 0.5 - CountX / 16

    TurnValue = (-76 + TurnAngle)*3000
    TurnAngle = 0
    if UsedTurnAngle > TurnValue:
        UsedTurnAngle += (TurnValue - UsedTurnAngle)/2
    if UsedTurnAngle < TurnValue:
        UsedTurnAngle += (-UsedTurnAngle + TurnValue)/2

    if UsedTurnAngle > TurnValue - 5000 and TurnValue > UsedTurnAngle - 5000:
        UsedTurnAngle = TurnValue
    if UsedTurnAngle < TurnValue - 5000 and TurnValue < UsedTurnAngle - 5000:
        UsedTurnAngle = TurnValue


    gamepad.left_joystick(x_value=clamp(round(UsedTurnAngle), -32000, 32000), y_value=0)  # values between -32768 and 32767

    gamepad.right_trigger(value=150)  # value between 0 and 255

    Text2 = cv2.putText(screen, '1: {}'.format(UsedTurnAngle), (10, 10), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    Text2 = cv2.putText(screen, '2: {}'.format(TurnValue), (10, 30), font, 0.5, (0, 255, 0),
                        1, cv2.LINE_AA)


    CountX = 0



    cv2.imshow('window', img)

    gamepad.update()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break