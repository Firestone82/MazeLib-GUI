import asyncio
import threading
import tkinter as tk
from time import sleep
from tkinter import ttk

from mazeLib import *

from src.library.lib import positionWindow


class TestGUI:

    # Properly close window
    def close(self):
        self.worker.call_soon_threadsafe(self.worker.stop)
        self.worker.call_soon_threadsafe(lambda: print("Maze testing interrupted."))
        self.window.destroy()

    # Fill table with algorithms
    def fillTable(self):
        self.table.delete(*self.table.get_children())

        for i, algo in enumerate(Algorithm.getSolvers()):
            self.table.insert("", "end", text="", iid=i, values=(algo.getName(), "Not Started", 0, "0us"))

    # Update table data
    def updateTable(self):
        for i, (algo, data) in enumerate(self.data.items()):
            self.table.set(i, column=1, value=data['status'])
            self.table.set(i, column=2, value=data['pathLength'])
            self.table.set(i, column=3, value=(str(data['time']) + "us"))

    # Test all algorithms
    async def processTest(self):
        print("Starting maze testing...")

        for algo, data in self.data.items():
            self.data[algo] = {'status': 'Waiting', 'pathLength': 0, 'time': 0}
        self.updateTable()

        for algo, data in self.data.items():

            # Set status to 1 (running)
            data["status"] = "Running"
            self.data[algo] = data
            self.updateTable()
            sleep(0.5)  # TODO: Remove if not needed

            # Get solver
            solver = Algorithm.getSolver(algo)

            # Solve maze
            mazePath = solver.solve(self.master.maze[1])
            if mazePath.hasError():
                data["status"] = "Failed"
                data["pathLength"] = 0
                data["time"] = 0
            else:
                mazePath = mazePath.value()

                data["status"] = "Success"
                data["pathLength"] = mazePath.getLength()
                data["time"] = mazePath.getSolvingTime()

            print(" - " + algo.ljust(self.longestName + 1) + ": " + str(data["status"]) + " (" + str(data["pathLength"]) + ", " + str(data["time"]) + ")")

            self.data[algo] = data
            self.updateTable()
            sleep(0.25)  # TODO: Remove if not needed

        print("Maze testing finished.")
        self.button.config(state="normal")

    def startTest(self):
        self.button.config(state="disabled")
        asyncio.run_coroutine_threadsafe(self.processTest(), self.worker)

    def draw(self):
        topFrame = tk.Frame(self.window)
        topFrame.pack(side="top", fill="x", expand=True, pady=5, padx=5)

        def drawTop():
            labelRow = tk.Frame(self.window)
            labelRow.pack(side="top", fill="x", expand=True)

            label = tk.Label(labelRow, text="Testování všech algoritmu", font=("Arial", 12, "bold"))
            label.pack(side="left", fill="x", expand=True)

            backButton = tk.Button(labelRow, text="Zpět", command=lambda: self.close(), width=10)
            backButton.pack(side="left", padx=10)
        drawTop()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=(5, 0), padx=5)

        def drawTable():
            frame = tk.Frame(self.window)
            frame.pack(side="top", fill="both", padx=5, pady=5)

            self.table = ttk.Treeview(frame, height=10, selectmode='browse', show='headings')
            self.table['columns'] = ('algorithm', 'status', 'pathLength', 'time')
            self.table.pack()

            self.table.column("#0", width=0, stretch=False)
            self.table.column("algorithm", anchor="w", width=200)
            self.table.column("status", anchor="n", width=100)
            self.table.column("pathLength", anchor="n", width=80)
            self.table.column("time", anchor="n", width=100)

            self.table.heading("#0", text="", anchor="n")
            self.table.heading("algorithm", text="Algoritmus", anchor="n")
            self.table.heading("status", text="Status", anchor="n")
            self.table.heading("pathLength", text="Délka", anchor="n")
            self.table.heading("time", text="Čas", anchor="n")

            self.fillTable()
        drawTable()

        ttk.Separator(self.window, orient="horizontal").pack(side="top", fill="x", pady=5, padx=5)

        self.button = tk.Button(self.window, text="Spustit testování", command=lambda: self.startTest())
        self.button.pack(side="top", padx=10, pady=(0, 10), fill="x", expand=True)

    def __init__(self, master):
        self.master = master

        # Window
        self.window = tk.Toplevel(master)
        self.window.transient(master)
        self.window.title("MazeLib - Testování bludiště")
        self.window.resizable(False, False)
        self.window.grab_set()
        positionWindow(self.window, 310, 250)

        # Variables
        self.table = None
        self.button = None
        self.data = {}
        self.worker = None
        self.longestName = 0

        # Initialize data
        for i, algo in enumerate(Algorithm.getSolvers()):
            if len(algo.getName()) > self.longestName:
                self.longestName = len(algo.getName())

            self.data[algo.getName()] = {'status': 'Waiting', 'pathLength': 0, 'time': 0}

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
