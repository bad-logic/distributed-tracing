#pragma once

#include <iostream>
#include <map>
#include <cppkafka/cppkafka.h>
#include <cpr/cpr.h>

// #include <opentelemetry/sdk/version/version.h>
#include <opentelemetry/trace/provider.h>

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

    // get the global tracer
    auto provider = opentelemetry::trace::Provider::GetTracerProvider();
    auto tracer = provider->GetTracer(std::getenv("SERVICE_NAME"));
    while (true)
    {
        cppkafka::Message message = consumer.poll();

        if (!message)
        {
            continue;
        }

        auto scoped_span = opentelemetry::trace::Scope(tracer->StartSpan(std::getenv("SERVICE_NAME")));
        if (message.get_error())
        {
            // librdkafka provides an error indicating we've reached the
            // end of a partition every time we do so. Make sure it's not one
            // of those cases, as it's not really an error
            if (!message.is_eof())
            {
                std::cout << "[+] Received error notification on topic -> " << message.get_topic() << " : " << message.get_error() << std::endl;
            }
            continue;
        }

        std::cout << "[+] Received message with key " << message.get_key() << " , topic -> " << message.get_topic() << " on Partition "
                  << message.get_partition() << ", offset " << message.get_offset() << ", with payload -> " << message.get_payload() << std::endl;

        // cppkafka::HeaderList headers = message.get_header_list() << std::endl;

        // std::ostream myout(std::cout.rdbuf());

        // std::ostringstream s2(std::ostringstream() << message.get_header_list());
        // myout << s2.str() << '\n';

        std::string topic = message.get_topic();
        std::vector<std::string> hosts = consumers[topic];

        for (int i = 0; i < hosts.size(); i++)
        {
            std::cout << "[+] Sending data to " << hosts[i] << " ..." << std::endl;
            cpr::Response response = cpr::Post(cpr::Url{hosts[i]},
                                               cpr::Body{std::string(message.get_payload())},
                                               cpr::Header{{"Content-Type", "application/json"}});
            if (response.status_code == 200)
            {
                std::cout << "✔️  Data Sent Successfully !!!" << std::endl;
                // Now commit the message
                consumer.commit(message);
            }
        }
    }
}