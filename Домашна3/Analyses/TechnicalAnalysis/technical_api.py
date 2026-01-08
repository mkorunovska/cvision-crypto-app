from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from technical_analysis import analyze_crypto, get_all_crypto_ids


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