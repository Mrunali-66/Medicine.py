import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.data_manager import MedicineDataManager
from src.analysis import MedicineAnalyzer


class MedicineAnalysisApp:
    def __init__(self, master):
        """
        Initialize the Medicine Analysis GUI Application

        Parameters:
        -----------
        master : tk.Tk
            The main window of the application
        """
        self.master = master
        master.title("Medicine Analysis System")
        master.geometry("800x600")

        # Initialize data manager and analyzer
        self.data_manager = MedicineDataManager()
        self.analyzer = MedicineAnalyzer(self.data_manager.dataframe)

        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create tabs
        self.create_inventory_tab()
        self.create_analysis_tab()
        self.create_charts_tab()
        self.create_actions_tab()

    def create_inventory_tab(self):
        """
        Create the Inventory Management Tab
        """
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        # Treeview for displaying medicines
        columns = ('Name', 'Category', 'Price', 'Stock', 'Expiry Date')
        self.medicine_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings')

        for col in columns:
            self.medicine_tree.heading(col, text=col)

        self.medicine_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Populate treeview
        self.update_medicine_treeview()

    def create_analysis_tab(self):
        """
        Create the Analysis Tab
        """
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Analysis")

        # Inventory Value
        total_value_label = ttk.Label(analysis_frame,
                                      text=f"Total Inventory Value: ${self.analyzer.calculate_total_inventory_value():.2f}")
        total_value_label.pack(pady=10)

        # Low Stock Medicines
        low_stock_frame = ttk.LabelFrame(analysis_frame, text="Low Stock Medicines")
        low_stock_frame.pack(padx=10, pady=10, fill='x')

        low_stock_columns = ('Name', 'Category', 'Current Stock')
        low_stock_tree = ttk.Treeview(low_stock_frame, columns=low_stock_columns, show='headings')

        for col in low_stock_columns:
            low_stock_tree.heading(col, text=col)

        low_stock_medicines = self.analyzer.get_low_stock_medicines()
        for _, row in low_stock_medicines.iterrows():
            low_stock_tree.insert('', 'end', values=(row['Name'], row['Category'], row['Stock']))

        low_stock_tree.pack(expand=True, fill='both', padx=10, pady=10)

    def create_charts_tab(self):
        """
        Create the Charts Tab
        """
        charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(charts_frame, text="Charts")

        # Stock Distribution Chart
        stock_fig, stock_ax = plt.subplots(figsize=(8, 4))
        stock_ax.bar(self.data_manager.dataframe['Name'], self.data_manager.dataframe['Stock'])
        stock_ax.set_title('Medicine Stock Levels')
        stock_ax.set_xlabel('Medicine Name')
        stock_ax.set_ylabel('Stock Quantity')
        stock_ax.tick_params(axis='x', rotation=45)

        stock_canvas