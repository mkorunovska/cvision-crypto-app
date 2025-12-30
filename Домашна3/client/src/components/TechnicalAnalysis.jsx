import React, { useEffect, useState } from "react";
import CryptoSearchBar from "./CryptoSearchBar.jsx";
import { getToken } from "../auth";



function badgeClass(signal) {
  switch (signal) {
    case "BUY":
      return "bg-green-100 text-green-800 border-green-200";
    case "SELL":
      return "bg-red-100 text-red-800 border-red-200";
    default:
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
  }
}


const TechnicalAnalysis = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [selectedCryptoId, setSelectedCryptoId] = useState("");

  const [period, setPeriod] = useState("day");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearchChange = (e) => {
    const q = e.target.value;
    setQuery(q);
    setAnalysis(null);

    if (q.trim().length < 2) {
      setResults([]);
      return;
    }

    fetch(`http://localhost:8000/api/crypto/search?query=${q}`)
      .then((res) => res.json())
      .then((data) => setResults(data))
      .catch(() => setError("Error searching cryptocurrencies"));
  };

  const handleSelectCrypto = (crypto) => {
    setSelectedCryptoId(crypto.id);
    setQuery(crypto.name);
    setResults([]);
    setError("");
  };

  const handleGetAnalysis = async (e) => {
    e.preventDefault();
    setError("");
    setAnalysis(null);

    if (!selectedCryptoId) {
      setError("Please select a cryptocurrency.");
      return;
    }
    const token = getToken();
    if (!token) {
      setError("You are not logged in. Please login again.");
      return;
    }

    setLoading(true);

    const url = `http://localhost:8000/api/analysis?cryptoId=${selectedCryptoId}&period=${period}`;

    try {
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const msg = await response.text();
        throw new Error(msg || `Request failed (${response.status})`);
      }

      const data = await response.json();
      setAnalysis(data);
    }catch(err){
      if (String(err.message).includes("401")) {
        setError("Session expired. Please login again.");
      } else {
        setError(err.message);
      }
    }finally{
      setLoading(false);
    }
  };

  const renderIndicators = () => {
    if (!analysis || !analysis.indicators) return null;

    return (
      <div className="mt-4 text-black bg-blue-50">
        {Object.entries(analysis.indicators).map(([name, obj]) => (
          <div key={name} className="flex justify-between py-2 border-b border-gray-200">
            <span className="w-1/3 font-semibold text-black">{name}</span>
            <span className="w-1/3 text-black">
              Value: {obj.value?.toFixed?.(3) || obj.value}
            </span>
            <span className="w-1/3 text-black">Signal: {obj.signal}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6 min-h-[80vh]">
      <h1 className="text-2xl font-bold mb-6 text-white">Technical Analysis</h1>

      <form onSubmit={handleGetAnalysis}>
        <CryptoSearchBar
          query={query}
          searchResults={results}
          onSearchChange={handleSearchChange}
          onCryptoSelect={handleSelectCrypto}
        />

        <label className="block mb-1 font-medium text-white">
          Select timeframe
        </label>
        <select
          className="w-full p-3 border border-gray-300 rounded mb-4 text-black"
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
        >
          <option value="day">Day</option>
          <option value="week">Week</option>
          <option value="month">Month</option>
        </select>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-50 text-darkblue py-3 rounded hover:bg-blue-100" >
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-black rounded">{error}</div>
      )}

      {analysis && (
        <div className="mt-6 p-4 border rounded bg-blue-50 shadow text-black ">
          <h2 className="text-xl font-semibold mb-2 text-black">
            {analysis.cryptoId}
          </h2>
          <p className="text-black">Date: {analysis.date}</p>
          <p className="text-black">Price: {analysis.price}</p>
          <p className="font-bold mt-2 text-black">
            Overall Signal:{" "}
            {/* <span className="text-black">{analysis.overall_signal}</span> */}
            <span className={`inline-flex items-center px-3 py-1 rounded-full border text-sm font-semibold ${badgeClass(analysis.overall_signal)}`}>
              {analysis.overall_signal}</span>
          </p>
          {renderIndicators()}
        </div>
      )}
    </div>
  );
};


export default TechnicalAnalysis;
