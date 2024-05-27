#pip  install streamlit 
# streamiit run 파일명
import streamlit as st
import pandas as pd

st.write("# chart view")
st.write("## raw cata")
view = [100, 150, 30]
st.bar_chart(view)
sview = pd.Series(view)
st.write(sview)

# streamlit라이브러리는 git hub와 연동됨

