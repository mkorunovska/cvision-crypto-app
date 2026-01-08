import numpy as np
from typing import List
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input


from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score

from db_connection import engine

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


def mape(y_true, y_pred):
    return mean_absolute_percentage_error(y_true, y_pred)


def r2(y_true, y_pred):
    return r2_score(y_true, y_pred)


FEATURES = ["open", "high", "low", "close", "volume"]


def parse_data(crypto_id: str) -> pd.DataFrame:
    query = """
        SELECT
            date,
            open_price  AS open,
            high_price  AS high,
            low_price   AS low,
            close_price AS close,
            volume_24 AS volume
        FROM daily_market_data
        WHERE crypto_id = %(crypto_id)s
        ORDER BY date;
    """
    df = pd.read_sql(query, engine, params={"crypto_id": crypto_id})

    if df.empty:
        raise ValueError(f"No data found for crypto_id={crypto_id}")

    return df

def get_all_crypto_ids() -> List[str]:
    query = """
        SELECT DISTINCT crypto_id
        FROM daily_market_data
        ORDER BY crypto_id;
    """
    df_ids = pd.read_sql(query, engine)
    return df_ids["crypto_id"].tolist()


def predictor_ohlcv(
    crypto_id: str,
    lag: int = 30,
    num_prediction: int = 7
):

    df = parse_data(crypto_id)

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    for c in FEATURES:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["open", "high", "low", "close"])
    df["volume"] = df["volume"].fillna(0)
    df.loc[df["volume"] < 0, "volume"] = 0

    if len(df) < max(60, lag + 10):
        raise ValueError("Not enough data for LSTM prediction")


    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[FEATURES].values)

    s = pd.DataFrame(scaled, index=df.index, columns=FEATURES)


    X_parts = []
    for p in range(lag, 0, -1):
        shifted = s.shift(p).copy()
        shifted.columns = [f"{c}_t-{p}" for c in FEATURES]
        X_parts.append(shifted)

    X_df = pd.concat(X_parts, axis=1)
    y_df = s[FEATURES]

    full = pd.concat([y_df, X_df], axis=1).dropna()

    y = full[FEATURES].values
    X = full.drop(columns=FEATURES).values

    n_features = len(FEATURES)

    X = X.reshape(X.shape[0], lag, n_features)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False
    )

    model = Sequential([
        Input(shape=(lag, n_features)),
        LSTM(100, activation="relu", return_sequences=True),
        LSTM(50, activation="relu"),
        Dense(n_features, activation="linear")
    ])

    # model.compile(
    #     loss=keras.losses.MeanSquaredError(),
    #     optimizer=keras.optimizers.Adam(),
    #     metrics=[
    #         keras.metrics.MeanSquaredError(),
    #         keras.metrics.MeanAbsoluteError()
    #     ]
    # )

    model.compile(
        loss="mse",
        optimizer="adam",
        metrics=["mse", "mae"]
    )

    model.fit(
        X_train,
        y_train,
        batch_size=16,
        validation_split=0.2,
        epochs=10,
        shuffle=False,
        verbose=0
    )


    y_test_pred_scaled = model.predict(X_test, verbose=0)

    y_test_real = scaler.inverse_transform(y_test)
    y_test_pred_real = scaler.inverse_transform(y_test_pred_scaled)

    evaluation = {}
    for i, feature in enumerate(FEATURES):
        evaluation[feature] = {
            "RMSE": rmse(y_test_real[:, i], y_test_pred_real[:, i]),
            "MAPE": mape(y_test_real[:, i], y_test_pred_real[:, i]),
            "R2": r2(y_test_real[:, i], y_test_pred_real[:, i]),
        }


    last_window = s.values[-lag:].copy()
    preds_scaled = []

    for _ in range(num_prediction):
        x_input = last_window.reshape(1, lag, n_features)
        next_scaled = model.predict(x_input, verbose=0)[0]

        next_scaled = np.clip(next_scaled, 0.0, 1.0)

        preds_scaled.append(next_scaled)
        last_window = np.vstack([last_window[1:], next_scaled])

    preds_scaled = np.array(preds_scaled)
    preds = scaler.inverse_transform(preds_scaled)

    for i in range(len(preds)):
        o, h, l, c, v = preds[i]
        h = max(h, o, c)
        l = min(l, o, c)
        v = max(v, 0.0)
        preds[i] = [o, h, l, c, v]


    last_date = df.index[-1]
    forecast_dates = [
        d.strftime("%Y-%m-%d")
        for d in pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=num_prediction,
            freq="D"
        )
    ]

    forecast = []
    for i in range(num_prediction):
        forecast.append({
            "date": forecast_dates[i],
            "open": float(preds[i, 0]),
            "high": float(preds[i, 1]),
            "low": float(preds[i, 2]),
            "close": float(preds[i, 3]),
            "volume": float(preds[i, 4]),
        })

    history_tail = df[FEATURES].tail(min(500, len(df)))
    history = [
        {
            "date": idx.strftime("%d.%m.%Y"),
            "open": float(r["open"]),
            "high": float(r["high"]),
            "low": float(r["low"]),
            "close": float(r["close"]),
            "volume": float(r["volume"]),
        }
        for idx, r in history_tail.iterrows()
    ]

    return {
        "crypto_id": crypto_id,
        "lag": lag,
        "horizon": num_prediction,
        "forecast": forecast,
        "evaluation": evaluation,
    }