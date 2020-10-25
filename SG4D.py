from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = True
#options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome("C:\\sw\\Python38\\chromedriver.exe",options=options)
output_file = open('result-tables.txt', 'w', encoding="utf-8")
URL_root = "https://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx?sppl=RHJhd051bWJlcj00"

if True:
    URL_list = []
#    for index3 in ['Nj']:
#        for index2 in ['A']:
#            for index1 in ['5','4','3','2','1','0','z','y','x','w']:
#                URL_list.append(URL_root+index3+index2+index1)
#    for index3 in ['NT', ND','Mz','Mj','MT','MD']:
#        for index2 in ['k','g','c','Y','U','Q','M','I','E','A']:
#            for index1 in ['5','4','3','2','1','0','z','y','x','w']:
#                URL_list.append(URL_root+index3+index2+index1)
    for index3 in ['NT']:
        for index2 in ['k','g','c','Y','U','Q','M','I','E','A']:
            for index1 in ['5','4','3','2','1','0','z','y','x','w']:
                URL_list.append(URL_root+index3+index2+index1)
else:
    URL_list = ["https://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx?sppl=RHJhd051bWJlcj00MTcw",
                "https://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx?sppl=RHJhd051bWJlcj00NjA2"]

for U in range(len(URL_list)):
    driver.get(URL_list[U])
    html = driver.execute_script("return document.documentElement.outerHTML")
#
    soup = BeautifulSoup(html, 'html.parser')
    soup_table = soup.find_all("table")
    df1 = pd.read_html(str(soup_table[1]), header=0)[0]
    df2 = pd.read_html(str(soup_table[2]), header=0)[0]
    df3 = pd.read_html(str(soup_table[3]), header=0)[0]

    dfx = pd.DataFrame(index=range(1,24), columns=["Date","Day", "Draw","Label","Value"])
    Date_v = str(df1.columns[0])

    for iDay in ["Wed","Sat","Sun"]:
        iDay1 = iDay+", "
#        print("xxx: ", Date_v.find(iDay))
        if (Date_v.find(iDay) >= 0):
            Date_v = Date_v.replace(iDay1,"")
            Day_v = iDay

    Draw_v = str(df1.columns[1])
    Draw_v1 = Draw_v.replace("Draw No.","")
#
    dfx = dfx.fillna(value={'Date' : Date_v.replace(" ","-") , 'Draw' : Draw_v1, 'Day' : Day_v ,'Label' : "Con"})
    dfx.at[1,'Label'] = "1st"
    dfx.at[2,'Label'] = "2nd"
    dfx.at[3,'Label'] = "3rd"
    dfx.at[1,'Value'] = df1.at[0,Draw_v]
    dfx.at[2,'Value'] = df1.at[1,Draw_v]
    dfx.at[3,'Value'] = df1.at[2,Draw_v]
    for i in range(4,9):
        dfx.at[i,'Value'] = df2.at[i-4,"Starter Prizes"]
    for i in range(9,14):
        dfx.at[i,'Value'] = df2.at[i-9,"Starter Prizes.1"]
    for i in range(4,14):
        dfx.at[i,'Label'] = "Sta"
    for i in range(14,19):
        dfx.at[i,'Value'] = df3.at[i-14,"Consolation Prizes"]
    for i in range(19,24):
        dfx.at[i,'Value'] = df3.at[i-19,"Consolation Prizes.1"]
    print(dfx)
    csv_filename = "Draw_" + Draw_v1 + ".csv"
    dfx.to_csv(csv_filename)

driver.quit()
