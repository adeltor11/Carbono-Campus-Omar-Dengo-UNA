# Dashboard de Inventario Arbóreo - Campus Omar Dengo
## Universidad Nacional de Costa Rica (UNA)
### Sistema de Monitoreo de Carbono y Biomasa Forestal

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Autor:** Adrián Delgado Torres — EDECA, UNA  
**App publicada:** https://carbono-campus-omar-dengo-una-ugybcv7sw8upkyyck5ltte.streamlit.app  
**Repositorio:** https://github.com/adeltor11/Carbono-Campus-Omar-Dengo-UNA

---

## 1. Descripción del Proyecto

Dashboard web interactivo desarrollado con Python y Streamlit para visualizar y analizar el inventario arbóreo del Campus Omar Dengo de la Universidad Nacional de Costa Rica. El sistema permite monitorear la evolución histórica del inventario forestal y estimar el almacenamiento de biomasa y captura de carbono.

### Características principales

- **Resumen Ejecutivo:** KPIs principales (árboles activos, especies, biomasa, carbono, CO₂ equivalente)
- **Análisis Temporal:** Evolución histórica del inventario (2018–2025)
- **Análisis por Especie:** Estadísticas detalladas y distribuciones diamétricas
- **Análisis de Biomasa:** Relaciones alométricas entre DAP, altura y carbono
- **Filtros interactivos:** Año, estado del árbol, especie, rango de DAP

### Datos del inventario

| Variable | Valor |
|---|---|
| Registros históricos | 8,192 |
| Árboles únicos | ~1,698 |
| Período cubierto | 2018–2025 |
| Especies registradas | 102+ |
| Área del campus | 18.5 hectáreas |
| Variables por árbol | 22 |

---

## 2. Estructura de Archivos

```
Proyecto_pagina/
├── app.py                                  # Código principal del dashboard
├── requirements.txt                        # Dependencias de Python
├── CENSO_Historico_UNA_con_calculos.xlsx   # Base de datos del inventario
├── DOCUMENTACION.md                        # Este documento
├── README.md                               # Descripción del repositorio
├── .gitignore                              # Exclusiones de Git
└── .streamlit/
    └── config.toml                         # Tema y configuración visual
```

---

## 3. Tecnologías Utilizadas

| Librería | Versión | Función |
|---|---|---|
| Streamlit | ≥ 1.30 | Framework de la aplicación web |
| Pandas | ≥ 2.0 | Carga y procesamiento de datos |
| Plotly | ≥ 5.18 | Gráficos interactivos |
| OpenPyXL | ≥ 3.1 | Lectura de archivos Excel |
| NumPy | ≥ 1.24 | Cálculos numéricos |

---

## 4. Instalación Local

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes)
- 500 MB de espacio en disco

### Pasos

**1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**2. Ejecutar el dashboard:**
```bash
streamlit run app.py
```

**3.** El dashboard se abre automáticamente en: `http://localhost:8501`

---

## 5. Aplicación Publicada en Streamlit Cloud

La aplicación está desplegada de forma gratuita en Streamlit Community Cloud y conectada al repositorio de GitHub. Cualquier actualización al repositorio se refleja automáticamente en la app en 2–3 minutos.

**URL pública:**  
https://carbono-campus-omar-dengo-una-ugybcv7sw8upkyyck5ltte.streamlit.app

**Repositorio GitHub:**  
https://github.com/adeltor11/Carbono-Campus-Omar-Dengo-UNA

### Características del plan gratuito

| Recurso | Límite |
|---|---|
| Apps públicas | Ilimitadas |
| Almacenamiento por app | 1 GB |
| Ancho de banda | Ilimitado |
| HTTPS | Incluido |

**Nota:** La app puede entrar en modo de reposo después de 7 días sin uso. Se reactiva en ~30 segundos al abrir la URL.

---

## 6. Actualización de Datos

Cuando se realice un nuevo censo, para actualizar los datos del dashboard:

### Desde GitHub (recomendado)

```bash
# En la carpeta del proyecto
git add CENSO_Historico_UNA_con_calculos.xlsx
git commit -m "Actualizar datos censo [AÑO]"
git push
```

Streamlit Cloud detecta el cambio y redesplega automáticamente.

### Desde la interfaz web de GitHub

