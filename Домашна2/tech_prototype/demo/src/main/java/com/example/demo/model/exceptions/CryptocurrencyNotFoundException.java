package com.example.demo.model.exceptions;

public class CryptocurrencyNotFoundException extends RuntimeException {
    public CryptocurrencyNotFoundException(Long id) {
        super(String.format("Could not find cryptocurrency with id %d", id));
    }
}
