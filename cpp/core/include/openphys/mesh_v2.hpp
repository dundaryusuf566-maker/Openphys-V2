#pragma once
#include <Eigen/Dense>
#include <string>

namespace openphys {

class DynamicMeshV2 {
public:
    // N x D boyutunda (Örn: 2000 nokta, 2 boyut) koordinat matrisi
    Eigen::MatrixXd coordinates;
    
    // Sınır noktalarının işaretçileri (Maskeler)
    Eigen::VectorXi boundary_flags;

    DynamicMeshV2(int num_nodes, int dim) {
        coordinates.resize(num_nodes, dim);
        boundary_flags.resize(num_nodes);
        boundary_flags.setZero();
    }

    // Zero-Copy için raw pointer atama metodu
    void map_from_raw(double* raw_coords, int rows, int cols) {
        new (&coordinates) Eigen::Map<Eigen::MatrixXd>(raw_coords, rows, cols);
    }
};

} // namespace openphys