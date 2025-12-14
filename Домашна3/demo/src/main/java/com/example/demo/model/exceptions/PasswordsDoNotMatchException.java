package com.example.demo.model.exceptions;

public class PasswordsDoNotMatchException extends RuntimeException {
  public PasswordsDoNotMatchException(String message) {
    super(message);
  }
}
