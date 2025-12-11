package com.example.demo.service;

import com.example.demo.model.DailyData;
import org.springframework.data.domain.Page;

import java.util.List;

public interface DailyDataService {
    List<DailyData> findAll();

    DailyData findById(Long id);

    Page<DailyData> findPage(int page, int size);

    List<DailyData> getLatestForCrypto(String cryptoId);

}
