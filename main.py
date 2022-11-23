try:
    from urequests import post as p
except:
    from requests import post as p
import network,time
from machine import reset as R
from machine import Pin as P
from json import load,dump,dumps
with open('config.json') as Y:
    x = load(Y)
    for n in x:
        globals()[str(n)] = x[n]
from os import listdir
if file not in listdir():
    with open(file,'w') as i:
        dump({"ids":list()},i)
if auto_off_pins:
    [P(i,P.OUT).off() for i in pins]
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, key)
        while not sta_if.isconnected():
            pass
do_connect()
def bot(method='getme',json_=dict(),token=token):
    if API_URL:
        url = str(API_URL)+'?method='+str(method)+'&token='+str(token)
        return p(url,json=json_).json()
    else:
        url = 'https://api.telegram.org/bot'+str(token)+'/'
        if json_:
            url += str('?'+''.join([str(i)+'='+str(json_[i])+'&' for i in json_]))[:-1:]
        return p(url).json()

def get_type(obj):
    if 'callback_query' in obj:
        return 'inline'
    elif 'message' in obj and 'text' in obj['message']:
        return 'text'

def get_updates():
    with open(file) as i:
        x = load(i)['ids']
    update = list()
    ITER = bot('getupdates')
    if 'result' in ITER:
        for n in ITER['result']:
                if not n['update_id'] in x:
                    update.append(n)
    return update if update else False
def delete_updates():
    with open(file) as i:
        x = load(i)
    x['ids'] = list()
    with open(file,'w') as i:
        dump(x,i)
    bot('setwebhook',{"url":"https://google.com","drop_pending_updates":True})
    time.sleep(1)
    bot('deletewebhook')['ok']

def read_update(update_id):
    with open(file) as i:
        x = load(i)
    if len(x['ids']) >= 3:
        delete_updates()
        x['ids'] = list()
        with open(file,'w') as i:
            dump(x,i)
    else:
        x['ids'].append(int(update_id))
        with open(file,'w') as i:
            dump(x,i)

def access(pin):
    if P(int(pin),P.OUT).value():
        return {'text':'%F0%9F%94%B4 off','callback_data':'off_'+str(pin)}
    else:
        return {'text':'%F0%9F%9F%A2 on','callback_data':'on_'+str(pin)}
delete_updates()
panel = 'Hello admin , welcome to the control panel.'
while True:
    try:
        update = get_updates()
        if update:
            for n in update:
                type_ = get_type(n)
                update_id = n['update_id']
                if type_ == 'text':
                    message_id = n['message']['message_id']
                    user_id = n['message']['from']['id']
                    if user_id not in ADMIN:
                        read_update(message_id)
                    elif n['message']['text'] == '/start':
                        key = {'inline_keyboard':list()}
                        for i in pins:
                            key['inline_keyboard'].append([{'text':'%F0%9F%93%8D Pin'+str(i),'callback_data':'pin_'+str(i)},access(i)])
                        bot('sendmessage',{'chat_id':user_id,'reply_to_message_id':message_id,'text':panel,'reply_markup':dumps(key)})
                        read_update(update_id)
                    else:
                        text = "if you want to see admin panel , use /start command."
                        bot('sendmessage',{'chat_id':user_id,'reply_to_message_id':message_id,'text':text})
                        read_update(update_id)
                elif type_ == 'inline':
                    data = n['callback_query']['data']
                    user_id = n['callback_query']['message']['chat']['id']
                    message_id = n['callback_query']['message']['message_id']
                    if user_id not in ADMIN:
                        read_update(message_id)
                    elif data.startswith('on'):
                        pin_num = data.split('_')[1]
                        exec('P('+str(pin_num)+',P.OUT).on()')
                        key = {'inline_keyboard':list()}
                        for i in pins:
                            key['inline_keyboard'].append([{'text':'%F0%9F%93%8D Pin'+str(i),'callback_data':'pin_'+str(i)},access(i)])
                        bot('editMessageReplyMarkup',{'chat_id':user_id,'message_id':message_id,'reply_markup':dumps(key)})
                    elif data.startswith('off'):
                        pin_num = data.split('_')[1]
                        exec('P('+str(pin_num)+',P.OUT).off()')
                        key = {'inline_keyboard':list()}
                        for i in pins:
                            key['inline_keyboard'].append([{'text':'%F0%9F%93%8D Pin'+str(i),'callback_data':'pin_'+str(i)},access(i)])
                        bot('editMessageReplyMarkup',{'chat_id':user_id,'message_id':message_id,'reply_markup':dumps(key)})
                    elif data.startswith('pin'):
                        key = {'inline_keyboard':list()}
                        for i in pins:
                            key['inline_keyboard'].append([{'text':'%F0%9F%93%8D Pin'+str(i),'callback_data':'pin_'+str(i)},access(i)])
                        bot('editMessageText',{'chat_id':user_id,'message_id':int(message_id),'text':str(str(panel)+'\n\n%E2%9A%99 Pin'+str(data.split('_')[1])+' : '+str('on' if P(int(data.split('_')[1]),P.OUT).value() else 'off')),'reply_markup':dumps(key)})
                    read_update(n['update_id'])
    except:
        R()
