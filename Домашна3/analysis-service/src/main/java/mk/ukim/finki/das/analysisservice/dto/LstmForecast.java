package mk.ukim.finki.das.analysisservice.dto;

import lombok.Data;

@Data
public class LstmForecast {
    private String date;
    private Double open;
    private Double high;
    private Double low;
    private Double close;
    private Double volume;
}
