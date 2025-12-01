package com.example.demo.service;

import com.example.demo.model.Cryptocurrency;

import java.util.List;

public interface CryptocurrencyService {
    List<Cryptocurrency> findAll();

    Cryptocurrency findById(Long id);

    List<Cryptocurrency> search(String query);
}
