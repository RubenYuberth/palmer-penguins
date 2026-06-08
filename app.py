from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Configuration ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Pingüinos de Palmer",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Main header ── */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #073042 45%, #0B5E6B 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .main-header h1 {
        color: #F8FAFC;
        font-weight: 700;
        font-size: 2.4rem;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: rgba(248,250,252,0.7);
        font-size: 1.1rem;
        margin: 0;
    }
    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: border-color .2s, box-shadow .2s;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #0891B2;
        box-shadow: 0 4px 12px rgba(8,145,178,0.12);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
    }
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0F172A;
    }
    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #F1F5F9;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        font-weight: 500;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    /* ── Sidebar ── */
    .stSidebar {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    .stSidebar [data-testid="stMarkdownContainer"] h1 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
    }
    section[data-testid="stSidebar"] {
        padding-top: 1.5rem;
    }
    /* ── Expander ── */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
    }
    /* ── Chart containers ── */
    .chart-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem 1rem 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.82rem;
        padding: 1.5rem 0 0.5rem;
    }
    .footer a {
        color: #0891B2;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    /* ── Remove extra spacing ── */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    #MainMenu { visibility: hidden; }
    footer { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ──────────────────────────────────────────────────────
URL_DATASET = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"

@st.cache_data
def cargar_datos() -> pd.DataFrame:
    df = pd.read_csv(URL_DATASET)
    df = df.dropna().rename(columns={
        "species": "especie",
        "island": "isla",
        "bill_length_mm": "longitud_pico_mm",
        "bill_depth_mm": "profundidad_pico_mm",
        "flipper_length_mm": "longitud_aleta_mm",
        "body_mass_g": "masa_corporal_g",
        "sex": "sexo",
    })
    df = df.assign(
        especie=df["especie"].str.capitalize(),
        isla=df["isla"].str.capitalize(),
        sexo=df["sexo"].str.capitalize(),
    )
    return df

df = cargar_datos()

# ─── Color Palette ─────────────────────────────────────────────────────
COLORS = {
    "Adelie": "#E8614B",
    "Chinstrap": "#4A8DB7",
    "Gentoo": "#3AA57C",
    "Torgersen": "#E9C46A",
    "Biscoe": "#9B5DE5",
    "Dream": "#F15BB5",
    "Male":   "#4361EE",
    "Female": "#F72585",
}

# ─── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🐧 Filtros")
    st.markdown("---")

    especies = st.multiselect(
        "**Especie**",
        options=sorted(df["especie"].unique()),
        default=sorted(df["especie"].unique()),
    )

    islas = st.multiselect(
        "**Isla**",
        options=sorted(df["isla"].unique()),
        default=sorted(df["isla"].unique()),
    )

    sexos = st.multiselect(
        "**Sexo**",
        options=sorted(df["sexo"].unique()),
        default=sorted(df["sexo"].unique()),
    )

    st.markdown("---")

    mask = (
        df["especie"].isin(especies)
        & df["isla"].isin(islas)
        & df["sexo"].isin(sexos)
    )
    n_filtrados = mask.sum()
    n_total = len(df)

    st.metric("Pingüinos seleccionados", f"{n_filtrados} / {n_total}")

    if n_filtrados == 0:
        st.warning("No hay datos con estos filtros. Ajústalos.")

    with st.popover("ℹ️ Acerca de"):
        st.markdown("""
        **Palmer Penguins**

        Dataset de pingüinos recolectados en el archipiélago Palmer, Antártida.

        - **Especies:** Adelie, Chinstrap, Gentoo
        - **Islas:** Torgersen, Biscoe, Dream
        - **Variables:** pico, aleta, masa corporal

        *Gorman, Williams & Fraser (2014)*
        """)

    st.markdown("---")
    st.markdown(
        "<small style='color:#94A3B8'>🐧 **Palmer Penguins**<br>Gorman, Williams & Fraser (2014)</small>",
        unsafe_allow_html=True,
    )

# ─── Filter ────────────────────────────────────────────────────────────
df_filtrado = df[mask]

# ─── Header ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🐧 Pingüinos de Palmer</h1>
        <p>
            Explora las características morfológicas de las tres especies de pingüinos
            que habitan en el archipiélago Palmer, Antártida
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Key Metrics ───────────────────────────────────────────────────────
if n_filtrados == 0:
    st.info("Ajusta los filtros en la barra lateral para visualizar los datos.")
    st.stop()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Pingüinos registrados", n_filtrados)
with kpi2:
    st.metric(
        "Pico (longitud promedio)",
        f"{df_filtrado['longitud_pico_mm'].mean():.1f} mm",
    )
with kpi3:
    st.metric(
        "Masa corporal promedio",
        f"{df_filtrado['masa_corporal_g'].mean():.0f} g",
    )
with kpi4:
    st.metric(
        "Aleta (longitud promedio)",
        f"{df_filtrado['longitud_aleta_mm'].mean():.1f} mm",
    )

# ─── Tabs ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visión General",
    "🪶 Características del Pico",
    "📏 Aleta y Masa Corporal",
    "📋 Datos Completos",
])

