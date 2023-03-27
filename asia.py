import json
import time
import os
import requests
import random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def asiacell(method, data, headers):
    r = requests.post(
        f"https://www.asiacell.com/api/v1/{method}?lang=ar", headers=headers, json=data)

    return r.json()


def asiacell2(method, headers):
    r = requests.get(
        f"https://www.asiacell.com/api/v1/{method}?lang=ar", headers=headers)

    return r.json()


bot = Client(
    "bot",
    api_id=19662621,
    api_hash='24c2270e7f1336eb59ca6c48e42ec6ca',
    bot_token='6090849226:AAFibp9FgaLBIUGFnFEP9ffQgwgkbvKK2xM'
)

SUDO = 5159123009


@bot.on_message(filters.command('start'))
def start(bot, msg):
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('اضف هاتف', callback_data=f"addnumber"),
        ],
        [
            InlineKeyboardButton('قائمة الهواتف المضافة',
                                 callback_data=f"knumbers"),
        ],
        [
            InlineKeyboardButton('كيفية استخدام البوت',
                                 callback_data=f"help"),
        ],
    ])
    bot.send_message(
        msg.chat.id, f"مرحبا بك عزيزي المستخدم،\nيمكنك التحكم في شريحة هاتفك،\n( الاسياسيل ) من خلال هذا البوت.", reply_markup=reply_markup)
    try:
        if str(msg.chat.id) in open("members.txt", "r").read():
            print("Done Save id : " + str(msg.chat.id) + " ok")
        else:
            print("Done Save id : " + str(msg.chat.id))
            open("members.txt", "a").write(str(msg.chat.id) + "\n")
            bot.send_message(SUDO, f"New Member Now\n - is Name : {msg.from_user.first_name} \n - is Username : @{msg.from_user.username} \n - Is Id : {msg.from_user.id}.")
    except:
        open("members.txt", "w")
        if str(msg.chat.id) in open("members.txt", "r").read():
            print("Done Save id : " + str(msg.chat.id) + " ok")
        else:
            print("Done Save id : " + str(msg.chat.id))
            open("members.txt", "a").write(str(msg.chat.id) + "\n")
            bot.send_message(SUDO, f"New Member Now\n - is Name : {msg.from_user.first_name} \n - is Username : @{msg.from_user.username} \n - Is Id : {msg.from_user.id}.")



@bot.on_callback_query()
def addnumber(bot, CallbackQuery):
    if CallbackQuery.data == "addnumber":
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('الغاء', callback_data=f"back"),
            ],
        ])
        bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,
                              f"حسناً، قم بأرسال رقم الهاتف بهذهِ الصيغة: \n\n `077********`", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)
        open(f"{CallbackQuery.message.chat.id}.txt", "w").write("bg")
    elif CallbackQuery.data.split("#")[0] == "info":
        fbg = open(f"access_token{CallbackQuery.message.chat.id}.txt", "r")
        bgc = int(CallbackQuery.data.split("#")[1])
        x = asiacell2("profile", {'Authorization': 'Bearer ' + open(f"access_token{CallbackQuery.message.chat.id}.txt",
                      "r").readlines()[bgc].replace("\n", ''), 'DeviceID': '6cf77389aa2b259c2951a12b3bad0175', })
        print(json.dumps(x))
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تحويل الرصيد', callback_data=f"addrsud#" + str(bgc)),
                InlineKeyboardButton('تعبئة الرصيد', callback_data=f"addfull#" + str(bgc)),
            ],
            [
                InlineKeyboardButton('رجوع', callback_data=f"back"),
            ],
        ])
        bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,
                              f"معلومات حول هذا الهاتف ( " + str(x['data']['bodies'][0]['items'][0]['phoneNumber']) + " ) \n\n الرصيد الحالي : ( " + str(x['data']['bodies'][1]['items'][0]['value']) + ").", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)
    elif CallbackQuery.data.split("#")[0] == "addfull":
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('الغاء', callback_data=f"back"),
            ],
        ])
        bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,
                              f"ادخل رقم البطاقة المكون من 13 او 14 رقم", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)
        open(f"{CallbackQuery.message.chat.id}.txt", "w").write("full")
        open(f"BG{CallbackQuery.message.chat.id}.txt", "w").write(CallbackQuery.data.split("#")[1])
    elif CallbackQuery.data == "addrsud":
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('الغاء', callback_data=f"back"),
            ],
        ])
        bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,
                              f"حسناً، قم بأرسال رقم الهاتف المراد تحويل له بهذهِ الصيغة: \n\n `077********`", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)
        open(f"{CallbackQuery.message.chat.id}.txt", "w").write("rsud")
    elif CallbackQuery.data == "back":
        try:
            os.remove(f"{CallbackQuery.message.chat.id}.txt")
        except:
            None
        bot.delete_messages(CallbackQuery.message.chat.id,
                            CallbackQuery.message.id)
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('اضف هاتف', callback_data=f"addnumber"),
            ],
            [
                InlineKeyboardButton(
                    'قائمة الهواتف المضافة', callback_data=f"knumbers"),
            ],
            [
                InlineKeyboardButton('كيفية استخدام البوت',
                                     callback_data=f"help"),
            ],
        ])
        bot.send_message(CallbackQuery.message.chat.id,
                         f"مرحبا بك عزيزي المستخدم،\nيمكنك التحكم في شريحة هاتفك،\n( الاسياسيل ) من خلال هذا البوت.", reply_markup=reply_markup)
    elif CallbackQuery.data == "help":
        open(f"{CallbackQuery.message.chat.id}.txt", "w")
        bot.delete_messages(CallbackQuery.message.chat.id,
                            CallbackQuery.message.id)
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('رجوع', callback_data=f"back"),
            ],
        ])
        bot.send_video(CallbackQuery.message.chat.id, "https://t.me/ALSH_3K/98",
                       f"فيديو شرح كيفية استخدام البوت.", reply_markup=reply_markup)
    elif CallbackQuery.data == "knumbers":
        try:
            ii = -1
            botm = []
            for i in open(f"access_token{CallbackQuery.message.chat.id}.txt", "r").readlines():
                ii += 1
                botm.append([InlineKeyboardButton(
                    ii, callback_data=f"info#" + str(ii))])
                print(ii)
            botm.append([InlineKeyboardButton("رجوع", callback_data=f"back")])

            reply_markup = InlineKeyboardMarkup(botm)
            bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,f"قائمة الهواتف المضافة.", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)
        except:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.edit_message_text(CallbackQuery.message.chat.id, CallbackQuery.message.id,f"لا يوجد الهواتف المضافة.", enums.ParseMode.MARKDOWN, reply_markup=reply_markup)


