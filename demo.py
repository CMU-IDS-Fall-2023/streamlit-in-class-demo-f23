import streamlit as st
import pandas as pd
import altair as alt

st.title("Our First Streamlit App")
st.write("Hello World!")

# df = pd.read_json("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

@st.cache_data
def load(url):
    return pd.read_json(url)

df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

if st.checkbox("Show Raw Data:"):
    st.write(df)

scatter = alt.Chart(df).mark_point().encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
)

# st.altair_chart(scatter, use_container_width=True, theme=None)



with st.sidebar:

    species_selected = st.multiselect("Filter by Species:", df["Species"].unique(), df["Species"].unique())

    col1, col2 = st.columns(2)

    with col1:
        flipper_values = st.slider('Filter by Flipper Length', df["Flipper Length (mm)"].min(), df["Flipper Length (mm)"].max(), (df["Flipper Length (mm)"].min(), df["Flipper Length (mm)"].max()))

    with col2:
        bodymass_values = st.slider('Filter by Body Mass', df["Body Mass (g)"].min(), df["Body Mass (g)"].max(), (df["Body Mass (g)"].min(), df["Body Mass (g)"].max()))



df_filtered = df[(df.Species.isin(species_selected))]
df_filtered = df_filtered[(df_filtered["Flipper Length (mm)"] >= flipper_values[0]) & (df_filtered["Flipper Length (mm)"] <= flipper_values[1])]
df_filtered = df_filtered[(df_filtered["Body Mass (g)"] >= bodymass_values[0]) & (df_filtered["Body Mass (g)"] <= bodymass_values[1])]


scatter = alt.Chart(df_filtered).mark_point().encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
)

#st.write(scatter)
st.altair_chart(scatter, use_container_width=True, theme=None)

hist = alt.Chart(df_filtered).mark_bar().encode(
    alt.X("Body Mass (g)", bin=True),
    alt.Y("count()"),
    alt.Color("Species")
)

st.altair_chart(hist, use_container_width=True, theme=None)
