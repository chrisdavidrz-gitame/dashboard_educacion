# --- IMPORTACIONES ---
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import base64

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos"
LOGOS_DIR = BASE_DIR / "logos"
STATIC_DIR = BASE_DIR / "static"

# (opcional) helper por si preferís usar función
def data_file(nombre: str) -> Path:
    return DATA_DIR / nombre


# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Secretaría de Educación - Capital Humano",
    layout="wide"
)

# --- FUNCIONES DE CARGA DE CSS Y JS ---
from pathlib import Path
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos"
LOGOS_DIR = BASE_DIR / "logos"
STATIC_DIR = BASE_DIR / "static"

def cargar_css_rel(path_rel: str):
    path = BASE_DIR / path_rel
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def cargar_js_rel(path_rel: str):
    path = BASE_DIR / path_rel
    js = path.read_text(encoding="utf-8")
    components.html(f"<script>{js}</script>", height=0)


# CSS SIEMPRE activo (incluso en pantalla de login)
cargar_css_rel("static/css/styles.css")
cargar_css_rel("static/css/progresar.css")
cargar_css_rel("static/css/botones.css")



# --- CONFIGURACIÓN DE SEGURIDAD Y AUTENTICACIÓN ---
credenciales = {
    "usernames": {
        "admin": {
            "name": "Administrador",
            "password": "$2b$12$6ADzfx7uVjgx.BCyXTBAOOMclBwLW3wbIFetxCn5qogmvrNTXR6pm"  # Educacion2026
        }
    }
}

authenticator = stauth.Authenticate(
    credenciales,
    "auth_cookie_educacion",
    "clave_secreta_123",
    cookie_expiry_days=30
)

# --- LOGIN ---
authenticator.login(location="main")

# --- ESTADO DE AUTENTICACIÓN ---
if st.session_state["authentication_status"] is False:
    st.error("Usuario o contraseña incorrectos")

elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, ingrese sus credenciales para acceder.")

