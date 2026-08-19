# cpp/CMakeLists_v2.txt
cmake_minimum_required(VERSION 3.20)
project(OpenPhysCoreV2 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Bağımlılıkları bul (LibTorch, pybind11, Eigen3, nlohmann_json)
find_package(Torch REQUIRED)
find_package(pybind11 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(nlohmann_json REQUIRED)

# Include dizinleri
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/core/include
    ${EIGEN3_INCLUDE_DIRS}
)

# Pybind11 Modülü Oluşturma
pybind11_add_module(openphys_core_v2 
    bindings/bindings_v2.cpp
    # Header-only sınıflarımızı kullanan bindings dosyası
)

# Kütüphaneleri bağla
target_link_libraries(openphys_core_v2 PRIVATE 
    ${TORCH_LIBRARIES} 
    nlohmann_json::nlohmann_json
)

# Gizlilik ve Optimizasyon ayarları
set_target_properties(openphys_core_v2 PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
)