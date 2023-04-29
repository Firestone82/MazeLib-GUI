import os


def getAllFiles(path, extension=None):
    files = []

    for file in os.listdir(path):
        if os.path.isdir(path + "/" + file):
            continue

        if extension is not None:
            if file.endswith(extension):
                files.append(file)
        else:
            files.append(file)

    return files


def centerWindow(root, width=300, height=200, x=0, y=0):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2) + x
    y = (screen_height / 2) - (height / 2) + y
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def positionWindow(root, xOff=0, yOff=0):
    x = root.winfo_x()
    y = root.winfo_y()
    root.geometry("+%d+%d" % (x + xOff, y + yOff))
