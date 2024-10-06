**Portfolio Management and Visualization**

This project is a backend system for processing and visualizing financial portfolio data. It allows users to calculate the total portfolio value, portfolio gain, and the XIRR (Extended Internal Rate of Return) based on a set of transactions. The application can fetch current NAV (Net Asset Value) for mutual fund schemes using the mstarpy library and visualize the results using Matplotlib. It also supports storing results in a MongoDB database for persistent storage.

Features
-Calculated Total Portfolio Value: Sum of (leftover units × NAV of scheme).

-Calculated Total Portfolio Gain: Sum of (Current Unit Value - Unit Acquisition Cost).

-Calculated Portfolio XIRR: Compute the XIRR based on the series of cash flows.

Additional Features I have implemented:
-Visualized Portfolio Allocation: Generated a pie chart for portfolio allocation.

-Visualized Gains/Losses by Scheme: Generated a bar chart for gains/losses by each scheme.

-Stored Results in MongoDB: Stored the results of calculations in a MongoDB database for persistent storage and future reference.


Setup and Installation

1)Clone the Repository:
git clone <repository-url>
cd backend_assignment

2)Install Dependencies:
pip install -r requirements.txt

3)Configure MongoDB:
Ensure that MongoDB is installed and running on your local machine. By default, the app connects to mongodb://localhost:27017 and uses a database named portfolio_db. If you need to change these configurations, update the connection string in portfolio.py.

5)Run the Flask Application:
python app.py
The application will start on http://127.0.0.1:5000 by default.

6) Running the Application 
Use The below Curl Command to send the json data to the /portfolio endpoint
curl -X POST http://127.0.0.1:5000/portfolio -H "Content-Type: application/json" -d @transaction_detail.json

or 
Simply send your test-json data to the endpoint using the modified curl command or postman with your json data .

7)Viewing the Output

Console Output: The total portfolio value, gain, and XIRR will be printed in the console.
MongoDB Storage: The results will be stored in the portfolio_db database in a collection named portfolio( I have Added Snapshots of MongoDb Database and collection which was created )
Visualizations: The charts will be saved as PNG files in the current working directory:
      portfolio_allocation.png: Pie chart for portfolio allocation.
      portfolio_gains.png: Bar chart for gains/losses by scheme.



      
