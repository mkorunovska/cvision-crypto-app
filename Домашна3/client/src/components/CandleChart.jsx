import React from "react";
import CandleTooltip from "./CandleToolTip.jsx"
import { ResponsiveContainer, ComposedChart, CartesianGrid, XAxis, YAxis, Tooltip, Bar,} from "recharts";

function CandleChart({ visibleData, loading }) {

  const Candle = (props) => {
    const { x, width, payload } = props;
    const { open, close, high, low} = payload;

    const color = close >= open ? "#1a6636ff" : "#9e3434ff";
    const center = x + width / 2;

    return (
      <g>
        <line
          x1={center}
          x2={center}
          y1={props.y + props.height * ((high - close) / (high - low || 1))}
          y2={props.y + props.height * ((low - close) / (high - low || 1))}
          stroke="#ede7e7ff"
          strokeWidth="1"
        />
        <rect
          x={x + width * 0.25}
          width={width * 0.5}
          y={
            props.y +
            props.height * ((Math.max(open, close) - close) / (high - low || 1))
          }
          height={
            props.height * (Math.abs(open - close) / (high - low || 1)) || 1
          }
          fill={color}
        />
      </g>
    );
  };
  
  if (loading) return <p>Loading chart...</p>;
  if (!visibleData || visibleData.length === 0) return null;

  return (
    <div className="h-[400px] mt-5">
      <ResponsiveContainer className="w-full h-full">
        <ComposedChart data={visibleData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" minTickGap={20} />
          <YAxis />
          <Tooltip content={<CandleTooltip />} />
          <Bar dataKey="close" shape={<Candle />} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CandleChart;
