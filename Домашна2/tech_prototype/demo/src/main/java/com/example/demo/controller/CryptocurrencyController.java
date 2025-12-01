package com.example.demo.controller;

import com.example.demo.model.Cryptocurrency;
import com.example.demo.model.exceptions.CryptocurrencyNotFoundException;
import com.example.demo.service.CryptocurrencyService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(value = "/api/crypto")
@Validated
@CrossOrigin(origins="*")
public class CryptocurrencyController {

    private final CryptocurrencyService cryptocurrencyService;

    public CryptocurrencyController(CryptocurrencyService cryptocurrencyService) {
        this.cryptocurrencyService = cryptocurrencyService;
    }

    @GetMapping(value = "/all")
    public ResponseEntity<List<Cryptocurrency>> getAllCryptocurrency() {
        List<Cryptocurrency> cryptocurrencies = cryptocurrencyService.findAll();
        return new ResponseEntity<>(cryptocurrencies, HttpStatus.OK);
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<Cryptocurrency> getCryptocurrencyById(@PathVariable(value = "id") Long id)
            throws CryptocurrencyNotFoundException {
        Cryptocurrency cryptocurrency = cryptocurrencyService.findById(id);
        return new ResponseEntity<>(cryptocurrency, HttpStatus.OK);
    }

    @GetMapping("/search")
    public ResponseEntity<List<Cryptocurrency>> search(
            @RequestParam String query
    ) {
        List<Cryptocurrency> result = cryptocurrencyService.search(query);
        return new ResponseEntity<>(result, HttpStatus.OK);
    }


}
