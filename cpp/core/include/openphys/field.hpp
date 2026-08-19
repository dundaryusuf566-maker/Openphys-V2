#pragma once
#include <Eigen/Dense>
#include <unordered_map>
#include <string>

namespace openphys {

struct FieldData {
    Eigen::MatrixXd values;
    FieldData() = default;
    FieldData(int rows, int cols) : values(Eigen::MatrixXd::Zero(rows, cols)) {}
};

using FieldMap = std::unordered_map<std::string, FieldData>;

struct EvaluationContext {
    Eigen::MatrixXd coords;
    FieldMap fields;
    bool has_field(const std::string& name) const {
        return fields.find(name) != fields.end();
    }
};

} // namespace openphys