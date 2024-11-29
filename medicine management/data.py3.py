import pandas as pd
import os


class MedicineDataManager:
    def __init__(self, data_path='data/medicines.csv'):
        """
        Initialize the data manager with a CSV file path

        Parameters:
        -----------
        data_path : str, optional
            Path to the medicines CSV file (default is 'data/medicines.csv')
        """
        self.data_path = data_path
        self.dataframe = None
        self.load_data()

    def load_data(self):
        """
        Load medicine data from CSV file

        Returns:
        --------
        pandas.DataFrame
            Loaded medicine data
        """
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)

            # Check if file exists, if not create a sample file
            if not os.path.exists(self.data_path):
                self._create_sample_data()

            # Load the CSV file
            self.dataframe = pd.read_csv(self.data_path)
            return self.dataframe
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def _create_sample_data(self):
        """
        Create a sample medicines dataset if no data exists
        """
        sample_data = pd.DataFrame({
            'Name': ['Aspirin', 'Ibuprofen', 'Paracetamol', 'Amoxicillin', 'Metformin'],
            'Category': ['Painkiller', 'Anti-inflammatory', 'Painkiller', 'Antibiotic', 'Diabetes'],
            'Price': [5.99, 7.50, 4.25, 12.99, 9.75],
            'Stock': [100, 85, 120, 50, 75],
            'Expiry_Date': ['2025-12-31', '2024-06-30', '2025-03-15', '2024-09-22', '2025-01-10']
        })
        sample_data.to_csv(self.data_path, index=False)

    def add_medicine(self, name, category, price, stock, expiry_date):
        """
        Add a new medicine to the dataset

        Parameters:
        -----------
        name : str
            Name of the medicine
        category : str
            Category of the medicine
        price : float
            Price of the medicine
        stock : int
            Number of items in stock
        expiry_date : str
            Expiry date of the medicine (YYYY-MM-DD)
        """
        new_medicine = pd.DataFrame({
            'Name': [name],
            'Category': [category],
            'Price': [price],
            'Stock': [stock],
            'Expiry_Date': [expiry_date]
        })

        self.dataframe = pd.concat([self.dataframe, new_medicine], ignore_index=True)
        self.dataframe.to_csv(self.data_path, index=False)

    def delete_medicine(self, medicine_name):
        """
        Delete a medicine from the dataset

        Parameters:
        -----------
        medicine_name : str
            Name of the medicine to delete
        """
        self.dataframe = self.dataframe[self.dataframe['Name'] != medicine_name]
        self.dataframe.to_csv(self.data_path, index=False)

    def update_medicine(self, name, **kwargs):
        """
        Update medicine information

        Parameters:
        -----------
        name : str
            Name of the medicine to update
        **kwargs : dict
            Keyword arguments for fields to update
        """
        mask = self.dataframe['Name'] == name
        for key, value in kwargs.items():
            self.dataframe.loc[mask, key] = value

        self.dataframe.to_csv(self.data_path, index=False)

    def get_medicine_by_name(self, name):
        """
        Retrieve medicine details by name

        Parameters:
        -----------
        name : str
            Name of the medicine

        Returns:
        --------
        pandas.Series or None
            Medicine details or None if not found
        """
        medicine = self.dataframe[self.dataframe['Name'] == name]
        return medicine.iloc[0] if not medicine.empty else None

    def search_medicines(self, **kwargs):
        """
        Search medicines based on various criteria

        Parameters:
        -----------
        **kwargs : dict
            Search criteria (e.g., category, price_range)

        Returns:
        --------
        pandas.DataFrame
            Filtered medicines
        """
        df = self.dataframe.copy()

        for key, value in kwargs.items():
            if key == 'category':
                df = df[df['Category'].str.contains(value, case=False)]
            elif key == 'price_range':
                min_price, max_price = value
                df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
            elif key == 'low_stock':
                df = df[df['Stock'] < value]

        return df