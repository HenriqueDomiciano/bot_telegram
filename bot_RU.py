from bs4 import BeautifulSoup 
import requests,lxml,telepot,datetime,re,schedule,time,csv,os

def bot():
    bot= telepot.Bot(os.environS['BOT_KEY'])
    try : 
        response=bot.getUpdates()
    except: 
        bot.deleteWebhook()
        response=bot.getUpdates()
    print(response)
    anterior=[]
    date=datetime.datetime.now()
    date_today=date.strftime('%d')+'/'+date.strftime('%m')

    with open (r'clientes.txt','r') as fr:
        for ids in fr: 
            anterior.append(ids)

    for r in range(len(response)):

        user_id=response[r]
        user_id=user_id['message']
        user_text=user_id['text']
        user_id=user_id['from'] 
        user_id=user_id['id']
        user_id=str(user_id)
        print(user_text)

    message=get_message()

    for k in range (len(anterior)):
        bot.sendMessage(int(anterior[k].rstrip()),message+'\n\n'+"Para parar de receber mensegens digite q ou s")

def get_message():
    index_contador=0
    texto=''
    teste=[]
    date=datetime.datetime.now()
    date_today=date.strftime('%d')+'/'+date.strftime('%m')
        
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
        
    message=get_message()

    for k in range (len(anterior)):
        bot.sendMessage(int(anterior[k].rstrip()),message+'\n\n'+"Para parar de receber mensegens digite q ou s")

bot()