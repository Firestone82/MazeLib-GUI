import asyncio
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from mazeLib import *

from src.library.lib import positionWindow


class SolveGUI:

    # Properly close window
    def close(self):
        self.worker.call_soon_threadsafe(self.worker.stop)
        self.worker.call_soon_threadsafe(lambda: print("Maze solving interrupted."))
        self.window.destroy()

    # Solve maze
    def processSolve(self):
        print("Starting solving creating...")

        solver = Algorithm.getSolver(self.settings["solver"].get())

        print((" - Solver: " + solver.getName()))

        mazePath = solver.solve(self.master.maze[1])
        if mazePath.hasError():
            print("Maze solving failed! Error:" + mazePath.error)
            return messagebox.showerror("MazeLib", "Error: Some parameters has wrong configuration. \nError: " + mazePath.error)
        mazePath = mazePath.value()

        ImageSavingMethod.save(self.master.maze[1], "mazes/temp/" + str(self.master.maze[1].getSeed()) + "-S.png", mazePath)
        self.master.maze = (self.master.maze[0], self.master.maze[1], mazePath)
        self.master.mazes[self.master.list.curselection()[0]] = self.master.maze
        self.close()

        self.master.gui.loadCanvas()

        print("Maze solved successfully!")
        return messagebox.showinfo("MazeLib", "Successful: Maze solved successfully")

    def startSolve(self):
        self.button.config(state="disabled")
        asyncio.run_coroutine_threadsafe(self.processSolve(), self.worker)

    def draw(self):
        topFrame = tk.Frame(self.window)
        topFrame.pack(side="top", fill="x", expand=True, pady=5, padx=5)

        def drawTop():
            label = tk.Label(topFrame, text="Vyřešení bludiště", font=("Arial", 12, "bold"))
            label.pack(side="left", fill="x", expand=True, pady=(5, 0))

            backButton = tk.Button(topFrame, text="Zpět", command=lambda: self.window.destroy(), width=10)
            backButton.pack(side="left", padx=10)
        drawTop()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=(5, 0), padx=5)

        def drawFields():
            fieldFrame = tk.Frame(self.window)
            fieldFrame.pack(side="top", fill="y", padx=5, pady=5)

            def drawSolvers():
                solverRow = tk.Frame(fieldFrame)
                solverRow.pack(side="top", fill="x", pady=5, padx=5)

                algorithmLabel = tk.Label(solverRow, text="Algoritmus:", width=15, anchor="w")
                algorithmLabel.pack(side="left")

                self.settings["solver"] = tk.StringVar()
                algorithmOptions = [x.getName() for x in Algorithm.getSolvers()]
                self.settings["solver"].set(algorithmOptions[0])
                generatorMenu = tk.OptionMenu(solverRow, self.settings["solver"], *algorithmOptions)
                generatorMenu.pack(side="left", fill="x", expand=True)
            drawSolvers()
        drawFields()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

        self.button = tk.Button(self.window, text="Vyřešit", command=lambda: self.processSolve())
        self.button.pack(side="top", padx=5, pady=(0, 10), fill="x", expand=True)

    def __init__(self, master):
        self.master = master

        self.window = tk.Toplevel(master)
        self.window.transient(master)
        self.window.title("MazeLib - Vyřešení bludiště")
        self.window.resizable(False, False)
        self.window.grab_set()
        positionWindow(self.window, 405, 250)

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
