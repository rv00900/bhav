import zipfile
import subprocess
import pandas as pd
import streamlit as st
from datetime import datetime
from jugaad_data.nse import bhavcopy_save
from pathlib import Path


option = st.sidebar.radio('Select an option:', ["BSE_BHAVCOPY", "NSE_BHAVCOPY"], index=0)

if option == "BSE_BHAVCOPY":
    d = st.date_input("BSE_BHAVCOPY_DATE", value=None)
    st.write("BHAVCOPY_DATE:", d)
    ea = pd.to_datetime(d).strftime("%d%m%y")
    ee = pd.to_datetime(d).strftime("%Y%m%d")
    

    try:
        df = pd.read_csv(f"/workspaces/bhav/BSE_BhavCopy/EQ{ea}.CSV")
        st.dataframe(df)
    except FileNotFoundError:
        url = f"https://www.bseindia.com/download/BhavCopy/Equity/EQ{ea}_CSV.ZIP"
        try:

            subprocess.run(["wget", "-q", "-P", "./BhavCopy_Zips", url], check=True)
            st.write(f"Downloaded: {url}")

            zip_file = f"/workspaces/bhav/BhavCopy_Zips/EQ{ea}_CSV.ZIP"
            extract_to = "/workspaces/bhav/BSE_BhavCopy/"
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
                file_path = Path(zip_file)
                file_path.unlink()

            

            df = pd.read_csv(f"/workspaces/bhav/BSE_BhavCopy/EQ{ea}.CSV")
            st.dataframe(df)

        except subprocess.CalledProcessError as e:
            #st.error(f"Failed to download {url}: {e}")
            url_alt = f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{ee}_F_0000.CSV"
            try:
                subprocess.run(["wget", "-q", "-P", "/workspaces/bhav/BSE_BhavCopy", url_alt], check=True)
                #st.write(f"Downloaded: {url_alt}")
                df = pd.read_csv(f"/workspaces/bhav/BSE_BhavCopy/BhavCopy_BSE_CM_0_0_0_{ee}_F_0000.CSV")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Failed to download {url_alt}: {e}")  
elif option == "NSE_BHAVCOPY":
    d = st.date_input("NSE_BHAVCOPY_DATE", value=None)
    st.write("BHAVCOPY_DATE:", d)
    
    er = d.strftime("%Y,%m,%d")
    year, month, day = map(int, er.split(","))
    
    ae = bhavcopy_save(datetime(year, month, day), "/workspaces/bhav/nsebhav")
    dt = pd.read_csv(f"{ae}")
    st.dataframe(dt)

