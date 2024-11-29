import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any


class MedicineAnalyzer:
    def __init__(self, dataframe):
        """
        Initialize the Medicine Analyzer with a DataFrame

        Parameters:
        -----------
        dataframe : pandas.DataFrame
            DataFrame containing medicine data
        """
        self.dataframe = dataframe

    def calculate_total_inventory_value(self) -> float:
        """
        Calculate the total inventory value

        Returns:
        --------
        float
            Total value of medicine inventory
        """
        return (self.dataframe['Price'] * self.dataframe['Stock']).sum()

    def get_low_stock_medicines(self, threshold: int = 50) -> pd.DataFrame:
        """
        Identify medicines with low stock

        Parameters:
        -----------
        threshold : int, optional
            Stock level threshold (default is 50)

        Returns:
        --------
        pandas.DataFrame
            Medicines with stock below the threshold
        """
        return self.dataframe[self.dataframe['Stock'] < threshold]

    def analyze_medicines_by_category(self) -> Dict[str, Any]:
        """
        Analyze medicines grouped by category

        Returns:
        --------
        dict
            Analysis of medicines by category
        """
        category_analysis = {}

        for category in self.dataframe['Category'].unique():
            category_df = self.dataframe[self.dataframe['Category'] == category]
            category_analysis[category] = {
                'count': len(category_df),
                'total_stock': category_df['Stock'].sum(),
                'avg_price': category_df['Price'].mean(),
                'total_inventory_value': (category_df['Price'] * category_df['Stock']).sum()
            }

        return category_analysis

    def plot_stock_distribution(self, save_path: str = 'stock_distribution.png'):
        """
        Create a bar plot of medicine stock levels

        Parameters:
        -----------
        save_path : str, optional
            Path to save the plot image
        """
        plt.figure(figsize=(10, 6))
        plt.bar(self.dataframe['Name'], self.dataframe['Stock'])
        plt.title('Medicine Stock Levels')
        plt.xlabel('Medicine Name')
        plt.ylabel('Stock Quantity')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    def plot_price_distribution(self, save_path: str = 'price_distribution.png'):
        """
        Create a bar plot of medicine prices

        Parameters:
        -----------
        save_path : str, optional
            Path to save the plot image
        """
        plt.figure(figsize=(10, 6))
        plt.bar(self.dataframe['Name'], self.dataframe['Price'])
        plt.title('Medicine Prices')
        plt.xlabel('Medicine Name')
        plt.ylabel('Price')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    def predict_restock_needs(self, critical_threshold: int = 30) -> List[Dict[str, Any]]:
        """
        Predict medicines that need restocking

        Parameters:
        -----------
        critical_threshold : int, optional
            Stock level considered critical (default is 30)

        Returns:
        --------
        list
            List of medicines needing restock with details
        """
        restock_needed = []

        for _, row in self.dataframe.iterrows():
            if row['Stock'] <= critical_threshold:
                restock_needed.append({
                    'Name': row['Name'],
                    'Current_Stock': row['Stock'],
                    'Recommended_Restock': critical_threshold * 2 - row['Stock']
                })

        return restock_needed