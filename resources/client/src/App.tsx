"use client"

import type React from "react"

import { useState } from "react"
import { CalendarDays, TrendingUp, DollarSign, BarChart3, Loader2 } from "lucide-react"
import Chart from "./Chart"

function App() {
  const [prices, setPrices] = useState([{}])
  const [startYear, setStartYear] = useState("2000")
  const [endYear, setEndYear] = useState("2024")
  const [startMonth, setStartMonth] = useState("01")
  const [endMonth, setEndMonth] = useState("01")
  const [startDay, setStartDay] = useState("01")
  const [endDay, setEndDay] = useState("28")
  const [ticker, setTicker] = useState("SPY")
  const [strategy, setStrategy] = useState("1")
  const [isLoading, setIsLoading] = useState(false)

  const [returnP, setReturnP] = useState("0")
  const [returnD, setReturnD] = useState("0")
  const [tradeNumber, setTradeNumber] = useState("0")
  const [winRate, setWinRate] = useState("0")
  const [exposureTime, setExposureTime] = useState("0")
  const [avgTrade, setAvgTrade] = useState("0")

  const changeStrategy = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setStrategy(e.target.value)
  }

  const getPricesInJson = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(
        `https://danielelbaz7.pythonanywhere.com/data/${ticker}/${startYear}-${startMonth}-${startDay}/${endYear}-${endMonth}-${endDay}/${strategy}`,
      )
      if (!response.ok) {
        console.log(response)
        throw new Error("Prices could not be fetched!")
      }
      const jsonPrices = await response.json()
      setPrices(jsonPrices)

      await getMetrics()
    } catch (error) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const getMetrics = async () => {
    try {
      const response = await fetch("https://danielelbaz7.pythonanywhere.com/getmetrics")
      if (!response.ok) {
        console.log(response)
        throw new Error("Metrics could not be fetched!")
      }
      const jsonMetrics = await response.json()
      setReturnP(jsonMetrics["return%"])
      setReturnD(jsonMetrics["return$"])
      setTradeNumber(jsonMetrics["trade#"])
      setWinRate(jsonMetrics["winrate%"])
      setExposureTime(jsonMetrics["exposuretime%"])
      setAvgTrade(jsonMetrics["avgtrade%"])
    } catch (error) {
      console.error(error)
    }
  }

  const formatValue = (value: string, suffix = "") => {
    return value !== "0" ? `${value}${suffix}` : "—"
  }

  const getReturnColor = (value: string) => {
    const num = Number.parseFloat(value)
    if (num > 0) return "text-green-600"
    if (num < 0) return "text-red-600"
    return "text-gray-500"
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="mx-auto max-w-7xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900">Stock Analysis Dashboard</h1>
          <p className="text-lg text-gray-600">Analyze historical stock performance with advanced trading strategies</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Controls Panel */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <h2 className="text-lg font-semibold text-gray-900">Analysis Parameters</h2>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="ticker" className="block text-sm font-medium text-gray-700">
                    Stock Ticker
                  </label>
                  <input
                    id="ticker"
                    type="text"
                    placeholder="e.g., SPY, AAPL, TSLA"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value.toUpperCase())}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono"
                  />
                </div>

                <div className="space-y-3">
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                    <CalendarDays className="h-4 w-4" />
                    Date Range
                  </label>

                  <div className="space-y-3">
                    <div>
                      <label className="text-sm text-gray-500">From</label>
                      <div className="grid grid-cols-3 gap-2 mt-1">
                        <input
                          type="number"
                          placeholder="Year"
                          value={startYear}
                          onChange={(e) => setStartYear(e.target.value)}
                          max={2025}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                        <input
                          type="number"
                          placeholder="Month"
                          value={startMonth}
                          onChange={(e) => setStartMonth(e.target.value.padStart(2, "0"))}
                          max={12}
                          min={1}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                        <input
                          type="number"
                          placeholder="Day"
                          value={startDay}
                          onChange={(e) => setStartDay(e.target.value.padStart(2, "0"))}
                          max={31}
                          min={1}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="text-sm text-gray-500">To</label>
                      <div className="grid grid-cols-3 gap-2 mt-1">
                        <input
                          type="number"
                          placeholder="Year"
                          value={endYear}
                          onChange={(e) => setEndYear(e.target.value)}
                          max={2025}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                        <input
                          type="number"
                          placeholder="Month"
                          value={endMonth}
                          onChange={(e) => setEndMonth(e.target.value.padStart(2, "0"))}
                          max={12}
                          min={1}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                        <input
                          type="number"
                          placeholder="Day"
                          value={endDay}
                          onChange={(e) => setEndDay(e.target.value.padStart(2, "0"))}
                          max={31}
                          min={1}
                          className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Trading Strategy</label>
                  <select
                    value={strategy}
                    onChange={changeStrategy}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="1">Median Reversion</option>
                    <option value="2">IQR Breakout</option>
                  </select>
                </div>

                <button
                  onClick={getPricesInJson}
                  disabled={isLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Run Analysis"
                  )}
                </button>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <h2 className="text-lg font-semibold text-gray-900">Performance Metrics</h2>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-1">
                      <DollarSign className="h-3 w-3 text-gray-400" />
                      <span className="text-xs text-gray-500">Return %</span>
                    </div>
                    <div className={`text-lg font-semibold ${getReturnColor(returnP)}`}>
                      {formatValue(returnP, "%")}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex items-center gap-1">
                      <DollarSign className="h-3 w-3 text-gray-400" />
                      <span className="text-xs text-gray-500">Return $</span>
                    </div>
                    <div className={`text-lg font-semibold ${getReturnColor(returnD)}`}>
                      {formatValue(returnD, "$")}
                    </div>
                  </div>
                </div>

                <hr className="border-gray-200" />

                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Trades</span>
                    <span className="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded">
                      {formatValue(tradeNumber)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Win Rate</span>
                    <span
                      className={`text-xs font-medium px-2.5 py-0.5 rounded ${
                        Number.parseFloat(winRate) > 50 ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {formatValue(winRate, "%")}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Exposure Time</span>
                    <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
                      {formatValue(exposureTime, "%")}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Avg Trade</span>
                    <span className="bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded">
                      {formatValue(avgTrade, "%")}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Chart Panel */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-full">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 text-center">
                  Historical Stock Price Analysis
                  {ticker && (
                    <span className="ml-2 bg-gray-100 text-gray-800 text-sm font-medium px-2.5 py-0.5 rounded">
                      {ticker}
                    </span>
                  )}
                </h2>
              </div>
              <div className="p-6 h-[600px]">
                <Chart prices={prices} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
