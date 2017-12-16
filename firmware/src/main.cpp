#include "Arduino.h"

const uint8_t tx_pin = 0; //TODO update pin number when known

char rx_buffer[32];

void setup()
{
    pinMode(tx_pin, OUTPUT);
    digitalWrite(tx_pin, LOW);
}

void tx_zero(void)
{
    digitalWrite(tx_pin, HIGH);
    delayMicroseconds(150);
    digitalWrite(tx_pin, LOW);
    delayMicroseconds(590);
}

void tx_one(void)
{
    digitalWrite(tx_pin, HIGH);
    delayMicroseconds(520);
    digitalWrite(tx_pin, LOW);
    delayMicroseconds(220);
}

void loop()
{
    Serial.println("---");
    Serial.print("waiting for packet...");
    uint8_t bytes_read =
        Serial.readBytesUntil('\0', rx_buffer, sizeof(rx_buffer));
    Serial.print("\n");

    if (bytes_read != 25)
    {
        Serial.print("invalid packet size: ");
        Serial.print(bytes_read);
        Serial.println(" packet data:");
        Serial.write(rx_buffer);
        Serial.print("\n");
        return;
    }

    Serial.println(" packet data:");
    Serial.write(rx_buffer);
    Serial.print("\n");

    for (uint8_t i=0; i < bytes_read; ++i)
    {
        switch (rx_buffer[i])
        {
            case '0':
                tx_zero();
                break;
            case '1':
                tx_one();
                break;
            default:
                Serial.print("invalid character in packet: ");
                Serial.println(rx_buffer[i]);
                return;
        }
    }

    Serial.println("transmit complete");
}
