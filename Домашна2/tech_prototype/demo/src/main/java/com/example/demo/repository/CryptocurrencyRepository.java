package com.example.demo.repository;

import com.example.demo.model.Cryptocurrency;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CryptocurrencyRepository extends JpaRepository<Cryptocurrency, Long> {
    List<Cryptocurrency> findByNameContainingIgnoreCaseOrSymbolContainingIgnoreCase(
            String name, String symbol
    );
}
