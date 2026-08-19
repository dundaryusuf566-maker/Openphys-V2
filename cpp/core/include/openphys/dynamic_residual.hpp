#pragma once
#include "openphys/plugin_interface.hpp"
#include "openphys/field.hpp"
#include <nlohmann/json.hpp>
#include <string>
#include <vector>

namespace openphys {

class DynamicStrongResidual : public IStrongResidual {
    std::string symbolic_expression_;
    std::vector<std::string> required_fields_;

public:
    void set_parameters(const nlohmann::json& params) override {
        symbolic_expression_ = params.value("symbolic_expression", "");
        if (params.contains("required_fields")) {
            for (const auto& f : params["required_fields"]) {
                required_fields_.push_back(f.get<std::string>());
            }
        }
    }

    nlohmann::json get_schema() const override {
        return {
            {"symbolic_expression", "string (SymPy compatible equation)"},
            {"required_fields", "list of strings"}
        };
    }

    void compute(const EvaluationContext& ctx, FieldMap& residuals_out) override {
        for (const auto& field : required_fields_) {
            if (ctx.has_field(field)) {
                residuals_out[field] = FieldData(ctx.coords.rows(), 1);
                residuals_out[field].values.setZero();
            }
        }
    }
};

REGISTER_STRONG_RESIDUAL("dynamic_pde", DynamicStrongResidual)

} // namespace openphys