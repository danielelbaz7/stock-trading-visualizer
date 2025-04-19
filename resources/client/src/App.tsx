import {SetStateAction, useState} from "react";

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


  const [startYear, setStartYear] = useState("2000");
  const [endYear, setEndYear] = useState("2024");

  const [startMonth, setStartMonth] = useState("01");
  const [endMonth, setEndMonth] = useState("01");

  const [startDay, setStartDay] = useState("01");
  const [endDay, setEndDay] = useState("28");

  const [ticker, setTicker] = useState('SPY');

  const getPricesInJson = async () => {
    try {
      const response = await fetch('http://localhost:5000/data/GOOG/2015-1-01/2024-01-01/');
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

  // @ts-ignore
  return (
      <div style={{width: 2400, height: 1200}}>
        <h2>Historical Stock Price (USD)</h2>
        <ResponsiveContainer>
          <LineChart
              data={prices}
              margin={{top: 5, right: 30, left: 20, bottom: 5}}
          >
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="date"/>
            <YAxis/>
            <Tooltip/>
            <Legend/>
            <Line
                type="monotone"
                dataKey="close"
                stroke="#0586f7"
                //sets the line and dot sizes
                strokeWidth={2}
                dot={{r: 0}}
                activeDot={{r: 8}}
            />
          </LineChart>
        </ResponsiveContainer>
        {/*<input type="text" placeholder="Ticker" onChange={changeTicker => setTicker(changeTicker.target.value)}/>*/}
        <button onClick={getPricesInJson}>Get Prices</button>
        <input type="number" placeholder="YYYY" max={2025} value = {startYear} onChange={(changeStartYear: { target: { value: SetStateAction<string>; }; }) => setStartYear(changeStartYear.target.value)}/>
        <input type="number" placeholder="MM" max={12} value = {startMonth} onChange={(changeStartMonth: { target: { value: SetStateAction<string>; }; }) => setStartYear(changeStartMonth.target.value)}/>
        <input type="number" placeholder="DD" max={31} value = {startDay} onChange={(changeStartDay: { target: { value: SetStateAction<string>; }; }) => setStartYear(changeStartDay.target.value)}/>
        to
        <input type="number" placeholder="YYYY" max={2025} value={endYear} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEndYear(e.target.value)} />
        <input type="number" placeholder="MM" max={12} value={endMonth} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEndMonth(e.target.value)} />
        <input type="number" placeholder="DD" max={31} value={endDay} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEndDay(e.target.value)} />


    </div>
  );
}

export default App;
