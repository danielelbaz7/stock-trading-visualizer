import {
    CartesianGrid,
    ComposedChart,
    Legend,
    Line,
    ResponsiveContainer,
    Scatter,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";
import React from "react";

function Chart({ prices }: { prices: any[] }) {
    return (
        <ResponsiveContainer width="120%" height={500}>
          <ComposedChart data={prices} margin={{top: 5, right: 30, left: 20, bottom: 5}}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="date"/>
            <YAxis/>
            <Tooltip/>
            <Legend/>
            <Line type="monotone" dataKey="Price" stroke="#0586f7" strokeWidth={2} dot={{r: 0}} activeDot={{r: 8}}/>
              <Scatter name="Entries" dataKey="EntryPrice" fill="green" shape="circle" isAnimationActive={false}/>
            <Scatter name="Exits" dataKey="ExitPrice" fill="red" shape="circle" isAnimationActive={false}/>
          </ComposedChart>
        </ResponsiveContainer>
    )
}

export default React.memo(Chart);
