@echo off
chcp 65001 > nul
echo ===================================================
echo   OpenPhys V2 - Complete Installation
echo ===================================================
echo.

set "ROOT_DIR=%CD%"

if exist "venv" goto VENV_EXISTS
echo [1/6] Creating virtual environment (venv)...
python -m venv venv
if errorlevel 1 goto ERROR_VENV
goto VENV_DONE

:VENV_EXISTS
echo [1/6] Virtual environment (venv) already exists.
:VENV_DONE

echo.
echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/6] Installing build tools, Ninja, and PyTorch...
python -m pip install --upgrade pip setuptools wheel cmake ninja pybind11
if errorlevel 1 goto ERROR_TORCH

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 goto ERROR_TORCH

echo.
echo [4/6] Installing OpenPhys V2 Python package...
if exist "setup_v2.py" (
    if not exist "setup.py" ren "setup_v2.py" "setup.py"
)
pip install -e .
if errorlevel 1 goto ERROR_PKG

echo.
echo [5/6] Configuring C++ dependencies...

if not exist "cpp\eigen" (
    echo Downloading Eigen3 automatically...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip' -OutFile 'eigen.zip'"
    powershell -Command "Expand-Archive -Path 'eigen.zip' -DestinationPath 'cpp\eigen_temp' -Force"
    cmake -S "cpp\eigen_temp\eigen-3.4.0" -B "cpp\eigen_temp\build" -DCMAKE_INSTALL_PREFIX="%ROOT_DIR%\cpp\eigen"
    cmake --install "cpp\eigen_temp\build"
    rmdir /s /q "cpp\eigen_temp"
    del "eigen.zip"
) else (
    echo Eigen3 already exists, skipping.
)

if not exist "cpp\nlohmann_json" (
    echo Downloading nlohmann_json automatically...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/nlohmann/json/archive/refs/tags/v3.11.3.zip' -OutFile 'json.zip'"
    powershell -Command "Expand-Archive -Path 'json.zip' -DestinationPath 'cpp\json_temp' -Force"
    cmake -S "cpp\json_temp\json-3.11.3" -B "cpp\json_temp\build" -DCMAKE_INSTALL_PREFIX="%ROOT_DIR%\cpp\nlohmann_json" -DJSON_BuildTests=OFF
    cmake --install "cpp\json_temp\build"
    rmdir /s /q "cpp\json_temp"
    del "json.zip"
) else (
    echo nlohmann_json already exists, skipping.
)

echo.
echo [6/6] Compiling C++ core...

if exist "cpp\CMakeLists_v2.txt" (
    if not exist "cpp\CMakeLists.txt" ren "cpp\CMakeLists_v2.txt" "CMakeLists.txt"
)

set "VS_VARS=C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not exist "%VS_VARS%" (
    echo ERROR: vcvars64.bat not found at specified location!
    goto ERROR_BUILD
)

echo Loading Visual Studio Compiler environment...
call "%VS_VARS%"

for /f "tokens=*" %%i in ('python -c "import torch.utils; print(torch.utils.cmake_prefix_path)"') do set "TORCH_CMAKE_PATH=%%i"
for /f "tokens=*" %%j in ('python -c "import pybind11; print(pybind11.get_cmake_dir())"') do set "PYBIND_CMAKE_PATH=%%j"

if exist "cpp\build" rmdir /s /q "cpp\build"
mkdir cpp\build
cd cpp\build

cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="%TORCH_CMAKE_PATH%;%PYBIND_CMAKE_PATH%;%ROOT_DIR%\cpp\eigen\share\eigen3\cmake;%ROOT_DIR%\cpp\nlohmann_json\share\cmake\nlohmann_json" ..
if errorlevel 1 goto ERROR_BUILD

cmake --build .
if errorlevel 1 goto ERROR_BUILD

echo.
echo Moving compiled C++ library...
if exist "*.pyd" (
    copy /Y "*.pyd" "..\..\src\openphys\"
)

cd ..\..

echo.
echo ===================================================
echo     Setup and Build Completed Successfully!     
echo ===================================================
echo.
pause
exit /b 0

:ERROR_VENV
echo ERROR: Failed to create virtual environment.
goto ERROR
:ERROR_TORCH
echo ERROR: Failed to install Python dependencies.
goto ERROR
:ERROR_PKG
echo ERROR: Failed to install OpenPhys package.
goto ERROR
:ERROR_BUILD
cd ..\..
echo ERROR: C++ Compilation failed.
:ERROR
pause
exit /b 1