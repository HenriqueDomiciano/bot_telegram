from bs4 import BeautifulSoup 
import requests,lxml,telepot,datetime,re,schedule,time,csv,os,psycopg2,threading

#bot= telepot.Bot(os.environ['BOT_KEY']) 
bot=telepot.Bot('1330666160:AAGPt1Kor8Xqz__oFeGVXgfArebUlzvlX90')
#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = 'postgres://jyrhwwwqkxzduy:1849ae52b469cee9a60ad69a503878e473bea88118301a9085d17dab31e0d5ae@ec2-3-231-241-17.compute-1.amazonaws.com:5432/df4lrfh3vh482n'

def conect_db():

    banco = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor=banco.cursor()
    '''
    try:
        cursor.execute("CREATE TABLE id0 (id integer NOT NULL)")
        cursor.close()
    except:
        cursor.close()
    '''
    return banco 
banco = conect_db()
cursor=banco.cursor()

def get_users(banco):

    cursor.execute("select * from id0")
    x=cursor.fetchall()
    x=[list(i)for i in x ]
    ida=[j for sub in x for j in sub]
    return ida

def insert_user(idb,banco,db):

    cursor=banco.cursor()
    cursor.execute("INSERT INTO id0 (id) VALUES (%s)",(idb,))
    banco.commit() 

def delete_user(idb,banco):
    
    cursor=banco.cursor()
    cursor.execute('DELETE from id0 where id = '+ str(idb))
    banco.commit()

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
    user_text = msg['text'] 
    quem=msg['from']
    ide=quem['id']
    str_ide=str(ide)
    bot.sendMessage(str_ide,get_message()+'Envie Q ou S para receber esta mensagem uma vez')
    db = get_users(banco)
    if user_text.lower() == 'q' or user_text.lower()=='s':
        if ide in db:
            delete_user(ide,banco) 
            bot.sendMessage(str_ide,"Você foi removido do banco de dados com sucesso")           
    else:
        if not (ide in db):
            insert_user(ide,banco,db)
            bot.sendMessage(str_ide,'Você foi adicionado ao banco de dados e irá receber esta mensagem todo dia as 6 AM')
        print(get_users(banco))

bot.message_loop(bote)
while(1):
    pass