1. Ir al repositorio en GitHub
2. Click en `CENSO_Historico_UNA_con_calculos.xlsx`
3. Click en el ícono de lápiz → "Upload a file"
4. Arrastrar el nuevo archivo Excel
5. Click en "Commit changes"

### Requisitos del archivo Excel actualizado

- Mismo nombre: `CENSO_Historico_UNA_con_calculos.xlsx`
- Hoja activa: `COD`
- Columnas requeridas: `ANIO MEDICION`, `NOMBRE COMUN`, `ESPECIE CIENTIFICA`, `DAP CM`, `ALTURA M`, `BIOMASA TOTAL KG`, `CARBONO TOTAL MG`, `CO2 EQUIVALENTE MG`, `ESTADO ARBOL`, `ID REGISTRO`, `NUMERO ARBOL`

---

## 7. Metodología de Cálculo

### Biomasa aérea

```
Biomasa_aérea (kg) = Volumen × Densidad_madera × 1000
Volumen (m³) = (π/4) × (DAP/100)² × Altura × Factor_forma
```

### Biomasa radicular

```
Biomasa_raíz (kg) = Biomasa_aérea × Factor_expansión_biomasa
```

### Biomasa total

```
Biomasa_total (kg) = Biomasa_aérea + Biomasa_raíz
```

### Carbono almacenado

```
Carbono (Mg) = Biomasa_total × 0.47 / 1000
```
*0.47 = fracción de carbono en materia seca (IPCC)*

### CO₂ equivalente

```
CO₂e (Mg) = Carbono (Mg) × 3.67
```
*3.67 = ratio peso molecular CO₂/C (44/12)*

**Fuentes metodológicas:**
- Ecuaciones alométricas específicas por especie
- IPCC Guidelines for National GHG Inventories
- Programa País Carbono Neutralidad 2.0 (PPCN 2.0) — Costa Rica

---

## 8. Personalización del Dashboard

### Cambiar colores (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#2d5f3f"             # Verde UNA
backgroundColor = "#ffffff"           # Fondo
secondaryBackgroundColor = "#f8f9fa" # Sidebar
textColor = "#262730"                # Texto
font = "sans serif"
```

### Cambiar logo en sidebar (`app.py`, línea ~113)

```python
# Logo desde URL (actual)
st.sidebar.image("https://upload.wikimedia.org/.../Logo_UNA.svg", width=200)

# Logo desde archivo local
st.sidebar.image("logo_una.png", width=200)
```

---

## 9. Solución de Problemas Comunes

| Error | Causa | Solución |
|---|---|---|
| `Module not found` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `File not found: CENSO_Historico...` | Excel no está en la carpeta | Verificar que el archivo está junto a `app.py` |
| Dashboard muy lento | Todos los filtros activos | Seleccionar un año específico o reducir filtros |
| Gráficos no se ven | JavaScript deshabilitado o navegador viejo | Usar Chrome actualizado |
| Puerto 8501 ocupado | Ya hay un Streamlit corriendo | `streamlit run app.py --server.port 8502` |
| App "dormida" en la nube | Inactividad > 7 días | Normal en plan gratuito, se activa en 30 seg |

---

## 10. Mejoras Futuras Sugeridas

- [ ] Mapas interactivos con coordenadas geográficas (Folium/Leaflet)
- [ ] Integración con base de datos PostgreSQL/PostGIS
- [ ] Reportes PDF automatizados desde el dashboard
- [ ] Autenticación de usuarios con contraseña
- [ ] Predicciones de captura futura con modelos de ML
- [ ] Replicación para otros campus UNA
- [ ] Integración con PPCN 2.0
- [ ] API REST para consultas externas

---

## 11. Contacto y Soporte

**Responsable técnico:**  
Adrián Delgado Torres  
Escuela de Ciencias Ambientales (EDECA)  
Universidad Nacional de Costa Rica  
Campus Omar Dengo, Heredia, Costa Rica

**Soporte técnico Streamlit:**  
https://discuss.streamlit.io

**Documentación oficial:**  
- Streamlit: https://docs.streamlit.io  
- Plotly: https://plotly.com/python/  
- Pandas: https://pandas.pydata.org/docs/

---

*Documento generado: Abril 2026 | Dashboard de Inventario Arbóreo — Campus Omar Dengo UNA*
