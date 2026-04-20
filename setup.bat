@echo off
echo ================================================
echo    Dashboard Inventario Arboreo - Campus COD
echo    Universidad Nacional de Costa Rica (UNA)
echo ================================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no encontrado. Por favor instala Python 3.8+
    pause
    exit /b 1
)
echo OK: Python encontrado
echo.

REM Verificar pip
echo Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip no encontrado
    pause
    exit /b 1
)
echo OK: pip encontrado
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error al instalar dependencias
    pause
    exit /b 1
)
echo OK: Dependencias instaladas
echo.

REM Verificar archivo de datos
echo Verificando archivo de datos...
if not exist "CENSO_Historico_UNA_con_calculos.xlsx" (
    echo Error: Archivo de datos no encontrado
    echo Por favor asegurate de que CENSO_Historico_UNA_con_calculos.xlsx
    echo este en el mismo directorio que este script
    pause
    exit /b 1
)
echo OK: Archivo de datos encontrado
echo.

echo ================================================
echo Configuracion completada!
echo ================================================
echo.
echo Para iniciar el dashboard, ejecuta:
echo.
echo     streamlit run app.py
echo.
echo El dashboard se abrira automaticamente en tu navegador
echo URL local: http://localhost:8501
echo.
pause
