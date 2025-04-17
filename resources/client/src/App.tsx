import {useState} from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';



function App() {

  const [prices, setPrices] = useState([{}]);

  const getPricesInJson = async () => {
    try {
      const response = await fetch('http://localhost:5000/data/GOOG/2015-01-01/2024-01-01/');
      if (!response.ok) {
        console.log(response);
        throw new Error('Prices could not be fetched!');
      }
      const jsonPrices = await response.json();
      setPrices(jsonPrices);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div style={{ width: 400, height: 400 }}>
      <h2>Historical Stock Price (USD)</h2>
      <ResponsiveContainer>
        <LineChart
          data={prices}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
      <button onClick={getPricesInJson}>Get Prices</button>
    </div>
  );
}

export default App;
