import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
from shiny.express import input,render,ui
from matplotlib.ticker import MaxNLocator
import numpy as np 
from pathlib import Path

from functools import partial
from shiny.express import ui
from shiny.ui import page_navbar


#df = pd.read_csv(Path(__file__).parent / "Global YouTube Statistics.csv")

#Uncomment this line for local use 
df = pd.read_csv(r"C:\Users\tonychen\Documents\Python Files\Shiny 2\Global YouTube Statistics.csv", encoding= "latin1")

# Filter the data only include rows where subscribers are under 50 million 
df['subscribers'] = pd.to_numeric(df['subscribers'], errors = 'coerce')
df_filtered = df[df['subscribers']< 50_000_000]
df_filtered = df_filtered.dropna(subset = ['subscribers'])
df_filtered = df_filtered[np.isfinite(df_filtered['subscribers'])]

ui.page_opts(
    title="Youtuber Dashboard",  
    page_fn=partial(page_navbar, id="page"),  
)

with ui.nav_panel("Visualization"):  
    with ui.layout_sidebar():
        with ui.sidebar(bg="#f8f8f8"):  
            "Options"
            
            #ui.input_dark_mode() # << 
            ui.input_slider("n", "Number of bins", 0, 100, 20)
            ui.input_text("text", "Youtuber Search", "")  

    @render.plot(alt="A histogram")  
    def distPlot():
        #Create Vis 
        searchtext = input.text().strip().lower()
        if searchtext:
            final_output = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na = False)]
        else:
            final_output = df_filtered
        fig, ax = plt.subplots(figsize =(10,6))
        ax.hist(final_output['subscribers'], input.n(), color = 'blue',  alpha = 0.7, density = True)
        ax.set_title('Distrubtion of Subscribers')
        ax.set_xlabel('Subscribers')
        ax.set_ylabel('Density')

        ax.xaxis.set_major_locator(MaxNLocator(integer = True))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        plt.xticks(rotation = 45)
        plt.grid(True)
        
        return fig
    @render.data_frame  
    def youtuber_df1():
        searchtext = input.text().strip().lower()
        if searchtext:
            final_output = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na = False)]
        else:
            final_output = df_filtered
        return render.DataGrid(final_output) 


with ui.nav_panel("Data"):  
    with ui.layout_columns():  
        with ui.card(): 


            @render.data_frame  
            def youtuber_df2():
                searchtext = input.text().strip().lower()
                if searchtext:
                    final_output = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na = False)]
                else:
                    final_output = df_filtered
                return render.DataGrid(final_output)    










