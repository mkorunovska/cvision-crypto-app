package mk.ukim.finki.das.authservice.dto;

import lombok.Data;

@Data
public class RegisterRequest {
    private String username;
    private String password;
    private String repeatPassword;
    private String name;
    private String surname;
}