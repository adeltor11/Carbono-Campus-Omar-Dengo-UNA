"""
Dashboard de Inventario Arbóreo - Campus Omar Dengo
Universidad Nacional de Costa Rica (UNA)
Sistema de Monitoreo de Carbono y Biomasa Forestal
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Inventario Arbóreo UNA - Campus Omar Dengo",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con colores UNA
st.markdown("""
    <style>
    /* Ocultar barra de herramientas de descarga en tablas */
    [data-testid="stDataFrameToolbar"] {
        display: none !important;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Forzar color oscuro en los valores de las métricas */
    .stMetric label {
        color: #2d5f3f !important;
        font-weight: 600;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #2d5f3f 0%, #3d7f5f 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1 {
        color: #2d5f3f;
        font-weight: 700;
    }
    h2, h3 {
        color: #3d7f5f;
    }
    .info-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-left: 4px solid #2d5f3f;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def cargar_datos():
    """Carga los datos del archivo Excel"""
    file_path = 'CENSO_Historico_UNA_con_calculos.xlsx'
    df = pd.read_excel(file_path, sheet_name='COD')
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Convertir año a entero
    df['ANIO MEDICION'] = pd.to_numeric(df['ANIO MEDICION'], errors='coerce')
    
    # Estandarizar nombres de especies
    df['NOMBRE COMUN'] = df['NOMBRE COMUN'].str.strip().str.title()
    
    return df

# Función para calcular métricas
def calcular_metricas(df):
    """Calcula métricas principales del inventario"""
    metricas = {
        'total_arboles': len(df[df['ESTADO ARBOL'] == 'Activo']),
        'total_especies': df['NOMBRE COMUN'].nunique(),
        'carbono_total': df[df['ESTADO ARBOL'] == 'Activo']['CARBONO TOTAL MG'].sum(),
        'co2_total': df[df['ESTADO ARBOL'] == 'Activo']['CO2 EQUIVALENTE MG'].sum(),
        'biomasa_total': df[df['ESTADO ARBOL'] == 'Activo']['BIOMASA TOTAL KG'].sum(),
        'dap_promedio': df[df['ESTADO ARBOL'] == 'Activo']['DAP CM'].mean(),
        'altura_promedio': df[df['ESTADO ARBOL'] == 'Activo']['ALTURA M'].mean(),
        'arboles_removidos': len(df[df['ESTADO ARBOL'] == 'Removido'])
    }
    return metricas

# Cargar datos
try:
    df_original = cargar_datos()
    st.success(f"✅ Datos cargados correctamente: {len(df_original):,} registros históricos")
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.stop()

# SIDEBAR - Filtros
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Logo_UNA.svg/1200px-Logo_UNA.svg.png", width=200)
st.sidebar.title("🔍 Filtros")

# Filtro de año
años_disponibles = sorted(df_original['ANIO MEDICION'].dropna().unique())
año_seleccionado = st.sidebar.selectbox(
    "📅 Año de medición",
    options=['Todos'] + [int(año) for año in años_disponibles],
    index=0
)

# Filtrar datos por año
if año_seleccionado == 'Todos':
    df = df_original.copy()
else:
    df = df_original[df_original['ANIO MEDICION'] == año_seleccionado].copy()

# Filtro de estado
estado_filtro = st.sidebar.multiselect(
    "🌳 Estado del árbol",
    options=df['ESTADO ARBOL'].unique(),
    default=['Activo']
)

df = df[df['ESTADO ARBOL'].isin(estado_filtro)]

# Filtro de especie
especies_disponibles = sorted(df['NOMBRE COMUN'].dropna().unique())
especie_filtro = st.sidebar.multiselect(
    "🍃 Especies",
    options=especies_disponibles,
    default=[]
)

if especie_filtro:
    df = df[df['NOMBRE COMUN'].isin(especie_filtro)]

# Filtro de rango de DAP
dap_min = float(df['DAP CM'].min())
dap_max = float(df['DAP CM'].max())
dap_range = st.sidebar.slider(
    "📏 Rango de DAP (cm)",
    min_value=dap_min,
    max_value=dap_max,
    value=(dap_min, dap_max)
)

df = df[(df['DAP CM'] >= dap_range[0]) & (df['DAP CM'] <= dap_range[1])]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Registros filtrados: **{len(df):,}**")

# HEADER
st.title("🌳 Inventario Arbóreo - Campus Omar Dengo")
st.markdown("### Universidad Nacional de Costa Rica (UNA)")
st.markdown("**Sistema de Monitoreo de Carbono y Biomasa Forestal**")

# Calcular métricas
metricas = calcular_metricas(df)

# PÁGINA 1: RESUMEN EJECUTIVO
st.markdown("---")
st.header("📊 Resumen Ejecutivo")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    st.metric(
        label="🌳 Árboles Activos",
        value=f"{metricas['total_arboles']:,}",
        delta="Total inventariados"
    )

with col2:
    st.metric(
        label="🍃 Especies",
        value=f"{metricas['total_especies']:,}",
        delta="Diversidad total"
    )

with col3:
    st.metric(
        label="⚖️ Biomasa Total",
        value=f"{metricas['biomasa_total']:,.0f}",
        delta="kg totales"
    )

with col4:
    st.metric(
        label="🌍 Carbono Total",
        value=f"{metricas['carbono_total']:.1f}",
        delta="Megagramos (Mg)"
    )

with col5:
    st.metric(
        label="💨 CO₂ Equivalente",
        value=f"{metricas['co2_total']:.1f}",
        delta="Megagramos CO₂e"
    )

with col6:
    st.metric(
        label="🪵 Removidos",
        value=f"{metricas['arboles_removidos']:,}",
        delta="Árboles históricos"
    )

with col7:
    st.metric(
        label="📏 DAP Promedio",
        value=f"{metricas['dap_promedio']:.1f} cm",
        delta="Diámetro medio"
    )

with col8:
    # Calcular equivalencia en autos
    autos_equivalentes = metricas['co2_total'] / 4.6  # 4.6 Mg CO2/año por auto
    st.metric(
        label="🚗 Equivalente",
        value=f"{autos_equivalentes:,.0f}",
        delta="autos/año compensados"
    )

# Gráficos de resumen
st.markdown("---")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌳 Top 10 Especies más Frecuentes")
    top_especies = df[df['ESTADO ARBOL'] == 'Activo']['NOMBRE COMUN'].value_counts().head(10)
    
    fig_especies = px.bar(
        x=top_especies.values,
        y=top_especies.index,
        orientation='h',
        labels={'x': 'Cantidad de Árboles', 'y': 'Especie'},
        color=top_especies.values,
        color_continuous_scale='Greens'
    )
    fig_especies.update_layout(
        showlegend=False,
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_especies, use_container_width=True)

with col_right:
    st.subheader("🌍 Captura de Carbono por Especie (Top 10)")
    carbono_por_especie = df[df['ESTADO ARBOL'] == 'Activo'].groupby('NOMBRE COMUN')['CARBONO TOTAL MG'].sum().sort_values(ascending=False).head(10)
    
    fig_carbono = px.pie(
        values=carbono_por_especie.values,
        names=carbono_por_especie.index,
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig_carbono.update_traces(textposition='inside', textinfo='percent+label')
    fig_carbono.update_layout(height=400)
    st.plotly_chart(fig_carbono, use_container_width=True)

# PÁGINA 2: ANÁLISIS TEMPORAL
st.markdown("---")
st.header("📈 Análisis Temporal del Inventario")

# Evolución del inventario
evolucion = df_original.groupby('ANIO MEDICION').agg({
    'ID REGISTRO': 'count',
    'CARBONO TOTAL MG': 'sum',
    'CO2 EQUIVALENTE MG': 'sum',
    'BIOMASA TOTAL KG': 'sum'
}).reset_index()

evolucion.columns = ['Año', 'Total Árboles', 'Carbono (Mg)', 'CO₂e (Mg)', 'Biomasa (kg)']

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("📊 Evolución del Número de Árboles")
    fig_arboles = px.line(
        evolucion,
        x='Año',
        y='Total Árboles',
        markers=True,
        line_shape='spline'
    )
    fig_arboles.update_traces(line_color='#2d5f3f', line_width=3)
    fig_arboles.update_layout(height=350)
    st.plotly_chart(fig_arboles, use_container_width=True)

with col_t2:
    st.subheader("🌍 Evolución de Carbono Almacenado")
    fig_carbono_tiempo = px.line(
        evolucion,
        x='Año',
        y='Carbono (Mg)',
        markers=True,
        line_shape='spline'
    )
    fig_carbono_tiempo.update_traces(line_color='#3d7f5f', line_width=3)
    fig_carbono_tiempo.update_layout(height=350)
    st.plotly_chart(fig_carbono_tiempo, use_container_width=True)

# Comparación año a año
st.subheader("📊 Comparación Interanual")
fig_comparacion = go.Figure()

fig_comparacion.add_trace(go.Bar(
    name='Carbono (Mg)',
    x=evolucion['Año'],
    y=evolucion['Carbono (Mg)'],
    marker_color='#2d5f3f'
))

fig_comparacion.add_trace(go.Bar(
    name='CO₂e (Mg)',
    x=evolucion['Año'],
    y=evolucion['CO₂e (Mg)'],
    marker_color='#5f9f5f'
))

fig_comparacion.update_layout(
    barmode='group',
    height=400,
    xaxis_title='Año',
    yaxis_title='Megagramos (Mg)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_comparacion, use_container_width=True)

# PÁGINA 3: ANÁLISIS POR ESPECIE
st.markdown("---")
st.header("🌿 Análisis Detallado por Especie")

# Tabla de estadísticas por especie
st.subheader("📋 Estadísticas por Especie")

especies_stats = df[df['ESTADO ARBOL'] == 'Activo'].groupby('NOMBRE COMUN').agg({
    'ID REGISTRO': 'count',
    'DAP CM': ['mean', 'min', 'max'],
    'ALTURA M': 'mean',
    'BIOMASA TOTAL KG': 'sum',
    'CARBONO TOTAL MG': 'sum',
    'CO2 EQUIVALENTE MG': 'sum'
}).round(2)

especies_stats.columns = ['Cantidad', 'DAP Prom (cm)', 'DAP Min (cm)', 'DAP Max (cm)', 
                          'Altura Prom (m)', 'Biomasa Total (kg)', 'Carbono (Mg)', 'CO₂e (Mg)']
especies_stats = especies_stats.sort_values('Cantidad', ascending=False)

st.dataframe(especies_stats, use_container_width=True)

# Distribución diamétrica
st.subheader("📏 Distribución de Clases Diamétricas")

# Crear clases diamétricas
df_activos = df[df['ESTADO ARBOL'] == 'Activo'].copy()
df_activos['Clase Diamétrica'] = pd.cut(
    df_activos['DAP CM'],
    bins=[0, 10, 20, 30, 40, 50, 100, 200],
    labels=['0-10', '10-20', '20-30', '30-40', '40-50', '50-100', '>100']
)

distribucion_dap = df_activos['Clase Diamétrica'].value_counts().sort_index()

fig_dap = px.bar(
    x=distribucion_dap.index,
    y=distribucion_dap.values,
    labels={'x': 'Clase Diamétrica (cm)', 'y': 'Frecuencia'},
    color=distribucion_dap.values,
    color_continuous_scale='Greens'
)
fig_dap.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_dap, use_container_width=True)

# Distribución diamétrica por especie (Top 5)
st.subheader("📊 Distribución Diamétrica - Top 5 Especies")

top5_especies = df_activos['NOMBRE COMUN'].value_counts().head(5).index

df_top5 = df_activos[df_activos['NOMBRE COMUN'].isin(top5_especies)]

fig_violin = px.violin(
    df_top5,
    y='NOMBRE COMUN',
    x='DAP CM',
    color='NOMBRE COMUN',
    box=True,
    points='all',
    orientation='h',
    color_discrete_sequence=px.colors.sequential.Greens_r
)
fig_violin.update_layout(
    showlegend=False,
    height=400,
    xaxis_title='DAP (cm)',
    yaxis_title=''
)
st.plotly_chart(fig_violin, use_container_width=True)

# PÁGINA 4: ANÁLISIS DE BIOMASA Y CARBONO
st.markdown("---")
st.header("⚖️ Análisis de Biomasa y Captura de Carbono")

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.subheader("🌳 Relación DAP vs Biomasa")
    
    # Muestra aleatoria para mejorar rendimiento del gráfico
    # Filtrar valores nulos en las columnas que se usarán
    muestra = df_activos.dropna(subset=['DAP CM', 'BIOMASA TOTAL KG', 'ALTURA M']).sample(n=min(1000, len(df_activos.dropna(subset=['DAP CM', 'BIOMASA TOTAL KG', 'ALTURA M']))))
    
    fig_scatter = px.scatter(
        muestra,
        x='DAP CM',
        y='BIOMASA TOTAL KG',
        color='NOMBRE COMUN',
        size='ALTURA M',
        hover_data=['NOMBRE COMUN', 'ALTURA M', 'CARBONO TOTAL MG'],
        opacity=0.6
    )
    fig_scatter.update_layout(
        showlegend=False,
        height=400,
        xaxis_title='DAP (cm)',
        yaxis_title='Biomasa Total (kg)'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_b2:
    st.subheader("📈 Relación Altura vs Carbono")
    
    # Filtrar valores nulos para el segundo gráfico
    muestra2 = df_activos.dropna(subset=['ALTURA M', 'CARBONO TOTAL MG', 'DAP CM']).sample(n=min(1000, len(df_activos.dropna(subset=['ALTURA M', 'CARBONO TOTAL MG', 'DAP CM']))))
    
    fig_scatter2 = px.scatter(
        muestra2,
        x='ALTURA M',
        y='CARBONO TOTAL MG',
        color='NOMBRE COMUN',
        size='DAP CM',
        hover_data=['NOMBRE COMUN', 'DAP CM', 'CO2 EQUIVALENTE MG'],
        opacity=0.6
    )
    fig_scatter2.update_layout(
        showlegend=False,
        height=400,
        xaxis_title='Altura (m)',
        yaxis_title='Carbono (Mg)'
    )
    st.plotly_chart(fig_scatter2, use_container_width=True)

# Distribución de carbono
st.subheader("🌍 Distribución de Carbono Almacenado")

df_activos['Rango Carbono'] = pd.cut(
    df_activos['CARBONO TOTAL MG'],
    bins=[0, 0.5, 1, 2, 5, 10, 100],
    labels=['<0.5', '0.5-1', '1-2', '2-5', '5-10', '>10']
)

dist_carbono = df_activos['Rango Carbono'].value_counts().sort_index()

fig_carbono_dist = px.bar(
    x=dist_carbono.index,
    y=dist_carbono.values,
    labels={'x': 'Rango de Carbono (Mg)', 'y': 'Cantidad de Árboles'},
    color=dist_carbono.values,
    color_continuous_scale='Greens'
)
fig_carbono_dist.update_layout(showlegend=False, height=350)
st.plotly_chart(fig_carbono_dist, use_container_width=True)

# PÁGINA 5: DATOS Y EXPORTACIÓN
st.markdown("---")
st.header("📥 Datos y Exportación")

st.subheader("🗂️ Vista de Datos Filtrados")

# Mostrar datos filtrados
columnas_mostrar = ['NUMERO ARBOL', 'NOMBRE COMUN', 'ESPECIE CIENTIFICA', 'ANIO MEDICION',
                    'DAP CM', 'ALTURA M', 'BIOMASA TOTAL KG', 'CARBONO TOTAL MG', 
                    'CO2 EQUIVALENTE MG', 'ESTADO ARBOL']

df_mostrar = df[columnas_mostrar].copy()
df_mostrar.columns = ['N° Árbol', 'Nombre Común', 'Especie Científica', 'Año',
                      'DAP (cm)', 'Altura (m)', 'Biomasa (kg)', 'Carbono (Mg)',
                      'CO₂e (Mg)', 'Estado']

st.dataframe(df_mostrar, use_container_width=True, height=400)


# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Dashboard de Inventario Arbóreo - Campus Omar Dengo</strong></p>
    <p>Universidad Nacional de Costa Rica (UNA)</p>
    <p>Escuela de Ciencias Ambientales (EDECA)</p>
    <p>Sistema de Monitoreo de Carbono y Biomasa Forestal</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        Desarrollado con 🌳 para la conservación y monitoreo del patrimonio arbóreo institucional
    </p>
    <p style='font-size: 0.8em; color: #999;'>
        Última actualización: {fecha}
    </p>
</div>
""".format(fecha=datetime.now().strftime("%B %Y")), unsafe_allow_html=True)

# Información adicional en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Información del Sistema")
st.sidebar.info("""
**Campus:** Omar Dengo  
**Área:** 18.5 hectáreas  
**Tipo:** Censo general  
**Años monitoreados:** 2018-2025  
**Frecuencia:** Anual
""")

st.sidebar.markdown("### 📚 Metodología")
st.sidebar.markdown("""
- **Ecuaciones alométricas** específicas por especie
- **Factor de expansión** de biomasa
- **Fracción de carbono:** 0.47
- **Factor CO₂:** 3.67
""")

st.sidebar.markdown("### 📞 Contacto")
st.sidebar.markdown("""
**EDECA - UNA**  
Escuela de Ciencias Ambientales  
Campus Omar Dengo  
Heredia, Costa Rica
""")
