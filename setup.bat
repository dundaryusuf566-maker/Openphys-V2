@echo off
chcp 65001 > nul
echo ===================================================
echo   OpenPhys V2 - Eksiksiz Kurulum
echo ===================================================
echo.

:: Proje ana dizinini hafızaya alıyoruz
set "ROOT_DIR=%CD%"

:: 1. Sanal Ortam Kontrolü
if exist "venv" goto VENV_EXISTS
echo [1/6] Sanal ortam venv olusturuluyor...
python -m venv venv
if errorlevel 1 goto ERROR_VENV
goto VENV_DONE

:VENV_EXISTS
echo [1/6] Sanal ortam venv zaten mevcut.
:VENV_DONE

:: 2. Sanal Ortamı Aktifleştirme
echo.
echo [2/6] Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate.bat

:: 3. Temel Araçlar ve PyTorch Kurulumu
echo.
echo [3/6] Temel araclar, Ninja ve PyTorch kuruluyor...
python -m pip install --upgrade pip setuptools wheel cmake ninja pybind11
if errorlevel 1 goto ERROR_TORCH

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 goto ERROR_TORCH

:: 4. Paket Kurulumu
echo.
echo [4/6] OpenPhys V2 Python paketi kuruluyor...
if exist "setup_v2.py" (
    if not exist "setup.py" ren "setup_v2.py" "setup.py"
)
pip install -e .
if errorlevel 1 goto ERROR_PKG

:: 5. C++ Bağımlılıklarının (Eigen3, nlohmann_json) İndirilmesi
echo.
echo [5/6] C++ Bagimliliklari ayarlaniyor...

:: Eigen3
if not exist "cpp\eigen" (
    echo Eigen3 otomatik olarak indiriliyor...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip' -OutFile 'eigen.zip'"
    powershell -Command "Expand-Archive -Path 'eigen.zip' -DestinationPath 'cpp\eigen_temp' -Force"
    cmake -S "cpp\eigen_temp\eigen-3.4.0" -B "cpp\eigen_temp\build" -DCMAKE_INSTALL_PREFIX="%ROOT_DIR%\cpp\eigen"
    cmake --install "cpp\eigen_temp\build"
    rmdir /s /q "cpp\eigen_temp"
    del "eigen.zip"
) else (
    echo Eigen3 zaten mevcut, atlandi.
)

:: nlohmann_json
if not exist "cpp\nlohmann_json" (
    echo nlohmann_json otomatik olarak indiriliyor...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/nlohmann/json/archive/refs/tags/v3.11.3.zip' -OutFile 'json.zip'"
    powershell -Command "Expand-Archive -Path 'json.zip' -DestinationPath 'cpp\json_temp' -Force"
    cmake -S "cpp\json_temp\json-3.11.3" -B "cpp\json_temp\build" -DCMAKE_INSTALL_PREFIX="%ROOT_DIR%\cpp\nlohmann_json" -DJSON_BuildTests=OFF
    cmake --install "cpp\json_temp\build"
    rmdir /s /q "cpp\json_temp"
    del "json.zip"
) else (
    echo nlohmann_json zaten mevcut, atlandi.
)

:: 6. Ninja ile C++ Çekirdeğini Derleme
echo.
echo [6/6] C++ cekirdegi derleniyor...

if exist "cpp\CMakeLists_v2.txt" (
    if not exist "cpp\CMakeLists.txt" ren "cpp\CMakeLists_v2.txt" "CMakeLists.txt"
)

:: =========================================================================
:: BURAYA KENDİ BİLGİSAYARINDAKİ vcvars64.bat DOSYASININ TAM YOLUNU YAZABILIRSİN:
:: =========================================================================
set "VS_VARS=C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not exist "%VS_VARS%" (
    echo HATA: Belirtilen konumda vcvars64.bat bulunamadi!
    goto ERROR_BUILD
)

echo Visual Studio Derleyici ortami yukleniyor...
call "%VS_VARS%"

:: Yolları çek
for /f "tokens=*" %%i in ('python -c "import torch.utils; print(torch.utils.cmake_prefix_path)"') do set "TORCH_CMAKE_PATH=%%i"
for /f "tokens=*" %%j in ('python -c "import pybind11; print(pybind11.get_cmake_dir())"') do set "PYBIND_CMAKE_PATH=%%j"

:: Önceki hatalı derleme kalıntılarını siliyoruz
if exist "cpp\build" rmdir /s /q "cpp\build"
mkdir cpp\build
cd cpp\build

:: Kütüphanelerin yollarını CMake'e veriyoruz
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="%TORCH_CMAKE_PATH%;%PYBIND_CMAKE_PATH%;%ROOT_DIR%\cpp\eigen\share\eigen3\cmake;%ROOT_DIR%\cpp\nlohmann_json\share\cmake\nlohmann_json" ..
if errorlevel 1 goto ERROR_BUILD

cmake --build .
if errorlevel 1 goto ERROR_BUILD

echo.
echo Derlenen C++ kutuphanesi tasiniyor...
if exist "*.pyd" (
    copy /Y "*.pyd" "..\..\src\openphys\"
)

cd ..\..

echo.
echo ===================================================
echo     Kurulum ve Derleme Basariyla Tamamlandi!     
echo ===================================================
echo.
pause
exit /b 0

:ERROR_VENV
echo HATA: Sanal ortam olusturulamadi.
goto ERROR
:ERROR_TORCH
echo HATA: Paketler kurulamadi.
goto ERROR
:ERROR_PKG
echo HATA: Python paketi kurulamadi.
goto ERROR
:ERROR_BUILD
cd ..\..
echo HATA: Derleme basarisiz oldu.
:ERROR
pause
exit /b 1