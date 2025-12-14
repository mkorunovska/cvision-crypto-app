package com.example.demo.service;


import com.example.demo.model.User;
import com.example.demo.model.enums.Role;
import org.springframework.security.core.userdetails.UserDetailsService;

public interface UserService extends UserDetailsService {
    User register(String username, String password, String repeatPassword, String name, String surname, Role role);
}
