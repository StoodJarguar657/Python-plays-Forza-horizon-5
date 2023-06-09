import math
import cv2
import numpy as np
import vgamepad as vg
from PIL import ImageGrab

Debug = True

gamepad = vg.VX360Gamepad()

ScreenGap = (50, 735)
Screensize = (340, 219 + 735)
SkipPixel = 2

GotoDirColor = (62, 237, 255)
Correction = 100
FoundCount = 0

Angle = 0


def clamp(Value, min, max):
    if Value > min and Value < max:
        return Value
    if Value < min and Value < max:
        return min
    if Value > min and Value > max:
        return max

Firstfoundx = False
Lastfoundx = False

while True:

    LowerColorRange = (GotoDirColor[0] - round(Correction), GotoDirColor[1] - round(Correction), GotoDirColor[2] - round(Correction))
    UpperColorRange = (GotoDirColor[0] + round(Correction), GotoDirColor[1] + round(Correction), GotoDirColor[2] + round(Correction))

    screen = np.array(ImageGrab.grab(bbox=(ScreenGap[0], ScreenGap[1], Screensize[0], Screensize[1])))


    # look for color
    for y in range(150, 200, SkipPixel):
        for x in range(95, 195, SkipPixel):

            if LowerColorRange[0] < screen[y, x, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x, 2] < UpperColorRange[2]:
                if LowerColorRange[0] < screen[y, x+1, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x+1, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x+1, 2] < UpperColorRange[2]:
                     if Firstfoundx == False:
                        img = cv2.circle(screen, (x, y), 1, (255, 0, 0), 4)
                        Firstfoundx = True

                if LowerColorRange[0] < screen[y, x-1, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x-1, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x-1, 2] < UpperColorRange[2]:
                    if Lastfoundx == False:
                        img = cv2.circle(screen, (x, y), 1, (255, 0, 0), 4)
                        Lastfoundx = True


                FoundCount += 1
            else:
                img = screen

    # auto correction
    if FoundCount < 5:
        Correction = Correction + 1 + FoundCount / 80
    if FoundCount > 60:
        Correction = Correction - 1 - FoundCount / 80

    # reset / updates
    TopX = 0
    TopY = 0
    TopX2 = 0
    TopY2 = 0
    Firstfoundx = False
    Lastfoundx = False

    FoundCount = 0

    cv2.rectangle(screen, (95, 150), (195, 200), (255, 0, 0), 1)

    cv2.imshow("Map", screen)

    # if pressed close window
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break