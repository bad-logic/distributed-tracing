#pragma once

#include <iostream>

#include <cppkafka/cppkafka.h>

void ListenToKafkaTopicsAndNotifyTheConsumers(std::map<std::string, std::vector<std::string>> consumers, std::string kafka_brokers)
{
    std::cout << "KAFKA_BROKERS: " << kafka_brokers << std::endl;
    std::vector<std::string> topics;
    // get the topics from the map where all the keys are the topics that we need to listen to.
    for (auto it = consumers.begin(); it != consumers.end(); it++)
    {
        topics.push_back(it->first);
    }

    std::cout << "Listening to below topics... " << std::endl;
    for (const auto &topic : topics)
    {
        std::cout << topic << std::endl;
    }

    cppkafka::Configuration config = {
        {"metadata.broker.list", kafka_brokers}, {"group.id", "global_consumer"}, {"enable.auto.commit", false}};

    cppkafka::Consumer consumer(config);
    consumer.subscribe({topics});

    // Print the assigned partitions on assignment
    consumer.set_assignment_callback([](const cppkafka::TopicPartitionList &partitions)
                                     { std::cout << "Got assigned: " << partitions << std::endl; });

    // Print the revoked partitions on revocation
    consumer.set_revocation_callback([](const cppkafka::TopicPartitionList &partitions)
                                     { std::cout << "Got revoked: " << partitions << std::endl; });

    // check for messages in those topics
    while (true)
    {
        cppkafka::Message message = consumer.poll();

        if (!message)
        {
            continue;
        }

        if (message.get_error())
        {
            // librdkafka provides an error indicating we've reached the
            // end of a partition every time we do so. Make sure it's not one
            // of those cases, as it's not really an error
            if (!message.is_eof())
            {
                std::cout << "[+] Received error notification: " << message.get_error() << std::endl;
            }
        }

        // checking if the message has a key
        if (message.get_key())
        {
            std::cout << message.get_key() << " -> ";
        }

        std::cout << "[+] Received message on partition " << message.get_topic() << "/"
                  << message.get_partition() << ", offset " << message.get_offset() << ", with payload -> " << message.get_payload() << std::endl;

        // Now commit the message
        // consumer.commit(message);
    }
}