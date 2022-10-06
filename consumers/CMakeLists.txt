cmake_minimum_required(VERSION 2.8.12)
project(KafkaConsumers)

add_definitions("-std=c++20")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(consumer src/main.cpp)
target_link_libraries(consumer ${CONAN_LIBS})