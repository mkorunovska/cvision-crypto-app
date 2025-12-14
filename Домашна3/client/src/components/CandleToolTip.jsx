import React from "react";

const CandleTooltip = ({ active, payload, label }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;

    const format = (v) =>
        typeof v === "number" ? v.toFixed(3) : "-";

    return (
      <div className=" bg-darkblue/60 p-10 border border-gray rounded">
        <div>
          <strong>{label}</strong>
        </div>
        <div>Open: {format(d.open)}</div>
        <div>High: {format(d.high)}</div>
        <div>Low: {format(d.low)}</div>
        <div>Close: {format(d.close)}</div>
      </div>
    );
  };

export default CandleTooltip;
  
