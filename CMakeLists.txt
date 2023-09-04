cmake_minimum_required(VERSION 3.15)
project(serial CXX)

set(serial_SRCS
    src/serial.cc
    include/serial/serial.h
)
if(APPLE)
    list(APPEND serial_SRCS src/impl/unix.cc)
    list(APPEND serial_SRCS src/impl/list_ports/list_ports_osx.cc)
    find_library(IOKIT_LIBRARY IOKit)
    find_library(FOUNDATION_LIBRARY Foundation)
elseif(UNIX)
    list(APPEND serial_SRCS src/impl/unix.cc)
    list(APPEND serial_SRCS src/impl/list_ports/list_ports_linux.cc)
elseif(WIN32)
    list(APPEND serial_SRCS src/impl/win.cc)
    list(APPEND serial_SRCS src/impl/list_ports/list_ports_win.cc)
else()
    message(FATAL_ERROR "Unsupported OS")
endif()

add_library(${PROJECT_NAME} ${serial_SRCS})
if(APPLE)
    target_link_libraries(${PROJECT_NAME} ${FOUNDATION_LIBRARY} ${IOKIT_LIBRARY})
elseif(UNIX)
    target_link_libraries(${PROJECT_NAME} rt pthread)
    elseif(WIN32)
    target_link_libraries(${PROJECT_NAME} setupapi)
endif()

target_include_directories(serial PUBLIC include)

set_target_properties(serial PROPERTIES PUBLIC_HEADER "include/serial/serial.h")
install(TARGETS serial)
