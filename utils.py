import datetime
from mstarpy import Funds
import numpy as np
import numpy_financial as npf  # Importing numpy_financial

def get_current_nav(isin):
    """Fetch the current NAV (Net Asset Value) using ISIN."""
    try:
        fund = Funds(term=isin, country="in")
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=1)
        history = fund.nav(start_date=start_date, end_date=end_date, frequency="daily")
        
        if isinstance(history, list) and history:
            return history[-1]['nav']
        else:
            print(f"No NAV data available for ISIN: {isin}")
            return None
    except Exception as e:
        print(f"Error fetching NAV for ISIN {isin}: {e}")
        return None

def calculate_xirr(cashflows):
    """Calculates the XIRR of a series of cash flows using numpy_financial."""
    dates = np.array([cf[0] for cf in cashflows], dtype='datetime64[D]')
    amounts = np.array([cf[1] for cf in cashflows])

    # Calculate the XIRR
    xirr = npf.irr(amounts) * 365  # Annualize the result
    return xirr
