from __future__ import annotations
import os
import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import requests
import feedparser
from transformers import pipeline


COIN_MAP = {
    "bitcoin":  {"asset": "BTC", "tvl_chain": None},
    "ethereum": {"asset": "ETH", "tvl_chain": "Ethereum"},
}

TIMEFRAME_RULE = {"day": "D", "week": "W", "month": "ME"}


NEWS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://news.google.com/rss/search?q=bitcoin+OR+ethereum+cryptocurrency&hl=en-US&gl=US&ceid=US:en",
]


BLOCKCHAIN_CHARTS = "https://api.blockchain.info/charts"
BTC_CHARTS = {
    "tx_count": "n-transactions",
    "hash_rate": "hash-rate",
}


DEFILLAMA_HISTORICAL_CHAIN_TVL = "https://api.llama.fi/v2/historicalChainTvl"


GLASSNODE_BASE = "https://api.glassnode.com/v1/metrics"
GLASSNODE_METRICS = {
    "active_addresses": "/addresses/active_count",
}


SENT_MODEL = os.getenv("SENTIMENT_MODEL", "ProsusAI/finbert")
sent_pipe = pipeline("text-classification", model=SENT_MODEL, tokenizer=SENT_MODEL, truncation=True)


def epoch_range(days_back: int) -> Tuple[int, int]:
    u = int(time.time())
    s = u - days_back * 24 * 3600
    return s, u


def resample_df(df: pd.DataFrame, timeframe: str) -> pd.Series:
    if timeframe not in TIMEFRAME_RULE:
        raise ValueError("timeframe must be: day|week|month")
    rule = TIMEFRAME_RULE[timeframe]
    dfi = df.set_index("date").sort_index()

    if timeframe == "day":
        s = dfi["value"]
    else:
        s = dfi["value"].resample(rule).mean()

    return s


def last_value_and_change(s: pd.Series) -> Dict[str, float]:
    s = s.dropna()
    if len(s) == 0:
        return {"value": float("nan"), "change_7": float("nan")}
    last = float(s.iloc[-1])
    if len(s) < 8:
        return {"value": last, "change_7": float("nan")}
    prev = float(s.iloc[-8])
    if prev == 0:
        return {"value": last, "change_7": float("nan")}
    return {"value": last, "change_7": (last - prev) / abs(prev) * 100.0}



def fetch_blockchain_chart(chart_name: str, days_back: int) -> pd.DataFrame:
    if days_back <= 370:
        timespan = "1year"
    elif days_back <= 760:
        timespan = "2years"
    else:
        timespan = "all"

    url = f"{BLOCKCHAIN_CHARTS}/{chart_name}"
    r = requests.get(url, params={"format": "json", "timespan": timespan}, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Blockchain.com {r.status_code}: {r.text[:200]}")
    js = r.json()
    values = js.get("values", [])
    df = pd.DataFrame(values)
    if df.empty:
        raise RuntimeError("Empty Blockchain.com chart data")

    df["date"] = pd.to_datetime(df["x"], unit="s", utc=True).dt.tz_convert(None)
    df["value"] = pd.to_numeric(df["y"], errors="coerce")
    df = df[["date", "value"]].dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    # trim to days_back (rough)
    cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=days_back)
    df = df[df["date"] >= cutoff].reset_index(drop=True)

    return df


def fetch_defillama_chain_tvl(chain: str, days_back: int) -> pd.DataFrame:
    r = requests.get(DEFILLAMA_HISTORICAL_CHAIN_TVL, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"DeFiLlama {r.status_code}: {r.text[:200]}")
    all_chains = r.json()
    if chain not in all_chains:
        raise RuntimeError(f"Chain '{chain}' not found in DeFiLlama")

    arr = all_chains[chain]
    df = pd.DataFrame(arr)
    if df.empty:
        raise RuntimeError("Empty DeFiLlama TVL data")

    df["date"] = pd.to_datetime(df["date"], unit="s", utc=True).dt.tz_convert(None)
    df["value"] = pd.to_numeric(df["tvl"], errors="coerce")
    df = df[["date", "value"]].dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=days_back)
    df = df[df["date"] >= cutoff].reset_index(drop=True)

    return df


