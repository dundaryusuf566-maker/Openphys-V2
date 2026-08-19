#pragma once
#include "openphys/field.hpp"
#include <nlohmann/json.hpp>
#include <string>

namespace openphys {

class IStrongResidual {
public:
    virtual ~IStrongResidual() = default;
    virtual void set_parameters(const nlohmann::json& params) = 0;
    virtual nlohmann::json get_schema() const = 0;
    virtual void compute(const EvaluationContext& ctx, FieldMap& residuals_out) = 0;
};

#define REGISTER_STRONG_RESIDUAL(name, cls) \
    /* Registry kayit makrosu */

} // namespace openphys