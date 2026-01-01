package mk.ukim.finki.das.analysisservice.dto;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class LstmAnalysis {
    private String cryptoId;
    private Integer lookback;
    private Integer horizon;
    List<LstmForecast> forecast;

}