########################################################################
# TAB 1 — Visión General
########################################################################
with tab1:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        fig_scatter = px.scatter(
            df_filtrado,
            x="longitud_pico_mm",
            y="profundidad_pico_mm",
            color="especie",
            symbol="sexo",
            size="masa_corporal_g",
            size_max=18,
            color_discrete_map=COLORS,
            hover_data={"isla": True, "masa_corporal_g": ":,.0f"},
            labels={
                "longitud_pico_mm": "Longitud del pico (mm)",
                "profundidad_pico_mm": "Profundidad del pico (mm)",
                "especie": "Especie",
                "sexo": "Sexo",
                "masa_corporal_g": "Masa corporal (g)",
            },
        )
        fig_scatter.update_traces(
            marker=dict(line=dict(width=0.8, color="white")),
            selector=dict(type="scatter"),
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="closest",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Longitud vs Profundidad del Pico**")
        st.plotly_chart(fig_scatter, width='stretch', config={"displayModeBar": False})

    with col_b:
        fig_hist = px.histogram(
            df_filtrado,
            x="masa_corporal_g",
            color="isla",
            marginal="box",
            barmode="overlay",
            opacity=0.6,
            color_discrete_map=COLORS,
            nbins=30,
            labels={
                "masa_corporal_g": "Masa corporal (g)",
                "isla": "Isla",
                "count": "Frecuencia",
            },
        )
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Distribución de la Masa Corporal**")
        st.plotly_chart(fig_hist, width='stretch', config={"displayModeBar": False})

########################################################################
# TAB 2 — Características del Pico
########################################################################
with tab2:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        fig_box_len = px.box(
            df_filtrado,
            x="especie",
            y="longitud_pico_mm",
            color="sexo",
            color_discrete_map=COLORS,
            notched=True,
            points="suspectedoutliers",
            labels={
                "especie": "Especie",
                "longitud_pico_mm": "Longitud del pico (mm)",
                "sexo": "Sexo",
            },
        )
        fig_box_len.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Longitud del Pico por Especie y Sexo**")
        st.plotly_chart(fig_box_len, width='stretch', config={"displayModeBar": False})

    with col_b:
        fig_box_depth = px.box(
            df_filtrado,
            x="especie",
            y="profundidad_pico_mm",
            color="sexo",
            color_discrete_map=COLORS,
            notched=True,
            points="suspectedoutliers",
            labels={
                "especie": "Especie",
                "profundidad_pico_mm": "Profundidad del pico (mm)",
                "sexo": "Sexo",
            },
        )
        fig_box_depth.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Profundidad del Pico por Especie y Sexo**")
        st.plotly_chart(fig_box_depth, width='stretch', config={"displayModeBar": False})

########################################################################
# TAB 3 — Aleta y Masa Corporal
########################################################################
with tab3:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        fig_violin = px.violin(
            df_filtrado,
            x="especie",
            y="longitud_aleta_mm",
            color="sexo",
            color_discrete_map=COLORS,
            box=True,
            points="suspectedoutliers",
            labels={
                "especie": "Especie",
                "longitud_aleta_mm": "Longitud de la aleta (mm)",
                "sexo": "Sexo",
            },
        )
        fig_violin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Longitud de la Aleta**")
        st.plotly_chart(fig_violin, width='stretch', config={"displayModeBar": False})

    with col_b:
        fig_mass = px.scatter(
            df_filtrado,
            x="masa_corporal_g",
            y="longitud_aleta_mm",
            color="especie",
            symbol="sexo",
            size="longitud_pico_mm",
            size_max=15,
            color_discrete_map=COLORS,
            hover_data={"isla": True},
            labels={
                "masa_corporal_g": "Masa corporal (g)",
                "longitud_aleta_mm": "Longitud de la aleta (mm)",
                "especie": "Especie",
                "sexo": "Sexo",
                "longitud_pico_mm": "Longitud del pico (mm)",
            },
        )
        fig_mass.update_traces(
            marker=dict(line=dict(width=0.8, color="white")),
            selector=dict(type="scatter"),
        )
        fig_mass.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="closest",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11),
            ),
            margin=dict(t=75, b=10),
            xaxis=dict(gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(gridcolor="#E2E8F0", zeroline=False),
        )
        st.markdown("**Masa Corporal vs Longitud de Aleta**")
        st.plotly_chart(fig_mass, width='stretch', config={"displayModeBar": False})

########################################################################
# TAB 4 — Datos Completos
########################################################################
with tab4:
    st.markdown("### Datos filtrados")

    st.dataframe(
        df_filtrado,
        width='stretch',
        hide_index=True,
        column_order=["especie", "isla", "sexo", "longitud_pico_mm", "profundidad_pico_mm", "longitud_aleta_mm", "masa_corporal_g"],
        column_config={
            "especie": "Especie",
            "isla": "Isla",
            "sexo": "Sexo",
            "longitud_pico_mm": st.column_config.NumberColumn("Pico (mm)", format="%.1f"),
            "profundidad_pico_mm": st.column_config.NumberColumn("Prof. pico (mm)", format="%.1f"),
            "longitud_aleta_mm": st.column_config.NumberColumn("Aleta (mm)", format="%.1f"),
            "masa_corporal_g": st.column_config.NumberColumn("Masa (g)", format="%d"),
        },
    )

    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="pingüinos_palmer_filtrados.csv",
        mime="text/csv",
        use_container_width=False,
    )

# ─── Footer ────────────────────────────────────────────────────────────
st.markdown("""<div class="footer">
    <b>Palmer Penguins</b> — Gorman, Williams &amp; Fraser (2014) ·
    Construido con 🐍 Streamlit + Plotly ·
    <a href="https://github.com/allisonhorst/palmerpenguins">Dataset original</a>
</div>""", unsafe_allow_html=True)
