import math
from typing import Dict, Tuple, List, Optional
import pandas as pd
import ta
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, ADXIndicator, CCIIndicator, SMAIndicator, EMAIndicator, WMAIndicator
from ta.volatility import BollingerBands
from db_connection import engine


Signal = str

def safe_val(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def load_data(crypto_id: str) -> pd.DataFrame:
    query = """
        SELECT
            date,
            open_price  AS open,
            high_price  AS high,
            low_price   AS low,
            close_price AS close,
            volume_24h   AS volume
        FROM daily_market_data
        WHERE crypto_id = %(crypto_id)s
        ORDER BY date;
    """
    df = pd.read_sql(query, engine, params={"crypto_id": crypto_id})
    if df.empty:
        raise ValueError(f"No data found for crypto_id={crypto_id}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").set_index("date")
    return df


def get_all_crypto_ids() -> List[str]:
    query = """
        SELECT DISTINCT crypto_id
        FROM daily_market_data
        ORDER BY crypto_id;
    """
    df_ids = pd.read_sql(query, engine)
    return df_ids["crypto_id"].tolist()


def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    df_res = df.resample(rule).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    ).dropna()
    return df_res


def calculate_relative_strength_index(close: pd.Series, window: int = 14) -> Tuple[Optional[float], Signal]:
    rsi_series = ta.momentum.RSIIndicator(close=close, window=window).rsi()
    rsi_val = safe_val(rsi_series.iloc[-1])

    if rsi_val is None:
        return None, "HOLD"

    if rsi_val < 30:
        return float(rsi_val), "BUY"
    if rsi_val > 70:
        return float(rsi_val), "SELL"
    return float(rsi_val), "HOLD"


def calculate_macd(close: pd.Series) -> Tuple[Optional[float], Signal]:
    macd_obj = ta.trend.MACD(close=close)
    macd_val = safe_val(macd_obj.macd().iloc[-1])
    macd_sig = safe_val(macd_obj.macd_signal().iloc[-1])

    if macd_val is None or macd_sig is None:
        return None, "HOLD"

    if macd_val > macd_sig:
        return float(macd_val), "BUY"
    if macd_val < macd_sig:
        return float(macd_val), "SELL"
    return float(macd_val), "HOLD"


def calculate_stochastic_oscillator(high: pd.Series,low: pd.Series,close: pd.Series) -> Tuple[Optional[float], Signal]:
    stoch = ta.momentum.StochasticOscillator(high=high, low=low, close=close)
    k_series = stoch.stoch()
    k_val = safe_val(k_series.iloc[-1])

    if k_val is None:
        return None, "HOLD"

    if k_val < 20:
        return float(k_val), "BUY"
    if k_val > 80:
        return float(k_val), "SELL"
    return float(k_val), "HOLD"


def calculate_adx(high: pd.Series,low: pd.Series,close: pd.Series) -> Tuple[Optional[float], Signal]:
    adx_series = ta.trend.ADXIndicator(high=high, low=low, close=close).adx()
    adx_val = safe_val(adx_series.iloc[-1])

    if adx_val is None:
        return None, "HOLD"

    if adx_val < 20:
        return float(adx_val), "HOLD"

    return float(adx_val), "BUY"


def calculate_cci(high: pd.Series,low: pd.Series, close: pd.Series,window: int = 20) -> Tuple[Optional[float], Signal]:
    cci_series = ta.trend.CCIIndicator(
        high=high,
        low=low,
        close=close,
        window=window
    ).cci()
    cci_val = safe_val(cci_series.iloc[-1])

    if cci_val is None:
        return None, "HOLD"

    if cci_val > 100:
        return float(cci_val), "BUY"
    if cci_val < -100:
        return float(cci_val), "SELL"
    return float(cci_val), "HOLD"


def calculate_moving_average_trend(close: pd.Series,window: int = 20
) -> Tuple[Optional[float], Optional[float], Optional[float], Signal]:

    sma_series = ta.trend.SMAIndicator(close=close, window=window).sma_indicator()
    ema_series = ta.trend.EMAIndicator(close=close, window=window).ema_indicator()
    wma_series = ta.trend.WMAIndicator(close=close, window=window).wma()

    sma_val = safe_val(sma_series.iloc[-1])
    ema_val = safe_val(ema_series.iloc[-1])
    wma_val = safe_val(wma_series.iloc[-1])

    price = safe_val(close.iloc[-1])

    if price is None or sma_val is None or ema_val is None or wma_val is None:
        return sma_val, ema_val, wma_val, "HOLD"

    above_sma = price > sma_val
    above_ema = price > ema_val
    above_wma = price > wma_val
    count_above = sum([above_sma, above_ema, above_wma])

    if count_above == 3:
        return float(sma_val), float(ema_val), float(wma_val), "BUY"
    if count_above == 0:
        return float(sma_val), float(ema_val), float(wma_val), "SELL"
    return float(sma_val), float(ema_val), float(wma_val), "HOLD"


