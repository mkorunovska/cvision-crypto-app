package com.example.demo.controller;

import com.example.demo.client.AnalysisClient;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/api/analysis")
@Validated
@CrossOrigin(origins="*")
@AllArgsConstructor
public class AnalysisController {
    private final AnalysisClient analysisClient;

    @GetMapping
    public ResponseEntity<JsonNode> getTechnicalAnalysis(@RequestParam String cryptoId,
                                                         @RequestParam String period){
        return ResponseEntity.ok(analysisClient.getTechnicalAnalysis(cryptoId, period));
    }

    @GetMapping("/lstm")
    public ResponseEntity<JsonNode> getLstm(@RequestParam String cryptoId) {
        return ResponseEntity.ok(analysisClient.getLstm(cryptoId));
    }

    @GetMapping("/onchain-sentiment")
    public ResponseEntity<JsonNode> getOnchainSentiment(@RequestParam String cryptoId,
                                                 @RequestParam(defaultValue = "day") String timeframe,
                                                 @RequestParam(defaultValue = "365") int daysBack,
                                                 @RequestParam(defaultValue = "40") int limit) {
        return ResponseEntity.ok(analysisClient.getOnchainSentiment(cryptoId, timeframe, daysBack, limit));
    }

}
