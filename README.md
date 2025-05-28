## Overview
This project implements and backtests two different complex trading algorithms, the IQR breakout and median reversion strategies.

## Tech Stack
- **Languages**: Python, TypeScript
- **Frameworks**: Flask, React
- **Other Dependencies**: backtesting.py (v0.6.4), yfinance (v0.2.55), npm (v23.11.0), Vite

## How to Use
First, install all of the dependencies using:

```pip install flask flask_cors backtesting yfinance```

Then, run the following command in the client folder:

```npm run dev```

Finally, run the following file in the server folder:

```server.py```

Afterwards, the project will be running on the frontend. From there you will select the following:
- Stock Ticker
- Start Date
- End Date
- Trading Strategy

And the selected algorithm will backtest and return the results of the trades it made.

## Algorithms Implemented

We implemented two trading strategies. The data structures and algorithms they rely on are listed:
- **Sliding Median Breakout**: Implements a double heap to create a running median. Implements a hash table to allow for delayed deletion, allowing removal of previous values to be less costly and mainting a quick sliding median.
- **Sliding IQR Breakout**: Implements a Red-Black tree to create a running range of values. Implements indexing to the balanced tree to quickly locate the first and third quartiles, and makes trades based off the current quartiles and IQR.

Both of these algorithms operate based on deviation from their selected data (e.g., both will buy if the price goes too high above the median/Q3, and will sell if the price goes too far below the median/Q1).

