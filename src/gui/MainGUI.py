import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from mazeLib import *

from src.gui.CreateGUI import CreateGUI
from src.gui.ExportGUI import ExportGUI
from src.gui.LoadGUI import LoadGUI
from src.gui.SolveGUI import SolveGUI
from src.gui.TestGUI import TestGUI
from src.library.lib import *


class MainGUI(tk.Tk):

    def loadCanvas(self):
        if self.list.curselection():
            self.maze = self.mazes[self.list.curselection()[0]]
        else:
            return

        print("Selecting maze " + self.maze[0] + "... Solved: " + ("No" if self.maze[2] is None else "Yes"))

        self.mazeInfo["width"].set(self.maze[1].getWidth())
        self.mazeInfo["height"].set(self.maze[1].getHeight())
        self.mazeInfo["algorithm"].set(self.maze[1].getGenerationAlgorithm())
        self.mazeInfo["generationTime"].set(str(round(float(self.maze[1].getGenerationTime()) / 1000 / 1000, 2)) + "ms")
        self.mazeInfo["start"].set(str(self.maze[1].getStart()[0]) + ", " + str(self.maze[1].getStart()[1]))
        self.mazeInfo["end"].set(str(self.maze[1].getEnd()[0]) + ", " + str(self.maze[1].getEnd()[1]))
        self.mazeInfo["seed"].set(self.maze[1].getSeed())
        self.mazeInfo["pathWidth"].set(self.maze[1].getPathWidth())
        self.mazeInfo["wallWidth"].set(self.maze[1].getWallWidth())

        path = "mazes/temp/" + str(self.maze[1].getSeed()) + ".png"
        if self.maze[2] is not None:
            self.mazeInfo["length"].set(self.maze[2].getLength())

            if Path("mazes/temp/" + str(self.maze[1].getSeed()) + "-S.png").is_file():
                path = "mazes/temp/" + str(self.maze[1].getSeed()) + "-S.png"
        else:
            self.mazeInfo["length"].set("N/A")

            if not Path("mazes/temp/" + str(self.maze[1].getSeed()) + ".png").is_file():
                ImageSavingMethod.save(self.maze[1], "mazes/temp/" + str(self.maze[1].getSeed()) + ".png")

        self.photo = tk.PhotoImage(file=path)
        self.image_id = self.canvas.create_image(self.photo.width() / 2, self.photo.height() / 2, image=self.photo)
        self.canvas.itemconfig(self.image_id, image=self.photo)

    def emptyCanvas(self):
        for info in self.mazeInfo:
            self.mazeInfo[info].set("N/A")

        self.photo = tk.PhotoImage(file="mazes/temp/empty.png")
        self.image_id = self.canvas.create_image(self.photo.width() / 2, self.photo.height() / 2, image=self.photo)
        self.canvas.itemconfig(self.image_id, image=self.photo)

    def processSearch(self, sv):
        self.list.delete(0, "end")

        for i, maze in enumerate(self.mazes):
            if sv.get().lower() in maze[0].lower():
                self.list.insert(i, maze[0])

    def processButton(self, button):
        if self.maze is not None:

            # Delete maze
            if button == "delete":
                self.maze = None
                self.mazes.remove(self.mazes[self.list.curselection()[0]])
                self.listVar.set([x[0] for x in self.mazes])

                return self.emptyCanvas()

            # Solve maze
            if button == "solve":
                return SolveGUI(self)

            # Test maze
            if button == "test":
                return TestGUI(self)

            # Export maze
            if button == "export":
                return ExportGUI(self)

        elif button in ["delete", "solve", "test", "export"]:
            messagebox.showerror("MazeLib", "Error! - No maze selected!")
            return print("No maze selected!")

        # Load maze
        if button == "load":
            return LoadGUI(self)

        # Create maze
        if button == "create":
            return CreateGUI(self)

        # Refresh list
        if button == "refresh":
            self.mazes = []
            self.maze = None
            self.emptyCanvas()

            for file in getAllFiles("mazes"):
                mazeBuilder = TextFileLoadingMethod.load("mazes/" + file)
                if mazeBuilder.hasError():
                    print("Loading maze " + file + " failed! Error: " + mazeBuilder.error)
                    continue
                mazeBuilder = mazeBuilder.value()

                maze = mazeBuilder.buildExpected()
                if maze.hasError():
                    print("Building maze " + file + " failed! Error: " + maze.error)
                    continue
                maze = maze.value()

                self.mazes.append((file, maze, None))
                print("Loaded maze " + file + " successfully!")

            self.listVar.set([x[0] for x in self.mazes])

    def drawMain(self):
        def drawLeft():
            leftFrame = tk.Frame(self.master)
            leftFrame.pack(side="left", pady=5, padx=5, fill="y")

            def drawLabel():
                labelRow = tk.Frame(leftFrame)
                labelRow.pack(side="top", fill="x")

                leftLabel = tk.Label(labelRow, text="Seznam bludišť", font=("Arial", 12, "bold"))
                leftLabel.pack(side="left", fill="x", expand=True)

                refreshButton = tk.Button(labelRow, text="Obnovit", command=lambda: self.processButton("refresh"))
                refreshButton.pack(side="right", padx=5)

            drawLabel()

            ttk.Separator(leftFrame, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

            def drawButtons():
                leftButtonFrame = tk.Frame(leftFrame)
                leftButtonFrame.pack(side="top")

                createButton = tk.Button(leftButtonFrame, text="Vytvořit bludiště", command=lambda: self.processButton("create"))
                createButton.pack(side="left", padx=5)

                loadButton = tk.Button(leftButtonFrame, text="Načíst bludiště", command=lambda: self.processButton("load"))
                loadButton.pack(side="left", padx=5)

                deleteButton = tk.Button(leftButtonFrame, text="Smazat bludiště", command=lambda: self.processButton("delete"))
                deleteButton.pack(side="left", padx=5)
            drawButtons()

            ttk.Separator(leftFrame, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

            def drawSearch():
                searchRow = tk.Frame(leftFrame)
                searchRow.pack(side="top", fill="x")

                searchLabel = tk.Label(searchRow, text="Filtrovat:")
                searchLabel.pack(side="left", fill="x", padx=5)

                searchVar = tk.StringVar()
                searchVar.trace("w", lambda name, index, mode, sv=searchVar: self.processSearch(sv))

                searchEntry = tk.Entry(searchRow, textvariable=searchVar)
                searchEntry.pack(side="left", fill="x", expand=True, padx=5)
            drawSearch()

            def drawList():
                listRow = tk.Frame(leftFrame)
                listRow.pack(side="top", fill="both", expand=True)

                self.listVar = tk.Variable(value=self.mazes)

                self.list = tk.Listbox(listRow, listvariable=self.listVar, height=6, selectforeground="white", selectbackground="#666666", selectmode="single")
                self.list.pack(side="left", fill="both", expand=True, padx=5, pady=5)

                scrollbar = tk.Scrollbar(listRow)
                scrollbar.pack(side="right", fill="y", padx=(0, 5))
                scrollbar.config(command=self.list.yview)

                self.list.bind("<<ListboxSelect>>", lambda e: self.loadCanvas())
                self.list.config(yscrollcommand=scrollbar.set)
            drawList()

            def drawInfo():
                infoRow = tk.Frame(leftFrame)
                infoRow.pack(side="top", fill="x", anchor="w")

                def drawInnerLabel():
                    labelRow = tk.Frame(infoRow)
                    labelRow.pack(side="top", fill="x", anchor="w")

                    infoLabel = tk.Label(labelRow, text="Informace o vybraném bludišti:")
                    infoLabel.pack(side="left", anchor="w", padx=5)

                drawInnerLabel()

                ttk.Separator(infoRow, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

                def drawSize():
                    sizeRow = tk.Frame(infoRow)
                    sizeRow.pack(side="top", fill="x", anchor="w")

                    widthLabel = tk.Label(sizeRow, text="Šířka: ", width=5)
                    widthLabel.pack(side="left", anchor="w", padx=(5, 0))

                    widthVar = tk.StringVar(value="0")
                    widthEntry = tk.Entry(sizeRow, textvariable=widthVar, width=2)
                    widthEntry.config(state="disabled")
                    widthEntry.pack(side="left", fill="x", expand=True)
                    self.mazeInfo["width"] = widthVar

                    heightLabel = tk.Label(sizeRow, text="Výška: ", width=5)
                    heightLabel.pack(side="left", anchor="w", padx=(5, 0))

                    heightVar = tk.StringVar(value="0")
                    heightEntry = tk.Entry(sizeRow, textvariable=heightVar, width=2)
                    heightEntry.config(state="disabled")
                    heightEntry.pack(side="left", fill="x", expand=True)
                    self.mazeInfo["height"] = heightVar

                    seedLabel = tk.Label(sizeRow, text="Seed: ", width=5)
                    seedLabel.pack(side="left", anchor="w", padx=(5, 0))

                    seedVar = tk.StringVar(value="...")
                    seedEntry = tk.Entry(sizeRow, textvariable=seedVar, width=5)
                    seedEntry.config(state="disabled")
                    seedEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))
                    self.mazeInfo["seed"] = seedVar
                drawSize()

                def drawOptions():
                    optionRow = tk.Frame(infoRow)
                    optionRow.pack(side="top", fill="x", anchor="w")

                    startLabel = tk.Label(optionRow, text="Start: ", width=5)
                    startLabel.pack(side="left", anchor="w", padx=(5, 0))

                    startVar = tk.StringVar(value="0, 0")
                    startEntry = tk.Entry(optionRow, textvariable=startVar, width=2)
                    startEntry.config(state="disabled")
                    startEntry.pack(side="left", fill="x", expand=True)
                    self.mazeInfo["start"] = startVar

                    endLabel = tk.Label(optionRow, text="Cíl: ", width=5)
                    endLabel.pack(side="left", anchor="w", padx=(5, 0))

                    endVar = tk.StringVar(value="0, 0")
                    endEntry = tk.Entry(optionRow, textvariable=endVar, width=2)
                    endEntry.config(state="disabled")
                    endEntry.pack(side="left", fill="x", expand=True)
                    self.mazeInfo["end"] = endVar

                    lengthLabel = tk.Label(optionRow, text="Délka: ", width=5)
                    lengthLabel.pack(side="left", anchor="w", padx=(5, 0))

                    lengthVar = tk.StringVar(value="0")
                    lengthEntry = tk.Entry(optionRow, textvariable=lengthVar, width=5)
                    lengthEntry.config(state="disabled")
                    lengthEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))
                    self.mazeInfo["length"] = lengthVar
                drawOptions()

                def drawAlgorithm():
                    algoRow = tk.Frame(infoRow)
                    algoRow.pack(side="top", fill="x", anchor="w")

                    algorithmLabel = tk.Label(algoRow, text="Generátor: ", width=10)
                    algorithmLabel.grid(row=0, column=0, padx=(5, 0))

                    algorithmVar = tk.StringVar(value="...")
                    algorithmEntry = tk.Entry(algoRow, textvariable=algorithmVar, width=5)
                    algorithmEntry.config(state="disabled", width=11)
                    algorithmEntry.grid(row=0, column=1, padx=(0, 5))
                    self.mazeInfo["algorithm"] = algorithmVar

                    generationTmeLabel = tk.Label(algoRow, text="Čas gener.: ", width=10)
                    generationTmeLabel.grid(row=0, column=2, padx=(5, 0))

                    generationTimeVar = tk.StringVar(value="0ms")
                    generationTimeEntry = tk.Entry(algoRow, textvariable=generationTimeVar, width=5)
                    generationTimeEntry.config(state="disabled", width=11)
                    generationTimeEntry.grid(row=0, column=3, padx=(0, 5))
                    self.mazeInfo["generationTime"] = generationTimeVar
                drawAlgorithm()

                def drawOptions2():
                    optionRow2 = tk.Frame(infoRow)
                    optionRow2.pack(side="top", fill="x")

                    pathWidthLabel = tk.Label(optionRow2, text="Šířka cesty: ", width=10)
                    pathWidthLabel.grid(row=0, column=0, padx=(5, 0))

                    pathWidthVar = tk.StringVar(value="0")
                    pathWidthEntry = tk.Entry(optionRow2, textvariable=pathWidthVar, width=5)
                    pathWidthEntry.config(state="disabled", width=11)
                    pathWidthEntry.grid(row=0, column=1, padx=(0, 5))
                    self.mazeInfo["pathWidth"] = pathWidthVar

                    wallWidthLabel = tk.Label(optionRow2, text="Šířka zdi: ", width=10)
                    wallWidthLabel.grid(row=0, column=2, padx=(5, 0))

                    wallWidthVar = tk.StringVar(value="0")
                    wallWidthEntry = tk.Entry(optionRow2, textvariable=wallWidthVar, width=5)
                    wallWidthEntry.config(state="disabled", width=11)
                    wallWidthEntry.grid(row=0, column=3, padx=(0, 5))
                    self.mazeInfo["wallWidth"] = wallWidthVar
                drawOptions2()
            drawInfo()
        drawLeft()

        ttk.Separator(self.master, orient="vertical").pack(side="left", fill="y", pady=5)

        def drawRight():
            rightFrame = tk.Frame(self.master)
            rightFrame.pack(side="left", pady=5, padx=5, expand=True, fill="both")

            def drawLabel():
                labelRow = tk.Frame(rightFrame)
                labelRow.pack(side="top", fill="x")

                rightLabel = tk.Label(labelRow, text="Bludiště", font=("Arial", 12, "bold"))
                rightLabel.pack(side="top", fill="x")
            drawLabel()

            ttk.Separator(rightFrame, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

            def drawButtons():
                rightButtonFrame = tk.Frame(rightFrame)
                rightButtonFrame.pack(side="top", fill="x")

                solveButton = tk.Button(rightButtonFrame, text="Vyřešit bludiště", command=lambda: self.processButton("solve"))
                solveButton.pack(side="left", padx=5, expand=True, fill="x")

                testButton = tk.Button(rightButtonFrame, text="Otestovat bludiště", command=lambda: self.processButton("test"))
                testButton.pack(side="left", padx=5, expand=True, fill="x")

                exportButton = tk.Button(rightButtonFrame, text="Exportovat bludiště", command=lambda: self.processButton("export"))
                exportButton.pack(side="left", padx=5, expand=True, fill="x")
            drawButtons()

            ttk.Separator(rightFrame, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

            self.canvas = tk.Canvas(rightFrame, background="gray")
            self.canvas.pack(side="bottom", expand=True, fill="both")
            self.emptyCanvas()
        drawRight()

    def __init__(self):
        super().__init__()
        self.title("MazeLib")
        centerWindow(self, 788, 541, -200, -200)

        # Remove temp files on closing
        def on_closing():
            for file in os.listdir("mazes/temp"):
                if file.endswith(".png") and file != "empty.png":
                    os.remove(os.path.join("mazes/temp", file))
            self.destroy()
            super()._exit(0)
        super().protocol("WM_DELETE_WINDOW", on_closing)

        self.mazes = []
        self.maze = None
        self.mazeInfo = {}

        self.list = None
        self.listVar = None

        self.image_id = None
        self.canvas = None
        self.photo = None

        self.gui = self
        self.drawMain()
        self.processButton("refresh")
