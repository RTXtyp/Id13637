import os
import telebot
from telebot import types
from random import shuffle
import django
django.setup()
from math_test.models import Question

API_TOKEN = '6556025703:AAELbyGavxR9JYf9y4PQY1ATHyYqv2cfAwI'

bot = telebot.TeleBot(API_TOKEN)

answers = []
questions = []
user_answers = []
correct_count = 0
incorrect_count = 0

def load_questions():
    db = Question.objects.all()
    for question in db:
        questions.append(question.question)
        answers.append([question.a, question.b, question.c])
        
def make_keyboard(question_id):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for answer_id, answer in enumerate(answers[question_id]):
        buttons.append(types.InlineKeyboardButton(text=answer, callback_data=f"{question_id}_{answer_id}"))
    shuffle(buttons)
    for button in buttons:
        markup.add(button)
    return markup

@bot.message_handler(commands=['test'])
def handle_test(msg):
    load_questions()
    bot.send_message(chat_id=msg.chat.id,
                     text=questions[0],
                     reply_markup=make_keyboard(0),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(cb):
    global user_answers
    global correct_count
    global incorrect_count
    
    question_id, answer_id = cb.data.split("_")
    user_answer = answers[int(question_id)][int(answer_id)]
    user_answers.append(user_answer)
    
    if user_answer == answers[int(question_id)][0]:
        correct_count += 1
    else:
        incorrect_count += 1
    
    if len(questions) > int(question_id) + 1:
        bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id,
                              text=questions[int(question_id) + 1], reply_markup=make_keyboard(int(question_id) + 1))
    else:
        bot.send_message(chat_id=cb.message.chat.id, text="Test is over.")
        bot.send_message(chat_id=cb.message.chat.id, text=f"Correct answers: {correct_count}")
        bot.send_message(chat_id=cb.message.chat.id, text=f"Incorrect answers: {incorrect_count}")
        bot.send_message(chat_id=cb.message.chat.id, text="Your answers:")
        for i, answer in enumerate(user_answers):
            bot.send_message(chat_id=cb.message.chat.id, text=f"Question {i+1}: {answer}")
    
bot.infinity_polling()