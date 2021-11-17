import plotly.offline as opy
import plotly.graph_objs as go
import plotly.express as px


class Graph:

    def get_context_data(self, df):
        fig = px.bar(df, x="Valor Disponibilizado (R$)", y="Quantidade")
        return fig.to_html()
