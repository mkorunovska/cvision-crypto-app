package mk.ukim.finki.das.analysisservice.controller;

import mk.ukim.finki.das.analysisservice.dto.LstmAnalysis;
import mk.ukim.finki.das.analysisservice.dto.TechnicalAnalysis;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import tools.jackson.databind.JsonNode;

@RestController
@RequestMapping(value = "/api/analysis")
@Validated
@CrossOrigin(origins="*")
public class AnalysisController {
    private final RestTemplate restTemplate;
    private final String baseUrl;

    public AnalysisController(RestTemplate restTemplate,
                              @Value("${python.analysis.base-url}") String baseUrl) {
        this.restTemplate = restTemplate;
        this.baseUrl = baseUrl;
    }

    @GetMapping
    public ResponseEntity<JsonNode> getTechnicalAnalysis(@RequestParam String cryptoId,
                                                         @RequestParam String period) {
        String url = baseUrl + "/technical_analysis/" + cryptoId + "?period=" + period;

        try{
            return ResponseEntity.ok(restTemplate.getForObject(url, JsonNode.class));

        }catch (Exception e){
            e.printStackTrace();
            return ResponseEntity.status(500)
                    .build();
        }
    }

    
    @GetMapping("/lstm")
    public ResponseEntity<JsonNode> getLstmAnalysis(@RequestParam String cryptoId) {
        String url = baseUrl + "/lstm_analysis/" + cryptoId;

        try {
            return ResponseEntity.ok(restTemplate.getForObject(url, JsonNode.class));

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).build();
        }
    }

    @GetMapping("/onchain-sentiment")
    public ResponseEntity<JsonNode> getOnchainSentiment(
            @RequestParam String cryptoId,
            @RequestParam(defaultValue = "day") String timeframe,
            @RequestParam(defaultValue = "365") int daysBack,
            @RequestParam(defaultValue = "40") int limit
    ) {
        String url = baseUrl + "/combined"
                + "?cryptoId=" + cryptoId
                + "&timeframe=" + timeframe
                + "&days_back=" + daysBack
                + "&limit=" + limit;

        try {
            return ResponseEntity.ok(restTemplate.getForObject(url, JsonNode.class));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).build();
        }
    }
}
