cmake_minimum_required(VERSION 3.20)
project(OpenPhysV2 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# 1. Python Bul
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

# 2. Pybind11 Bul veya Otomatik İndir (FetchContent)
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG        v2.11.1
    )
    FetchContent_MakeAvailable(pybind11)
endif()

# 3. Eigen3 Bul veya Otomatik İndir (FetchContent)
find_package(Eigen3 CONFIG QUIET)
if(NOT Eigen3_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        Eigen3
        GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
        GIT_TAG        3.4.0
    )
    FetchContent_MakeAvailable(Eigen3)
endif()

# 4. Derlenen binary eklentisini (.pyd / .so) doğrudan Python paket klasörüne (src/openphys) at
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/src/openphys)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/src/openphys)

# 5. C++ Kaynak Dosyalarını Taraması
file(GLOB_RECURSE CORE_SOURCES
    "src/cpp/*.cpp"
    "src/openphys/*.cpp"
)

if(CORE_SOURCES)
    pybind11_add_module(openphys_core_v2 ${CORE_SOURCES})
    
    if(TARGET Eigen3::Eigen)
        target_link_libraries(openphys_core_v2 PRIVATE Eigen3::Eigen)
    endif()

    target_include_directories(openphys_core_v2 PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/openphys
    )
    
    message(STATUS "[OpenPhys CMake] openphys_core_v2 C++ modülü derleme hedeflerine eklendi.")
else()
    message(STATUS "[OpenPhys CMake] C++ kaynak dosyası (.cpp) bulunamadı. Sadece Python modülleri kullanılacak.")
endif()
