# Python program to implement
# Webcam Motion Detector

# importing OpenCV, time and Pandas library
import cv2, time, pandas, pyautogui
import tkinter as tk

# importing datetime class from datetime library
from datetime import datetime

rectanglex0 = rectangley0 = rectanglex1 = rectangley1 = 0

alt_tab = False

backgroundpic = cv2.VideoCapture(0)
ret, frame = backgroundpic.read()

while True:
    cv2.imwrite('C:\\Users\\shrey\\PycharmProjects\\pythonProject\\Evade\\background.png', frame)
    cv2.destroyAllWindows()
    break

backgroundpic.release()


class RectangleDrawer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.x2 = self.y2 = 0
        self.title("WAYD")
        self.iconphoto(False, tk.PhotoImage(file="C:\\Users\\shrey\\PycharmProjects\\pythonProject\\Evade\\icon.png"))
        self.filename = tk.PhotoImage(file='C:\\Users\\shrey\\PycharmProjects\\pythonProject\\Evade\\background.png')
        self.background_label = tk.Label(self, image=self.filename)
        self.background_label.bind("<ButtonPress-1>", self.on_button_press)
        self.background_label.bind("<ButtonRelease-1>", self.on_button_release)
        self.background_label.pack()

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        x0,y0 = (self.x, self.y)
        self.x2 = event.x
        self.y2 = event.y
        x1,y1 = (event.x, event.y)

        if x0 > self.x2:
            temp = self.x2
            self.x2 = x0
            self.x = temp

            tempy = self.y2
            self.y2 = y0
            self.y = tempy
        # self.background_label.create_rectangle(x0,y0,x1,y1, fill="black")
        self.destroy()

rectanglething = RectangleDrawer()

rectanglething.mainloop()
rectanglex0 = rectanglething.x
rectangley0 = rectanglething.y
rectanglex1 = rectanglething.x2
rectangley1 = rectanglething.y2

print(rectanglex0,rectangley0,rectanglex1,rectangley1)


# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [None, None]

# Time of movement
time = []

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns=["Start", "End"])

# Capturing video
video = cv2.VideoCapture(0)


userx = rectanglex0
userx1 = rectanglex1
usery = rectangley0
usery1 = rectangley1
# Infinite while loop to treat stack of image as video

while True:
    # Reading frame(image) from video
    check, frame = video.read()
    crop = frame[usery:usery1+1, userx:userx1+1]

    # Initializing motion = 0(no motion)
    motion = 0

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur
    # so that change can be find easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # In first iteration we assign the value
    # of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue

    # Difference between static background
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)

    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 50, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contour of moving object
    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000 and not alt_tab:
            alt_tab = True
            pyautogui.hotkey('alt', 'tab')
            continue
        motion = 1

        (x, y, w, h) = cv2.boundingRect(contour)
          # making green rectangle around the moving object
        cv2.rectangle(frame, (rectanglex0 + w, rectangley0 + h), (rectanglex0 + x, rectangley0 + y), (0, 255, 0), 2)
        cv2.putText(frame, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 3)
        # pyautogui.hotkey('alt', 'tab')

    cv2.rectangle(frame, (rectanglex0, rectangley0), (rectanglex1, rectangley1), (230, 216, 173), 3)

    # Appending status of motion
    motion_list.append(motion)

    motion_list = motion_list[-2:]

    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time.append(datetime.now())

    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time.append(datetime.now())

    # Debug screens (grayscale and threshold view)
    # cv2.imshow("Gray Frame", gray)
    # cv2.imshow("Threshold Frame", thresh_frame)

    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        # if something is moving then it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break

# Appending time of motion in DataFrame
for i in range(0, len(time), 2):
    df = df.append({"Start": time[i], "End": time[i + 1]}, ignore_index=True)

# Creating a CSV file in which time of movements will be saved
df.to_csv("Time_of_movements.csv")

video.release()

# Destroying all the windows
cv2.destroyAllWindows()