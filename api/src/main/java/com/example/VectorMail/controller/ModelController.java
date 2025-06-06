package com.example.VectorMail.controller;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class ModelController {

    @PostMapping("/evaluate-email")
    public String evaluateEmail(@RequestBody String emailToEvaluate) {

        final String flaskUrl = "http://localhost:5000/";

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;


        try {
            HttpHeaders header = new HttpHeaders();
            header.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> requestEntity = new HttpEntity<>(emailToEvaluate, header);

            response = restTemplate.postForEntity(String.format("%s/evaluate-email", flaskUrl), requestEntity, String.class);

            return response.getBody();

        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }
}
