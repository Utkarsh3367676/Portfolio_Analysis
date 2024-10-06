import json
import datetime
from mstarpy import Funds
from pymongo import MongoClient
from models import Transaction
from utils import get_current_nav, calculate_xirr
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import warnings

# Suppress warnings from Matplotlib
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017')
db = client['portfolio_db']
portfolio_collection = db['portfolio']

class PortfolioProcessor:
    def __init__(self):
        self.transactions = []
        self.portfolio = {}

    def parse_transactions(self, data):
        """Parses JSON data to extract transactions."""
        for item in data['data']:
            for trxn in item.get('dtTransaction', []):
                transaction = Transaction(trxn)
                self.transactions.append(transaction)

    def process_portfolio_data(self):
        """Processes portfolio data based on transactions."""
        for transaction in self.transactions:
            isin = transaction.isin
            if isin not in self.portfolio:
                self.portfolio[isin] = {
                    'scheme_name': transaction.schemeName,
                    'folio': transaction.folio,
                    'units': 0,
                    'cost_value': 0,
                    'transactions': []
                }
            # Update portfolio based on transaction
            self.portfolio[isin]['transactions'].append(transaction.to_dict())  # Convert to dict for storage
            if transaction.trxnUnits > 0:  # Purchase
                self.portfolio[isin]['units'] += transaction.trxnUnits
                self.portfolio[isin]['cost_value'] += transaction.trxnAmount
            else:  # Sell
                units_to_sell = abs(transaction.trxnUnits)
                if self.portfolio[isin]['units'] >= units_to_sell:
                    self.portfolio[isin]['units'] -= units_to_sell
                else:
                    print(f"Warning: Trying to sell more units than available for {isin}")

    def calculate_portfolio_value(self):
        """Calculates the total portfolio value based on the current NAV."""
        total_value = 0
        for isin, details in self.portfolio.items():
            current_nav = get_current_nav(isin)
            if current_nav is not None:
                value = details['units'] * current_nav
                total_value += value
                details['current_value'] = value
                details['current_nav'] = current_nav
            else:
                details['current_value'] = 0
                details['current_nav'] = 0  # Fallback to 0 if NAV is not available
        return total_value

    def calculate_portfolio_gain(self):
        """Calculates the portfolio gains/losses."""
        total_gain = 0
        for details in self.portfolio.values():
            gain = details['current_value'] - details['cost_value']
            total_gain += gain
            details['gain'] = gain
        return total_gain

    def calculate_xirr(self):
        """Calculates XIRR for the portfolio."""
        cashflows = []
        for details in self.portfolio.values():
            for transaction in details['transactions']:
                cashflow_date = transaction['trxnDate']
                cashflow_amount = -transaction['trxnAmount'] if transaction['trxnUnits'] > 0 else transaction['trxnAmount']
                cashflows.append((cashflow_date, cashflow_amount))

        # Add the total current portfolio value as a cash inflow on the calculation date
        current_date = datetime.datetime.now()
        total_value = self.calculate_portfolio_value()
        cashflows.append((current_date, total_value))

        return calculate_xirr(cashflows)

    def visualize_portfolio(self):
        """Visualizes portfolio allocation and gains/losses using charts."""
        # Pie chart for portfolio allocation
        labels = [f"{details['scheme_name']} ({details['folio']})" for details in self.portfolio.values()]
        sizes = [details['current_value'] for details in self.portfolio.values()]
        
        plt.figure(figsize=(12, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Portfolio Allocation')
        plt.tight_layout()  # Ensure the layout is tight
        plt.savefig('portfolio_allocation.png')
        plt.close()

        # Bar chart for gains/losses
        schemes = [details['scheme_name'][:20] for details in self.portfolio.values()]
        gains = [details['gain'] for details in self.portfolio.values()]
            
        plt.figure(figsize=(12, 8))
        plt.bar(schemes, gains)
        plt.title('Gains/Losses by Scheme')
        plt.xlabel('Schemes')
        plt.ylabel('Gain/Loss (₹)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()  # Ensure the layout is tight
        plt.savefig('portfolio_gains.png')
        plt.close()
    def calculate_portfolio(self, data):
        """Main method to calculate portfolio values, gains, and visualize results."""
        self.parse_transactions(data)
        self.process_portfolio_data()
        total_value = self.calculate_portfolio_value()
        total_gain = self.calculate_portfolio_gain()
        xirr = self.calculate_xirr()  # Calculate XIRR

        # Visualize the portfolio
        self.visualize_portfolio()

        # Store results in MongoDB
        result = {
            "calculation_date": datetime.datetime.now(),
            "total_value": total_value,
            "total_gain": total_gain,
            "xirr": xirr,
            "portfolio": self.portfolio
        }
        portfolio_collection.insert_one(result)  # Insert result into MongoDB collection

        return {
            'total_portfolio_value': total_value,
            'total_portfolio_gain': total_gain,
            'xirr': xirr,
            'portfolio': self.portfolio
        }
