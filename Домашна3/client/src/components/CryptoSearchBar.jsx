import React from "react";

function CryptoSearchBar({ query, searchResults, onSearchChange, onCryptoSelect }) {
  
  return (
    <div>
      <h2 className="text-white">Choose a cryptocurrency</h2>
      <input
        type="text"
        value={query}
        onChange={onSearchChange}
        placeholder="Search cryptocurrency (e.g. bitcoin)..."
        className="w-full p-3 mb-3 border border-gray-400 rounded text-black " />

      {searchResults.length > 0 && (
        <div className="border border-gray-300 rounded bg-white max-h-[200px] overflow-y-auto text-black">
          {searchResults.map((crypto) => (
            <div className="p-3 border-b border-gray-200 cursor-pointer"
              key={crypto.id}
              onClick={() => onCryptoSelect(crypto)} >
              <strong>{crypto.name}</strong> ({crypto.symbol})
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CryptoSearchBar;
