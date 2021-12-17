# M. Zacky Mulatif
# 12220119

#import library
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from collections import OrderedDict
from streamlit.logger import get_logger
from PIL import Image
import base64

#-------create function def-------------


main_bg = "background.jpg"
main_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# import & linking json with csv
df_kode_negara = pd.read_json("kode_negara_lengkap.json")
df_produksi = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.merge(df_produksi,df_kode_negara,left_on='kode_negara',right_on='alpha-3')

list_negara = df["name"].unique().tolist()
list_negara.sort()

#home
def home():

    #box command
    st.sidebar.success("Silahkan pilih menu")

    st.markdown("<h1 style='text-align: right; color: green;'> Data Produksi Minyak Mentah </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: right; color: green;'> M. Zacky Mulatif </h3>", unsafe_allow_html=True)

#No 1.A
def no1a():

    data_negara = df["name"].unique().tolist()
    data_negara.sort()

    negara = st.sidebar.selectbox("Select country", data_negara)

    kode = df_kode_negara[(df_kode_negara["name"] == negara)]["alpha-3"].to_list()[0]
    df_states = df_produksi[(df_produksi.kode_negara == kode)].copy().set_index("tahun")
    st.subheader(f'Berikut adalah grafik berbentuk bar chart dari negara {negara}.')

    origin = df[(df["name"] == negara)]
    
    chart = alt.Chart(origin).mark_bar(opacity=1).encode(
        x='tahun:N',
        y='produksi'
    )
    st.altair_chart(chart, use_container_width=True)
    
    a = origin.set_index("tahun").rename(columns={"produksi": "Produksi"})["Produksi"]
    st.dataframe(a)
#No 1.B
def no1b():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih jumlah negara", range(1, len(list_negara)), 9)
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi terbesar pada tahun {tahun}')

    res = df[(df.tahun == tahun)][["name", "produksi"]].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar(opacity=1).encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )
    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='black',
        dx=10 
    ).encode(
        text='produksi'
    )
    chart = (bars).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Total Produksi"}))

#No 1.C
def no1c():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi keseluruhan terbesar')

    res = df[["name", "produksi"]].groupby(['name'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )


    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='white',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars+text).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Total Produksi"}))


#No 1.D
def no1d():

    #command control streamlit
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    total_produksi2 = df.groupby(['name', 'kode_negara', 'region', 'sub-region'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    total_produksi = df.sort_values(by=['produksi'], ascending=False)
    total_produksi_max = total_produksi[(total_produksi["produksi"] > 0)].iloc[0]
    total_produksi_min = total_produksi[(total_produksi["produksi"] > 0)].iloc[-1]
    total_produksi_max_kumulatif = total_produksi2[(total_produksi2["produksi"] > 0)].iloc[0]
    total_produksi_min_kumulatif = total_produksi2[(total_produksi2["produksi"] > 0)].iloc[-1]
    total_produksi_nol = total_produksi[(total_produksi["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    total_produksi_nol.index += 1

    produksi_tahun = df[(df["tahun"] == tahun)][['name', 'kode_negara', 'region', 'sub-region', 'produksi']].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    produksi_tahun_max = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[0]
    produksi_tahun_min = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[-1]
    produksi_tahun_nol = produksi_tahun[(produksi_tahun["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    produksi_tahun_nol.index += 1

    
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi keseluruhan tahun terbesar
        Negara: {total_produksi_max["name"]}\n
        Kode negara: {total_produksi_max["kode_negara"]}\n
        Region: {total_produksi_max["region"]}\n
        Sub-region: {total_produksi_max["sub-region"]}\n
        Jumlah produksi: {total_produksi_max["produksi"]}\n

        #### Negara dengan jumlah produksi terbesar pada tahun {tahun}  
        Negara: {produksi_tahun_max["name"]}\n
        Kode negara: {produksi_tahun_max["kode_negara"]}\n
        Region: {produksi_tahun_max["region"]}\n
        Sub-region: {produksi_tahun_max["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_max["produksi"]}\n

        #### Negara dengan jumlah produksi keseluruhan tahun terkecil
        Negara: {total_produksi_min["name"]}\n
        Kode negara: {total_produksi_min["kode_negara"]}\n
        Region: {total_produksi_min["region"]}\n
        Sub-region: {total_produksi_min["sub-region"]}\n
        Jumlah produksi: {total_produksi_min["produksi"]}\n

        #### Negara dengan jumlah produksi terkecil pada tahun {tahun}  
        Negara: {produksi_tahun_min["name"]}\n
        Kode negara: {produksi_tahun_min["kode_negara"]}\n
        Region: {produksi_tahun_min["region"]}\n
        Sub-region: {produksi_tahun_min["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_min["produksi"]}\n

        #### Negara dengan total produksi keseluruhan tahun terbesar(kumulatif)
        Negara: {total_produksi_max_kumulatif["name"]}\n
        Kode negara: {total_produksi_max_kumulatif["kode_negara"]}\n
        Region: {total_produksi_max_kumulatif["region"]}\n
        Sub-region: {total_produksi_max_kumulatif["sub-region"]}\n
        Jumlah produksi: {total_produksi_max_kumulatif["produksi"]}\n

        #### Negara dengan total produksi keseluruhan tahun terkecil(kumulatif)
        Negara: {total_produksi_min_kumulatif["name"]}\n
        Kode negara: {total_produksi_min_kumulatif["kode_negara"]}\n
        Region: {total_produksi_min_kumulatif["region"]}\n
        Sub-region: {total_produksi_min_kumulatif["sub-region"]}\n
        Jumlah produksi: {total_produksi_min_kumulatif["produksi"]}\n
    """
    )
    st.markdown(
        """
        #### Negara dengan total produksi keseluruhan tahun sama dengan nol
        
    """
    )
    total_produksi_nol = total_produksi_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(total_produksi_nol)
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi sama dengan nol pada tahun {tahun}
        
    """
    )
    produksi_tahun_nol = produksi_tahun_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(produksi_tahun_nol)

#panggil fungsi yang telah dibuat

LOGGER = get_logger(__name__)


FITUR = OrderedDict(
    [
        ("Home", (home, None)),
        (
            "No. 1.a",
            (
                no1a,
                """
                Jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara
                """,
            ),
        ),
        (
            "No. 1.b",
            (
                no1b,
                """
                Negara dengan produksi minyak mentah terbesar pada tahun tertentu
                """,
            ),
        ),
        (
            "No. 1.c",
            (
                no1c,
                """
                Negara dengan total jumlah produksi minyak mentah keseluruhan tahun terbesar
                """,
            ),
        ),
        (
            "No. 1.d",
            (
                no1d,
                """
                Negara Dengan Produksi Terbesar, Terkecil, dan Tidak memproduksi Minyak:
                """,
            ),
        ),

    ]
)


def run():
    demo_name = st.sidebar.selectbox("Silahkan pilih menu", list(FITUR.keys()), 0)

    demo = FITUR[demo_name][0]
    if demo_name == "Home":
        pass
    else:
        st.markdown("# %s" % demo_name)
        description = FITUR[demo_name][1]
        if description:
            st.write(description)

        for i in range(10):
            st.empty()

    demo()

    st.sidebar.image("images.jpg", use_column_width=True)


if __name__ == "__main__":
    run()