
package com.example.demo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "daily_market_data")
public class DailyData {

    @Id
    private Long id;

    @ManyToOne
    @JoinColumn(name = "crypto_id", referencedColumnName = "id")
    private Cryptocurrency cryptocurrency;
    
    private String date;
    
    private Double open_price;
    
    private Double high_price;
    
    private Double low_price;
    
    private Double close_price;
    
    private Double volume_24;

    public DailyData() {
    }

    public DailyData(Long id,
                     Cryptocurrency cryptocurrency,
                     String date,
                     Double open_price,
                     Double high_price,
                     Double low_price,
                     Double closePrice,
                     Double volume24) {
        this.id = id;
        this.cryptocurrency = cryptocurrency;
        this.date = date;
        this.open_price = open_price;
        this.high_price = high_price;
        this.low_price = low_price;
        this.close_price = closePrice;
        this.volume_24 = volume24;
    }

    public Long getId() {
        return id;
    }

    public Cryptocurrency getCryptocurrency() {
        return cryptocurrency;
    }

    public String getDate() {
        return date;
    }


    public Double getOpen_price() {
        return open_price;
    }

    public Double getHigh_price() {
        return high_price;
    }

    public Double getLow_price() {
        return low_price;
    }


    public Double getClose_price() {
        return close_price;
    }


    public Double getVolume_24() {
        return volume_24;
    }

}
