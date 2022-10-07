#include <iostream>
#include <cppkafka/cppkafka.h>
#include "lib/read_yaml"
#include "lib/notify_consumers"

int main()
{
    const char *kafka_brokers = std::getenv("KAFKA_BROKERS");
    ListenToKafkaTopicsAndNotifyTheConsumers(getKafkaTopicAndItsListeners(), kafka_brokers);
    return 0;
}