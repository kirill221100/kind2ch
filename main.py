from flask import Flask, render_template, redirect, flash, url_for, request
from flask_apscheduler import APScheduler
import requests, json, re

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

scheduler = APScheduler(app=app)
# print(requests.get('https://2ch.hk/b/res/266820522.json').json())
# print('----------')
fil = r'заебашить,плюнуть мне в ебало,как же бесят,как же мне все надоело,как же заебал,пидорах,чмондель,капитализм,' \
      r'совёнок фест,зоо порно,фап контент,суицид,спецоперац,мы обречены страдать,почему блять,куколд,хрю,хохол,хохл,' \
      r'русн,сармат,усыпить,урод,я ненавижу,норми,быдлан,фап тред,fap тред,украин,это говно,консерватор,ты чмо,' \
      r'чмошник,полуголых тянок тред,ножки зумерш,у тебя никогда такого не будет,слушаю ваши оправдания,сисян,либерал,' \
      r'либерах,докажите мне обратное,пыня,ебланок,старую ебнутую мразь,АЙТИ ВСЁ,ПЬЯНЫМ ЗА РУЛЁМ,Как распознать гея,обращаюсь к вам за помощью,что мужчин любить не стоит,МИЛФОТРЕД,Тест на быдло,россиян,топить за страну,бесхребетные тряпки,депресси,нормальной стране,вайфу,большевизм,' \
      r'напали сoбаки,ДЯДЬ ВОВ,сочной пухлой жопы,лживое говно,Швайнокарас,скотопидараш,лахт,фаптред,порно актрис,шкваришь,ради чего я живу,охуеваю с малолетних долбаебов,политолог,Завидуете мне,Вы все ПИДОРГИ,отвернулись все друзья,ты никому не нужен.,нет талантов,русофоб,dark webm'
# with open('threads.json', 'r', encoding='utf-8') as f:
#     req = json.load(f)
# with open('threads.txt', 'r', encoding='utf-8') as f:
#     req = f.read()
req = []
@app.before_first_request
def bfr():
    for i in range(10):
        req.append(requests.get(f'https://2ch.hk/b/{i+1}.json').json())
    # with open('threads.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(req))
# print(req)
# print(eval(req))
@scheduler.task('interval', id='do_job_1', seconds=600)
def job1():
    for i in range(10):
        req.append(requests.get(f'https://2ch.hk/b/{i+1}.json').json())

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 0, type=int)
    #req = requests.get('https://2ch.hk/b/1.json').json()
    #print(req)
    threads = []
    for i in req[page]['threads']:
        res = re.compile('|'.join(fil.split(',')),re.IGNORECASE).search(i['posts'][0]['comment'])
        if not res:
            threads.append(i)
        else:
            print(res)
            print(i['posts'][0]['comment'])
            print('---------------------')

    return render_template('index.html', req=threads, page=page)

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    req_cat = requests.get('https://2ch.hk/b/catalog.json').json()
    threads = []
    for i in req_cat['threads']:
        res = re.compile('|'.join(fil.split(',')),re.IGNORECASE).search(i['comment'])
        if not res:
            threads.append(i)
        else:
            print(res)
            print(i['comment'])
            print('---------------------')

    return render_template('catalog.html', req=threads)

if __name__ == '__main__':
    app.run(debug=True)

