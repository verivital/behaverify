cmake_minimum_required(VERSION 3.10)
project(hello_world)

set(CMAKE_CXX_STANDARD 17)

# Update this path to wherever you cloned it
set(BTCPP_DIR "/home/serena/DVol/git/git_repos_others/BehaviorTree.CPP-parent/BehaviorTree.CPP")

# Include BT headers and link the library
include_directories(${BTCPP_DIR}/include)
link_directories(${BTCPP_DIR}/build)

add_executable(hello_world hello_world.cpp)
target_link_libraries(hello_world behaviortree_cpp)
