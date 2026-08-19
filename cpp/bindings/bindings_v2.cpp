#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <nlohmann/json.hpp>
#include "openphys/dynamic_residual.hpp"
#include "openphys/mesh_v2.hpp"

namespace py = pybind11;

// Pybind11 için JSON dönüştürücü yardımcı fonksiyon
nlohmann::json py_dict_to_json(const py::dict& d) {
    // İleride detaylandırılacak olan dict -> json parse mekanizması
    return nlohmann::json::object(); 
}

PYBIND11_MODULE(openphys_core_v2, m) {
    m.doc() = "OpenPhys V2 Core Bindings - Dynamic PDE and Zero-Copy Support";

    // Dinamik residual arayüzünü dışarı açıyoruz
    py::class_<openphys::DynamicStrongResidual, std::shared_ptr<openphys::DynamicStrongResidual>>(m, "DynamicStrongResidual")
        .def(py::init<>())
        .def("set_parameters", [](openphys::DynamicStrongResidual& self, py::dict py_params) {
            self.set_parameters(py_dict_to_json(py_params));
        })
        .def("get_schema", &openphys::DynamicStrongResidual::get_schema);
        
    // Sıfır-kopya tensör enjeksiyon fonksiyonu (PyTorch -> C++)
    m.def("inject_dynamic_residual", [](uintptr_t torch_data_ptr, int rows, int cols, openphys::FieldData& field_data) {
        // PyTorch tensörünün bellek adresini C++ Eigen Map üzerinden doğrudan bağlıyoruz
        // Bu işlem autograd'ın oluşturduğu hesaplama grafiğini (computational graph) koparmaz.
        new (&field_data.values) Eigen::Map<Eigen::MatrixXd>(reinterpret_cast<double*>(torch_data_ptr), rows, cols);
    }, "Injects PyTorch autograd results back to C++ memory directly via pointers");
}