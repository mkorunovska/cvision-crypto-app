import React, { useMemo, useState } from "react";
import CryptoSearchBar from "../components/CryptoSearchBar";
import { getToken } from "../auth.js";

const SUPPORTED = new Set(["bitcoin", "ethereum"]);
const SPRING_BASE = "http://localhost:8000";

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

function StatCard({ label, value }) {
  return (
    <div className="border border-slate-200 rounded-xl p-3 bg-slate-50">
      <div className="text-xs text-slate-600">{label}</div>
      <div className="text-lg font-bold text-slate-900 mt-1">{value}</div>
    </div>
  );
}

const SentimentAnalysis = () => {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const [selectedCrypto, setSelectedCrypto] = useState(null);

  const [loading, setLoading] = useState(false);
  const [warn, setWarn] = useState("");
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  const endpoint = useMemo(() => {
    if (!selectedCrypto?.id) return "";
    const params = new URLSearchParams({
      cryptoId: selectedCrypto.id,
      timeframe: "day",
      daysBack: "365",
      limit: "40",
    });

    return `${SPRING_BASE}/api/analysis/onchain-sentiment?${params.toString()}`;
  }, [selectedCrypto]);

  const onSearchChange = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const res = await fetch(
        `http://localhost:8000/api/crypto/search?query=${encodeURIComponent(
          value
        )}`
      );
      const data = await res.json();
      setSearchResults(Array.isArray(data) ? data : []);
    } catch {
      setSearchResults([]);
    }
  };

  const onCryptoSelect = async (crypto) => {
    setQuery(crypto.name);
    setSearchResults([]);
    setError("");
    setData(null);

    if (!SUPPORTED.has(crypto.id)) {
      setSelectedCrypto(null);
      setWarn(
        "On-chain and sentiment analysis is not available for selected cryptocoin."
      );
      return;
    }

    setWarn("");
    setSelectedCrypto(crypto);

    await runAnalysis(crypto.id);
  };

  const runAnalysis = async (cryptoIdOverride) => {
    const cryptoId = cryptoIdOverride || selectedCrypto?.id;
    if (!cryptoId) return;

    setLoading(true);
    setError("");
    setData(null);

    const params = new URLSearchParams({
      cryptoId,
      timeframe: "day",
      daysBack: "365",
      limit: "40",
    });

    const url = `${SPRING_BASE}/api/analysis/onchain-sentiment?${params.toString()}`;

    try {
      const token = getToken();
      if (!token) {
        throw new Error("Not logged in. Please login.");
      }

      const res = await fetch(url, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `HTTP ${res.status}`);
      }
      const json = await res.json();
      setData(json);
    } catch (e) {
      setError(e?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  const combined = data?.combined;
  const sentiment = data?.sentiment;
  const metrics = data?.onchain?.metrics;

  return (
    <div className="min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6 mx-6 text-white">
          On Chain and Sentiment Analysis
        </h1>

        <div className="mt-6 rounded-xl p-5">
          <CryptoSearchBar
            query={query}
            searchResults={searchResults}
            onSearchChange={onSearchChange}
            onCryptoSelect={onCryptoSelect}
          />

          {warn && (
            <div className="mt-3 p-3 bg-blue-50 border border-darkblue-300 rounded text-black">
              {warn}
            </div>
          )}

          <div className="flex items-end">
            <button
              onClick={() => runAnalysis()}
              disabled={!selectedCrypto || loading}
              className="w-full px-4 py-2 rounded-lg bg-white text-darkblue font-semibold hover:bg-slate-100"
            >
              {loading ? "Running..." : "Run analysis"}
            </button>
          </div>
        </div>

        {data && (
          <div className="mt-6 space-y-6">
            <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h2 className="text-xl font-semibold text-slate-900">
                    Combined signal
                  </h2>
                </div>

                <div className="flex items-center gap-3">
                  <span
                    className={`inline-flex items-center px-3 py-1 rounded-full border text-sm font-semibold ${badgeClass(
                      combined?.signal
                    )}`}
                  >
                    {combined?.signal || "—"}
                  </span>
                  <div className="text-right">
                    <div className="text-xs text-slate-500">Score</div>
                    <div className="text-lg font-bold text-slate-900">
                      {combined?.score?.toFixed?.(2) ?? "—"}
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-2">
                  Reasons
                </h3>
                {combined?.reasons?.length ? (
                  <ul className="list-disc ml-5 text-slate-700 space-y-1">
                    {combined.reasons.map((r, idx) => (
                      <li key={idx}>{r}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-600 text-sm">No reasons provided.</p>
                )}
              </div>
            </section>

            <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
              <h2 className="text-xl font-semibold text-slate-900">
                On-chain metrics
              </h2>

              <div className="overflow-x-auto mt-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-slate-600 border-b">
                      <th className="py-2 pr-4">Metric</th>
                      <th className="py-2 pr-4">Value</th>
                      <th className="py-2 pr-4">Change (7)</th>
                    </tr>
                  </thead>
                  <tbody className="text-slate-800">
                    {metrics ? (
                      Object.entries(metrics).map(([k, v]) => (
                        <tr key={k} className="border-b last:border-b-0">
                          <td className="py-2 pr-4 font-medium">{k}</td>
                          <td className="py-2 pr-4">{v?.value}</td>
                          <td className="py-2 pr-4">{v?.change_7}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td className="py-2 text-slate-600" colSpan={3}>
                          No on-chain metrics returned.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>

            <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
              <h2 className="text-xl font-semibold text-slate-900">
                Sentiment
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mt-4">
                <StatCard label="Label" value={sentiment?.label ?? "—"} />
                <StatCard
                  label="Avg score"
                  value={sentiment?.avg_score?.toFixed?.(4) ?? "—"}
                />
                <StatCard label="Headlines" value={sentiment?.count ?? "—"} />
                <StatCard
                  label="Positive/Neutral/Negative"
                  value={`${sentiment?.positive ?? 0}/${
                    sentiment?.neutral ?? 0
                  }/${sentiment?.negative ?? 0}`}
                />
              </div>

              <div className="mt-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-2">
                  Headlines
                </h3>
                {sentiment?.examples?.length ? (
                  <ul className="list-disc ml-5 text-slate-700 space-y-1">
                    {sentiment.examples.map((h, idx) => (
                      <li key={idx}>{h}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-600 text-sm">No examples.</p>
                )}
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  );
};

export default SentimentAnalysis;
