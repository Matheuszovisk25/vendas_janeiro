import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas - Janeiro 2025", layout="wide")
st.markdown("# 📊 Relatório Comercial - Janeiro 2025")
st.markdown("### Análise de desempenho por canal de venda")

@st.cache_data
def carregar_dados():
    df = pd.read_excel("dados_vendas_janeiro.xlsx")
    df["TIPO_DE_VENDA"] = df["TIPO_DE_VENDA"].str.strip().str.upper()
    return df

df = carregar_dados()


total_reservas = df.shape[0]
receita_total = df["Valor"].sum()


st.divider()
st.subheader("Indicadores Gerais")
col1, col2 = st.columns(2)
col1.metric("Total de Reservas", f"{total_reservas}")
col2.metric("Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


agrupado = df.groupby("TIPO_DE_VENDA").agg(
    Total_Reservas=("TIPO_DE_VENDA", "count"),
    Receita_Total_Rs=("Valor", "sum")
).reset_index()


st.divider()
st.subheader("Receita por Canal de Venda")

fig = px.bar(
    agrupado.sort_values("Receita_Total_Rs", ascending=False),
    x="TIPO_DE_VENDA",
    y="Receita_Total_Rs",
    title="Receita Total por Canal",
    labels={"TIPO_DE_VENDA": "Canal", "Receita_Total_Rs": "Receita (R$)"},
    text_auto='.2s'
)
fig.update_layout(xaxis_title=None, yaxis_title="Receita (R$)", title_x=0.2)
st.plotly_chart(fig, use_container_width=True)


st.markdown("### Detalhamento por Canal")
st.dataframe(agrupado.sort_values("Receita_Total_Rs", ascending=False), use_container_width=True)

