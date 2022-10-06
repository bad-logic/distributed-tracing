#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <yaml-cpp/yaml.h>

struct listeners
{
    std::vector<std::string> listeners;
};

int main()
{

    try
    {
        std::string yaml_file_path = "configs/routes.yaml";
        std::string yaml_file_abs_path = std::filesystem::absolute(yaml_file_path);

        YAML::Node config = YAML::LoadFile(yaml_file_abs_path);
        std::map<std::string, listeners> yaml_configs = {};

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
            yaml_configs[topic].listeners = listeners;
        }
        std::cout << "consumers->topics: " << yaml_configs << std::endl;
    }
    catch (std::exception &e)
    {
        std::cout << "Unable to read yaml file: " << e.what() << std::endl;
    }

    return 0;
}