import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="DataMorph JSON", layout="wide")

st.title("🔄 DataMorph JSON")
st.write("Convierte listas de objetos JSON en tablas usando **pandas.json_normalize**")

# JSON de ejemplo
json_ejemplo = """
[
  {
    "id": 1,
    "nombre": "Ana",
    "edad": 29,
    "ciudad": "Madrid"
  },
  {
    "id": 2,
    "nombre": "Luis",
    "email": "luis@email.com",
    "activo": true
  },
  {
    "id": 3,
    "nombre": "María",
    "edad": 35,
    "hobbies": ["lectura", "viajes"],
    "direccion": {
      "ciudad": "Barcelona",
      "pais": "España"
    }
  }
]
"""

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 JSON de entrada")
    json_input = st.text_area(
        "Pega aquí una lista de objetos JSON:",
        value=json_ejemplo,
        height=400
    )

with col2:
    st.subheader("📊 Tabla normalizada")

    try:
        # Intentar parsear el JSON
        data = json.loads(json_input)

        if not isinstance(data, list):
            st.error("❌ El JSON debe ser una lista de objetos (array de diccionarios).")
        else:
            df = pd.json_normalize(data)
            st.dataframe(df, use_container_width=True)

            # -------------------------
            # 🔎 ANÁLISIS DE ESQUEMA
            # -------------------------
            st.subheader("🧬 Análisis automático del esquema")

            columnas = df.columns.tolist()
            nulos_por_columna = df.isna().sum()
            nulos_totales = int(nulos_por_columna.sum())

            st.markdown("**Columnas detectadas:**")
            st.write(columnas)

            st.markdown("**Valores nulos por columna:**")
            st.dataframe(
                nulos_por_columna
                .reset_index()
                .rename(columns={"index": "Columna", 0: "Nulos"}),
                use_container_width=True
            )

            st.markdown(f"**Total de valores nulos:** `{nulos_totales}`")

            if nulos_totales > 0:
                st.warning(
                    "⚠️ Se detectaron valores nulos. "
                    "En **bases de datos SQL**, esto suele indicar un esquema rígido "
                    "mal diseñado o exceso de columnas opcionales. "
                    "En **NoSQL**, este patrón es normal y se conoce como "
                    "**datos dispersos (Sparse Data)**."
                )

    except json.JSONDecodeError:
        st.error(
            "❌ El JSON está mal escrito.\n\n"
            "👉 Revisa comas, llaves `{}`, corchetes `[]` y comillas dobles."
        )
    except Exception as e:
        st.error("❌ Ocurrió un error inesperado al procesar el JSON.")
        st.code(str(e))

# -------------------------
# 📚 EXPLICACIÓN CONCEPTUAL
# -------------------------
with st.expander("📘 Esquema Fijo (SQL) vs Esquema Flexible (NoSQL)"):
    st.markdown("""
**🔒 Esquema Fijo (SQL)**  
- La estructura de la tabla se define **antes** de insertar datos  
- Todas las filas deben cumplir el mismo esquema  
- Los valores nulos suelen indicar:
  - Columnas innecesarias
  - Problemas de normalización
- Ideal para datos **estructurados y consistentes**

**🔓 Esquema Flexible (NoSQL)**  
- Cada documento puede tener **campos distintos**
- No es obligatorio definir un esquema previo
- Los valores nulos o campos ausentes son normales
- Ideal para:
  - APIs
  - Eventos
  - Datos semi-estructurados
  - Evolución rápida del modelo

👉 Esta app muestra cómo un dataset NoSQL se “fuerza” a un formato tabular, revelando
los compromisos entre ambos enfoques.
""")
