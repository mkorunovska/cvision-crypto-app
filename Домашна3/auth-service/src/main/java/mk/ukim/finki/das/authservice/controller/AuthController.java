package mk.ukim.finki.das.authservice.controller;

import mk.ukim.finki.das.authservice.dto.JwtResponse;
import mk.ukim.finki.das.authservice.dto.LoginRequest;
import mk.ukim.finki.das.authservice.dto.RegisterRequest;
import mk.ukim.finki.das.authservice.model.User;
import mk.ukim.finki.das.authservice.model.enums.Role;
import mk.ukim.finki.das.authservice.security.JwtService;
import mk.ukim.finki.das.authservice.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins="*")
public class AuthController {

    private final UserService userService;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;

    public AuthController(UserService userService,
                          AuthenticationManager authenticationManager,
                          JwtService jwtService) {
        this.userService = userService;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
    }

    @PostMapping("/register")
    public ResponseEntity<Void> register(@RequestBody RegisterRequest req) {
        userService.register(
                req.getUsername(),
                req.getPassword(),
                req.getRepeatPassword(),
                req.getName(),
                req.getSurname(),
                Role.ROLE_USER
        );
        return ResponseEntity.status(201).build();
    }

    @PostMapping("/login")
    public ResponseEntity<JwtResponse> login(@RequestBody LoginRequest req) {
        Authentication auth = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(req.getUsername(), req.getPassword())
        );

        User user = (User) auth.getPrincipal();
        String token = jwtService.generateToken(user);

        return ResponseEntity.ok(new JwtResponse(token));
    }
}

