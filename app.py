import streamlit as st
import random

st.set_page_config(page_title="Aprende Matemáticas", page_icon="📚", layout="wide")

# Variables de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'age' not in st.session_state:
    st.session_state.age = None
if 'grade' not in st.session_state:
    st.session_state.grade = None
if 'subject' not in st.session_state:
    st.session_state.subject = "Matemáticas"
if 'progress' not in st.session_state:
    st.session_state.progress = {}
if 'current_level' not in st.session_state:
    st.session_state.current_level = None

# ==================== LOGIN ====================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🚀 Aprende Matemáticas")
        st.subheader("Bienvenido")

        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])

        with tab1:
            username = st.text_input("Usuario", key="login_user")
            password = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Iniciar Sesión"):
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

        with tab2:
            new_user = st.text_input("Elige un usuario", key="reg_user")
            new_pass = st.text_input("Elige una contraseña", type="password", key="reg_pass")
            if st.button("Registrarse"):
                if new_user and new_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = new_user
                    st.rerun()

else:
    # Barra superior
    st.title(f"📚 Aprende Matemáticas - {st.session_state.username}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Grado:** {st.session_state.grade or '—'}")
    with col2:
        st.write(f"**Materia:** {st.session_state.subject}")
    with col3:
        if st.button("🚪 Cerrar Sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.divider()

    # Datos del estudiante (solo la primera vez)
    if not st.session_state.grade:
        st.header("📋 Información del estudiante")
        st.session_state.age = st.number_input("¿Cuántos años tienes?", 8, 13, 10)
        
        st.write("¿En qué grado estás?")
        grade = st.radio("Grado", ["4° de primaria", "5° de primaria", "6° de primaria"], horizontal=True)
        st.session_state.grade = grade
        
        subject = st.radio("¿Qué materia quieres aprender?", ["Matemáticas", "Inglés"], horizontal=True)
        st.session_state.subject = subject
        
        if st.button("Continuar al Mapa de Niveles", type="primary"):
            st.rerun()

    else:
        # Mapa de Niveles
        st.header("🗺️ Mapa de Niveles - Progreso")
        
        secciones = ["Básicos", "Álgebra", "Geometría", "Estadística"]
        
        for i, seccion in enumerate(secciones):
            st.subheader(f"📍 Sección {i+1}: {seccion}")
            cols = st.columns(5)
            for nivel in range(1, 11):
                with cols[(nivel-1) % 5]:
                    nivel_id = f"{seccion}_{nivel}"
                    estrellas = st.session_state.progress.get(nivel_id, 0)
                    
                    desbloqueado = (nivel == 1) or (st.session_state.progress.get(f"{seccion}_{nivel-1}", 0) == 3)
                    
                    if desbloqueado:
                        if st.button(f"Nivel {nivel} {'⭐' * estrellas}", key=nivel_id):
                            st.session_state.current_level = nivel_id
                            st.rerun()
                    else:
                        st.button(f"🔒 Nivel {nivel}", disabled=True)

        # Evaluación del nivel actual
        if st.session_state.current_level:
            st.divider()
            seccion_actual, nivel_actual = st.session_state.current_level.split("_")
            st.header(f"✍️ Nivel {nivel_actual} - {seccion_actual}")
            
            # Preguntas de ejemplo (puedes agregar más)
            preguntas = [
                {"q": "¿Cuánto es 45 + 37?", "o": ["72", "82", "92"], "r": "82"},
                {"q": "Si 3x = 24, ¿cuánto vale x?", "o": ["6", "8", "9"], "r": "8"},
                {"q": "¿Cuál es el área de un rectángulo de 6 x 4?", "o": ["20", "24", "28"], "r": "24"}
            ]
            
            p = random.choice(preguntas)
            st.write(f"**Pregunta:** {p['q']}")
            respuesta = st.radio("Elige una opción:", p["o"], key="resp")
            
            if st.button("Enviar respuesta"):
                if respuesta == p["r"]:
                    st.success("¡Correcto! +1 estrella")
                    current = st.session_state.progress.get(st.session_state.current_level, 0)
                    st.session_state.progress[st.session_state.current_level] = min(3, current + 1)
                else:
                    st.error("Incorrecto. Inténtalo otra vez.")
                st.rerun()
