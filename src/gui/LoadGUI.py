from tkinter import ttk, filedialog, messagebox

from mazeLib import TextFileLoadingMethod


class LoadGUI:

    def processLoad(self):
        file = filedialog.askopenfile(parent=self.master, title='MazeLib - Načtení bludiště', filetypes=[('Maze files', '*.txt;*.json')])

        if file is not None:
            mazeBuilder = TextFileLoadingMethod.load(file.name)
            if mazeBuilder.hasError():
                print("Loading maze from file failed! Error: " + mazeBuilder.error)
                return messagebox.showerror("MazeLib", "Error: Maze file is corrupted! \nError: " + mazeBuilder.error)
            mazeBuilder = mazeBuilder.value()

            maze = mazeBuilder.buildExpected()
            if maze.hasError():
                print("Building maze from file failed! Error: " + maze.error)
                return messagebox.showerror("MazeLib", "Error: Maze file is corrupted! \nError: " + maze.error)
            maze = maze.value()

            self.master.mazes.append((file.name, maze, None))
            self.master.listVar.set([x[0] for x in self.master.mazes])

            print("Loaded maze " + file.name + " successfully!")
            return messagebox.showinfo("MazeLib", "Successful: Maze loaded successfully!")

        # print("Loading maze from file failed! Error: File corrupted or not found")
        # return messagebox.showerror("MazeLib", "Error: Maze file corrupted or not found!")

    def __init__(self, master):
        self.master = master
        self.processLoad()
