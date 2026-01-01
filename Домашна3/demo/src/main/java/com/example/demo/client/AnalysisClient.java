package com.example.demo.client;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Service
public class AnalysisClient {
    private final RestTemplate restTemplate;
    private final String analysisBaseUrl;

    public AnalysisClient(RestTemplate restTemplate,
                          @Value("${services.analysis.url}") String analysisBaseUrl) {
        this.restTemplate = restTemplate;
        this.analysisBaseUrl = analysisBaseUrl;
    }

    public JsonNode getTechnicalAnalysis(String cryptoId, String period) {
        String url = UriComponentsBuilder
                .fromHttpUrl(analysisBaseUrl + "/api/analysis")
                .queryParam("cryptoId", cryptoId)
                .queryParam("period", period)
                .toUriString();

        return restTemplate.getForObject(url, JsonNode.class);
    }

    public JsonNode getLstm(String cryptoId) {
        String url = UriComponentsBuilder
                .fromHttpUrl(analysisBaseUrl + "/api/analysis/lstm")
                .queryParam("cryptoId", cryptoId)
                .toUriString();

        return restTemplate.getForObject(url, JsonNode.class);
    }

    public JsonNode getOnchainSentiment(String cryptoId, String timeframe, int daysBack, int limit) {
        String url = UriComponentsBuilder
                .fromHttpUrl(analysisBaseUrl + "/api/analysis/onchain-sentiment")
                .queryParam("cryptoId", cryptoId)
                .queryParam("timeframe", timeframe)
                .queryParam("daysBack", daysBack)
                .queryParam("limit", limit)
                .toUriString();

        return restTemplate.getForObject(url, JsonNode.class);
    }
}
