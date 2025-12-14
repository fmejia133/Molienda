import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

st.title("💰 Calculadora de Nómina con Reportes y Guardado")

st.markdown("""
<style>
/* Aumentar el tamaño de las etiquetas de los inputs (~40%) */
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# Botón para reiniciar sesión
if st.button("🔄 Reiniciar aplicación"):
    st.session_state.clear()
    st.experimental_rerun()

# Crear carpeta para archivos
CARPETA_SALIDA = "nomina_guardada"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

datos_nomina = []
df = pd.DataFrame()

# Ingresos por panela
st.subheader("📈 Ingresos por Panela Vendida")
cargas_vendidas = st.number_input("Número de cargas de panela vendidas", min_value=0, step=1)
precio_por_carga = st.number_input("Precio por carga de panela", min_value=0, step=1000)
ingresos = cargas_vendidas * precio_por_carga
st.markdown(f"### 💵 Ingresos totales: **${ingresos:,.0f}**")

# Tarifas por actividad
st.subheader("💵 Tarifas por Actividad")
pago_molienda = st.number_input("Pago por carga de **panela**", min_value=0, step=500, value=10000)
pago_corte = st.number_input("Pago por carga de **corte**", min_value=0, step=500, value=2000)
pago_jornal_corte = st.number_input("Pago por **jornal de corte**", min_value=0, step=500, value=40000)
pago_cargueria = st.number_input("Pago por **jornal de carguería**", min_value=0, step=500, value=40000)
pago_encarre = st.number_input("Pago por **jornal de encarre**", min_value=0, step=500, value=30000)
pago_molienda_hornero = st.number_input("Pago por carga de **panela hornero**", min_value=0, step=500, value=12000)

# Entrada manual de trabajadores
st.subheader("👷 Lista de Trabajadores")
n_trabajadores = st.number_input("¿Cuántos trabajadores deseas ingresar?", min_value=1, step=1)

for i in range(n_trabajadores):
    st.markdown(f"### Trabajador #{i + 1}")

    nombre = st.text_input("**Nombre del trabajador**", key=f"nombre_{i}")

    molienda = st.number_input("**Cargas de panela**", min_value=0, step=1, key=f"molienda_{i}")

    molienda_hornero = st.number_input("**Cargas de panela hornero**", min_value=0, step=1, key=f"molienda_hornero_{i}")

    corte = st.number_input("**Número de cargas cortadas**", min_value=0, step=1, key=f"corte_{i}")

    jornales_corte = st.number_input("**Jornales de corte**", min_value=0, step=1, key=f"jornales_corte_{i}")

    cargueria = st.number_input("**Jornales de carguería**", min_value=0, step=1, key=f"cargueria_{i}")

    encarre = st.number_input("**Encarre**", min_value=0, step=1, key=f"encarre_{i}")

    nomina_directa = st.number_input("**Nómina directa**", min_value=0, step=1000, key=f"nomina_{i}")

    contratos = st.number_input("**Contratos**", min_value=0, step=1000, key=f"contratos_{i}")

    alimentaciones = st.number_input("**Alimentaciones (+)**", min_value=0, step=1000, key=f"alimentaciones_{i}")

    varios_molienda = st.number_input("**Varios molienda**", min_value=0, step=1000, key=f"varios_molienda_{i}")

    varios = st.number_input("**Varios**", min_value=0, step=1000, key=f"varios_{i}")

    pago_bodega = st.number_input("**Pago bodega**", min_value=0, step=1000, key=f"bodega_{i}")

    alimentacion_descuento = st.number_input("**Alimentación (-)**", min_value=0, step=1000, key=f"desc_alimentacion_{i}")

    prestamo = st.number_input("**Préstamo**", min_value=0, step=1000, key=f"prestamo_{i}")

    anticipo = st.number_input("**Anticipo**", min_value=0, step=1000, key=f"anticipo_{i}")

    concepto_adhoc_nombre = st.text_input("**Concepto adicional (opcional)**", key=f"adhoc_nombre_{i}")

    concepto_adhoc_valor = st.number_input("**Valor del concepto adicional**", step=1000, key=f"adhoc_valor_{i}")


    if nombre:
        conceptos = {
            "Trabajador": nombre,
            "Cargas de panela": molienda * pago_molienda,
            "Cargas de panela hornero": molienda_hornero * pago_molienda_hornero,
            "Corte": corte * pago_corte,
            "Jornales de Corte": jornales_corte * pago_jornal_corte,
            "Carguería": cargueria * pago_cargueria,
            "Encarre": encarre * pago_encarre,
            "Nómina Directa": nomina_directa,
            "Contratos": contratos,
            "Alimentaciones (+)": alimentaciones,
            "Varios Molienda": varios_molienda,
            "Varios": varios,
            "Pago Bodega": pago_bodega,
            concepto_adhoc_nombre or "Concepto Adicional": concepto_adhoc_valor,
            "Alimentación (-)": -alimentacion_descuento,
            "Préstamo": -prestamo,
            "Anticipo": -anticipo,
        }
        conceptos["Total a Pagar"] = sum(conceptos[c] for c in conceptos if c != "Trabajador")
        datos_nomina.append(conceptos)
df = pd.DataFrame(datos_nomina)

# Mostrar resumen si hay datos válidos
if not df.empty:
    st.subheader("📊 Resumen de Nómina")
    numeric_cols = df.select_dtypes(include='number').columns
    st.dataframe(df.style.format({col: "${:,.0f}" for col in numeric_cols}))

    st.markdown(f"### 🧾 Total General a Pagar: **${df['Total a Pagar'].sum():,.0f}**")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar Nómina en CSV", data=csv, file_name="nomina_completa.csv", mime="text/csv")

    if st.button("💾 Guardar Nómina en Carpeta Local"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(CARPETA_SALIDA, f"nomina_{timestamp}.csv")
        df.to_csv(filename, index=False)
        st.success(f"✅ Nómina guardada en {filename}")

    if st.button("🖨️ Exportar Reporte por Trabajador a PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=14)

        for idx, row in df.iterrows():
            if idx % 3 == 0:
                pdf.add_page()
            pdf.set_font("Arial", "B", size=14)
            pdf.cell(0, 10, f"Trabajador: {row['Trabajador']}", ln=True)
            pdf.set_font("Arial", size=14)
            for col, val in row.items():
                # Saltar la columna de nombre
                if col == "Trabajador":
                    continue

                # Saltar valores NaN o vacíos
                if pd.isna(val):
                    continue

                # Saltar conceptos en cero
                if val == 0:
                    continue

                pdf.cell(0, 10, f"- {col}: ${val:,.0f}", ln=True)

            pdf.ln(5)

        path_pdf = os.path.join(CARPETA_SALIDA, "reporte_trabajadores.pdf")
        pdf.output(path_pdf)
        st.success(f"📄 PDF generado exitosamente: {path_pdf}")
else:
    st.info("Completa la información para generar la nómina.")


