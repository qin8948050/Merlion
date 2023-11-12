#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dash_table, dcc
from merlion.dashboard.settings import *


def data_table(df, n=1000, page_size=10):
    if df is not None:
        df = df.head(n)
        columns = [{"name": "Index", "id": "Index"}] + [{"name": c, "id": c} for c in df.columns]
        data = []
        for i in range(df.shape[0]):
            d = {c: v for c, v in zip(df.columns, df.values[i])}
            d.update({"Index": df.index[i]})
            data.append(d)

        table = dash_table.DataTable(
            id="table",
            columns=columns,
            data=data,
            style_cell_conditional=[{"textAlign": "center"}],
            style_table={"overflowX": "scroll"},
            editable=False,
            column_selectable="single",
            page_action="native",
            page_size=page_size,
            page_current=0,
            style_header=dict(backgroundColor=TABLE_HEADER_COLOR),
            style_data=dict(backgroundColor=TABLE_DATA_COLOR),
        )
        return table
    else:
        return dash_table.DataTable()


def plot_timeseries(ts,figure_height=500):
    traces = []
    color_list = plotly.colors.qualitative.Dark24

    for i, col in enumerate(ts.columns):
        v = ts[col]
        if v.dtype in ["int", "float", "bool"]:
            v = v.astype(float)
            color = color_list[i % len(color_list)]
            traces.append(go.Scatter(name=col, x=v.index, y=v.values.flatten(), mode="lines", line=dict(color=color)))
            #异常子序列
            # x0_index = v.index.get_loc("2014-04-16 03:24:00")
            # x1_index = v.index.get_loc("2014-04-16 14:19:00")
            # traces.append(go.Scatter(name="anomaly", x=v.index[x0_index:x1_index+7], y=v.values[x0_index:x1_index].flatten(), mode="lines", line=dict(color="rgba(255, 0, 0, 0.8)")))
    layout = dict(
        # showlegend=True,
        xaxis=dict(
            title="",
            type="date",
            showline=True,
            showticklabels=False,
            title_standoff=10,
            side="bottom",
            # rangeselector=dict(
            #     buttons=list(
            #         [
            #             dict(count=7, label="1w", step="day", stepmode="backward"),
            #             dict(count=1, label="1m", step="month", stepmode="backward"),
            #             dict(count=6, label="6m", step="month", stepmode="backward"),
            #             dict(count=1, label="1y", step="year", stepmode="backward"),
            #             dict(step="all"),
            #         ]
            #     )
            # ),
        ),
    )
    fig = make_subplots(figure=go.Figure(layout=layout),x_title="Time")
    fig.update_yaxes(title_text="Time Series",title_standoff=0)
    for trace in traces:
        fig.add_trace(trace)
    fig.update_layout(
        height=figure_height,
        width=500,
        xaxis_rangeselector_font_color="white",
        xaxis_rangeselector_activecolor="#0176D3",
        xaxis_rangeselector_bgcolor="#1B96F1",
        xaxis_rangeselector_font_family="Salesforce Sans",
    )
    #标注异常
    fig.add_vrect(x0="2014-04-23 15:54:00", x1="2014-04-23 20:24:00",
                  annotation_text="", annotation_position="top left",
                  fillcolor="red", opacity=0.5, line_width=0)
    return dcc.Graph(figure=fig)
