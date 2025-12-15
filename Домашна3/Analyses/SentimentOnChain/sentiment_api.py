from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sentiment_analysis import *
app = FastAPI(title="On-chain + Sentiment (BTC/ETH)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sentiment")
def api_sentiment(cryptoId: str, limit: int = 40):
    key = cryptoId.lower().strip()
    if key not in COIN_MAP:
        raise HTTPException(status_code=400, detail="Supported: bitcoin, ethereum")

    headlines = fetch_headlines(query=key, limit=limit)
    sent = sentiment_transformers(headlines)
    return {"cryptoId": key, "sentiment": sent}


@app.get("/onchain")
def api_onchain(cryptoId: str, timeframe: str = "day", days_back: int = 365):
    key = cryptoId.lower().strip()
    timeframe = timeframe.lower()

    if key not in COIN_MAP:
        raise HTTPException(status_code=400, detail="Supported: bitcoin, ethereum")
    if timeframe not in TIMEFRAME_RULE:
        raise HTTPException(status_code=400, detail="timeframe must be day|week|month")

    asset = COIN_MAP[key]["asset"]
    tvl_chain = COIN_MAP[key]["tvl_chain"]

    out: Dict[str, Any] = {}
    errors: Dict[str, str] = {}

    if asset == "BTC":
        try:
            df_tx = fetch_blockchain_chart(BTC_CHARTS["tx_count"], days_back=days_back)
            s_tx = resample_df(df_tx, timeframe)
            stats = last_value_and_change(s_tx)
            out["tx_count"] = {"value": stats["value"], "change_7": stats["change_7"]}
        except Exception as e:
            errors["tx_count"] = str(e)

        try:
            df_hr = fetch_blockchain_chart(BTC_CHARTS["hash_rate"], days_back=days_back)
            s_hr = resample_df(df_hr, timeframe)
            stats = last_value_and_change(s_hr)
            out["hash_rate"] = {"value": stats["value"], "change_7": stats["change_7"]}
        except Exception as e:
            errors["hash_rate"] = str(e)

        try:
            df_aa = fetch_glassnode_active_addresses(asset="BTC", days_back=days_back)
            s_aa = resample_df(df_aa, timeframe)
            stats = last_value_and_change(s_aa)
            out["active_addresses"] = {"value": stats["value"], "change_7": stats["change_7"]}
        except Exception as e:
            errors["active_addresses"] = str(e)

    if asset == "ETH" and tvl_chain:
        try:
            df_tvl = fetch_defillama_chain_tvl(chain=tvl_chain, days_back=days_back)
            s_tvl = resample_df(df_tvl, timeframe)
            stats = last_value_and_change(s_tvl)
            out["tvl"] = {"value": stats["value"], "change_7": stats["change_7"], "chain": tvl_chain}
        except Exception as e:
            errors["tvl"] = str(e)

    return {"cryptoId": key, "asset": asset, "timeframe": timeframe, "days_back": days_back, "metrics": out, "errors": errors}


@app.get("/combined")
def api_combined(cryptoId: str, timeframe: str = "day", days_back: int = 365, limit: int = 40):
    key = cryptoId.lower().strip()
    timeframe = timeframe.lower()

    if key not in COIN_MAP:
        raise HTTPException(status_code=400, detail="Supported: bitcoin, ethereum")
    if timeframe not in TIMEFRAME_RULE:
        raise HTTPException(status_code=400, detail="timeframe must be day|week|month")

    oc = api_onchain(cryptoId=key, timeframe=timeframe, days_back=days_back)
    sent = api_sentiment(cryptoId=key, limit=limit)["sentiment"]

    combo = combine_signal(oc["metrics"], sent)

    return {
        "cryptoId": key,
        "asset": oc["asset"],
        "timeframe": timeframe,
        "onchain": oc,
        "sentiment": sent,
        "combined": combo,
    }
