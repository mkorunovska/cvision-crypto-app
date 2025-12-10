package com.example.demo.service.impl;

import com.example.demo.model.DailyData;
import com.example.demo.model.exceptions.DailyMarketDataNotFoundException;
import com.example.demo.repository.DailyDataRepository;
import com.example.demo.service.DailyDataService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DailyDataServiceImpl implements DailyDataService {
    private final DailyDataRepository dailyDataRepository;

    public DailyDataServiceImpl(DailyDataRepository dailyDataRepository) {
        this.dailyDataRepository = dailyDataRepository;
    }

    @Override
    public List<DailyData> findAll() {
        return dailyDataRepository.findAll();
    }

    @Override
    public DailyData findById(Long id) {
        return dailyDataRepository.findById(id)
                .orElseThrow(() -> new DailyMarketDataNotFoundException(id));
    }

    @Override
    public Page<DailyData> findPage(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return dailyDataRepository.findAll(pageable);
    }

    @Override
    public List<DailyData> getLatestForCrypto(String cryptoId) {
        return dailyDataRepository.findByCryptocurrency_IdOrderByDateDesc(cryptoId);
    }


}
