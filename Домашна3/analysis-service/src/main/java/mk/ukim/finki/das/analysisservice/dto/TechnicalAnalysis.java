package mk.ukim.finki.das.analysisservice.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

import java.util.Map;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class TechnicalAnalysis {
    private String cryptoId;
    private String date;
    private Double price;
    private String overall_signal;
    private Map<String, Indicator> indicators;
}
