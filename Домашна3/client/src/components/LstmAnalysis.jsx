import React, { useState } from "react";
import CryptoSearchBar from "./CryptoSearchBar.jsx";
import Range from "./Range.jsx";
import CandleChart from "./CandleChart.jsx";
import { getToken } from "../auth.js";

const BASE = import.meta.env.VITE_BACKEND_HOST;


const LstmAnalysis = () => {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedCrypto, setSelectedCrypto] = useState(null);

  const [ohlc, setOhlc] = useState([]);

  const [forecast, setForecast] = useState([]);
  const [evaluation, setEvaluation] = useState(null);
  const [lookback, setLookback] = useState(30);
  const [horizon, setHorizon] = useState(7);

  const [loading, setLoading] = useState(false);
  const [range, setRange] = useState("ALL");
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const res = await fetch(
        `${BASE}/api/crypto/search?query=${encodeURIComponent(
          value
        )}`
      );
      const data = await res.json();
      setSearchResults(data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadOhlc = async (cryptoId) => {
    const token = getToken();
    if (!token) {
      throw new Error("Not logged in. Please login again.");
    }

    const res = await fetch(
      `${BASE}/api/data/daily/${cryptoId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) {
      throw new Error("Failed to load historical OHLC");
    }

    const data = await res.json();

    const mapped = data.map((d) => ({
      date: d.date,
      open: d.open_price,
      high: d.high_price,
      low: d.low_price,
      close: d.close_price,
    }));

    mapped.sort((a, b) => new Date(a.date) - new Date(b.date));
    setOhlc(mapped);
  };

  const loadLstm = async (cryptoId) => {
    const token = getToken();
    if (!token) {
      throw new Error("Not logged in. Please login again.");
    }

    const res = await fetch(
      `${BASE}/api/analysis/lstm?cryptoId=${encodeURIComponent(cryptoId)}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}));
      throw new Error(errJson.detail || "Failed to fetch LSTM forecast");
    }

    const data = await res.json();

    const mappedForecast = (data.forecast || []).map((d) => ({
      date: d.date,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));

    mappedForecast.sort((a, b) => new Date(a.date) - new Date(b.date));

    setForecast(mappedForecast);
    setEvaluation(data.evaluation || null);
  };

  const chooseCrypto = async (crypto) => {
    setSelectedCrypto(crypto);
    setQuery(crypto.name);
    setSearchResults([]);
    setError("");

    setLoading(true);
    try {
      setOhlc([]);
      setForecast([]);
      setEvaluation(null);

      await loadOhlc(crypto.id);
      await loadLstm(crypto.id);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const combined = [...ohlc, ...forecast].sort(
    (a, b) => new Date(a.date) - new Date(b.date)
  );

  const getVisibleData = () => {
    if (range === "ALL") return combined;

    const n = parseInt(range, 10);
    if (!combined || combined.length <= n) return combined;
    return combined.slice(combined.length - n);
  };

  const visibleData = getVisibleData();

  return (
    <div
      className="p-20 maxWidth:900 m-auto"
      data-aos="fade-up"
      data-aos-delay="600"
    >
      <CryptoSearchBar
        query={query}
        searchResults={searchResults}
        onSearchChange={handleSearch}
        onCryptoSelect={chooseCrypto}
      />

      {error && (
        <div className="mt-4 p-3 rounded-lg bg-red-100 text-red-700">
          {error}
        </div>
      )}

      {(ohlc.length > 0 || forecast.length > 0) && !loading && (
        <div className="mt-6 flex items-center justify-between gap-4 flex-wrap">
          <Range range={range} onChange={setRange} />
        </div>
      )}

      <div className="mt-6">
        <CandleChart visibleData={visibleData} loading={loading} />
      </div>
    </div>
  );
}

export default LstmAnalysis;
