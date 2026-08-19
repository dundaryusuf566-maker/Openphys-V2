#include "openphys/plugin_interface.hpp"
#include <iostream>

namespace openphys {

// Singleton Registry'nin statik instance'ı
PluginRegistry& PluginRegistry::instance() {
    static PluginRegistry instance_;
    return instance_;
}

void PluginRegistry::register_strong_residual(const std::string& name, std::function<std::shared_ptr<IStrongResidual>()> factory) {
    strong_residuals_[name] = factory;
}

std::shared_ptr<IStrongResidual> PluginRegistry::create_strong_residual(const std::string& name) {
    auto it = strong_residuals_.find(name);
    if (it != strong_residuals_.end()) {
        return it->second();
    }
    std::cerr << "[Registry] Uyarı: Strong Residual '" << name << "' bulunamadı!" << std::endl;
    return nullptr;
}

// Benzer şekilde sınır koşulları (Conditions) için de factory metodları...
} // namespace openphys