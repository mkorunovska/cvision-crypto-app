
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

}
