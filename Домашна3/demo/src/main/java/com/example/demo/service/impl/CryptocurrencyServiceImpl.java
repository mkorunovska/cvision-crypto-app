package com.example.demo.service.impl;

import com.example.demo.model.Cryptocurrency;
import com.example.demo.model.exceptions.CryptocurrencyNotFoundException;
import com.example.demo.repository.CryptocurrencyRepository;
import com.example.demo.service.CryptocurrencyService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CryptocurrencyServiceImpl implements CryptocurrencyService {
    private final CryptocurrencyRepository cryptocurrencyRepository;

    public CryptocurrencyServiceImpl(CryptocurrencyRepository cryptocurrencyRepository) {
        this.cryptocurrencyRepository = cryptocurrencyRepository;
    }

    @Override
    public List<Cryptocurrency> findAll() {
        return cryptocurrencyRepository.findAll();
    }

    @Override
    public Cryptocurrency findById(Long id) {
        return cryptocurrencyRepository.findById(id)
                .orElseThrow(() -> new CryptocurrencyNotFoundException(id));
    }

    @Override
    public List<Cryptocurrency> search(String query) {
        return cryptocurrencyRepository
                .findByNameContainingIgnoreCaseOrSymbolContainingIgnoreCase(query, query);
    }
}
