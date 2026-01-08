from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from lstm_analysis import predictor_ohlcv, get_all_crypto_ids

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