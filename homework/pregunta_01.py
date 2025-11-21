# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


"""
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

"""


import os

import matplotlib.pyplot as plt
import pandas as pd


def pregunta_01():
    """
    Lee el archivo de datos y garantiza la existencia de la carpeta docs.
    """
    carpeta_salida = "docs"
    os.makedirs(carpeta_salida, exist_ok=True)

    ruta_datos = "files/input/shipping-data.csv"
    datos = pd.read_csv(ruta_datos)

    return datos


def grafico_envios_por_bodega(df: pd.DataFrame) -> str:
    """
    Genera un gráfico de barras con la cantidad de envíos por bloque de bodega.
    """
    datos = df.copy()

    plt.figure()
    conteos = datos["Warehouse_block"].value_counts()

    conteos.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8,
    )

    eje = plt.gca()
    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)

    ruta_salida = "docs/shipping_per_warehouse.png"
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida


def grafico_modo_de_envio(df: pd.DataFrame) -> str:
    """
    Genera un gráfico de pastel con la distribución del modo de envío.
    """
    datos = df.copy()

    plt.figure()
    conteos = datos["Mode_of_Shipment"].value_counts()

    conteos.plot.pie(
        title="Mode of shipment",
        wedgeprops={"width": 0.35},
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )

    ruta_salida = "docs/mode_of_shipment.png"
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida


def grafico_calificacion_promedio(df: pd.DataFrame) -> str:
    """
    Genera un gráfico horizontal con min, max y promedio de Customer_rating
    por modo de envío.
    """
    datos = df.copy()

    plt.figure()
    resumen = (
        datos[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    resumen.columns = resumen.columns.droplevel()
    resumen = resumen[["mean", "min", "max"]]

    # Barra de rango [min, max]
    plt.barh(
        y=resumen.index.values,
        width=resumen["max"].values - 1,
        left=resumen["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    # Color verde si mean >= 3.0, naranja en caso contrario
    colores = [
        "tab:green" if valor >= 3.0 else "tab:orange"
        for valor in resumen["mean"].values
    ]

    # Barra centrada en el promedio
    plt.barh(
        y=resumen.index.values,
        width=resumen["mean"].values - 1,
        left=resumen["min"].values,
        color=colores,
        height=0.5,
        alpha=1.0,
    )

    plt.title("Average Customer Rating")

    eje = plt.gca()
    eje.spines["left"].set_color("gray")
    eje.spines["bottom"].set_color("gray")
    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)

    ruta_salida = "docs/average_customer_rating.png"
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida


def grafico_distribucion_peso(df: pd.DataFrame) -> str:
    """
    Genera un histograma de la distribución de pesos enviados.
    """
    datos = df.copy()

    plt.figure()
    datos["Weight_in_gms"].plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
    )

    eje = plt.gca()
    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)

    ruta_salida = "docs/weight_distribution.png"
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

    return ruta_salida


def crear_dashboard_html() -> str:
    """
    Crea el archivo docs/index.html que arma el dashboard
    con las cuatro imágenes generadas.
    """
    contenido_html = """<!DOCTYPE html>
<html>
  <body>
    <h1>Shipping Dashboard Example</h1>

    <div style="width:45%;float:left">
      <img src="shipping_per_warehouse.png" alt="Fig 1">
      <img src="mode_of_shipment.png" alt="Fig 2">
    </div>

    <div style="width:45%;float:left">
      <img src="average_customer_rating.png" alt="Fig 3">
      <img src="weight_distribution.png" alt="Fig 4">
    </div>
  </body>
</html>
"""

    ruta_html = "docs/index.html"
    with open(ruta_html, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_html)

    return ruta_html


if __name__ == "__main__":
    df = pregunta_01()
    grafico_envios_por_bodega(df)
    grafico_modo_de_envio(df)
    grafico_calificacion_promedio(df)
    grafico_distribucion_peso(df)
    archivo_html = crear_dashboard_html()
    print(archivo_html)
