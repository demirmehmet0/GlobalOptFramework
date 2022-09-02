cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

add_executable(untitled main.cpp strategy.cpp strategy.h matrix.cpp matrix.h reduce.cpp reduce.h)
add_executable(convert convert.cpp)