xx = 0


@bot.on_message(filters.text)
def sendmember(bot, msg):
    f = open(f"{msg.chat.id}.txt", "r").read()
    if len(msg.text) == 11 and f == "bg":
        if "077" in msg.text:
            bot.delete_messages(msg.chat.id, msg.id-1)
            x = asiacell("captcha", {}, {'DeviceID': '6cf77389aa2b259c2951a12b3bad0175'})[
                'captcha']
            image = x['originSource'] + x['resourceUrl']
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('الغاء', callback_data=f"back"),
                ],
            ])
            bot.send_photo(
                msg.chat.id, image, f"أرسل رمز التحقق الموجود في الصورة اعلاه.", reply_markup=reply_markup)
            open(f"{msg.chat.id}.txt", "w").write("sendmember")
            open(f"BG{msg.chat.id}.txt", "w").write(msg.text)
        else:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('الغاء', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, "رقم الهاتف غير صحيح", reply_markup=reply_markup)

    elif len(msg.text) == 6 and f == "sendmember":
        bot.delete_messages(msg.chat.id, msg.id-1)
        number = open(f"BG{msg.chat.id}.txt", "r").read()
        x = asiacell("loginV2", {"username": number, "captchaCode": msg.text}, {
                     'DeviceID': '6cf77389aa2b259c2951a12b3bad0175'})
        if x['success'] == True:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('الغاء', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, x['message'], reply_markup=reply_markup)
            open(f"{msg.chat.id}.txt", "w").write("sendcode")
            PID = x['nextUrl'].split("PID=")[1]
            open(f"BG{msg.chat.id}.txt", "w").write(PID)
        elif x['message'] != "Invalid captcha" and x['success'] == False:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            #bot.send_message(msg.chat.id, "لقد قمت بأرسال رمز تحقق خاطئ.", reply_markup=reply_markup)
            bot.send_message(
                msg.chat.id, x['message'], reply_markup=reply_markup)
        elif x['message'] == "Invalid captcha" and x['success'] == False:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, "لقد قمت بأرسال رمز تحقق خاطئ.", reply_markup=reply_markup)
    elif len(msg.text) == 6 and f == "sendcode":
        bot.delete_messages(msg.chat.id, msg.id-1)
        PID = open(f"BG{msg.chat.id}.txt", "r").read()
        x = asiacell("smsvalidation", {"PID": PID, "passcode": msg.text}, {
                     'DeviceID': '6cf77389aa2b259c2951a12b3bad0175'})
        print(json.dumps(x))
        if x['success'] == True:
            try:
                f = open(f"access_token{msg.chat.id}.txt", "r")
                global xx
                xx = len(f.readlines())-1
            except:
                open(f"access_token{msg.chat.id}.txt", "w")
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        'معلومات الهاتف', callback_data=f"info#" + str(xx)),
                ],
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, "تم تسجيل دخول  بهذا الهاتف ( " + x['username'] + " ) بنجاح.", reply_markup=reply_markup)
            open(f"access_token{msg.chat.id}.txt", "a").write(
                x['access_token'] + "\n")
            os.remove(f"BG{msg.chat.id}.txt")
        elif x['success'] == False:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, "لقد قمت بأرسال رمز تسجيل دخول خاطئ.", reply_markup=reply_markup)
    elif len(msg.text) == 13 and f == "full" or len(msg.text) == 14 and f == "full":
        bot.delete_messages(msg.chat.id, msg.id-1)
        bgc = int(open(f"BG{msg.chat.id}.txt","r").read())
        x = asiacell("top-up", {"iccid":'null',"voucher":int(msg.text),"msisdn":'null',"rechargeType":1},{'Authorization': 'Bearer '+open(f"access_token{msg.chat.id}.txt","r").readlines()[bgc].split("\n")[0],'DeviceID': '6cf77389aa2b259c2951a12b3bad0175',})
        print(json.dumps(x))
        if x['success'] == True:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.send_message(
                msg.chat.id, "تم التعبئة بالنجاح.", reply_markup=reply_markup)
            os.remove(f"BG{msg.chat.id}.txt")
        elif x['success'] == False:
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('رجوع', callback_data=f"back"),
                ],
            ])
            bot.send_message(msg.chat.id, "رقم الكرت او البطاقة غير صالحة.", reply_markup=reply_markup)
            os.remove(f"BG{msg.chat.id}.txt")


bot.run()
