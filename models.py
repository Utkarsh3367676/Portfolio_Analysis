import datetime

class Transaction:
    """Class representing a single financial transaction."""
    
    def __init__(self, data):
        self.trxnDate = datetime.datetime.strptime(data['trxnDate'], "%d-%b-%Y")
        self.scheme = data['scheme']
        self.trxnDesc = data['trxnDesc']
        self.schemeName = data['schemeName']
        self.purchasePrice = float(data['purchasePrice'])
        self.trxnUnits = float(data['trxnUnits'])
        self.trxnAmount = float(data['trxnAmount'])
        self.folio = data['folio']
        self.isin = data['isin']

    def to_dict(self):
        """Convert the transaction to a dictionary for MongoDB."""
        return {
            'trxnDate': self.trxnDate.isoformat(),  # Convert datetime to string
            'scheme': self.scheme,
            'trxnDesc': self.trxnDesc,
            'schemeName': self.schemeName,
            'purchasePrice': self.purchasePrice,
            'trxnUnits': self.trxnUnits,
            'trxnAmount': self.trxnAmount,
            'folio': self.folio,
            'isin': self.isin
        }
