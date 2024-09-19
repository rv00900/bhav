import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pytz
import os
import plotly.express as px
import streamlit as st
import streamlit as st
import pandas as pd
import datetime
import glob
import matplotlib.pyplot as plt
from streamlit import runtime
import plotly.graph_objects as go

option = st.sidebar.radio(
    'Select an option:', 
    ["BSE_BHAVCOPY","NSE_BHAVCOPY"],index=0)

if option =="BSE_BHAVCOPY":
    import os
    import zipfile
    import pandas as pd
    import streamlit as st
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    import glob


    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1900,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")


    download_dir = "/home/micro2/Documents/bhavt1/" 
    chrome_prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,  
        "download.directory_upgrade": True,  
        "safebrowsing.enabled": True  
    }
    options.add_experimental_option("prefs", chrome_prefs)


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    d = st.date_input("BSE_BHAVCOPY_DATE", value=None)
    st.write("BHAVCOPY_DATE:", d)
    ea = pd.to_datetime(d).strftime("%d%m%y")
    print("EQ",ea)
    directory = "/bhbse/"
    files = os.listdir(directory)
    file_name = f"EQ{ea}.CSV" 
    file_path = os.path.join(directory, file_name)


    directory1 = "/bhavt1/"
    files1 = os.listdir(directory1)
    ee = pd.to_datetime(d).strftime("%Y%m%d")
    print("bhav",ee)
    file_name1 = f"BhavCopy_BSE_CM_0_0_0_{ee}_F_0000.CSV"  
    file_path1 = os.path.join(directory1, file_name1)
    if file_name in files:
        st.write(f"Found in directory: {file_name}")
        df = pd.read_csv(file_path)
        st.dataframe(df)
    elif file_name1 in files1: 
        st.write(f"Found in directory: {file_name1}")
        df = pd.read_csv(file_path1)
        st.dataframe(df)
    elif file_name not in files:
        try:
            url =f"https://www.bseindia.com/download/BhavCopy/Equity/EQ{ea}_CSV.ZIP"
            driver.get(url)
            time.sleep(2)
            print(url)
            zip_folder = "/home/micro2/Documents/bhavt1/" 
            extract_folder = '/home/micro2/Documents/bhbse/'
            os.makedirs(extract_folder, exist_ok=True)
            for file_name in os.listdir(zip_folder):
                if file_name.endswith(".ZIP"):
                    zip_path = os.path.join(zip_folder, file_name)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)
                        print(f"Extracted {file_name} to {extract_folder}")
                        df1 =pd.read_csv(file_path)
                        st.dataframe(df1)
        except Exception as e:
            print(e)
            try:
                url =f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{ee}_F_0000.CSV"
                print(url)
                #st.write(f"Downloading from: {url}")
                driver.get(url)
                time.sleep(2)
                dfw = pd.read_csv(f"BhavCopy_BSE_CM_0_0_0_{ee}_F_0000.CSV")
                #print(dfw)
                st.dataframe(dfw)
            except Exception as e:
                print(e)

if option == "NSE_BHAVCOPY":
    from datetime import date
    from jugaad_data.nse import bhavcopy_save
    import streamlit as st
    

    d = st.date_input("NSE_BHAVCOPY_DATE", value=None)
    
    st.write("BHAVCOPY_DATE:", d)
    
    er = d.strftime("%Y,%m,%d")
    
    year, month, day = map(int, er.split(","))
    print("year",year)
    print("month",month)
    print("day",day)
    ae =bhavcopy_save(date(year,month,day), "/nsebha/")
    print(ae)
    dt = pd.read_csv(f"{ae}")
    st.dataframe(dt)



