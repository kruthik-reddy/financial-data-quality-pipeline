import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import yfinance as yf
import os
import plotly.graph_objects as go
from datetime import datetime as dt
from flask import send_file

# App init
app = dash.Dash(__name__)
server = app.server
app.title = "Stock Downloader"

stock_list = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'NVDA', 'AMZN', 'META', 'NFLX', 'INTC', 'IBM']

# App layout
app.layout = html.Div([
    html.H2("Stock Data Downloader & Technical Indicators"),
    html.Label("Select Ticker(s):"),
    dcc.Dropdown(
        id="ticker-dropdown",
        options=[{"label": t, "value": t} for t in stock_list],
        multi=True,
        searchable=True,
        placeholder="Choose stock symbols..."
    ),
    html.Br(),
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id="date-picker",
        min_date_allowed=dt(2015, 1, 1),
        max_date_allowed=dt.now(),
        start_date=dt(2023, 1, 1),
        end_date=dt.now()
    ),
    html.Br(),
    html.Button("Download, Plot & Export", id="submit-btn", n_clicks=0),
    html.Div(id="output-messages"),
    html.Br(),
    html.A("📥 Download Full Excel Report", href="/download/stock_report.xlsx", target="_blank", style={"fontSize": 18})
])

@app.callback(
    Output("output-messages", "children"),
    Input("submit-btn", "n_clicks"),
    State("ticker-dropdown", "value"),
    State("date-picker", "start_date"),
    State("date-picker", "end_date"),
)
def fetch_and_plot(n_clicks, symbols, start_date, end_date):
    if not symbols or not start_date or not end_date:
        return "Please select tickers and date range."

    start_date = pd.to_datetime(start_date).strftime("%Y-%m-%d")
    end_date = pd.to_datetime(end_date).strftime("%Y-%m-%d")

    messages = []
    
    excel_writer = pd.ExcelWriter("data/stock_report.xlsx", engine="xlsxwriter")

    for symbol in symbols:
        try:
            df = yf.download(symbol, start=start_date, end=end_date, group_by="ticker", auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df = df[symbol]
            df.columns.name = None

            os.makedirs("data", exist_ok=True)
            csv_path = f"data/{symbol}_raw.csv"
            df.to_csv(csv_path)

            if "Close" not in df.columns or df["Close"].dropna().empty:
                messages.append(html.P(f"{symbol}: 'Close' column missing or empty."))
                continue

            # Technical indicators
            df["MA_7"] = df["Close"].rolling(7).mean()
            df["MA_30"] = df["Close"].rolling(30).mean()
            df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
            df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
            df["MACD"] = df["EMA_12"] - df["EMA_26"]
            delta = df["Close"].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = -delta.where(delta < 0, 0).rolling(14).mean()
            rs = gain / loss
            df["RSI"] = 100 - (100 / (1 + rs))
            df["BB_MID"] = df["Close"].rolling(20).mean()
            df["BB_UPPER"] = df["BB_MID"] + 2 * df["Close"].rolling(20).std()
            df["BB_LOWER"] = df["BB_MID"] - 2 * df["Close"].rolling(20).std()

            # Save to Excel
            df.to_excel(excel_writer, sheet_name=symbol)

            # Plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close"))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA_7"], mode="lines", name="MA 7"))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA_30"], mode="lines", name="MA 30"))
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_UPPER"], mode="lines", name="BB Upper", line=dict(dash="dot")))
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_LOWER"], mode="lines", name="BB Lower", line=dict(dash="dot")))
            fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD"))
            fig.update_layout(
                title=f"{symbol} Price with Indicators",
                xaxis_title="Date",
                yaxis_title="Value",
                template="plotly_white"
            )

            preview_table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.reset_index().columns],
                data=df.reset_index().head(5).to_dict("records"),
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "5px"},
                style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
                page_size=5
            )

            download_link = html.A(
                f"Download {symbol} CSV",
                href=f"/download/{symbol}_raw.csv",
                target="_blank",
                style={"color": "blue", "textDecoration": "underline"}
            )

            messages.append(html.Div([
                html.H4(f"{symbol} Preview"),
                dcc.Graph(figure=fig),
                preview_table,
                download_link,
                html.Hr()
            ]))

        except Exception as e:
            messages.append(html.P(f"Error downloading {symbol}: {str(e)}"))

    excel_writer.close()
    return messages

@server.route("/download/<path:filename>")
def serve_static_csv(filename):
    return send_file(f"data/{filename}", as_attachment=True)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("🔥 Dash app failed to start:", e)
