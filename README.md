# home-assistant-threema-gateway-notifier
Integration for Home Assistant that implements a notifier for the Threema Gateway.

## Installation
Copy all files to the Home Assistant directory `config/custom_components/threema-gateway`

## Obtaining an ID
See https://gateway.threema.ch/

## Sample Config
### Basic mode
```
notify:
  - name: threema
    platform: threema-gateway
    gateway_mode: "basic"
    threema_id: "*THREEMA" # the sender id
    secret: "id secret"
    recipients: # one or more recipients
      - "YOURID00"
```

### End-to-end encrypted mode
TODO
