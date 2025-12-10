import React from "react";

const CandleTooltip = ({ active, payload, label }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;

    return (
      <div className=" bg-darkblue/60 p-10 border border-gray rounded">
        <div>
          <strong>{label}</strong>
        </div>
        <div>Open: {d.open}</div>
        <div>High: {d.high}</div>
        <div>Low: {d.low}</div>
        <div>Close: {d.close}</div>
      </div>
    );
  };

export default CandleTooltip;
  
