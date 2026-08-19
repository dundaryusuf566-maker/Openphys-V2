#pragma once
#include <Eigen/Dense>
#include "openphys/field.hpp"
#include <stdexcept>
#include <iostream>

namespace openphys {

class ZeroCopyBridge {
public:
    static void map_torch_to_eigen(uintptr_t ptr, int rows, int cols, FieldData& target_field) {
        if (ptr == 0) {
            throw std::runtime_error("[ZeroCopyBridge] Hata: PyTorch veri işaretçisi (pointer) boş (null).");
        }
        
        if (rows <= 0 || cols <= 0) {
            throw std::runtime_error("[ZeroCopyBridge] Hata: Geçersiz tensör boyutları.");
        }

        double* raw_data = reinterpret_cast<double*>(ptr);
        new (&target_field.values) Eigen::Map<Eigen::MatrixXd>(raw_data, rows, cols);
    }
};

} // namespace openphys