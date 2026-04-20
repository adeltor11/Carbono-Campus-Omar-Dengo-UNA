#!/bin/bash

echo "================================================"
echo "   Dashboard Inventario Arbóreo - Campus COD"
echo "   Universidad Nacional de Costa Rica (UNA)"
echo "================================================"
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if command -v python3 &> /dev/null
then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8+"
    exit 1
fi

# Verificar pip
echo ""
echo "🔍 Verificando pip..."
if command -v pip3 &> /dev/null
then
    PIP_VERSION=$(pip3 --version)
    echo "✅ pip encontrado"
else
    echo "❌ pip no encontrado. Por favor instala pip"
    exit 1
fi

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Verificar archivo de datos
echo ""
echo "🔍 Verificando archivo de datos..."
if [ -f "CENSO_Historico_UNA_con_calculos.xlsx" ]; then
    FILE_SIZE=$(du -h "CENSO_Historico_UNA_con_calculos.xlsx" | cut -f1)
    echo "✅ Archivo de datos encontrado ($FILE_SIZE)"
else
    echo "❌ Archivo de datos no encontrado"
    echo "   Por favor asegúrate de que CENSO_Historico_UNA_con_calculos.xlsx"
    echo "   esté en el mismo directorio que este script"
    exit 1
fi

# Todo listo
echo ""
echo "================================================"
echo "✅ ¡Configuración completada!"
echo "================================================"
echo ""
echo "Para iniciar el dashboard, ejecuta:"
echo ""
echo "    streamlit run app.py"
echo ""
echo "El dashboard se abrirá automáticamente en tu navegador"
echo "URL local: http://localhost:8501"
echo ""
