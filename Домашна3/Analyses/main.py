from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from TechnicalAnalysis.technical_analysis import analyze_crypto, get_all_crypto_ids
from LSTM.lstm_analysis import predictor_ohlcv
from SentimentOnChain.sentiment_analysis import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/cryptos", response_model=List[str])
def get_crypto_ids():
    ids = get_all_crypto_ids()
    if not ids:
        raise HTTPException(status_code=404, detail="No cryptocurrencies found in DB")
    return ids


@app.get("/technical_analysis/{crypto_id}")
def get_technical_analysis(
    crypto_id: str,
    period: str = Query("day", description="One of: day, week, month"),
):

    period_map = {
        "day": "1D",
        "week": "1W",
        "month": "1M",
    }

    if period not in period_map:
        raise HTTPException(
            status_code=400,
            detail="Invalid period. Use one of: day, week, month",
        )

    try:
        all_results = analyze_crypto(crypto_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while analyzing crypto_id={crypto_id}: {e}",
        )

    tf_key = period_map[period]

    if tf_key not in all_results:
        raise HTTPException(
            status_code=404,
            detail=f"No analysis result for period {period} ({tf_key})",
        )

    tf_result = all_results[tf_key]

    return {
        "cryptoId": crypto_id,
        "timeframe": tf_key,
        "date": tf_result["date"],
        "price": tf_result["price"],
        "overall_signal": tf_result["overall_signal"],
        "indicators": tf_result["indicators"],
    }


@app.get("/lstm_analysis/{crypto_id}")
def get_lstm_analysis(crypto_id: str):
    LOOKBACK = 30
    HORIZON = 7

    try:

        ids = get_all_crypto_ids()
        if crypto_id not in ids:
            raise HTTPException(status_code=404, detail=f"crypto_id '{crypto_id}' not found")

        result = predictor_ohlcv(crypto_id=crypto_id, lag=LOOKBACK, num_prediction=HORIZON)

        if "evaluation" in result:
            for _, metrics in result["evaluation"].items():
                for k, v in metrics.items():
                    metrics[k] = float(v)

        return {
            "cryptoId": result["crypto_id"],
            "lookback": LOOKBACK,
            "horizon": HORIZON,
            "forecast": result["forecast"],
            "evaluation": result.get("evaluation"),
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while LSTM for {crypto_id}: {e}")



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

    return {
        "cryptoId": key,
        "asset": asset,
        "timeframe": timeframe,
        "days_back": days_back,
        "metrics": out,
        "errors": errors
    }

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




