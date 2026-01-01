package mk.ukim.finki.das.authservice.dto;

import lombok.Data;

@Data
public class LoginRequest {
    private String username;
    private String password;
}
