import React, { useState } from "react";
import CryptoSearchBar from "./CryptoSearchBar.jsx"
import Range from "./Range.jsx";
import CandleChart from "./CandleChart.jsx";

function DetailsPage() {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedCrypto, setSelectedCrypto] = useState(null);
  const [ohlc, setOhlc] = useState([]);
  const [loading, setLoading] = useState(false);
  const [range, setRange] = useState("ALL");

  const handleSearch = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length < 2) {
      setSearchResults([]);
      return;
    }

    const res = await fetch(
      `http://localhost:8000/api/crypto/search?query=${encodeURIComponent(
        value
      )}`
    );
    const data = await res.json();
    setSearchResults(data);
  };

  const chooseCrypto = async (crypto) => {
    setSelectedCrypto(crypto);
    setQuery(crypto.name);
    setSearchResults([]);

    await loadOhlc(crypto.id);
  };

  const loadOhlc = async (cryptoId) => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/api/data/daily/${cryptoId}`);
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
    setLoading(false);
  };

  const getVisibleData = () => {
    if (range === "ALL") return ohlc;

    const n = parseInt(range, 10); 
    if (!ohlc || ohlc.length <= n) return ohlc;
    return ohlc.slice(ohlc.length - n); 
  };

  const visibleData = getVisibleData();

  return (
    <div className="p-20 maxWidth:900 m-auto" data-aos='fade-up' data-aos-delay='600' 
    >
      <CryptoSearchBar
        query={query}
        searchResults={searchResults}
        onSearchChange={handleSearch}
        onCryptoSelect={chooseCrypto}
      />

      {ohlc.length > 0 && !loading && (
        <Range range={range} onChange={setRange} />
      )}

      <CandleChart visibleData={visibleData} loading={loading} />
    </div>
  );
}

export default DetailsPage;
