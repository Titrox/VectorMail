package com.example.VectorMail.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class ModelController {

    @PostMapping("/evaluate-email")
    public ResponseEntity<String> evaluateEmail(@RequestBody String emailToEvaluate) {

        final String flaskUrl = "http://localhost:5000";
        RestTemplate restTemplate = new RestTemplate();

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> requestEntity = new HttpEntity<>(emailToEvaluate, headers);
            ResponseEntity<String> response = restTemplate.postForEntity(
                    flaskUrl + "/evaluate-email",
                    requestEntity,
                    String.class
            );

            return ResponseEntity.ok(response.getBody());

        } catch (Exception e) {
            System.err.println("Request to Flask failed: " + e.getMessage());

            return ResponseEntity
                    .status(HttpStatus.BAD_GATEWAY)
                    .body("Fehler beim Aufruf des Modells: " + e.getMessage());
        }
    }
}