def fetch_glassnode_active_addresses(asset: str, days_back: int) -> pd.DataFrame:
    api_key = os.getenv("GLASSNODE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("No GLASSNODE_API_KEY set")

    s, u = epoch_range(days_back)
    url = f"{GLASSNODE_BASE}{GLASSNODE_METRICS['active_addresses']}"
    params = {"a": asset.upper(), "i": "24h", "s": s, "u": u, "api_key": api_key}

    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Glassnode {r.status_code}: {r.text[:200]}")
    data = r.json()
    df = pd.DataFrame(data)
    if df.empty or "t" not in df.columns or "v" not in df.columns:
        raise RuntimeError("Bad response")

    df["date"] = pd.to_datetime(df["t"], unit="s", utc=True).dt.tz_convert(None)
    df["value"] = pd.to_numeric(df["v"], errors="coerce")
    df = df[["date", "value"]].dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


def fetch_headlines(query: str, limit: int = 40) -> List[str]:
    query_l = query.lower().strip()
    out: List[str] = []
    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)
        for e in feed.entries[:80]:
            title = (getattr(e, "title", "") or "").strip()
            if not title:
                continue
            if query_l and query_l not in title.lower():
                continue
            out.append(title)
            if len(out) >= limit:
                return out
    return out


def sentiment_transformers(headlines: List[str]) -> Dict[str, Any]:
    if not headlines:
        return {
            "count": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "avg_score": 0.0,
            "label": "neutral",
            "examples": [],
        }

    preds = sent_pipe(headlines)

    pos = neu = neg = 0
    score_sum = 0.0

    for r in preds:
        label = r["label"].lower()
        score = float(r["score"])
        if "pos" in label:
            pos += 1
            score_sum += score
        elif "neg" in label:
            neg += 1
            score_sum -= score
        else:
            neu += 1

    avg_score = score_sum / max(1, len(headlines))

    if avg_score >= 0.05:
        overall = "positive"
    elif avg_score <= -0.05:
        overall = "negative"
    else:
        overall = "neutral"

    return {
        "count": len(headlines),
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "avg_score": float(avg_score),
        "label": overall,
        "examples": headlines[:5],
    }


def combine_signal(onchain: Dict[str, Any], sent: Dict[str, Any]) -> Dict[str, Any]:
    score = 0.0
    reasons: List[str] = []


    if sent["label"] == "positive":
        score += 1.0
        reasons.append("Sentiment is positive.")
    elif sent["label"] == "negative":
        score -= 1.0
        reasons.append("Sentiment is negative.")
    else:
        reasons.append("Sentiment is neutral.")

    tx = onchain.get("tx_count")
    if tx and not np.isnan(tx.get("change_7", np.nan)):
        if tx["change_7"] > 5:
            score += 0.6
            reasons.append("Transaction count increased.")
        elif tx["change_7"] < -5:
            score -= 0.6
            reasons.append("Transaction count decreased.")


    hr = onchain.get("hash_rate")
    if hr and not np.isnan(hr.get("change_7", np.nan)):
        if hr["change_7"] > 3:
            score += 0.4
            reasons.append("Hash rate increased.")
        elif hr["change_7"] < -3:
            score -= 0.4
            reasons.append("Hash rate decreased.")


    tvl = onchain.get("tvl")
    if tvl and not np.isnan(tvl.get("change_7", np.nan)):
        if tvl["change_7"] > 5:
            score += 0.5
            reasons.append("TVL increased.")
        elif tvl["change_7"] < -5:
            score -= 0.5
            reasons.append("TVL decreased.")


    aa = onchain.get("active_addresses")
    if aa and not np.isnan(aa.get("change_7", np.nan)):
        if aa["change_7"] > 5:
            score += 0.5
            reasons.append("Active addresses increased.")
        elif aa["change_7"] < -5:
            score -= 0.5
            reasons.append("Active addresses decreased.")


    if score >= 1.2:
        signal = "BUY"
    elif score <= -1.2:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {"signal": signal, "score": float(score), "reasons": reasons}

