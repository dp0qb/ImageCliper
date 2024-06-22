import cv2
import numpy as np
import PySimpleGUI as sg



def crop(input_fname, fname, width, height):
    img = cv2.imread(input_fname).astype(np.uint8)
    origin_size = img.shape
    origin_aspect_ratio = round(origin_size[0] / origin_size[1], 4)

    target_aspect_ratio = round(height / width, 4)

    if origin_aspect_ratio < target_aspect_ratio:
        target_width = int(origin_size[0] / target_aspect_ratio)
        left = int((origin_size[1] - target_width) / 2)
        right = left + target_width

        img = img[0: origin_size[0], left: right]
    
    elif origin_aspect_ratio > target_aspect_ratio:
        target_height = int(origin_size[1] * target_aspect_ratio)
        top = int((origin_size[1] - target_height) / 2)
        bottom = top + target_height

        img = img[top: bottom, 0: origin_size[1]]
    
    new_img = cv2.resize(img, (width, height))
    cv2.imwrite(fname, new_img)


def main():
    support_file_type = ["bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp", "pbm", "pgm", "ppm", "pxm", "pnm", "tiff", "tiff"]
    layout = [
        [sg.I(size=(22, 2)), sg.FileBrowse(key="-filename-")],
        [sg.T('size:'), sg.I(size=(6, 2), key="-width-"), sg.T('x'), sg.I(size=(6, 2), key="-height-"), sg.B("Save")],
    ]

    title = "Image Cliper"
    window = sg.Window(title=title, layout=layout)

    while True:
        events, value = window.read()

        if events == "Save":
            file_type = value["-filename-"].split('.')[-1]
            if file_type not in support_file_type:
                sg.popup("Not supported file type!")
            elif not value["-width-"].isdigit() or not value["-height-"].isdigit():
                sg.popup("Please input both width and height correctly!")
            else:
                width = int(value["-width-"])
                height = int(value["-height-"])
                fname = value["-filename-"].replace(f".{file_type}", f"_{width}x{height}.{file_type}")
                try:
                    crop(value["-filename-"], fname, width, height)
                except:
                    sg.popup("Unknow error!")

        if events == None:
            break


if __name__=="__main__":
    main()