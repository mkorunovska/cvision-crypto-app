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
    private final String technicalUrl;
    private final String lstmUrl;
    private final String sentimentUrl;

    public AnalysisController(RestTemplate restTemplate,
                              @Value("${python.technical.base-url}") String technicalUrl,
                              @Value("${python.lstm.base-url}") String lstmUrl,
                              @Value("${python.sentiment.base-url}")String sentimentUrl) {
        this.restTemplate = restTemplate;
        this.technicalUrl = technicalUrl;
        this.lstmUrl = lstmUrl;
        this.sentimentUrl = sentimentUrl;
    }

    @GetMapping
    public ResponseEntity<JsonNode> getTechnicalAnalysis(@RequestParam String cryptoId,
                                                         @RequestParam String period) {
        String url = technicalUrl + "/technical_analysis/" + cryptoId + "?period=" + period;

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
        String url = lstmUrl + "/lstm_analysis/" + cryptoId;

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
        String url = sentimentUrl + "/combined"
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
