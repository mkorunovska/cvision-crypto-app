package com.example.demo.client;

import com.example.demo.dto.JwtResponse;
import com.example.demo.dto.LoginRequest;
import com.example.demo.dto.RegisterRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class AuthClient {

    private final RestTemplate restTemplate;
    private final String authBaseUrl;

    public AuthClient(RestTemplate restTemplate,
                      @Value("${services.auth.url}") String authBaseUrl) {
        this.restTemplate = restTemplate;
        this.authBaseUrl = authBaseUrl;
    }

    public void register(RegisterRequest req) {
        restTemplate.postForEntity(authBaseUrl + "/api/auth/register", req, Void.class);
    }

    public JwtResponse login(LoginRequest req) {
        return restTemplate.postForObject(authBaseUrl + "/api/auth/login", req, JwtResponse.class);
    }
}