elif st.session_state["authentication_status"]:

  # ==================================================
  # ICONOS PNG PARA BOTONES DEL MENÚ (NO PROGRESAR)
  # ==================================================
    def inject_png_icon_for_button(class_name: str, png_path):
        try:
            with open(png_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            data_uri = f"data:image/png;base64,{b64}"

            st.markdown(
                f"""
                <style>
                button.{class_name}::before {{
                    background-image: url("{data_uri}") !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error cargando ícono {png_path}: {e}")

    # Iconos de botones (NO Progresar)
    inject_png_icon_for_button("btn-menu-vouchers", LOGOS_DIR / "vouchers.png")
    inject_png_icon_for_button("btn-menu-becas", LOGOS_DIR / "becas.png")
    inject_png_icon_for_button("btn-menu-comedores", LOGOS_DIR / "comida.png")
    inject_png_icon_for_button("btn-menu-libros", LOGOS_DIR / "libros.png")


 
    # ------------------------------------------------------------------
    # CARGA DE ICONO PROGRESAR (PNG → base64)
    # ------------------------------------------------------------------
    svg_uri = ""
    try:
        with open(LOGOS_DIR / "escuela.png", "rb") as f:
            png_data = base64.b64encode(f.read()).decode()
        svg_uri = f"data:image/png;base64,{png_data}"
    except Exception as e:
        st.error(f"Error cargando icono Progresar: {e}")

    if svg_uri:
        st.markdown(
            f"""
            <style>
            button.btn-progresar-icon::before {{
                background-image: url("{svg_uri}") !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # ------------------------------------------------------------------
    # HEADER SUPERIOR CON LOGOUT
    # ------------------------------------------------------------------
    top_c1, top_c2, top_c3 = st.columns([7, 1, 1])

    with top_c3:
        st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
        authenticator.logout("Cerrar sesión")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # CARGA DE JAVASCRIPT (logout, chips, botón Progresar)
    # ------------------------------------------------------------------
    cargar_js_rel("static/js/ui.js")

    # ------------------------------------------------------------------
    # FUNCIÓN PARA CAMBIO DE PROGRAMA
    # ------------------------------------------------------------------
    def seleccionar_programa(nombre):
        st.session_state.programa_seleccionado = nombre
        components.html(
            "<script>window.parent.document.getElementById('resultados').scrollIntoView({behavior:'smooth'});</script>",
            height=0,
        )

    # ------------------------------------------------------------------
    # ENCABEZADO
    # ------------------------------------------------------------------
    col_log1, col_log2, col_log3 = st.columns([1, 2, 1])
    with col_log2:
        try:
            st.image(str(LOGOS_DIR / "logo_SE_CH.png"), use_container_width=True)

        except:
            st.markdown(
                "<h2 style='text-align:center;'>Secretaría de Educación</h2>",
                unsafe_allow_html=True
            )

    st.markdown(
        "<h1 style='text-align:center;'>Dirección Nacional de Políticas de Fortalecimiento Educativo</h1>",
        unsafe_allow_html=True
    )
    st.divider()

    # ------------------------------------------------------------------
    # BOTONES DE NAVEGACIÓN
    # ------------------------------------------------------------------
    if "programa_seleccionado" not in st.session_state:
        st.session_state.programa_seleccionado = "General"

    f1_c1, f1_c2, f1_c3, f1_c4 = st.columns(4)

    with f1_c1:
        if st.button("Progresar", key="btn_progresar", use_container_width=True):
            seleccionar_programa("Progresar")

    with f1_c2:
        if st.button("Vouchers\nEducativos", use_container_width=True):
            seleccionar_programa("Vouchers")

    with f1_c3:
        if st.button("Becas\nFortalecimiento", use_container_width=True):
            seleccionar_programa("Becas")

    with f1_c4:
        if st.button("Comedores\nEscolares", use_container_width=True):
            seleccionar_programa("Comedores")

    f2_c1, f2_c2, f2_c3, f2_c4 = st.columns(4)
    with f2_c1:
        if st.button("Libros para\naprender", use_container_width=True):
            seleccionar_programa("Libros")

    st.divider()
    st.markdown("<div id='resultados'></div>", unsafe_allow_html=True)
    st.subheader(f"Visualizando: {st.session_state.programa_seleccionado}")

    # ------------------------------------------------------------------
    # VISUALIZACIONES (LÓGICA ORIGINAL, SIN CAMBIOS)
    # ------------------------------------------------------------------

    # --- COMEDORES ---
    if st.session_state.programa_seleccionado == "Comedores":
        try:
            df_comedores = pd.read_excel(DATA_DIR / "Resumen_rondos_comedores.xlsx")
            df_comedores = df_comedores[df_comedores["Jurisdicción"] != "Totales"]

            st.info("Datos de Comedores Escolares cargados")

            provincias = st.multiselect(
                "Filtrar Provincias:",
                options=df_comedores["Jurisdicción"].unique(),
                default=df_comedores["Jurisdicción"].unique()
            )

            df_filtrado = df_comedores[df_comedores["Jurisdicción"].isin(provincias)]

            m1, m2 = st.columns(2)
            m1.metric("Monto Anual Total", f"$ {df_filtrado['Monto Anual'].sum():,.0f}")
            m2.metric(
                "Promedio de Ejecución",
                f"{df_filtrado['Ejecución Presupuestaria %'].mean():.2f}%"
            )

            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    px.bar(
                        df_filtrado,
                        y="Jurisdicción",
                        x="Monto Anual",
                        orientation="h",
                        title="Inversión por Jurisdicción",
                        color="Monto Anual",
                        color_continuous_scale="Blues"
                    ),
                    width="stretch"
                )

            with c2:
                st.plotly_chart(
                    px.scatter(
                        df_filtrado,
                        x="Ejecución Presupuestaria %",
                        y="Jurisdicción",
                        size="Monto Anual",
                        color="Ejecución Presupuestaria %",
                        color_continuous_scale="RdYlGn"
                    ),
                    width="stretch"
                )

            st.dataframe(
                df_filtrado[
                    [
                        "Jurisdicción",
                        "Organismo provincial responsable",
                        "Monto Anual",
                        "Ejecución Presupuestaria %"
                    ]
                ],
                width="stretch"
            )

        except Exception as e:
            st.error(f"Error en Comedores: {e}")

# Vouchers educativos 

    elif st.session_state.programa_seleccionado == "Vouchers":
        try:
            df_vouchers = pd.read_excel(DATA_DIR / "20251215_VOUCHERS.xlsx", header=1)
            df_vouchers = df_vouchers.dropna(subset=[df_vouchers.columns[0]])
            df_vouchers = df_vouchers[
                ~df_vouchers.iloc[:, 0].str.contains("TOTAL|Total", na=False)
            ]

            for i in [2, 3, 5, 6, 8, 9]:
                df_vouchers.iloc[:, i] = pd.to_numeric(
                    df_vouchers.iloc[:, i], errors="coerce"
                ).fillna(0)

            total_alumnos = df_vouchers.iloc[:, [2, 5, 8]].sum(axis=1)
            total_inversion = df_vouchers.iloc[:, [3, 6, 9]].sum(axis=1)

            v1, v2, v3 = st.columns(3)
            v1.metric("Total Beneficiarios", f"{total_alumnos.sum():,.0f}")
            v2.metric("Inversión Total", f"$ {total_inversion.sum():,.0f}")
            v3.metric("Jurisdicciones", len(df_vouchers))

            c1, c2 = st.columns(2)
            with c1:
                niv_data = pd.DataFrame({
                    "Nivel": ["Inicial", "Primario", "Secundario"],
                    "Inversión": [
                        df_vouchers.iloc[:, 3].sum(),
                        df_vouchers.iloc[:, 6].sum(),
                        df_vouchers.iloc[:, 9].sum()
                    ]
                })
                st.plotly_chart(
                    px.pie(niv_data, values="Inversión", names="Nivel",
                        title="Distribución de Inversión"),
                    width="stretch"
                )

            with c2:
                df_bar = pd.DataFrame({
                    "Jurisdicción": df_vouchers.iloc[:, 0],
                    "Alumnos": total_alumnos
                }).sort_values("Alumnos", ascending=False)

                st.plotly_chart(
                    px.bar(
                        df_bar,
                        x="Jurisdicción",
                        y="Alumnos",
                        color="Alumnos",
                        color_continuous_scale="Blues",
                        title="Alumnos por Jurisdicción"
                    ),
                    width="stretch"
                )

        except Exception as e:
            st.error(f"Error en Vouchers: {e}")

# BECAS DE FORTALECIMIENTO

    elif st.session_state.programa_seleccionado == "Becas":
        try:
            df_becas = pd.read_excel(DATA_DIR / "Becas_Fortaleciemiento.xlsx")
            df_becas.columns = df_becas.columns.str.strip()
            df_becas = df_becas[
                ~df_becas["Jurisdicción"].astype(str).str.contains("TOTAL|Total", na=False)
            ]

            def buscar_col(texto):
                for c in df_becas.columns:
                    if texto in c:
                        return c
                return None

            c_vg = buscar_col("VG")
            c_fondos = buscar_col("Fondos")
            c_becarios = buscar_col("Becarios")

            for c in [c_vg, c_fondos, c_becarios]:
                if c:
                    df_becas[c] = pd.to_numeric(df_becas[c], errors="coerce").fillna(0)

            b1, b2 = st.columns(2)
            b1.metric("Monto Total Fondos", f"$ {df_becas[c_fondos].sum():,.0f}")
            b2.metric("Total Becarios", f"{df_becas[c_becarios].sum():,.0f}")

            opciones = {
                "Becas VG": c_vg,
                "Becas AP": buscar_col("AP"),
                "Becas AI": buscar_col("AI")
            }
            validas = {k: v for k, v in opciones.items() if v}

            sel = st.selectbox("Seleccione línea de beca:", list(validas.keys()))

            st.plotly_chart(
                px.bar(
                    df_becas,
                    x="Jurisdicción",
                    y=validas[sel],
                    color=validas[sel],
                    color_continuous_scale="Viridis"
                ),
                width="stretch"
            )

        except Exception as e:
            st.error(f"Error en Becas: {e}")

# LIBROS PARA APRENDER

    elif st.session_state.programa_seleccionado == "Libros":
        try:
            df_libros = pd.read_excel(DATA_DIR / "Libros_Anexo_III.xlsx")
            df_libros["Cantidad"] = pd.to_numeric(
                df_libros["Cantidad"], errors="coerce"
            ).fillna(0)

            st.info("Distribución Nacional de Libros - Anexo III")

            with st.expander("🔍 Ver Tabla de Datos Completa"):
                st.dataframe(df_libros, width="stretch")

            m1, m2 = st.columns(2)
            m1.metric("Total Ejemplares", f"{df_libros['Cantidad'].sum():,.0f}")
            m2.metric("Editoriales", df_libros["Editorial"].nunique())

            c1, c2 = st.columns(2)
            with c1:
                df_juris = (
                    df_libros.groupby("Jurisdicción")["Cantidad"]
                    .sum()
                    .reset_index()
                    .sort_values("Cantidad", ascending=False)
                )
                st.plotly_chart(
                    px.bar(
                        df_juris,
                        x="Jurisdicción",
                        y="Cantidad",
                        color="Cantidad",
                        color_continuous_scale="Blues",
                        title="Total por Provincia"
                    ),
                    width="stretch"
                )

            with c2:
                df_area = (
                    df_libros.groupby(["Área", "Grado"])["Cantidad"]
                    .sum()
                    .reset_index()
                )
                st.plotly_chart(
                    px.bar(
                        df_area,
                        x="Grado",
                        y="Cantidad",
                        color="Área",
                        barmode="group",
                        title="Libros por Área y Grado"
                    ),
                    width="stretch"
                )

        except Exception as e:
            st.error(f"Error en Libros: {e}")

# PROGRESAR

    elif st.session_state.programa_seleccionado == "Progresar":
        try:
            df_prog = pd.read_excel(DATA_DIR / "Progresar.xlsx", skiprows=1)
            df_prog.columns = [
                "Provincia",
                "Obligatorio_Adj", "Obligatorio_Ins",
                "Superior_Adj", "Superior_Ins",
                "Trabajo_Adj", "Trabajo_Ins"
            ]

            df_total = df_prog[df_prog["Provincia"] == "Total País"].iloc[0]
            df_prov = df_prog[df_prog["Provincia"] != "Total País"].copy()

            for c in df_prov.columns[1:]:
                df_prov[c] = pd.to_numeric(df_prov[c], errors="coerce").fillna(0)

            st.info("Visualizando: Programa Progresar 2025")

            total_adj = df_total[
                ["Obligatorio_Adj", "Superior_Adj", "Trabajo_Adj"]
            ].sum()
            total_ins = df_total[
                ["Obligatorio_Ins", "Superior_Ins", "Trabajo_Ins"]
            ].sum()

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Adjudicados", f"{total_adj:,.0f}")
            m2.metric("Total Inscriptos", f"{total_ins:,.0f}")
            m3.metric("Tasa de Adjudicación", f"{(total_adj / total_ins) * 100:.1f}%")

            c1, c2 = st.columns(2)
            with c1:
                dist = pd.DataFrame({
                    "Línea": ["Obligatorio", "Superior", "Trabajo"],
                    "Adjudicados": [
                        df_total["Obligatorio_Adj"],
                        df_total["Superior_Adj"],
                        df_total["Trabajo_Adj"]
                    ]
                })
                st.plotly_chart(
                    px.pie(dist, values="Adjudicados", names="Línea",
                        title="Distribución por Línea", hole=0.4),
                    width="stretch"
                )

            with c2:
                df_prov["Total_Adj"] = (
                    df_prov["Obligatorio_Adj"] +
                    df_prov["Superior_Adj"] +
                    df_prov["Trabajo_Adj"]
                )
                st.plotly_chart(
                    px.bar(
                        df_prov.sort_values("Total_Adj"),
                        y="Provincia",
                        x="Total_Adj",
                        orientation="h",
                        color="Total_Adj",
                        color_continuous_scale="GnBu",
                        title="Adjudicados por Jurisdicción"
                    ),
                    width="stretch"
                )

            with st.expander("🔍 Ver Detalle por Línea y Provincia"):
                st.dataframe(df_prov, width="stretch")

        except Exception as e:
            st.error(f"Error en Progresar: {e}")




    
    # ------------------------------------------------------------------
    # PIE DE PÁGINA
    # ------------------------------------------------------------------
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; opacity:0.5;'>Sistema de Monitoreo Educativo 2026 - Acceso Restringido</p>",
        unsafe_allow_html=True
    )
