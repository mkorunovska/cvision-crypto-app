package com.example.demo.model;

import lombok.Data;

import java.util.Map;

@Data
public class TechnicalAnalysis {
    private String cryptoId;
    private String date;
    private Double price;
    private String overall_signal;
    private Map<String, Indicator> indicators;
}
