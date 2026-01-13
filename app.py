import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Secretaría de Educación - Capital Humano", layout="wide")

# --- 2. CONFIGURACIÓN DE SEGURIDAD ---
credenciales = {
    "usernames": {
        "admin": {
            "name": "Administrador",
            "password": "$2b$12$6ADzfx7uVjgx.BCyXTBAOOMclBwLW3wbIFetxCn5qogmvrNTXR6pm" # Educacion2026
        }
    }
}

authenticator = stauth.Authenticate(
    credenciales,
    "auth_cookie_educacion", 
    "clave_secreta_123",      
    cookie_expiry_days=30
)

# Renderizar Login
authenticator.login(location='main')

if st.session_state["authentication_status"] is False:
    st.error('Usuario o contraseña incorrectos')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, ingrese sus credenciales para acceder.')
elif st.session_state["authentication_status"]:
    
    # --- INTERFAZ DEL DASHBOARD ---

    # --- HEADER SUPERIOR ---
    top_c1, top_c2, top_c3 = st.columns([8, 1, 2])


    with top_c3:
        st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
        authenticator.logout("Cerrar sesión")
        st.markdown('</div>', unsafe_allow_html=True)

    
    # Estilo CSS
    st.markdown("""
        <style>
        html { scroll-behavior: smooth; }
        .stApp { background-color: #232D4F; color: white; }
        div.stButton > button {
            background-color: #45658D; color: white; border-radius: 15px;
            height: 140px; font-size: 24px !important; font-weight: bold;
            border: 2px solid #3d3dcf; transition: all 0.3s ease;
            margin-bottom: 10px; white-space: pre-wrap;
        }
        div.stButton > button:hover { background-color: #3d3dcf; border-color: #ffffff; transform: scale(1.02); }
        [data-testid="stMetricValue"] { color: #00ffcc; font-size: 40px; }
        h1, h2, h3, p { color: white !important; }
                
                /* Sidebar completa */
        section[data-testid="stSidebar"] {
            background-color: #232D4F;
        }

        /* Contenido interno de la sidebar */
        section[data-testid="stSidebar"] > div {
            background-color: #232D4F;
            color: white;
        }

                /* Botón logout superior derecho */
        button[kind="secondary"] {
            background-color: transparent;
            color: #ffffff;

            border-radius: 22px;
            border: 1px solid #5f7db0;

            /* 🔹 FORZAR HORIZONTAL */
            height: auto;
            min-height: unset;
            min-width: 190px;
            padding: 0.3em 2.6em;

            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.6px;

            white-space: nowrap;       /* 👈 una sola línea */
            text-align: center;
        }

        /* Hover suave */
        button[kind="secondary"]:hover {
            background-color: rgba(255, 255, 255, 0.08);
            border-color: #ffffff;
        }

        .logout-wrap button {
            background-color: transparent !important;
            border: 1px solid #5f7db0 !important;
            border-radius: 22px !important;

            min-width: 190px !important;     /* más largo */
            width: 190px !important;         /* fija el ancho para que no parta */
            padding: 0.3em 1.6em !important;

            font-size: 12px !important;
            font-weight: 500 !important;
        }

        /* el texto del botón, una sola línea */
        .logout-wrap button * {
            white-space: nowrap !important;

        </style>
    """, unsafe_allow_html=True)

    def seleccionar_programa(nombre):
        st.session_state.programa_seleccionado = nombre
        components.html(
            f"<script>window.parent.document.getElementById('resultados').scrollIntoView({{behavior: 'smooth'}});</script>",
            height=0,
        )

    

    # Encabezado con Logo
    col_log1, col_log2, col_log3 = st.columns([1, 2, 1])
    with col_log2: 
        try:
            st.image("logo_SE_CH.png", use_container_width=True)
        except:
            st.markdown("<h2 style='text-align: center;'>Secretaría de Educación</h2>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Dirección Nacional de Políticas de Fortalecimiento Educativo</h1>", unsafe_allow_html=True)
    st.divider()

    # Botones de Navegación
    if "programa_seleccionado" not in st.session_state:
        st.session_state.programa_seleccionado = "General"

    f1_c1, f1_c2, f1_c3, f1_c4 = st.columns(4)
    with f1_c1:
        if st.button("🎓\nProgresar", use_container_width=True): seleccionar_programa("Progresar")
    with f1_c2:
        if st.button("🎫\nVouchers\nEducativos", use_container_width=True): seleccionar_programa("Vouchers")
    with f1_c3:
        if st.button("🤝\nBecas\nFortalecimiento", use_container_width=True): seleccionar_programa("Becas")
    with f1_c4:
        if st.button("🍎\nComedores\nEscolares", use_container_width=True): seleccionar_programa("Comedores")
    
    f2_c1, f2_c2, f2_c3, f2_c4 = st.columns(4)
    with f2_c1:
        if st.button("📖\nLibros para\naprender", use_container_width=True): seleccionar_programa("Libros")

    st.divider()
    st.markdown("<div id='resultados'></div>", unsafe_allow_html=True)
    st.subheader(f"Visualizando: {st.session_state.programa_seleccionado}")

    # --- LÓGICA DE VISUALIZACIÓN ---

    # 1. COMEDORES
    if st.session_state.programa_seleccionado == "Comedores":
        try:
            df_comedores = pd.read_excel("Resumen_rondos_comedores.xlsx")
            df_comedores = df_comedores[df_comedores['Jurisdicción'] != 'Totales']
            st.info("Datos de Comedores Escolares cargados")
            provincias = st.multiselect("Filtrar Provincias:", options=df_comedores['Jurisdicción'].unique(), default=df_comedores['Jurisdicción'].unique())
            df_filtrado = df_comedores[df_comedores['Jurisdicción'].isin(provincias)]
            m1, m2 = st.columns(2)
            m1.metric("Monto Anual Total", f"$ {df_filtrado['Monto Anual'].sum():,.0f}")
            m2.metric("Promedio de Ejecución", f"{df_filtrado['Ejecución Presupuestaria %'].mean():.2f}%")
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.plotly_chart(px.bar(df_filtrado, y='Jurisdicción', x='Monto Anual', orientation='h', title="Inversión por Jurisdicción", color='Monto Anual', color_continuous_scale='Blues'), use_container_width=True)
            with col_g2:
                st.plotly_chart(px.scatter(df_filtrado, x='Ejecución Presupuestaria %', y='Jurisdicción', size='Monto Anual', color='Ejecución Presupuestaria %', color_continuous_scale='RdYlGn'), use_container_width=True)
            st.dataframe(df_filtrado[['Jurisdicción', 'Organismo provincial responsable', 'Monto Anual', 'Ejecución Presupuestaria %']], use_container_width=True)
        except Exception as e: st.error(f"Error en Comedores: {e}")

    # 2. VOUCHERS
    elif st.session_state.programa_seleccionado == "Vouchers":
        try:
            df_vouchers = pd.read_excel("20251215_VOUCHERS.xlsx", header=1)
            df_vouchers = df_vouchers.dropna(subset=[df_vouchers.columns[0]])
            df_vouchers = df_vouchers[df_vouchers.iloc[:, 0].str.contains("TOTAL|Total") == False]
            for i in [2, 3, 5, 6, 8, 9]:
                df_vouchers.iloc[:, i] = pd.to_numeric(df_vouchers.iloc[:, i], errors='coerce').fillna(0)
            total_alumnos = df_vouchers.iloc[:, [2, 5, 8]].sum(axis=1)
            total_inversion = df_vouchers.iloc[:, [3, 6, 9]].sum(axis=1)
            v1, v2, v3 = st.columns(3)
            v1.metric("Total Beneficiarios", f"{total_alumnos.sum():,.0f}")
            v2.metric("Inversión Total", f"$ {total_inversion.sum():,.0f}")
            v3.metric("Jurisdicciones", len(df_vouchers))
            cv1, cv2 = st.columns(2)
            with cv1:
                niv_data = pd.DataFrame({'Nivel': ['Inicial', 'Primario', 'Secundario'], 'Inversión': [df_vouchers.iloc[:, 3].sum(), df_vouchers.iloc[:, 6].sum(), df_vouchers.iloc[:, 9].sum()]})
                st.plotly_chart(px.pie(niv_data, values='Inversión', names='Nivel', title="Distribución de Inversión"), use_container_width=True)
            with cv2:
                df_bar = pd.DataFrame({'Jurisdicción': df_vouchers.iloc[:, 0], 'Alumnos': total_alumnos}).sort_values('Alumnos', ascending=False)
                st.plotly_chart(px.bar(df_bar, x='Jurisdicción', y='Alumnos', color='Alumnos', color_continuous_scale='Blues', title="Alumnos por Jurisdicción"), use_container_width=True)
        except Exception as e: st.error(f"Error en Vouchers: {e}")

    # 3. BECAS
    elif st.session_state.programa_seleccionado == "Becas":
        try:
            df_becas = pd.read_excel("Becas_Fortaleciemiento.xlsx")
            df_becas.columns = df_becas.columns.str.strip()
            df_becas = df_becas[df_becas['Jurisdicción'].astype(str).str.contains("TOTAL|Total") == False]
            def buscar_col(texto):
                for c in df_becas.columns:
                    if texto in c: return c
                return None
            c_vg, c_fondos, c_becarios = buscar_col("VG"), buscar_col("Fondos"), buscar_col("Becarios")
            if c_vg and c_fondos:
                for c in [c_vg, c_fondos, c_becarios]:
                    df_becas[c] = pd.to_numeric(df_becas[c], errors='coerce').fillna(0)
                b1, b2 = st.columns(2)
                b1.metric("Monto Total Fondos", f"$ {df_becas[c_fondos].sum():,.0f}")
                b2.metric("Total Becarios", f"{df_becas[c_becarios].sum():,.0f}")
                opciones = {"Becas VG": c_vg, "Becas AP": buscar_col("AP"), "Becas AI": buscar_col("AI")}
                validas = {k: v for k, v in opciones.items() if v is not None}
                sel = st.selectbox("Seleccione línea de beca:", list(validas.keys()))
                st.plotly_chart(px.bar(df_becas, x='Jurisdicción', y=validas[sel], color=validas[sel], color_continuous_scale='Viridis'), use_container_width=True)
        except Exception as e: st.error(f"Error en Becas: {e}")

    # 4. LIBROS
    elif st.session_state.programa_seleccionado == "Libros":
        try:
            df_libros = pd.read_excel("Libros_Anexo_III.xlsx")
            df_libros['Cantidad'] = pd.to_numeric(df_libros['Cantidad'], errors='coerce').fillna(0)
            st.info("Distribución Nacional de Libros - Anexo III")
            with st.expander("🔍 Ver Tabla de Datos Completa"):
                st.dataframe(df_libros, use_container_width=True)
            m1, m2 = st.columns(2)
            m1.metric("Total Ejemplares", f"{df_libros['Cantidad'].sum():,.0f}")
            m2.metric("Editoriales", df_libros['Editorial'].nunique())
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                df_juris = df_libros.groupby('Jurisdicción')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=False)
                st.plotly_chart(px.bar(df_juris, x='Jurisdicción', y='Cantidad', color='Cantidad', color_continuous_scale='Blues', title="Total por Provincia"), use_container_width=True)
            with col_l2:
                df_area = df_libros.groupby(['Área', 'Grado'])['Cantidad'].sum().reset_index()
                st.plotly_chart(px.bar(df_area, x='Grado', y='Cantidad', color='Área', barmode='group', title="Libros por Área y Grado"), use_container_width=True)
        except Exception as e: st.error(f"Error en Libros: {e}")

    # 5. PROGRESAR
    elif st.session_state.programa_seleccionado == "Progresar":
        try:
            # Leemos Progresar.xlsx saltando la primera fila de cabecera combinada
            df_prog = pd.read_excel("Progresar.xlsx", skiprows=1)
            df_prog.columns = ['Provincia', 'Obligatorio_Adj', 'Obligatorio_Ins', 'Superior_Adj', 'Superior_Ins', 'Trabajo_Adj', 'Trabajo_Ins']
            
            # Limpieza
            df_total = df_prog[df_prog['Provincia'] == 'Total País'].iloc[0]
            df_prov = df_prog[df_prog['Provincia'] != 'Total País'].copy()
            for col in df_prov.columns[1:]:
                df_prov[col] = pd.to_numeric(df_prov[col], errors='coerce').fillna(0)

            st.info("Visualizando: Programa Progresar 2024")
            
            # Métricas
            total_adj = df_total[['Obligatorio_Adj', 'Superior_Adj', 'Trabajo_Adj']].astype(float).sum()
            total_ins = df_total[['Obligatorio_Ins', 'Superior_Ins', 'Trabajo_Ins']].astype(float).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Adjudicados", f"{total_adj:,.0f}")
            m2.metric("Total Inscriptos", f"{total_ins:,.0f}")
            m3.metric("Tasa de Adjudicación", f"{(total_adj/total_ins)*100:.1f}%")

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                dist_lineas = pd.DataFrame({'Línea': ['Obligatorio', 'Superior', 'Trabajo'], 'Adjudicados': [df_total['Obligatorio_Adj'], df_total['Superior_Adj'], df_total['Trabajo_Adj']]})
                st.plotly_chart(px.pie(dist_lineas, values='Adjudicados', names='Línea', title="Distribución por Línea", hole=0.4), use_container_width=True)
            with col_p2:
                df_prov['Total_Adj'] = df_prov['Obligatorio_Adj'] + df_prov['Superior_Adj'] + df_prov['Trabajo_Adj']
                st.plotly_chart(px.bar(df_prov.sort_values('Total_Adj'), y='Provincia', x='Total_Adj', orientation='h', title="Adjudicados por Jurisdicción", color='Total_Adj', color_continuous_scale='GnBu'), use_container_width=True)

            with st.expander("🔍 Ver Detalle por Línea y Provincia"):
                st.dataframe(df_prov, use_container_width=True)
        except Exception as e: st.error(f"Error en Progresar: {e}")

    # Pie de página
    st.markdown("---")
    st.markdown("<p style='text-align: center; opacity: 0.5;'>Sistema de Monitoreo Educativo 2026 - Acceso Restringido</p>", unsafe_allow_html=True)