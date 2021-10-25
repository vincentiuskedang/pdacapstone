from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table',attrs={'class':'table table-striped text-sm text-lg-normal'})
row = soup.find_all('th',attrs={'class':'font-semibold text-center'})

row_length = len(row)

temp = [] #initiating a tuple

for i in range(0, row_length):

    #finding all Dates in table
    Date = soup.find_all('th',attrs={'class':'font-semibold text-center'})[i].text
    Date = Date.strip('\n')
    
    # finding all Volume in table
    Volume = soup.find_all('td',attrs={'class':'text-center'})[i*4+1].text
    Volume = Volume.strip('\n')
    
    #append the data that has been obtained, into an array.
    temp.append((Date, Volume))

#reverse the order of the list   
temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp,columns=('Date', 'Volume'))

#insert data wrangling here
#change to datetime64 type
df['Date'] = df['Date'].astype('datetime64')

#cleaning the data so we can analyze much better
df['Volume'] = df['Volume'].str.replace('$','')
df['Volume'] = df['Volume'].str.replace(',','')

#change to int64 type
df['Volume'] = df['Volume'].astype('float64')

#make Date as index
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (10,5))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)