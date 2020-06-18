"""Represents the shopper table."""

from ShopperModel import Configuration


class ShopperTable:
    """Represents the shopper table."""
    def __init__(self, configuration):
        """Instantiates the ShopperTable object by taking a configuration object."""
        if Configuration != isinstance(configuration):
            raise TypeError("TypeError. Please provide a Configuration object.")
        self.configuration = configuration
        self.data_frame = None

    def generate_shopper_table(self):
        """Generates the shopper table and stores it as self.data_frame"""

    def export_shopper_table_as_csv(self):
        """Exports the shopper table as a csv."""
        if self.data_frame is None:
            self.generate_shopper_table()

        # TODO: parameter below should be coming from config
        csv_path = "shoppers.csv"

        self.data_frame.to_csv(csv_path)

    def get_data_frame(self):
        """
        Returns the shopper table as a pandas data frame object.
        :return: the shopper table as a pandas data frame object.
        """
        if self.data_frame is None:
            self.generate_shopper_table()

        return self.data_frame
