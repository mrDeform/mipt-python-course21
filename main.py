from tkinter import *
from PIL import Image, ImageTk
import cv2
from tkinter.messagebox import showinfo


class App:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Final task")
        self.video_source = video_source
        self.vid = Video(video_source)

        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.lbl = Label(window, text="Название кадра:")
        self.lbl.pack(side=LEFT, padx=5, pady=10)

        self.name = Entry(window, width=40)
        self.name.pack(side=LEFT, padx=10, pady=10)

        self.btn = Button(window, text="Сохранить скриншот", width=20, command=self.screenshot)
        self.btn.pack(side=LEFT, padx=10, pady=10)

        self.scale = Scale(window, orient="horizontal", resolution=1, from_=-100, to=100)
        self.scale.pack(side=LEFT, padx=30)

        self.btn = Button(window, text="Закрыть", width=15, command=self.close)
        self.btn.pack(side=LEFT, padx=10, pady=10)

        self.idle()

        self.window.mainloop()

    def screenshot(self):
        frame = self.get_finish_frame()
        name_screenshot = self.name.get() + ".jpg"
        cv2.imwrite(name_screenshot, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        showinfo(title='SAVED', message=name_screenshot)


    def idle(self):
        frame = self.get_finish_frame()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(20, self.idle)

    def get_finish_frame(self):
        success, hsv = self.vid.get_frame()
        if success:
            value = self.scale.get()
            if value > 0:
                limit = 255 - value
                hsv[:, :, 2][hsv[:, :, 2] > limit] = 255
                hsv[:, :, 2][hsv[:, :, 2] <= limit] += value
            elif value < 0:
                value *= -1
                hsv[:, :, 2][hsv[:, :, 2] < value] = 0
                hsv[:, :, 2][hsv[:, :, 2] >= value] -= value
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        else:
            raise ValueError("Unable to open video source", self.video_source)

    def close(self):
        del self.vid
        self.window.destroy()


class Video:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            success, frame = self.vid.read()
            if success:
                return success, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            else:
                self.vid.set(2, frame)
                success, frame = self.vid.read()
                if success:
                    return success, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                else:
                    return success, None
        else:
            raise ValueError("Unable to open video source", self.video_source)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def main():
    root = Tk()
    App(root, 0)
    # App(root, "D:/a.mp4")
    # App(root, "http://192.168.0.101:8080/video")


if __name__ == '__main__':
    main()
