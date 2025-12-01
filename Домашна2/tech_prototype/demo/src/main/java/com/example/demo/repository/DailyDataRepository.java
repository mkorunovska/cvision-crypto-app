package com.example.demo.repository;

import com.example.demo.model.DailyData;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DailyDataRepository extends JpaRepository<DailyData, Long> {
    //List<DailyData> findByCryptocurrency_IdOrderByDateDesc(String cryptoId, Pageable pageable);
    List<DailyData> findByCryptocurrency_IdOrderByDateDesc(String cryptoId);
}
