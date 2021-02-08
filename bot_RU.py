from bs4 import BeautifulSoup 
import requests,lxml,telepot,datetime,re,time,csv,os,psycopg2

def bot():
    DATABASE_URL = os.environ['DATABASE_URL']
    bot= telepot.Bot(os.environ['BOT_KEY'])
    def conect_db():
        banco = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor=banco.cursor()
        return banco 

    def get_users(banco):
        cursor=banco.cursor()
        cursor.execute("SELECT * from id0")
        x=cursor.fetchall()
        x=[list(i)for i in x ]
        ida=[j for sub in x for j in sub]
        cursor.close()
        return ida

    banco=conect_db()
    date=datetime.datetime.now()
    date_today=date.strftime('%d')+'/'+date.strftime('%m')
    anterior = get_users(banco)
    anterior = [str(i) for i in anterior]
    message=get_message()
    banco.close()
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
bot()