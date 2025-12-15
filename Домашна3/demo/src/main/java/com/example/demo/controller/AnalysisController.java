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

    
    @GetMapping("/lstm")
    public ResponseEntity<?> getLstmAnalysis(@RequestParam String cryptoId) {
        String url = "http://localhost:8001/lstm_analysis/" + cryptoId;

        try {
            Object body = restTemplate.getForObject(url, Object.class);
            return ResponseEntity.ok(body);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).build();
        }
    }

    @GetMapping("/onchain-sentiment")
    public ResponseEntity<?> getOnchainSentiment(
            @RequestParam String cryptoId,
            @RequestParam(defaultValue = "day") String timeframe,
            @RequestParam(defaultValue = "365") int daysBack,
            @RequestParam(defaultValue = "40") int limit
    ) {
        String url = "http://localhost:8002/combined"
                + "?cryptoId=" + cryptoId
                + "&timeframe=" + timeframe
                + "&days_back=" + daysBack
                + "&limit=" + limit;

        try {
            Object body = restTemplate.getForObject(url, Object.class);
            return ResponseEntity.ok(body);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).build();
        }
    }
}
