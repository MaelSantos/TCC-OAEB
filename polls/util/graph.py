import plotly.express as px


class Graph:

    def get_context_data(self, df):
        fig = px.bar(df, x="Data", y="Quantidade", color="Valor Disponibilizado (R$)", barmode="group",
                     text="Quantidade")
        fig.update_traces(textposition='outside')
        return fig.to_html()

    def format_valor(self, x):
        if x == "Nenhum registro encontrado":
            return x

        if str(x).find(",") is not -1:
            valor = float(str(x).replace(".", "").replace(",", "."))
        else:
            valor = float(x) / 100

        if valor < 600:
            return "< 600"
        elif valor == 600:
            return "= 600"
        elif 600 < valor < 1200:
            return "> 600 e < 1200"
        elif valor == 1200:
            return "= 1200"
        elif valor > 1200:
            return "> 1200"
        else:
            return "Outro"
