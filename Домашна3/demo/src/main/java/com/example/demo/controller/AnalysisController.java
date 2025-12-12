package com.example.demo.controller;

import com.example.demo.model.TechnicalAnalysis;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping(value = "/api/analysis")
@Validated
@CrossOrigin(origins="*")
public class AnalysisController {
    private final RestTemplate restTemplate;

    public AnalysisController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping
    public ResponseEntity<TechnicalAnalysis> getTechnicalAnalysis(@RequestParam String cryptoId,
                                                                  @RequestParam String period) {

        String url = "http://localhost:8001/technical_analysis/" + cryptoId + "?period=" + period;

        try{
            TechnicalAnalysis body = restTemplate.getForObject(url, TechnicalAnalysis.class);
            return ResponseEntity.ok(body);

        }catch (Exception e){
            e.printStackTrace();
            return ResponseEntity.status(500)
                    .build();
        }
    }
}
