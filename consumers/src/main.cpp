#include <iostream>
#include <cstdlib>
#include "lib/notify_consumers.cpp"
#include "lib/read_yaml.cpp"
#include "lib/telemetry.cpp"

int main()
{
    try
    {
        const char *kafka_brokers = std::getenv("KAFKA_BROKERS");

        std::string brokers(kafka_brokers ? kafka_brokers : "");

        if (brokers.empty())
        {
            throw std::invalid_argument("KAFKA_BROKERS not provided");
        }
        setUpTelemetry();
        ListenToKafkaTopicsAndNotifyTheConsumers(getKafkaTopicAndItsListeners(), brokers);
    }
    catch (std::invalid_argument &e)
    {
        std::cout << "Error: " << e.what() << std::endl;
        exit(EXIT_FAILURE);
        return 0;
    }
    return 0;
}