def calculate_bollinger_bands(close: pd.Series, window: int = 20,window_dev: float = 2.0
) -> Tuple[Optional[float], Optional[float], Optional[float], Signal]:

    bb = ta.volatility.BollingerBands(
        close=close, window=window,
        window_dev=window_dev
    )

    mid_series = bb.bollinger_mavg()
    low_series = bb.bollinger_lband()
    up_series = bb.bollinger_hband()

    mid_val = safe_val(mid_series.iloc[-1])
    low_val = safe_val(low_series.iloc[-1])
    up_val = safe_val(up_series.iloc[-1])

    price = safe_val(close.iloc[-1])

    if price is None or low_val is None or up_val is None:
        return mid_val, low_val, up_val, "HOLD"

    if price < low_val:
        return float(mid_val), float(low_val), float(up_val), "BUY"
    if price > up_val:
        return float(mid_val), float(low_val), float(up_val), "SELL"
    return float(mid_val), float(low_val), float(up_val), "HOLD"


def calculate_volume_ma(volume: pd.Series,window: int = 20,high_ratio: float = 1.2,low_ratio: float = 0.8
) -> Tuple[Optional[float], Signal]:

    vol_ma_series = ta.trend.SMAIndicator(close=volume, window=window).sma_indicator()
    vol_ma_val = safe_val(vol_ma_series.iloc[-1])
    vol_val = safe_val(volume.iloc[-1])

    if vol_ma_val is None or vol_val is None or vol_ma_val == 0:
        return vol_ma_val, "HOLD"

    ratio = vol_val / vol_ma_val

    if ratio > high_ratio:
        return float(vol_ma_val), "BUY"
    if ratio < low_ratio:
        return float(vol_ma_val), "SELL"
    return float(vol_ma_val), "HOLD"


def overall_signal(indicator_signals: Dict[str, Signal]) -> Signal:
    counter = {"BUY": 0, "SELL": 0, "HOLD": 0}

    for sig in indicator_signals.values():
        counter[sig] += 1

    best_label, best_count = max(counter.items(), key=lambda kv: kv[1])

    if list(counter.values()).count(best_count) > 1:
        return "HOLD"

    return best_label


def analyze_indicators(df: pd.DataFrame) -> Dict:
    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    last_price = safe_val(close.iloc[-1])
    price = float(last_price) if last_price is not None else None

    rsi_val, rsi_sig = calculate_relative_strength_index(close)
    macd_val, macd_sig = calculate_macd(close)
    stoch_val, stoch_sig = calculate_stochastic_oscillator(high, low, close)
    adx_val, adx_sig = calculate_adx(high, low, close)
    cci_val, cci_sig = calculate_cci(high, low, close)

    sma_val, ema_val, wma_val, ma_sig = calculate_moving_average_trend(close)
    bb_mid, bb_low, bb_up, bb_sig = calculate_bollinger_bands(close)
    vol_ma_val, vol_sig = calculate_volume_ma(volume)

    indicators = {
        "RSI": {
            "value": rsi_val,
            "signal": rsi_sig,
        },
        "MACD": {
            "value": macd_val,
            "signal": macd_sig,
        },
        "Stochastic": {
            "value": stoch_val,
            "signal": stoch_sig,
        },
        "ADX": {
            "value": adx_val,
            "signal": adx_sig,
        },
        "CCI": {
            "value": cci_val,
            "signal": cci_sig,
        },
        "SMA": {
            "value": sma_val,
            "signal": ma_sig,
        },
        "EMA": {
            "value": ema_val,
            "signal": ma_sig,
        },
        "WMA": {
            "value": wma_val,
            "signal": ma_sig,
        },
        "Bollinger": {
            "value": bb_mid,
            "signal": bb_sig,
        },
        "Volume_MA": {
            "value": vol_ma_val,
            "signal": vol_sig,
        },
    }

    signals_only = {name: info["signal"] for name, info in indicators.items()}
    overall = overall_signal(signals_only)

    return {
        "price": price,
        "indicators": indicators,
        "overall_signal": overall,
    }


def analyze_timeframe(df: pd.DataFrame, label: str) -> Dict:
    result = analyze_indicators(df)
    last_date = df.index[-1]

    return {
        "timeframe": label,
        "date": last_date.strftime("%Y-%m-%d"),
        "price": result["price"],
        "indicators": result["indicators"],
        "overall_signal": result["overall_signal"],
    }


def analyze_crypto(crypto_id: str) -> Dict[str, Dict]:
    df_raw = load_data(crypto_id)

    daily_result = analyze_timeframe(df_raw, "1D")

    df_weekly = resample_ohlcv(df_raw, "W")
    weekly_result = analyze_timeframe(df_weekly, "1W")

    df_monthly = resample_ohlcv(df_raw, "ME")
    monthly_result = analyze_timeframe(df_monthly, "1M")

    return {
        "1D": daily_result,
        "1W": weekly_result,
        "1M": monthly_result,
    }


def analyze_all_cryptos() -> Dict[str, Dict[str, Dict]]:
    crypto_ids = get_all_crypto_ids()

    all_results: Dict[str, Dict[str, Dict]] = {}

    for cid in crypto_ids:
        try:
            results = analyze_crypto(cid)
            all_results[cid] = results

            for tf, res in results.items():
                print(f"\nTimeframe: {tf}")
                print("Date:", res["date"])
                print("Price:", res["price"])
                print("Overall signal:", res["overall_signal"])
                print("Indicators:")
                for name, info in res["indicators"].items():
                    value = info["value"]
                    if value is None:
                        val_str = "None"
                    else:
                        val_str = f"{value:.3f}"
                    print(f"  {name:12s} -> value={val_str}, signal={info['signal']}")
                print()

        except Exception as e:
            print(f"[SKIP] {cid} due to error: {e}")

    return all_results


if __name__ == "__main__":
    analyze_all_cryptos()
