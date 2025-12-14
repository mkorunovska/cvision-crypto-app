package com.example.demo.model.exceptions;

public class InvalidArgumentsException extends RuntimeException {
  public InvalidArgumentsException(String message) {
    super(message);
  }
}
