#pragma once
#include "openphys/plugin_interface.hpp"
#include <string>

namespace openphys {

// Statik sınır koşulları yerine, sembolik ifadeleri kabul eden evrensel arayüz.
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

    // C++ bellek tarafında sınır noktalarını (boundary nodes/collocation points)
    // işaretlemek ve değer ataması için PyTorch'a alan açar.
    void apply(EvaluationContext& ctx) override {
        if (!ctx.has_field(field_name_)) return;

        // Gerçek hesaplama solver_v2.py (Python) tarafında autograd ile yapılacak.
        // Burada sadece C++ veri yapısında "Boundary" maskelemesi yapılabilir.
        // Sıfır-kopya (zero-copy) mimarisi sayesinde değerler anında buraya yansıyacak.
    }
};

// Dinamik sınır koşulunun C++ Plugin Registry'sine kaydı
REGISTER_CONDITION("dynamic_condition", DynamicCondition)

} // namespace openphys