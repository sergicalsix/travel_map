import streamlit as st
from .codes.geocode import get_place_data,str_list_to_numpy_array

st.set_page_config(
   page_title="Travel Planer",
)

st.title("Travel Planer")
st.write('<style>h1 {color: red;}</style>', unsafe_allow_html=True)

#st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
#st.markdown('<i class="material-icons">face</i>', unsafe_allow_html=True)
#st.image('img/icons/sch.png')
#st.image('<i class="material-icons"> ":face:" </i>', unsafe_allow_html=True)
#password = st.text_input('パスワードを入力してください')

#st.sidebar.image('img/icons/flag.png')

st.markdown("""-----""")
st.sidebar.markdown("""-----""")

go = st.sidebar.checkbox('実行!!')



st.markdown("""-----""")
