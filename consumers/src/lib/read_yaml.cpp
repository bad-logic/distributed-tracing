#pragma once

#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>

#include <yaml-cpp/yaml.h>

// struct listeners
// {
//     std::vector<std::string> listeners;
// };

std::map<std::string, std::vector<std::string>> getKafkaTopicAndItsListeners()
{

    std::map<std::string, std::vector<std::string>> kafka_configs = {};
    try
    {
        std::string yaml_file_path = "configs/routes.yaml";
        std::string yaml_file_abs_path = std::filesystem::absolute(yaml_file_path);

        YAML::Node config = YAML::LoadFile(yaml_file_abs_path);

        YAML::Node topics = config["consumers"]["topics"];

        for (const auto &n : topics)
        {
            std::vector<std::string> listeners;
            std::string topic = n["topic"].as<std::string>();
            for (const auto &l : n["listeners"])
            {
                std::string callback = l["host"].as<std::string>() + l["path"].as<std::string>();
                listeners.push_back(callback);
            }
            kafka_configs[topic] = listeners;
        }
    }
    catch (std::exception &e)
    {
        std::cout << "Unable to read yaml file: " << e.what() << std::endl;
    }

    return kafka_configs;
}