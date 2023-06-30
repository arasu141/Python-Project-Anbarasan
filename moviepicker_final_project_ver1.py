
# Importing all necessary modules
import numpy as np
import pandas as pd
import random
import requests
import openpyxl
from bs4 import BeautifulSoup
from lxml import html 
from requests_html import AsyncHTMLSession
from tkinter import messagebox
global genre_list, genre

# creating folder
import os
pathss = os.path.exists("C:/MOVIE_PICKER")
if pathss is True:
    path2 = "C:/MOVIE_PICKER"
    # if path2 is True:
    all_files = os.listdir(path2)

    # deleting the files in the folder
    files_to_delete = [ff for ff in all_files if ff.endswith('.xlsx')]
    # print(files_to_delete)
    for ff in files_to_delete:
        paths_object = os.path.join(path2, ff)
        # print(paths)
        os.remove(paths_object)
    os.rmdir(path2)
    os.mkdir("C:/MOVIE_PICKER")

else:
    os.mkdir("C:/MOVIE_PICKER")



import requests_html
session = requests_html.HTMLSession()



# function for creating the layout of the panel
def template1():
    global u_id
    import PySimpleGUI as sg
    import sys

    # creating the layout
    col = [[sg.Radio(x, 1, key ="k_"+str(x))] for x in genre_list]

    layout = [
                [sg.Text('My layout')],
                [sg.Column(col, size=(300, 300), scrollable=True)],
                [sg.Button('OK')],
                [sg.Cancel("Cancel")]
            ]

    window = sg.Window('Movie Picker', layout)

    while True:             # Event Loop
        event, values = window.Read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        if event == 'OK':
            for x in range(len(genre_list)):
                u_id = genre_list[x]
                k_val = values["k_"+str(u_id)]
                # print(k_val)
                if k_val == True:
                    print(u_id)
                    window.Close()
                    select_genere(u_id)
                
        break
                
    window.Close()

# Function for data manupulation in the dataframe
def select_genere(genere_one):
    global newdf, final_movie
    import random
    # newdf = pd.DataFrame(columns=['Movie List','movie year','genere list'])
    # newdf.iloc[0:0]
    
    try:
        # print("calling select_genere function")
        newdf = df[df['genere list'] == u_id]
        print(newdf[['Movie List','movie year','genere list']])
        sample_movie = newdf.sample(n=1)
        final_movie = sample_movie['Movie List'].to_string(index=False)

        # final_movie = random.choice(newdf['Movie List'])
        print('******************************************************************************')
        print(" THE MOVIE YOU HAVE TO WATCH IS : " , final_movie)

        choice  = input( " Do you want to select another movie? Y/N :")
        if choice == "Y":
            template1()
        else:
            print("BYE Thanks")
    except ValueError:
        print(" There is no data for this Genere")
        template1()


# defining Main function
def main():
    global df, genre_list, movie_list, genre_cluster, movie_year_list
    print("Extracting the database from 'IMDB.com'.It will take 2-3 min, please wait till the process finishes....")

    r = session.get('https://www.imdb.com/feature/genre/')
    
    genre_list = []
    movie_list = []
    genre_cluster = []
    movie_year_list=[]
    df = []
    try:
        empty_df = pd.DataFrame()
        # get the list of geners
        for item in r.html.xpath('//div[@class="sc-243fb82e-2 kwKkbX ipc-page-grid__item ipc-page-grid__item--span-2"]/section[2]/div[2]/div/a'):
            genre = item.text
            genre_list.append(genre)
            # print(genre)

            
            rr = session.get('https://www.imdb.com/search/title/?genres='+ genre +'&explore=genres&title_type=feature&ref_=ft_movie_0')
            for mov in rr.html.xpath('//div[@class="lister-item mode-advanced"]/div[3]/h3/a'):
                movie = mov.text
                movie_list.append(movie)
                genre_cluster.append(genre)
                for year in rr.html.xpath('//div[@class="lister-item mode-advanced"]/div[3]/h3/span[2]'):
                    years = year.text
                    movie_year_list.append(years)

                df = pd.DataFrame(zip(movie_list,movie_year_list,genre_cluster), columns=["Movie List",'movie year','genere list'])
                df.to_excel(r"C:\MOVIE_PICKER\final.xlsx", index=False)

            print("extracting", genre)

        messagebox.showinfo("", "The database has been downloaded")
            

    except NoSuchElementException:
        print("No element was found, check for network connectivity / Rerun the program")

# Calling the MAIN function
if __name__ == '__main__':
    inpu_from_user = input("do you wantto pick up a movie to watch ? Y/N :")
    if inpu_from_user == 'Y':
        # print("running main")
        print(main())
        template1()
    elif inpu_from_user == 'N':
        print("Ok bye")
    else:
        print("Re-Run Program, and enter the correct values")
    