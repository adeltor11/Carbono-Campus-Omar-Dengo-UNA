# 🌳 Dashboard de Inventario Arbóreo - Campus Omar Dengo

Dashboard interactivo de Streamlit para visualizar y analizar el inventario arbóreo del Campus Omar Dengo de la Universidad Nacional de Costa Rica (UNA), con estimaciones de biomasa y captura de carbono.

## 📋 Características Principales

- **Resumen Ejecutivo**: KPIs principales (árboles, especies, carbono, CO₂e)
- **Análisis Temporal**: Evolución histórica del inventario (2018-2025)
- **Análisis por Especie**: Estadísticas detalladas y distribuciones diamétricas
- **Análisis de Biomasa**: Relaciones alométricas y captura de carbono
- **Exportación de Datos**: Descarga de datos en formato CSV

## 🚀 Instalación Local

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o Descargar los Archivos

Descarga estos archivos en una carpeta:
```
dashboard-una/
├── app.py
├── requirements.txt
├── CENSO_Historico_UNA_con_calculos.xlsx
└── .streamlit/
    └── config.toml
```

### Paso 2: Instalar Dependencias

Abre una terminal/consola en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar el Dashboard

```bash
streamlit run app.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## ☁️ Publicación en Streamlit Community Cloud (RECOMENDADO)

### Ventajas
- ✅ **Gratuito** hasta 1GB de datos
- ✅ **Sin servidor propio** necesario
- ✅ **URL pública** compartible
- ✅ **Actualizaciones automáticas** desde GitHub
- ✅ **HTTPS** incluido

### Paso a Paso

#### 1. Crear cuenta en GitHub (si no tienes)
- Ve a https://github.com
- Crea una cuenta gratuita

#### 2. Crear un Repositorio

a. En GitHub, haz clic en "New repository"
b. Configura:
   - **Nombre**: `inventario-arboreo-una-cod`
   - **Descripción**: "Dashboard de inventario arbóreo Campus Omar Dengo - UNA"
   - **Visibilidad**: Público o Privado (según preferencia)
c. Haz clic en "Create repository"

#### 3. Subir los Archivos

**Opción A - Por interfaz web (más fácil):**
1. En tu repositorio, haz clic en "Add file" > "Upload files"
2. Arrastra estos archivos:
   - `app.py`
   - `requirements.txt`
   - `CENSO_Historico_UNA_con_calculos.xlsx`
3. Crea una carpeta `.streamlit` y sube `config.toml`
4. Haz clic en "Commit changes"

**Opción B - Por línea de comandos:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/inventario-arboreo-una-cod.git
git push -u origin main
```

#### 4. Crear cuenta en Streamlit Community Cloud

- Ve a https://streamlit.io/cloud
- Haz clic en "Sign up" y conéctate con tu cuenta de GitHub

#### 5. Deployar la Aplicación

1. En Streamlit Cloud, haz clic en "New app"
2. Configura:
   - **Repository**: Selecciona `TU_USUARIO/inventario-arboreo-una-cod`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Haz clic en "Deploy!"

#### 6. ¡Listo! 🎉

Tu dashboard estará disponible en:
```
https://TU_USUARIO-inventario-arboreo-una-cod.streamlit.app
```

## 🔧 Otras Opciones de Publicación

### Opción 2: Heroku (Gratis hasta cierto límite)

1. Crea cuenta en https://heroku.com
2. Instala Heroku CLI
3. Crea archivo `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

4. Crea `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

5. Deploy:
```bash
heroku login
heroku create inventario-una-cod
git push heroku main
```

### Opción 3: Render (Gratis)

1. Crea cuenta en https://render.com
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT`
4. Deploy

### Opción 4: Servidor Institucional UNA

Si UNA tiene servidor web con Python:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con puerto específico
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

Configurar reverse proxy (nginx):
```nginx
location /inventario {
    proxy_pass http://localhost:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## 📊 Actualización de Datos

Para actualizar los datos del dashboard:

1. Reemplaza el archivo `CENSO_Historico_UNA_con_calculos.xlsx`
2. Si usas GitHub/Streamlit Cloud:
   ```bash
   git add CENSO_Historico_UNA_con_calculos.xlsx
   git commit -m "Actualizar datos inventario"
   git push
   ```
3. Streamlit Cloud detectará el cambio y redesplegará automáticamente

## 🎨 Personalización

### Cambiar colores (archivo `.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#2d5f3f"      # Verde UNA
backgroundColor = "#ffffff"    # Fondo blanco
secondaryBackgroundColor = "#f8f9fa"  # Gris claro
```

### Agregar logo UNA:
En `app.py`, línea 150:
```python
st.sidebar.image("ruta/a/logo_una.png", width=200)
```

## 📱 Características del Dashboard

### Filtros Interactivos
- Año de medición
- Estado del árbol (Activo/Removido)
- Especies específicas
- Rango de DAP

### Visualizaciones
- Métricas de resumen (KPIs)
- Gráficos de especies más frecuentes
- Distribución de captura de carbono
- Evolución temporal del inventario
- Distribuciones diamétricas
- Relaciones alométricas (DAP vs biomasa)

### Exportación
- Datos filtrados (CSV)
- Resumen ejecutivo (CSV)
- Estadísticas por especie (CSV)

## 🔒 Consideraciones de Seguridad

- El archivo Excel se incluye en el repositorio
- Para datos sensibles, considera usar:
  - Variables de entorno
  - Streamlit Secrets
  - Base de datos externa (PostgreSQL)

## 📞 Soporte Técnico

**EDECA - UNA**  
Escuela de Ciencias Ambientales  
Campus Omar Dengo  
Heredia, Costa Rica

---

## 📝 Notas Técnicas

- **Framework**: Streamlit 1.30+
- **Datos**: Excel (8,192 registros históricos)
- **Período**: 2018-2025
- **Especies**: 100+ especies forestales
- **Metodología**: Ecuaciones alométricas específicas

## 🌟 Mejoras Futuras Sugeridas

- [ ] Integración con base de datos PostgreSQL/PostGIS
- [ ] Mapas interactivos con coordenadas geográficas
- [ ] Autenticación de usuarios
- [ ] Reportes PDF automatizados
- [ ] API REST para consultas externas
- [ ] Integración con PPCN 2.0
- [ ] Predicciones de captura futura (ML)

---

**Desarrollado para la Universidad Nacional de Costa Rica (UNA)**  
*Sistema de Monitoreo de Carbono y Biomasa Forestal*
