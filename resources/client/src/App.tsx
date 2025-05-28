import { SetStateAction, useState } from "react";
import Chart from "./Chart.tsx";

function App() {
  const [prices, setPrices] = useState([{}]);
  const [startYear, setStartYear] = useState("2000");
  const [endYear, setEndYear] = useState("2024");
  const [startMonth, setStartMonth] = useState("01");
  const [endMonth, setEndMonth] = useState("01");
  const [startDay, setStartDay] = useState("01");
  const [endDay, setEndDay] = useState("28");
  const [ticker, setTicker] = useState('SPY');
  const [strategy, setStrategy] = useState("1"); // 1 is median conversion, 2 is iqr breakout

  const [returnP, setReturnP] = useState("0");
  const [returnD, setReturnD] = useState("0");
  const [tradeNumber, setTradeNumber] = useState("0");
  const [winRate, setWinRate] = useState("0");
  const [exposureTime, setExposureTime] = useState("0");
  const [avgTrade, setAvgTrade] = useState("0");
  
  const changeStrategy = (e: { target: { value: SetStateAction<string> } }) => {
    setStrategy(e.target.value);
  };

  const getPricesInJson = async () => {
    try {
      const response = await fetch(
        `https://danielelbaz7.pythonanywhere.com/data/${ticker}/${startYear}-${startMonth}-${startDay}/${endYear}-${endMonth}-${endDay}/${strategy}`
      );
      if (!response.ok) {
        console.log(response);
        throw new Error('Prices could not be fetched.');
      }
      const jsonPrices = await response.json();
      setPrices(jsonPrices);

      await getMetrics();

    } catch (error) {
      console.error(error);
    }
  };

  const getMetrics = async () => {
    try {
      const response = await fetch (
          'https://danielelbaz7.pythonanywhere.com/getmetrics',
      );
      if (!response.ok) {
        console.log(response);
        throw new Error('Metrics could not be fetched!');
      }
      const jsonMetrics = await response.json();
      setReturnP(jsonMetrics['return%']);
      setReturnD(jsonMetrics['return$']);
      setTradeNumber(jsonMetrics['trade#']);
      setWinRate(jsonMetrics['winrate%']);
      setExposureTime(jsonMetrics['exposuretime%']);
      setAvgTrade(jsonMetrics['avgtrade%']);
    } catch (error) {
      console.error(error);
    }
  };

  const styles: {
  [key: string]: React.CSSProperties & {
    WebkitAppearance?: string;
  };
} = {
  container: {
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    color: '#333',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  controls: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    gap: '12px',
    marginBottom: '20px',
  },
  row: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  input: {
    backgroundColor: '#e5e5e5',
    color: '#000',
    padding: '8px 12px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    WebkitAppearance: 'none',
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#0586f7',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  chartTitle: {
    textAlign: 'center',
    fontSize: '24px',
    marginBottom: '10px',
  },
};

  // @ts-ignore
  return (
      <div style={styles.container}>
        <div
      style={{
        position: 'fixed',
        top: 20,
        right: 20,
        backgroundColor: '#fff',
        padding: '4px 8px',
        borderRadius: '4px',
        boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
        zIndex: 1000,
      }}
    >
          <div>
            <div>Return %: {returnP}</div>
            <div>Return $: {returnD}</div>
            <div>Trade #: {tradeNumber}</div>
            <div>Win Rate %: {winRate}</div>
            <div>Exposure Time %: {exposureTime}</div>
            <div>Avg Trade %: {avgTrade}</div>
          </div>
        </div>

        <h2 style={styles.chartTitle}>Historical Stock Price (USD)</h2>

        <div style={styles.controls}>
          <div style={styles.row}>
            <label>Ticker:</label>
            <input
                type="text"
                placeholder="Ticker"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                style={styles.input}
            />
          </div>

          <div style={styles.row}>
            <label>From:</label>
            <input
                type="number"
                placeholder="YYYY"
                max={2025}
                value={startYear}
                onChange={(e) => setStartYear(e.target.value)}
                style={styles.input}
            />
            <input
                type="number"
                placeholder="MM"
                max={12}
                value={startMonth}
                onChange={(e) => setStartMonth(e.target.value)}
                style={styles.input}
            />
            <input
                type="number"
                placeholder="DD"
                max={31}
                value={startDay}
                onChange={(e) => setStartDay(e.target.value)}
                style={styles.input}
            />
          </div>

          <div style={styles.row}>
            <label>To:</label>
            <input
                type="number"
                placeholder="YYYY"
                max={2025}
                value={endYear}
                onChange={(e) => setEndYear(e.target.value)}
                style={styles.input}
            />
            <input
                type="number"
                placeholder="MM"
                max={12}
                value={endMonth}
                onChange={(e) => setEndMonth(e.target.value)}
                style={styles.input}
            />
            <input
                type="number"
                placeholder="DD"
                max={31}
                value={endDay}
                onChange={(e) => setEndDay(e.target.value)}
                style={styles.input}
            />
          </div>

          <div style={styles.row}>
            <select
                value={strategy}
                onChange={changeStrategy}
                style={styles.input}
            >
              <option value="1">Median Reversion</option>
              <option value="2">IQR Breakout</option>
            </select>
            <button style={styles.button} onClick={getPricesInJson}>
              Get Prices
            </button>
          </div>
        </div>
        <Chart prices={prices} />
      </div>
  );
}

export default App;
