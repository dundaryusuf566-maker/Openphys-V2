#pragma once
#include "openphys/plugin_interface.hpp"
#include <string>

namespace openphys {

class DynamicCondition : public ICondition {
    std::string type_;
    std::string region_;
    std::string field_name_;
    std::string symbolic_expression_;

public:
    void set_parameters(const nlohmann::json& params) override {
        type_ = params.value("type", "Dirichlet");
        region_ = params.value("region", "boundary");
        field_name_ = params.value("field_name", "");
        symbolic_expression_ = params.value("symbolic_expression", "0.0");
    }

    void apply(EvaluationContext& ctx) override {
        if (!ctx.has_field(field_name_)) return;
    }
};

REGISTER_CONDITION("dynamic_condition", DynamicCondition)

} // namespace openphys