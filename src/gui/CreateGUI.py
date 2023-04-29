import asyncio
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from mazeLib import *

from src.library.lib import positionWindow


class CreateGUI:

    # Properly close window
    def close(self):
        self.worker.call_soon_threadsafe(self.worker.stop)
        self.window.destroy()

    # Create maze
    async def processCreate(self):
        print("Starting maze creating...")

        generator = None
        if self.settings["seed"].get() == "0":
            generator = Algorithm.getGenerator(self.settings["generator"].get())
        else:
            # TODO: Fix seed from int to long
            generator = Algorithm.getGenerator(self.settings["generator"].get(), self.settings["seed"].get())

        print(" - Generator: " + self.settings["generator"].get())
        print(" - Seed: " + self.settings["seed"].get())

        mazeBuilder = generator.generate(self.settings["width"].get(), self.settings["height"].get())
        if mazeBuilder.hasError():
            print("Maze creating failed! Error: " + mazeBuilder.error)
            return messagebox.showerror('MazeLib', 'Error: Some parameters has wrong configuration. \nError: ' + mazeBuilder.error)
        mazeBuilder = mazeBuilder.value()

        mazeBuilder.setPathWidth(self.settings["pathWidth"].get())
        mazeBuilder.setWallWidth(self.settings["wallWidth"].get())
        mazeBuilder.setStart((self.settings["startX"].get(), self.settings["startY"].get()))
        mazeBuilder.setEnd((self.settings["endX"].get(), self.settings["endY"].get()))

        maze = mazeBuilder.buildExpected()
        if maze.hasError():
            print("Maze building failed! Error: " + maze.error)
            return messagebox.showerror('MazeLib', 'Error: Some parameters has wrong configuration. \nError: ' + maze.error)
        maze = maze.value()

        self.master.mazes.append(("createdMaze-" + str(maze.getSeed()), maze, None))
        self.master.listVar.set([x[0] for x in self.master.mazes])
        self.close()

        print("Maze building finished.")
        return messagebox.showinfo("MazeLib", "Successful: Maze created successfully.")

    def startCreate(self):
        self.button.config(state="disabled")
        asyncio.run_coroutine_threadsafe(self.processCreate(), self.worker)

    def draw(self):
        topFrame = tk.Frame(self.window)
        topFrame.pack(side="top", fill="x", expand=True, pady=5, padx=5)

        def drawTop():
            label = tk.Label(topFrame, text="Vytvoření bludiště", font=("Arial", 12, "bold"))
            label.pack(side="left", fill="x", expand=True, pady=(5, 0))

            backButton = tk.Button(topFrame, text="Zpět", command=lambda: self.window.destroy(), width=10)
            backButton.pack(side="left", padx=10)
        drawTop()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=(5, 0), padx=5)

        def drawFields():
            fieldFrame = tk.Frame(self.window)
            fieldFrame.pack(side="top", fill="y", padx=5, pady=5)

            def isDigit(string):
                return string.isdigit()

            def drawGenerators():
                generatorRow = tk.Frame(fieldFrame)
                generatorRow.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                generatorLabel = tk.Label(generatorRow, text="Generator:", width=15, anchor="w")
                generatorLabel.pack(side="left")

                self.settings["generator"] = tk.StringVar()
                generatorOptions = [x.getName() for x in Algorithm.getGenerators()]
                self.settings["generator"].set(generatorOptions[0])
                generatorMenu = tk.OptionMenu(generatorRow, self.settings["generator"], *generatorOptions)
                generatorMenu.pack(side="left", fill="x", expand=True)
            drawGenerators()

            def drawSeed():
                seedRow = tk.Frame(fieldFrame)
                seedRow.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                seedLabel = tk.Label(seedRow, text="Seed:", width=15, anchor="w")
                seedLabel.pack(side="left")

                self.settings["seed"] = tk.StringVar()
                self.settings["seed"].set("0")
                seedEntry = tk.Spinbox(seedRow, width=10, textvariable=self.settings["seed"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                seedEntry.pack(side="left", fill="x", expand=True)

                randomizeButton = tk.Button(seedRow, text="Rand", command=lambda: self.settings["seed"].set(str(random.randint(0, 999999999999999))), width=5)
                randomizeButton.pack(side="left", padx=5)
            drawSeed()

            def drawWidth():
                widthRow = tk.Frame(fieldFrame)
                widthRow.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                widthLabel = tk.Label(widthRow, text="Šířka:", width=15, anchor="w")
                widthLabel.pack(side="left")

                self.settings["width"] = tk.IntVar()
                self.settings["width"].set(25)
                widthSpinbox = tk.Spinbox(widthRow, width=10, from_=1, to=1000, textvariable=self.settings["width"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                widthSpinbox.pack(side="left", fill="x", expand=True)
            drawWidth()

            def drawHeight():
                heightRow = tk.Frame(fieldFrame)
                heightRow.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                heightLabel = tk.Label(heightRow, text="Výška:", width=15, anchor="w")
                heightLabel.pack(side="left")

                self.settings["height"] = tk.IntVar()
                self.settings["height"].set(25)
                heightEntry = tk.Spinbox(heightRow, width=10, from_=1, to=1000, textvariable=self.settings["height"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                heightEntry.pack(side="left", fill="x", expand=True)
            drawHeight()

            ttk.Separator(fieldFrame, orient="horizontal").grid(row=4, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

            def drawPathWidth():
                pathWidthRow = tk.Frame(fieldFrame)
                pathWidthRow.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                pathWidthLabel = tk.Label(pathWidthRow, text="Šířka cesty:", width=15, anchor="w")
                pathWidthLabel.pack(side="left")

                self.settings["pathWidth"] = tk.IntVar()
                self.settings["pathWidth"].set(15)
                pathWidthEntry = tk.Spinbox(pathWidthRow, width=10, from_=1, to=1000, textvariable=self.settings["pathWidth"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                pathWidthEntry.pack(side="left", fill="x", expand=True)
            drawPathWidth()

            def drawWallWidth():
                wallWidthRow = tk.Frame(fieldFrame)
                wallWidthRow.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                wallWidthLabel = tk.Label(wallWidthRow, text="Šířka zdi:", width=15, anchor="w")
                wallWidthLabel.pack(side="left")

                self.settings["wallWidth"] = tk.IntVar()
                self.settings["wallWidth"].set(3)
                wallWidthEntry = tk.Spinbox(wallWidthRow, width=10, from_=1, to=1000, textvariable=self.settings["wallWidth"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                wallWidthEntry.pack(side="left", fill="x", expand=True)
            drawWallWidth()

            def drawStart():
                startPointRow = tk.Frame(fieldFrame)
                startPointRow.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                startPointLabel = tk.Label(startPointRow, text="Počáteční bod:", width=15, anchor="w")
                startPointLabel.pack(side="left")

                self.settings["startX"] = tk.IntVar()
                self.settings["startX"].set(0)
                startPointXEntry = tk.Spinbox(startPointRow, width=10, from_=0, to=1000, textvariable=self.settings["startX"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                startPointXEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))

                self.settings["startY"] = tk.IntVar()
                self.settings["startY"].set(0)
                startPointYEntry = tk.Spinbox(startPointRow, width=10, from_=0, to=1000, textvariable=self.settings["startY"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                startPointYEntry.pack(side="left", fill="x", expand=True, padx=(5, 0))
            drawStart()

            def drawEnd():
                endPointRow = tk.Frame(fieldFrame)
                endPointRow.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

                endPointLabel = tk.Label(endPointRow, text="Koncový bod:", width=15, anchor="w")
                endPointLabel.pack(side="left")

                self.settings["endX"] = tk.IntVar()
                self.settings["endX"].set(24)
                endPointXEntry = tk.Spinbox(endPointRow, width=10, from_=0, to=1000, textvariable=self.settings["endX"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                endPointXEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))

                self.settings["endY"] = tk.IntVar()
                self.settings["endY"].set(24)
                endPointYEntry = tk.Spinbox(endPointRow, width=10, from_=0, to=1000, textvariable=self.settings["endY"], validate="key", validatecommand=(self.window.register(isDigit), "%P"))
                endPointYEntry.pack(side="left", fill="x", expand=True, padx=(5, 0))
            drawEnd()
        drawFields()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

        self.button = tk.Button(self.window, text="Vytvořit", command=lambda: self.startCreate())
        self.button.pack(side="top", padx=5, pady=(0, 10), fill="x", expand=True)

    def __init__(self, master):
        self.master = master

        # Window
        self.window = tk.Toplevel(master)
        self.window.transient(master)
        self.window.title("MazeLib - Vytvoření bludiště")
        self.window.resizable(False, False)
        self.window.grab_set()
        positionWindow(self.window, 390, 250)

        # Variables
        self.settings = {}
        self.button = None
        self.worker = None

        # Run the asyncio event loop in a worker thread.
        def asyncWorker():
            self.worker = asyncio.new_event_loop()
            asyncio.set_event_loop(self.worker)
            self.worker.run_forever()
        threading.Thread(target=asyncWorker).start()

        # Stop worker thread when window is closed.
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.close())

        # Draw window
        self.draw()
