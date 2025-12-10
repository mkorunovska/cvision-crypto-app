package com.example.demo.controller;

import com.example.demo.model.Cryptocurrency;
import com.example.demo.model.DailyData;
import com.example.demo.model.exceptions.CryptocurrencyNotFoundException;
import com.example.demo.model.exceptions.DailyMarketDataNotFoundException;
import com.example.demo.service.DailyDataService;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(value = "/api/data")
@Validated
@CrossOrigin(origins="*")
public class DailyDataController {
    private final DailyDataService dailyDataService;

    public DailyDataController(DailyDataService dailyDataService) {
        this.dailyDataService = dailyDataService;
    }

//    @GetMapping(value = "/all")
//    public ResponseEntity<List<DailyData>> getAllDailyData() {
//        List<DailyData> dailyData = dailyDataService.findAll();
//        return new ResponseEntity<>(dailyData, HttpStatus.OK);
//    }

    @GetMapping("/all")
    public ResponseEntity<Page<DailyData>> getAllPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Page<DailyData> result = dailyDataService.findPage(page, size);
        return new ResponseEntity<>(result, HttpStatus.OK);
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<DailyData> getDailyDataById(@PathVariable(value = "id") Long id)
            throws DailyMarketDataNotFoundException {
        DailyData data = dailyDataService.findById(id);
        return new ResponseEntity<>(data, HttpStatus.OK);
    }

    @GetMapping("/daily/{cryptoId}")
    public ResponseEntity<List<DailyData>> getDailyForCrypto(
            @PathVariable String cryptoId

    ) {
        List<DailyData> data = dailyDataService.getLatestForCrypto(cryptoId);
        return new ResponseEntity<>(data, HttpStatus.OK);
    }
}
