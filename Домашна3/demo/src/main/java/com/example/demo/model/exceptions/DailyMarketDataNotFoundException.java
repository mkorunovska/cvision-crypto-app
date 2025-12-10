package com.example.demo.model.exceptions;

public class DailyMarketDataNotFoundException extends RuntimeException {
    public DailyMarketDataNotFoundException(Long id) {
        super(String.format("Could not find daily market data with id %d", id));
    }
}
