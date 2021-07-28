
import numpy as np

"""
Implements denoising using OpenCV.
"""
import cv2

class GetCapturedVideo():
    """
    Get a video frame from a video file.
    """
    capture = cv2.VideoCapture(r"C:\Users\sydni\Downloads\input.mp4")
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    ret = capture.set(3, frame_width)
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ret = capture.set(4, frame_height)

    fourcc = cv2.VideoWriter_fourcc(*"XPID")
    out = cv2.VideoWriter("output8.avi", fourcc, 20.0, (frame_width, frame_height))

    def Get_FramesforCheck(self ):
        """Summary  of the Function

        Purpose
           To check if there are any frames available

          If the function returns true,the next frame will be taken
        """
    while capture.isOpened():
        ret, frame = capture.read()
        if ret is True:
            gaussianblur = cv2.GaussianBlur(frame, (5, 5), 0)
            """
             Blurs a gray frame using a Gaussian blur.
             """
            dst = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
            """
            Implements denoising using OpenCV.
            """
            # write the flipped frame
            out.write(frame)
            cv2.imshow("frame", dst)
            # cv2.imshow(window_name, image)

        else:
            break
    # .waitKey(0) will display the window infinitely until any keypress (it is suitable for image display).
    # 2.waitKey(1) will display a frame for 1 ms, after which display will be automatically closed. Since the OS has a
    key = cv2.waitKey(1)
    if key == ord("q"):
break
# Release everything if job is finished cap. release() and cv2. destroyAllWindows() are the methods to close video
# files or the capturing device, and destroy the window, which was created by the imshow method. ... The further dive
# into OpenCV for video processing is up to the reader.
capture.release()
out.release()
cv2.destroyAllWindows()
