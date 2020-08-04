from bs4 import BeautifulSoup 
import requests,lxml,telepot,datetime,re,schedule,time,csv,os
bot= telepot.Bot(os.environ['BOT_KEY']) 
def already_in_clients():
    clientes=[]
    with open(r'clientes.txt','r') as f:
        for files in f: 
            clientes.append(files)
    return clientes

def get_message():

    date=datetime.datetime.now()
    date_today=date.strftime('%d')+'/'+date.strftime('%m')
    index_contador=0
    texto=''
    teste=[]

    value = requests.get(r'http://www.pra.ufpr.br/portal/ru/ru-centro-politecnico/')

    value_new= value.text

            
    soup=BeautifulSoup(value_new,'lxml')
    cardapio=soup.find('div', id='post')
    teste=cardapio.find_all('p')

    for x in range (len(teste)):
        teste[x]=teste[x].text

    for values in teste:
        if date_today in values:  
            index_contador = teste.index(values)
            
    for l in range (index_contador,index_contador+4):
        texto=texto+((teste[l]))+','
    return texto

def bote(msg): 
    quem=msg['from']
    ide=quem['id']
    ide=str(ide)
    clientes=already_in_clients()
    if not(ide in clientes):
        with open('clientes.txt','a') as f:
            f.write(ide+'\n') 
    bot.sendMessage(ide,get_message())
    
bot.message_loop(bote)

while(1):
    pass
