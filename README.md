# 🐧 Dashboard Interactivo de Pingüinos de Palmer

Dashboard interactivo construido con **Streamlit** y **Plotly** para explorar las características morfológicas de los pingüinos del archipiélago Palmer, Antártida.

## ✨ Funcionalidades

- **Filtros dinámicos** — Selecciona por especie, isla y sexo para explorar los datos a detalle.
- **Visualizaciones interactivas** — Gráficos de dispersión, histogramas, diagramas de caja y violín que responden a tus filtros en tiempo real.
- **Métricas clave** — Promedios de longitud de pico, masa corporal y longitud de aleta actualizados al instante.
- **Tabla de datos** — Vista detallada con formato condicional y descarga en CSV.
- **Diseño responsivo** — Adaptado para verse bien en cualquier pantalla.

## 🗂️ Estructura

```
├── app.py                  # Dashboard principal
├── requirements.txt        # Dependencias para Streamlit Cloud
├── .streamlit/
│   └── config.toml         # Tema y configuración de Streamlit
└── README.md
```

## 🚀 Ejecutar localmente

```bash
git clone <repo>
cd <repo>
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
streamlit run app.py
```

## 📊 Dataset

**Palmer Penguins** — Gorman, Williams & Fraser (2014).  
Disponible en [palmerpenguins](https://github.com/allisonhorst/palmerpenguins).

## 🛠️ Stack

- Python 3.14+
- Streamlit — UI interactiva
- Plotly — Gráficos vectoriales interactivos
- Pandas — Procesamiento de datos
- Matplotlib — Formato condicional en tablas
