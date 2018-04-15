#include <stdlib.h>
#include <stdio.h>

#include "mosquitto.h"

/* Hostname and port for the MQTT broker. */
#define BROKER_HOSTNAME "localhost"
#define BROKER_PORT 1883

void connect_callback(struct mosquitto *mosq, void *obj, int result) {}
void message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message) {}

int main(int argc, char * argv []) {
    struct mosquitto* st_mosquitto = NULL;

    puts("mosquitto_lib_init");
    if (mosquitto_lib_init() != MOSQ_ERR_SUCCESS) {
        return EXIT_FAILURE;
    }

    puts("mosquitto_new");
    st_mosquitto = mosquitto_new("foobar", true, NULL);
    if (!st_mosquitto) {
        return EXIT_FAILURE;
    }

    puts("mosquitto_connect_callback_set");
    mosquitto_connect_callback_set(st_mosquitto, connect_callback);
	mosquitto_message_callback_set(st_mosquitto, message_callback);

    puts("mosquitto_connect");
    if (mosquitto_connect(st_mosquitto, BROKER_HOSTNAME, BROKER_PORT, 60) != MOSQ_ERR_SUCCESS) {
        return EXIT_FAILURE;
    }

    puts("mosquitto_subscribe");
    if (mosquitto_subscribe(st_mosquitto, NULL, "#", 0) != MOSQ_ERR_SUCCESS) {
        return EXIT_FAILURE;
    }

    puts("mosquitto_destroy");
	mosquitto_destroy(st_mosquitto);

    puts("mosquitto_lib_cleanup");
	if (mosquitto_lib_cleanup() != MOSQ_ERR_SUCCESS) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}