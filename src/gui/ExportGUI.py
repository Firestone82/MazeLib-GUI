import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from mazeLib import *

from src.library.lib import centerWindow, positionWindow


class ExportGUI:

    def processExport(self):
        run = False

        if self.settings["pathToFileCheck"].get():
            if self.master.maze[2] is not None:
                TextFileSavingMethod.save(self.master.maze[1], self.settings["pathToFile"].get() + "/maze-" + str(self.master.maze[1].getSeed()) + ".txt", self.master.maze[2])
            else:
                TextFileSavingMethod.save(self.master.maze[1], self.settings["pathToFile"].get())

            run = True

        if self.settings["pathToImageCheck"].get():
            ImageSavingMethod.save(self.master.maze[1], self.settings["pathToImage"].get())

            if self.master.maze[2] is not None:
                pathArgs = self.settings["pathToImage"].get().split(".")
                pathArgs[-2] += "-Solved"
                path = ".".join(pathArgs)
                ImageSavingMethod.save(self.master.maze[1], path, self.master.maze[2])

            run = True

        self.window.destroy()

        if run:
            print("Successfully exported maze.")
            return messagebox.showinfo("MazeLib", "Successful: Maze exported successfully")

    def draw(self):
        topFrame = tk.Frame(self.window)
        topFrame.pack(side="top", fill="x", expand=True, pady=5, padx=5)

        def drawTop():
            labelRow = tk.Frame(self.window)
            labelRow.pack(side="top", fill="x", expand=True)

            label = tk.Label(labelRow, text="Exportovat bludiště", font=("Arial", 12, "bold"))
            label.pack(side="left", fill="x", expand=True)

            backButton = tk.Button(labelRow, text="Zpět", command=lambda: self.back(), width=10)
            backButton.pack(side="left", padx=10)
        drawTop()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=(5, 0), padx=5)

        def drawFields():
            fieldFrame = tk.Frame(self.window)
            fieldFrame.pack(side="top", fill="both", padx=5, pady=5)

            def drawPathToFile():
                pathToFileRow = tk.Frame(fieldFrame)
                pathToFileRow.pack(side="top", fill="x")

                pathToFileLabelRow = tk.Frame(pathToFileRow)
                pathToFileLabelRow.pack(side="top", fill="x", pady=(5, 0))

                pathToFileEntryRow = tk.Frame(pathToFileRow)
                pathToFileEntryRow.pack(side="top", fill="x", padx=5)

                self.settings["pathToFileCheck"] = tk.IntVar()
                pathToFileCheck = tk.Checkbutton(pathToFileLabelRow, text="Uložit", variable=self.settings["pathToFileCheck"], command=lambda: dialogButton.config(state="normal" if self.settings["pathToFileCheck"].get() else "disabled"))
                pathToFileCheck.pack(side="left")

                pathToFileLabel = tk.Label(pathToFileLabelRow, text="Cesta k uložení souboru:", anchor="w")
                pathToFileLabel.pack(side="left", anchor="w")

                self.settings["pathToFile"] = tk.StringVar()
                self.settings["pathToFile"].set("C:/Users/Pavel/VSB-TUO/Login/MIK0486")
                pathToFileEntry = tk.Entry(pathToFileEntryRow, textvariable=self.settings["pathToFile"], width=50)
                pathToFileEntry.config(state="disabled")
                pathToFileEntry.pack(side="left", fill="x", expand=True)

                def dialogFile():
                    self.settings["pathToFile"].set(filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")]))

                dialogButton = tk.Button(pathToFileEntryRow, text="Zvolit", command=dialogFile)
                dialogButton.config(state="disabled")
                dialogButton.pack(side="left", padx=(5, 0))
            drawPathToFile()

            def drawPathToImage():
                pathToImageRow = tk.Frame(fieldFrame)
                pathToImageRow.pack(side="top", fill="x")

                pathToImageLabelRow = tk.Frame(pathToImageRow)
                pathToImageLabelRow.pack(side="top", fill="x", pady=(5, 0))

                pathToImageEntryRow = tk.Frame(pathToImageRow)
                pathToImageEntryRow.pack(side="top", fill="x", padx=5)

                self.settings["pathToImageCheck"] = tk.IntVar()
                pathToImageCheck = tk.Checkbutton(pathToImageLabelRow, text="Uložit", variable=self.settings["pathToImageCheck"], command=lambda: dialogButton.config(state="normal" if self.settings["pathToImageCheck"].get() else "disabled"))
                pathToImageCheck.pack(side="left")

                pathToImageLabel = tk.Label(pathToImageLabelRow, text="Cesta k uložení obrázku:", anchor="w")
                pathToImageLabel.pack(side="left", anchor="w")

                self.settings["pathToImage"] = tk.StringVar()
                self.settings["pathToImage"].set("C:/Users/Pavel/VSB-TUO/Login/MIK0486")
                pathToImageEntry = tk.Entry(pathToImageEntryRow, textvariable=self.settings["pathToImage"], width=50)
                pathToImageEntry.config(state="disabled")
                pathToImageEntry.pack(side="left", fill="x", expand=True)

                def dialogFile():
                    self.settings["pathToImage"].set(filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image file", "*.png")]))

                dialogButton = tk.Button(pathToImageEntryRow, text="Zvolit", command=dialogFile)
                dialogButton.config(state="disabled")
                dialogButton.pack(side="left", padx=(5, 0))
            drawPathToImage()
        drawFields()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

        exportButton = tk.Button(self.window, text="Exportovat", command=lambda: self.processExport())
        exportButton.pack(side="top", padx=10, pady=(0, 10), fill="x", expand=True)

    def __init__(self, master):
        self.master = master

        # Window
        self.window = tk.Toplevel(master)
        self.window.transient(master)
        self.window.title("MazeLib - Exportování bludiště")
        self.window.resizable(False, False)
        self.window.grab_set()
        positionWindow(self.window, 310, 250)

        # Variables
        self.settings = {}

        # Draw window
        self.draw()
