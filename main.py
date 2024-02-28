
# TG related libraries and modules
import telebot
from telebot import types
import re
from random import choice
from module import user_datapdf_creation

# Database and credential connection related libraries and modules
import psycopg2
from module import database
import os
from dotenv import load_dotenv
import time
load_dotenv()


PAYMENT_TOKEN = os.environ["PAYMENT_TOKEN"]
TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)

usersall = {}

# Handler to start the bot and request the user's full name


@bot.message_handler(commands=['start'])
def start(message):

    connection = get_connection()
    user_data_from_db = database.get_user_data(
        connection, user_id=str(message.from_user.id))

    # try:
    #     print('full set')
    #     print(user_data_from_db)
    #     print()
    #     # print(user_data_from_db[0])
    #     print('id')
    #     print()
    #     print(user_data_from_db[0][0])
    #     print()
    #     print('set only 1 try')
    #     print(user_data_from_db[0][1])
    #     print()
    #     # print('set only 2 try')
    #     # print(user_data_from_db[0][1][str(message.from_user.id)])
    #     print()
    #     print('good')
    # except:
    #     pass

    # if message.from_user.id in database:
    if len(user_data_from_db) > 0:
        usersall[int(user_data_from_db[0][0])] = user_data_from_db[0][1]

        bot.send_message(
            message.chat.id, f"Hey, {usersall[message.from_user.id]['full_name']}! \U0001F44B \nWelcome back to the CV Bot!\nWhat are you going to do?")
        menu_options(message)
        return
    else:

        usersall[message.from_user.id] = {
            'flag': 'fill', 'cw': 0, 'ce': 0, 'skil': 0}
        usersall[message.from_user.id]["skills"] = {}
        usersall[message.from_user.id]["work_exp"] = {}
        usersall[message.from_user.id]["edu_exp"] = {}

        # if first and last names are mentioned in Telegram users info
        if message.from_user.first_name and message.from_user.last_name:
            bot.send_message(
                message.chat.id, f"Hey, <b>{message.from_user.first_name} {message.from_user.last_name}</b>! \U0001F44B  \nWelcome to the CV Bot! \nI will help you to create your best CV.\nLet's start!",
                parse_mode='HTML')
            usersall[message.from_user.id][
                'full_name'] = f"{message.from_user.first_name} {message.from_user.last_name}"

            keep_or_change = f"\nDo you want to change your name on your CV or leave it as {message.from_user.first_name} {message.from_user.last_name}?"

            keyboard = types.InlineKeyboardMarkup()
            keep_btn = types.InlineKeyboardButton(
                text="Keep It \U0001F64C", callback_data="keep_name")
            change_btn = types.InlineKeyboardButton(
                text="Change It \U0001F504", callback_data="change_name")
            keyboard.add(keep_btn, change_btn)
            bot.send_message(message.chat.id, keep_or_change,
                             reply_markup=keyboard)
        # condition if there are no first and last names
        else:
            bot.send_message(
                message.chat.id, f"Hey, {message.from_user.username}! \U0001F44B \nWelcome to the CV Bot! \nI will help you to create your best CV. \nLets start! \nWhat's your full name? \n( Ex: Hans Guberman )")
            bot.register_next_step_handler(message, get_full_name)


# filling func
def get_full_name(message):
    # pattern checks the correctness of the entered text
    pattern = r'^[a-zA-Z\s]+$'

    # checking if message is text
    if check_type_message(message, get_full_name):
        return
    else:
        usersall[message.from_user.id]['full_name'] = message.text
        # pattern checking
        if re.match(pattern, message.text):
            bot.send_message(
                message.chat.id, f"Great, {usersall[message.from_user.id]['full_name']}!")
            print('NAME - ', message.from_user.id)
            print('SET -  ', usersall[message.from_user.id])
            add_user(message.from_user.id, usersall[message.from_user.id])
            menu_options(message)
            return
        # pattern checking error
        else:
            check_invalid_pattern(message, get_full_name, pattern)


def get_position(message, edit=False):
    # pattern checks the correctness of the entered text
    pattern = r'[a-zA-Z\s&\(\)]+$'
    # checking if message is text
    if check_type_message(message, get_position):
        return

    # pattern checking
    if re.match(pattern, message.text):
        usersall[message.from_user.id]['position'] = message.text
        # if editing process
        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Position was successfully updated!")
            menu_options(message)
        # if not edit, moving to the next step
        else:
            bot.send_message(
                message.chat.id, f"Great choice! \n\U0001F4CD What is your current place of residence? \n( Ex: Berlin, Germany )")
            bot.register_next_step_handler(message, get_residence)
    # pattern checking error
    else:
        check_invalid_pattern(message, get_position, pattern)


def get_residence(message, edit=False):
    pattern = r'^[A-Za-z\s]+([ ,\s-]+)?([A-Za-z\s]+)?$'

    if check_type_message(message, get_residence):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['residence'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Residence was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Got it! \n\u2709 What is your email? \n( Ex: hans.guber@gmail.com )")
            bot.register_next_step_handler(message, get_email)
    else:
        check_invalid_pattern(message, get_residence, pattern)


def get_email(message, edit=False):
    pattern = r'^([A-Za-z0-9\.-_]+)?[A-Za-z0-9]+@[A-Za-z0-9-]+.[A-Za-z]+$'
    if check_type_message(message, get_email):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['email'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Email was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Data is saved! \n\U0001F517 What is the link to your Portfolio? \n( Ex: https://www.linkedin.com/in/hans-guberman/ )")
            bot.register_next_step_handler(message, get_portfolio)
    else:
        check_invalid_pattern(message, get_email, pattern)


def get_portfolio(message, edit=False):
    pattern = r'^(https?|ftp)://(www\.)?.{3,}$'
    if check_type_message(message, get_portfolio):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['portfolio'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your link to the Portfolio was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, "All right! \U0001F525\U0001F525\U0001F525 \nYou filled your Personal Information Section. \nWhat is next?")
            menu_options(message)
    else:
        check_invalid_pattern(message, get_portfolio, pattern)


def get_about_me(message, edit=False):
    if check_type_message(message, get_about_me):
        return
    else:
        usersall[message.from_user.id]['about_me'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your About Me Section was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, "Well done! \U0001F525\U0001F525\U0001F525 \n You complete About Me section. \nWhat is your next step?")
            menu_options(message)


def get_work_name(message, work_n, edit=False):

    pattern = r'^[a-zA-Z0-9\s\-,]+$'

    if check_type_message(message, get_work_name, work_edu_n=work_n, edit=edit):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['work_exp'][f'work{work_n}']['work_name'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Work Comapany Name was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Great! \nWhat is/was your position there? \n( Ex: Assistant Marketing Director )")
            bot.register_next_step_handler(
                message, get_pos_work, work_n=work_n)
    else:
        check_invalid_pattern(message, get_work_name,
                              pattern, work_edu_n=work_n, edit=edit)


def get_pos_work(message, work_n, edit=False):

    pattern = r'[a-zA-Z\s&\(\)]+$'

    if check_type_message(message, get_pos_work, work_edu_n=work_n, edit=edit):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['work_exp'][f'work{work_n}']['pos_work'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Work Position was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Cool! \nHow long are/were you employed there? \n( Ex: September 2022 — July 2023 )\n( Ex: August 2021 — up to now )")
            bot.register_next_step_handler(
                message, get_beg_end_work, work_n=work_n)
    else:
        check_invalid_pattern(message, get_pos_work,
                              pattern, work_edu_n=work_n, edit=edit)


def get_beg_end_work(message, work_n, edit=False):
    pattern = r'^[a-zA-Z ]+(\d{4})[ ,\—\-\s]+(([a-zA-Z ]+(\d{4}))|(up to now))$'

    if check_type_message(message, get_beg_end_work, work_edu_n=work_n, edit=edit):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id]['work_exp'][f'work{work_n}']['start_end_work'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Period of Employment was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Awesome! \nPlease describe your main responsibilities. \n( Ex: Creating markiting design posters... )")
            bot.register_next_step_handler(
                message, get_desc_work, work_n=work_n)
    else:
        check_invalid_pattern(message, get_beg_end_work,
                              pattern, work_edu_n=work_n, edit=edit)


def get_desc_work(message, work_n, edit=False):
    if check_type_message(message, get_desc_work, work_edu_n=work_n, edit=edit):
        return

    else:
        usersall[message.from_user.id]['work_exp'][f'work{work_n}']['desc_work'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Work Description Section was successfully updated!")
            menu_options(message)

        # suggest a new field entering
        else:
            another_work = "Do you have any other work experience you'd like to add?"

            keyboard = types.InlineKeyboardMarkup()
            yes_btn = types.InlineKeyboardButton(
                text="YES \U00002705", callback_data="another_work")
            no_btn = types.InlineKeyboardButton(
                text="NO \U0000274C", callback_data="no_more_work")
            keyboard.add(yes_btn, no_btn)
            bot.send_message(message.chat.id, another_work,
                             reply_markup=keyboard)


def get_study_name_course(message, edu_n, edit=False):
    pattern = r'^[A-Za-z\D\s]+$'

    if check_type_message(message, get_study_name_course, work_edu_n=edu_n, edit=edit):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id][f'edu_exp'][f'edu{edu_n}']['educate_name'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Educational Institution and Programm were successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Nice place! \nWhere is it located? \n( Ex: Paris, France )")
            bot.register_next_step_handler(
                message, get_study_location, edu_n=edu_n)
    else:
        check_invalid_pattern(message, get_study_name_course,
                              pattern, work_edu_n=edu_n, edit=edit)


def get_study_location(message, edu_n, edit=False):
    pattern = r'^[A-Za-z\s]+([ ,\s-]+)?([A-Za-z\s]+)?$'

    if check_type_message(message, get_study_location, work_edu_n=edu_n, edit=edit):
        return
    elif re.match(pattern, message.text):
        usersall[message.from_user.id][f'edu_exp'][f'edu{edu_n}']['educate_place'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Educational Institution Location was successfully updated!")
            menu_options(message)
        else:
            bot.send_message(
                message.chat.id, f"Cool! \nHow long have you studied? \n( Ex: January 2015 — March 2017 )\n( Ex: October 2019 — up to now )")
            bot.register_next_step_handler(
                message, get_beg_end_study, edu_n=edu_n)
    else:
        check_invalid_pattern(message, get_study_location,
                              pattern, work_edu_n=edu_n, edit=edit)


def get_beg_end_study(message, edu_n, edit=False):
    pattern = r'^[a-zA-Z ]+(\d{4})[ ,\—\-\s]+(([a-zA-Z ]+(\d{4}))|(up to now))$'

    if check_type_message(message, get_beg_end_study, work_edu_n=edu_n, edit=edit):
        return

    elif re.match(pattern, message.text):
        usersall[message.from_user.id][f'edu_exp'][f'edu{edu_n}']['start_end_study'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Period of Study was successfully updated!")
            menu_options(message)
        else:
            another_educate = "Have you studied another place you'd like to add?"

            keyboard = types.InlineKeyboardMarkup()
            yes_btn = types.InlineKeyboardButton(
                text="YES \U00002705", callback_data="another_educate")
            no_btn = types.InlineKeyboardButton(
                text="NO \U0000274C", callback_data="no_more_educate")
            keyboard.add(yes_btn, no_btn)
            bot.send_message(message.chat.id, another_educate,
                             reply_markup=keyboard)
    else:
        check_invalid_pattern(message, get_beg_end_study,
                              pattern, work_edu_n=edu_n, edit=edit)


def get_skills(message, skil_n, edit=False):
    pattern = r'^[a-zA-Z\D\s]+$'

    if check_type_message(message, get_skills, work_edu_n=skil_n):
        return

    elif re.match(pattern, message.text):
        usersall[message.chat.id]['skills'][f'skill{skil_n}'] = message.text

        if edit:
            bot.send_message(
                message.chat.id, f"\u2705 Your Skills Section was successfully updated!")
            menu_options(message)
        else:
            another_skill = "Do you have another Skill you'd like to add?"

            keyboard = types.InlineKeyboardMarkup()
            yes_btn = types.InlineKeyboardButton(
                text="YES \U00002705", callback_data="another_skill")
            no_btn = types.InlineKeyboardButton(
                text="NO \U0000274C", callback_data="no_more_skill")
            keyboard.add(yes_btn, no_btn)
            bot.send_message(message.chat.id, another_skill,
                             reply_markup=keyboard)

    else:
        check_invalid_pattern(message, get_skills, pattern, work_edu_n=skil_n)


# output of all fields of contact info (editting)
def edit_contact_info(message):
    keyboard = types.InlineKeyboardMarkup()

    position = types.InlineKeyboardButton(
        text="Position \U0001F454", callback_data="edit_position")
    residence = types.InlineKeyboardButton(
        text="Residence \U0001F3E0", callback_data="edit_residence")
    email = types.InlineKeyboardButton(
        text="Email \U0001F4E7", callback_data="edit_email")
    portfolio = types.InlineKeyboardButton(
        text="Portfolio \U0001F4C3", callback_data="edit_portfolio")
    back_button = types.InlineKeyboardButton(
        text="Back \U000021A9", callback_data="menu")
    keyboard.add(position, residence, email, portfolio, back_button)
    bot.send_message(message.chat.id, 'What you want to edit?',
                     reply_markup=keyboard)


# output by company names of all work experinces (editting / displaying (show = True if display))
def choose_work_exp(message, show=False):
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(text="Back", callback_data="menu")
    emojis = ["\U0001F3E2", "\U0001F4C8", "\U0001F310"]

    # creating all work experiences based on work counter
    for i in range(1, usersall[message.chat.id]['cw'] + 1):
        #  if displaying changing callback_data for handlers
        if show:
            callback_data = f"show_which_work{i}"
        else:
            callback_data = f"edit_which_work{i}"
        text = usersall[message.chat.id][f'work_exp'][f'work{i}'][f'work_name']

        which_work = types.InlineKeyboardButton(
            text=f"{text} {choice(emojis)}", callback_data=callback_data)
        keyboard.add(which_work)
    keyboard.add(back_button)
    bot.send_message(
        message.chat.id, 'Which Work Experience you want to change?', reply_markup=keyboard)


# output of all fields of work experince (editting)
def edit_work_exp(message, work_n):
    keyboard = types.InlineKeyboardMarkup()

    work_name = types.InlineKeyboardButton(
        text="Comapany Name \U0001F3DB", callback_data=f"edit_work_name{work_n}")
    pos_work = types.InlineKeyboardButton(
        text="Position \U0001F4BC", callback_data=f"edit_pos_work{work_n}")
    get_beg_end_work = types.InlineKeyboardButton(
        text=f"Period of Employment \U0001F550", callback_data=f"edit_get_beg_end_work{work_n}")
    desc_work = types.InlineKeyboardButton(
        text=f"Description \U0001F4D6", callback_data=f"edit_desc_work{work_n}")
    back_button = types.InlineKeyboardButton(
        text=f"Back \U000021A9", callback_data="menu")
    keyboard.add(work_name, pos_work, get_beg_end_work, desc_work, back_button)
    bot.send_message(message.chat.id, 'What you want to edit?',
                     reply_markup=keyboard)


def choose_edu_exp(message, show=False):
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(text="Back", callback_data="menu")
    emojis = ["\U0001F3EB", "\U0001F4DA", "\U0001F393", "\U0001F4D6"]

    for i in range(1, usersall[message.chat.id]['ce'] + 1):
        if show:
            callback_data = f"show_which_study{i}"
        else:
            callback_data = f"edit_which_study{i}"
        text = usersall[message.chat.id][f'edu_exp'][f'edu{i}'][f'educate_name']

        which_edu = types.InlineKeyboardButton(
            text=f"{text} {choice(emojis)}", callback_data=callback_data)

        keyboard.add(which_edu)
    keyboard.add(back_button)
    bot.send_message(
        message.chat.id, 'Which Education Place you want to change?', reply_markup=keyboard)


def edit_education(message, edu_n):
    keyboard = types.InlineKeyboardMarkup()

    educate_name = types.InlineKeyboardButton(
        text=f"Name and Programm \U0001F4D6", callback_data=f"edit_educate_name{edu_n}")
    educate_place = types.InlineKeyboardButton(
        text=f"Location \U0001F3EB", callback_data=f"edit_educate_place{edu_n}")
    start_end_study = types.InlineKeyboardButton(
        text=f"Period of Study \U0001F553", callback_data=f"edit_start_end_study{edu_n}")
    back_button = types.InlineKeyboardButton(
        text=f"Back \U000021A9", callback_data="menu")
    keyboard.add(educate_name, educate_place, start_end_study, back_button)
    bot.send_message(message.chat.id, 'What you want to edit?',
                     reply_markup=keyboard)


def choose_skill(message, show=False):
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(text="Back", callback_data="menu")
    emojis = ["\U0001F6E0", "\U0001F9E0"]

    for i in range(1, usersall[message.chat.id]['skil'] + 1):
        if show:
            callback_data = f"show_which_skill{i}"
        else:
            callback_data = f"edit_which_skill{i}"

        text = usersall[message.chat.id][f'skills'][f'skill{i}']

        which_skill = types.InlineKeyboardButton(
            text=f"{text} {choice(emojis)}", callback_data=callback_data)

        keyboard.add(which_skill)
    keyboard.add(back_button)
    bot.send_message(
        message.chat.id, 'Which Skill you want to change?', reply_markup=keyboard)


def confirm_to_del(message, edu_work, n):
    keyboard = types.InlineKeyboardMarkup()

    yes_btn = types.InlineKeyboardButton(
        text="YES \U00002705", callback_data=f"yes_del_{edu_work}{n}")
    no_btn = types.InlineKeyboardButton(
        text="NO \U0000274C", callback_data=f"no_del_{edu_work}{n}")

    keyboard.add(yes_btn, no_btn)
    bot.send_message(
        message.chat.id, 'The data will be permanently lost \U0001F631\nAre you sure you want to delete this data ?', reply_markup=keyboard)


# displaying menu section
def menu_options(message):
    menu = f"<b>Menu options</b>" + '\n' \
        f"{'_'*30}\n" \
        f"{'.'*11}Personal Information{'.'*13}\n" \
        f"{'.'*20}About Me{'.'*20}\n" \
        f"{'.'*14}Work Experience{'.'*15}\n" \
        f"{'.'*20}Education{'.'*20}\n" \
        f"{'.'*24}Skills{'.'*24}\n" \

    keyboard = types.InlineKeyboardMarkup()
    choose_button = types.InlineKeyboardButton(
        text="Fill data \U0001F4DD", callback_data="fill")
    edit_button = types.InlineKeyboardButton(
        text="Edit data \U0001F527", callback_data="edit")
    check_data = types.InlineKeyboardButton(
        text="Check data \U0001F50D", callback_data="check")
    delete_button = types.InlineKeyboardButton(
        text="Delete data \U0001F5D1", callback_data="delete")

    keyboard.add(choose_button, edit_button, check_data, delete_button)
    bot.send_message(message.chat.id, menu,
                     reply_markup=keyboard, parse_mode='HTML')


# handler which accepts every call EXCEPT calls starting with "edit_"
@bot.callback_query_handler(func=lambda call: True if str(call.data)[:5] != 'edit_' else False)
def callback_handler_option(call):

    if call.data != "keep_name" or call.data != "change_name":
        edit_user(str(call.from_user.id), usersall[call.from_user.id])

    # variable True when call is edit (activates only when callling function "menu_option")
    edit_or_not = True if usersall[call.from_user.id]['flag'] == 'edit' else False

    # checking if funcation "menu_options" is called
    if call.data == 'fill' or call.data == 'check' or call.data == 'edit':
        # changing the flag onlu from "menu_options" call
        usersall[call.from_user.id]['flag'] = call.data

        keyboard = types.InlineKeyboardMarkup()
        contact_info = types.InlineKeyboardButton(
            text="Personal Information \U0001F464", callback_data="contact_info")
        about_me = types.InlineKeyboardButton(
            text="About Me \U0001F44B", callback_data="about_me")
        work_exp = types.InlineKeyboardButton(
            text="Work Experience \U0001F4BC", callback_data="work_exp")
        education = types.InlineKeyboardButton(
            text="Education \U0001F4D6", callback_data="education")
        skills = types.InlineKeyboardButton(
            text="Skills \U0001F4CA", callback_data="skills")
        menu = types.InlineKeyboardButton(
            text="Back \U000021A9", callback_data="menu")
        keyboard.add(contact_info, about_me, work_exp, education, skills, menu)

        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text='Choose the group:', reply_markup=keyboard)

    elif call.data == 'menu':
        menu_options(call.message)

    elif call.data == 'delete':
        usersall[call.from_user.id]['flag'] = call.data

        keyboard = types.InlineKeyboardMarkup()
        del_work_exp = types.InlineKeyboardButton(
            text="Work Experience \U0001F4BC\u2192\U0001F5D1", callback_data="del_work_exp")
        del_education = types.InlineKeyboardButton(
            text="Education \U0001F4D6\u2192\U0001F5D1", callback_data="del_education")
        del_skills = types.InlineKeyboardButton(
            text="Skills \U0001F4CA\u2192\U0001F5D1", callback_data="del_skills")
        menu = types.InlineKeyboardButton(
            text="Back \U000021A9", callback_data="menu")

        keyboard.add(del_work_exp, del_education, del_skills, menu)

        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text='Choose the group in which you want to delete data:', reply_markup=keyboard)

    elif usersall[call.from_user.id]['flag'] == 'delete':

        if call.data == 'del_work_exp':
            if usersall[call.from_user.id]["cw"] != 0:
                choose_work_exp(call.message, show=True)
            elif usersall[call.from_user.id]["cw"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Work Experience Section is empty \U0001F914\nPlease fill your Work Experience Section firstly")
                menu_options(call.message)
        # finding work_exp user want to delete
        elif str(call.data)[:15] == 'show_which_work':
            # generating info user want to delete
            generate_work_exp(call.message, work_n=str(
                call.data)[15:], menu_show=False)
            # confirm user sure he wants to delete
            confirm_to_del(call.message, edu_work='work',
                           n=str(call.data)[15:])
        elif str(call.data)[:12] == 'yes_del_work':
            keys_to_rename = []
            company_name_del = usersall[call.from_user.id][
                'work_exp'][f"work{str(call.data)[12:]}"]['work_name']
            # checking for renaming different work_exp
            for key in usersall[call.from_user.id]['work_exp']:
                if int(key[4:]) > int(str(call.data)[12:]):
                    keys_to_rename += [key]
            # deleting work_exp user want to delete
            for each in keys_to_rename:
                new_key = f'work{(int(each[4:]) - 1)}'
                usersall[call.from_user.id]['work_exp'][f'{new_key}'] = usersall[call.from_user.id]['work_exp'].pop(
                    each)
            #  decreasing the counter of work_exp
            usersall[call.from_user.id]['cw'] -= 1
            bot.send_message(
                call.from_user.id, f"Well done! \U0001F44D\nYou successfully deleted your <b><u>{company_name_del}</u></b> data", parse_mode='HTML')
            menu_options(call.message)
        elif str(call.data)[:11] == 'no_del_work':
            menu_options(call.message)

        elif call.data == 'del_education':
            if usersall[call.from_user.id]["ce"] != 0:
                choose_edu_exp(call.message, show=True)
            elif usersall[call.from_user.id]["ce"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Education Section is empty \U0001F914\nPlease fill your Education Section firstly")
                menu_options(call.message)
        elif str(call.data)[:16] == 'show_which_study':
            generate_education(call.message, edu_n=str(
                call.data)[16:], menu_show=False)
            confirm_to_del(call.message, edu_work='edu', n=str(call.data)[16:])

        elif str(call.data)[:11] == 'yes_del_edu':
            keys_to_rename = []
            study_name_del = usersall[call.from_user.id]['edu_exp'][
                f"edu{str(call.data)[11:]}"]['educate_name']

            for key in usersall[call.from_user.id]['edu_exp']:
                if int(key[3:]) > int(str(call.data)[11:]):
                    keys_to_rename += [key]

            for each in keys_to_rename:
                new_key = f'edu{(int(each[3:]) - 1)}'
                usersall[call.from_user.id]['edu_exp'][f'{new_key}'] = usersall[call.from_user.id]['edu_exp'].pop(
                    each)

            usersall[call.from_user.id]['ce'] -= 1
            bot.send_message(
                call.from_user.id, f"Well done! \U0001F44D\nYou successfully deleted your <b><u>{study_name_del}</u></b> data", parse_mode='HTML')
            menu_options(call.message)
        elif str(call.data)[:10] == 'no_del_edu':
            menu_options(call.message)

        elif call.data == 'del_skills':
            if usersall[call.from_user.id]["skil"] != 0:
                choose_skill(call.message, show=True)
            elif usersall[call.from_user.id]["skil"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Skill Section is empty \U0001F914\nPlease fill your Skill Section firstly")
                menu_options(call.message)
        elif str(call.data)[:16] == 'show_which_skill':
            keys_to_rename = []
            skill_to_del = usersall[call.from_user.id][
                'skills'][f"skill{str(call.data)[16:]}"]

            for key in usersall[call.from_user.id]['skills']:
                if int(key[5:]) > int(str(call.data)[16:]):
                    keys_to_rename += [key]

            for each in keys_to_rename:
                new_key = f'skill{(int(each[5:]) - 1)}'
                usersall[call.from_user.id]['skills'][f'{new_key}'] = usersall[call.from_user.id]['skills'].pop(
                    each)

            usersall[call.from_user.id]['skil'] -= 1
            bot.send_message(
                call.from_user.id, f"Well done! \U0001F44D\nYou successfully deleted your <b><u>{skill_to_del}</u></b> data", parse_mode='HTML')
            menu_options(call.message)

    elif call.data == 'keep_name':
        # pattern for keeping full name from Telegram user info
        pattern = r'^[a-zA-Z\s]+$'
        if re.match(pattern, usersall[call.from_user.id]['full_name']):
            add_user(call.from_user.id, usersall[call.from_user.id])
            bot.send_message(call.from_user.id,
                             "Nice! \nWhat are you going to do?")
            menu_options(call.message)
        else:
            check_invalid_pattern(
                call.message, get_full_name, pattern)

    elif call.data == 'change_name':
        bot.send_message(
            call.from_user.id, "Got it! \nThen what is your full name? \n( Ex: Hans Guberman )")
        bot.register_next_step_handler(call.message, get_full_name)

    elif call.data == 'another_work':
        # increasing work exprerience counter
        usersall[call.from_user.id]['cw'] += 1
        number_of_work_exp = usersall[call.from_user.id]['cw']
        # creating new dict for new work experience
        usersall[call.from_user.id]['work_exp'][f'work{number_of_work_exp}'] = {
        }
        bot.send_message(
            call.from_user.id, "Got it! \n What is the Name of the Company? \n( Ex: Yandex LLC )")
        # filling new work experience
        bot.register_next_step_handler(
            call.message, get_work_name, number_of_work_exp, edit=True)

    elif call.data == 'no_more_work':
        bot.send_message(
            call.from_user.id, f"Cool! \U0001F525\U0001F525\U0001F525 \nYou filled Work Experience Section. \nWhat is next?")
        menu_options(call.message)

    elif call.data == 'another_educate':
        usersall[call.from_user.id]['ce'] += 1
        number_of_edu_exp = usersall[call.from_user.id]['ce']
        usersall[call.from_user.id]['edu_exp'][f'edu{number_of_edu_exp}'] = {}
        bot.send_message(
            call.from_user.id, "Cool! \nWhat are the Name of Place and Programm you are/were studying? \n( Ex: University of Applied Sciences (Data Analytics) )")
        bot.register_next_step_handler(
            call.message, get_study_name_course, number_of_edu_exp, edit=False)

    elif call.data == 'no_more_educate':
        bot.send_message(
            call.from_user.id, f"Well done! \U0001F525\U0001F525\U0001F525\nYou filled Education Section. \nWhat is next?")
        menu_options(call.message)

    elif call.data == 'another_skill':
        usersall[call.from_user.id]['skil'] += 1
        number_of_skills = usersall[call.from_user.id]['skil']
        usersall[call.from_user.id]['skills'][f'skill{number_of_skills}'] = ''
        bot.send_message(
            call.from_user.id, "Great! \n Which Skill you want to add? \n( Ex: Good at negotiations )")
        bot.register_next_step_handler(
            call.message, get_skills, number_of_skills, edit=False)

    elif call.data == 'no_more_skill':
        bot.send_message(
            call.from_user.id, f"WOW! \nYou filled Skills Section. \nWhat is next?")
        menu_options(call.message)

    # if displaying (flag == check)
    elif usersall[call.from_user.id]['flag'] == "check":
        if call.data == "contact_info":
            generate_contact_info(call.message)

        elif call.data == "about_me":
            generate_about_me(call.message)

        elif call.data == "work_exp":
            if usersall[call.from_user.id]["cw"] != 0:
                choose_work_exp(call.message, show=True)
            elif usersall[call.from_user.id]["cw"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Work Experience Section is empty \U0001F914\nPlease fill your Work Experience Section firstly")
                menu_options(call.message)
        # if first 15 chars of call are "show_which_work".
        # Format is used because at the end of the call there is a number of experience of work on which changes are made
        elif str(call.data)[:15] == 'show_which_work':
            generate_work_exp(call.message, work_n=str(call.data)[15:])

        elif call.data == "education":
            if usersall[call.from_user.id]["ce"] != 0:
                choose_edu_exp(call.message, show=True)
            elif usersall[call.from_user.id]["ce"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Education Section is empty \U0001F914\nPlease fill your Education Section firstly")
                menu_options(call.message)

        elif str(call.data)[:16] == 'show_which_study':
            generate_education(call.message, edu_n=str(call.data)[16:])

        elif call.data == "skills":
            if usersall[call.from_user.id]["skil"] != 0:
                generate_skills(
                    call.message, skil_n=usersall[call.from_user.id]["skil"])
            elif usersall[call.from_user.id]["skil"] == 0:
                bot.send_message(
                    call.from_user.id, f"Your Skill Section is empty \U0001F914\nPlease fill your Skill Section firstly")
                menu_options(call.message)

    elif call.data == "contact_info":
        # checking is user want to edit info or fill
        # edit section
        if edit_or_not:
            generate_contact_info(call.message, menu_show=False)
            try:
                if usersall[call.from_user.id]['full_name'] and usersall[call.from_user.id]['position'] and usersall[call.from_user.id]['residence'] and usersall[call.from_user.id]['email'] and usersall[call.from_user.id]['portfolio']:
                    edit_contact_info(call.message)
            except KeyError:
                pass
        # fill section
        else:
            bot.send_message(
                call.from_user.id, "\u270D What position do you want to apply for? \n( Ex: Full-Stack Developer )")
            bot.register_next_step_handler(
                call.message, get_position, edit=False)

    elif call.data == "about_me":
        if edit_or_not:
            generate_about_me(call.message, menu_show=False)
            try:
                if usersall[call.from_user.id]['about_me']:
                    bot.send_message(
                        call.from_user.id, "Please, provide New Description about yourself... \U0001F4DD\n( Ex: Combine scientific approach, using qualitive and quantitive methods... )")
                    bot.register_next_step_handler(
                        call.message, get_about_me, edit=edit_or_not)
            except KeyError:
                pass
        else:
            bot.send_message(
                call.from_user.id, "Please, provide The Description about yourself... \U0001F4DD\n( Ex: Combine scientific approach, using qualitive and quantitive methods... )")
            bot.register_next_step_handler(
                call.message, get_about_me, edit=False)

    elif call.data == "work_exp":
        if edit_or_not and usersall[call.from_user.id]['cw'] != 0:
            choose_work_exp(call.message)
        else:
            usersall[call.from_user.id]['cw'] += 1
            number_of_work_exp = usersall[call.from_user.id]['cw']
            usersall[call.from_user.id]["work_exp"][f'work{number_of_work_exp}'] = {
            }
            bot.send_message(
                call.from_user.id, "Great! \n\U0001F4BC Let's fill data about your Work Experience! \nWhat is the name of oranization you are/were working in? \n( Ex: Apple GmbH )")
            bot.register_next_step_handler(
                call.message, get_work_name, usersall[call.from_user.id]['cw'], edit=False)

    elif call.data == "education":
        if edit_or_not and usersall[call.from_user.id]['ce'] != 0:
            choose_edu_exp(call.message)
        else:
            usersall[call.from_user.id]['ce'] += 1
            number_of_education = usersall[call.from_user.id]['ce']
            usersall[call.from_user.id]["edu_exp"][f'edu{number_of_education}'] = {
            }
            bot.send_message(
                call.from_user.id, "Super!\n\U0001F393 Let's fill data about your Education!\nWhat are the Name of Place and Programm are/were studying ?\n( Ex: Harvard University (Visual Design) )")
            bot.register_next_step_handler(
                call.message, get_study_name_course, usersall[call.from_user.id]['ce'], edit=False)

    elif call.data == "skills":
        if edit_or_not and usersall[call.from_user.id]['skil'] != 0:
            choose_skill(call.message)
        else:
            usersall[call.from_user.id]['skil'] += 1
            bot.send_message(
                call.from_user.id, "\U0000270C What Skills do you have?\nWrite them down one by one \n( Ex: Project management )")
            bot.register_next_step_handler(
                call.message, get_skills, usersall[call.from_user.id]['skil'], edit=False)


# handler which accepts ONLY calls starting with "edit_"
@bot.callback_query_handler(func=lambda call: str(call.data)[:5] == 'edit_')
def callback_handler_edit(call):
    connection = get_connection()
    dict_users = {}
    dict_users[call.from_user.id] = usersall[call.from_user.id]
    database.edit_data(connection, user_id=str(
        call.from_user.id), data=dict_users)

    # calling function with flag (edit) ==  TRUE
    if call.data == 'edit_position':
        bot.send_message(
            call.from_user.id, f"What position do you want to apply for? \n( Ex: HR )")
        bot.register_next_step_handler(call.message, get_position, edit=True)

    elif call.data == 'edit_residence':
        bot.send_message(
            call.from_user.id, f"What is your current place of residence? \n( Ex: Miami, USA )")
        bot.register_next_step_handler(call.message, get_residence, edit=True)

    elif call.data == 'edit_email':
        bot.send_message(
            call.from_user.id, f"What is your email? \n( Ex: hans-guberman@yahoo.com )")
        bot.register_next_step_handler(call.message, get_email, edit=True)

    elif call.data == 'edit_portfolio':
        bot.send_message(
            call.from_user.id, f"What is the link to your Portfolio? \n( Ex: https://www.linkedin.com/in/hans_guber )")
        bot.register_next_step_handler(call.message, get_portfolio, edit=True)

    # choosing the work experience that gonna be changed
    elif str(call.data)[:15] == 'edit_which_work':
        generate_work_exp(call.message, work_n=str(
            call.data)[15:], menu_show=False)
        edit_work_exp(call.message, work_n=str(call.data)[15:])

    elif str(call.data)[:14] == 'edit_work_name':
        bot.send_message(
            call.from_user.id, "Write your New Work Organization Name \n( Ex: Yahoo LLC )")
        bot.register_next_step_handler(
            call.message, get_work_name, work_n=str(call.data)[14:], edit=True)

    elif str(call.data)[:13] == 'edit_pos_work':
        bot.send_message(call.from_user.id,
                         "Write your New Position in Work \n( Ex: Tester )")
        bot.register_next_step_handler(
            call.message, get_pos_work, work_n=str(call.data)[13:], edit=True)

    elif str(call.data)[:21] == 'edit_get_beg_end_work':
        bot.send_message(
            call.from_user.id, "Write your New Period of Working \n( Ex: August 2011 - April 2015 )")
        bot.register_next_step_handler(
            call.message, get_beg_end_work, work_n=str(call.data)[21:], edit=True)

    elif str(call.data)[:14] == 'edit_desc_work':
        bot.send_message(
            call.from_user.id, "Write your New Work Description \n( Ex: Testing the mobile app for bugs... )")
        bot.register_next_step_handler(
            call.message, get_desc_work, work_n=str(call.data)[14:], edit=True)

    elif str(call.data)[:16] == 'edit_which_study':
        generate_education(call.message, edu_n=str(
            call.data)[16:], menu_show=False)
        edit_education(call.message, edu_n=str(call.data)[16:])

    elif str(call.data)[:17] == 'edit_educate_name':
        bot.send_message(
            call.from_user.id, "Write your New Study Place and Programm \n( Ex: MiT (Software Development) )")
        bot.register_next_step_handler(
            call.message, get_study_name_course, edu_n=str(call.data)[17:], edit=True)

    elif str(call.data)[:18] == 'edit_educate_place':
        bot.send_message(
            call.from_user.id, "Write your New Study Location \n( Ex: Cambridge, USA )")
        bot.register_next_step_handler(
            call.message, get_study_location, edu_n=str(call.data)[18:], edit=True)

    elif str(call.data)[:20] == 'edit_start_end_study':
        bot.send_message(
            call.from_user.id, "Write your New Period of Study \n( Ex: February 2008 - May 2011 )")
        bot.register_next_step_handler(
            call.message, get_beg_end_study, edu_n=str(call.data)[20:], edit=True)

    elif str(call.data)[:16] == 'edit_which_skill':
        bot.send_message(call.from_user.id,
                         "Write your New Skill \n( Ex: Patient )")
        bot.register_next_step_handler(
            call.message, get_skills, skil_n=str(call.data)[16:], edit=True)


# displaying data info
def generate_contact_info(message, menu_show=True):
    # try/except construction is used to bypass an error if any of the fields are not filled (empty)
    try:
        contact_info_output = f"Personal Information Section has been Generated\n\n" \
            f"<b><u>Full Name</u></b>: {usersall[message.chat.id]['full_name']}\n" \
            f"<b><u>Position</u></b>: {usersall[message.chat.id]['position']}\n" \
            f"<b><u>Residence</u></b>: {usersall[message.chat.id]['residence']}\n" \
            f"<b><u>Email</u></b>: {usersall[message.chat.id]['email']}\n" \
            f"<b><u>Portfolio</u></b>: {usersall[message.chat.id]['portfolio']}\n" \

        bot.send_message(
            message.chat.id, f"\U00002B07 Here is your Personal Information data\n {contact_info_output}", parse_mode='HTML')
        if menu_show:
            menu_options(message)
    # if field is empty call function to fill the whole section
    except KeyError:
        bot.send_message(
            message.chat.id, 'Your Personal Information data is not filled. \nPlease fill missing data. \nWhat position do you want to apply for? \n( Ex: Developer Assistant )')
        bot.register_next_step_handler(message, get_position)


def generate_about_me(message, menu_show=True):
    try:
        about_me_output = f"About Me Section has been Generated\n\n" \
            f"<b><u>About Me</u></b>: {usersall[message.chat.id]['about_me']}\n" \

        bot.send_message(
            message.chat.id, f"\U00002B07 Here is your About Me data\n {about_me_output}", parse_mode='HTML')
        if menu_show:
            menu_options(message)

    except KeyError:
        bot.send_message(message.chat.id, 'Your About Me Section is not filled. \nPlease fill missing data. \nPlease, provide the description about yourself. \n( Ex: Combine scientific approach, using qualitive and quantitive methods... )')
        bot.register_next_step_handler(message, get_about_me)


def generate_work_exp(message, work_n, menu_show=True):
    try:
        work_exp_output = f"Work Experience {work_n} Section has been Generated\n\n" \
            f"<b><u>Name of Organisation</u></b>: {usersall[message.chat.id]['work_exp'][f'work{work_n}']['work_name']}\n" \
            f"<b><u>Position in Organisation</u></b>: {usersall[message.chat.id]['work_exp'][f'work{work_n}']['pos_work']}\n" \
            f"<b><u>Period of being Employed</u></b>: {usersall[message.chat.id]['work_exp'][f'work{work_n}']['start_end_work']}\n" \
            f"<b><u>Work Description</u></b>: {usersall[message.chat.id]['work_exp'][f'work{work_n}']['desc_work']}\n" \

        bot.send_message(
            message.chat.id, f'\U00002B07 Here is your Work Experience data \n{work_exp_output}', parse_mode='HTML')
        if menu_show:
            menu_options(message)

    except KeyError:
        bot.send_message(
            message.chat.id, 'Your Work Experience data is not filled. \nPlease fill missing data. \nPlease, provide the information about your Work Experience. \nWhat is the name of oranization you are/were working in? \n( Ex: BMW LLC )')
        bot.register_next_step_handler(message, get_work_name, work_n=work_n)


def generate_education(message, edu_n, menu_show=True):
    try:
        education_output = f"Education Background N{edu_n} Section has been Generated\n\n" \
            f"<b><u>Name of Programm of Study</u></b>: {usersall[message.chat.id][f'edu_exp'][f'edu{edu_n}']['educate_name']}\n" \
            f"<b><u>Study Location</u></b>: {usersall[message.chat.id][f'edu_exp'][f'edu{edu_n}']['educate_place']}\n" \
            f"<b><u>Period of Studying</u></b>: {usersall[message.chat.id][f'edu_exp'][f'edu{edu_n}']['start_end_study']}\n" \

        bot.send_message(
            message.chat.id, f"\U00002B07 Here is your Education data \n{education_output}", parse_mode='HTML')
        if menu_show:
            menu_options(message)

    except KeyError:
        bot.send_message(
            message.chat.id, 'Your Education data is not filled. \nPlease fill missing data. \nPlease, provide the description about your Education.')
        bot.register_next_step_handler(
            message, get_study_name_course, edu_n=edu_n)


def generate_skills(message, skil_n):
    try:
        get_skills_output = ''
        for i in range(1, usersall[message.chat.id]['skil'] + 1):
            get_skills_output += f'<b><u>Skill{i}</u></b>: {usersall[message.chat.id][f"skills"][f"skill{i}"]}\n'

        bot.send_message(
            message.chat.id, f"\U00002B07 Here is your Skills data\n {get_skills_output}", parse_mode='HTML')
        menu_options(message)

    except KeyError:
        bot.send_message(
            message.chat.id, 'Your data is not filled. \nPlease fill missing data. \nPlease, provide the description about your Skills.')
        bot.register_next_step_handler(message, get_skills, skil_n)


def check_type_message(message, func_name, work_edu_n=False, edit=False):
    # if type of message is not text
    if message.content_type != 'text':
        bot.send_message(
            message.chat.id, "Your message should contain only text \U0001F6AB\nPlease try again.")
        # Since different default conditions are used for different arguments for different functions
        if work_edu_n:
            bot.register_next_step_handler(
                message, func_name, work_edu_n, edit)
        else:
            bot.register_next_step_handler(message, func_name)
        return True
    else:
        return False


def check_invalid_pattern(message, func_name, pattern, work_edu_n=False, edit=False, another_str=False):
    # It is also possible to have argems default to string(str) format rather than message(message) format

    error_message = f"Your message contains invalid characters \U0001F6AB\nWrite in the same format as in the example \U0001F64F\nPlease try again."
    bot.send_message(message.chat.id, error_message)
    if work_edu_n:
        bot.register_next_step_handler(message, func_name, work_edu_n, edit)
    else:
        bot.register_next_step_handler(message, func_name)


@bot.message_handler(commands=['help'])
def helper(message):
    help_info = f"<b>What CV Bot can do?</b> \n" \
                f"\U0001F4AC Create sections of your CV step-by-step in a chat format \n" \
                f"\U0001F4DD Review and edit information in your CV \n" \
                f"\U0001F517 Combine all parts into a single PDF file"
    bot.send_message(message.chat.id, f"{help_info}", parse_mode='HTML')


@bot.message_handler(commands=['buy'])
def buy(message):
    PRICE = types.LabeledPrice(
        label="Get the full version of CV", amount=2 * 100)  # in eurocents
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        pay = types.InlineKeyboardButton(text="Pay", pay=True)
        menu = types.InlineKeyboardButton(
            text="Back \U000021A9", callback_data="menu")
        keyboard.add(pay, menu)

        bot.send_invoice(message.chat.id,
                         title="CV FULL VERSION",
                         description="Pay 2 euro and get a full PDF version of your created CV",
                         provider_token=PAYMENT_TOKEN,
                         currency="eur",
                         photo_url="https://i.postimg.cc/cJrLK1Fb/Payment-pic.png",
                         photo_width=512,
                         photo_height=512,
                         photo_size=512,
                         is_flexible=False,
                         prices=[PRICE],
                         start_parameter="full_version_payment",
                         invoice_payload="test-invoice-payload",
                         reply_markup=keyboard)


def get_connection():
    load_dotenv()
    database_uri = os.environ["DATABASE_URI"]
    connection = psycopg2.connect(database_uri)
    # Automatically creates the userall table if it is not exists
    database.create_table(connection)
    return connection


# function for inserting data into database
def add_user(user_id: str, data: dict):  # Add new user data
    connection = get_connection()
    database.inser_user_data(connection, user_id=str(user_id), data=data)


def create_pdf_for_user(message, final_dict: dict):

    user = user_datapdf_creation.UserProfilePDFHandler(usersall=final_dict)
    user.format_user_data()
    user.create_pdf()
    # Create function that would take a file send it to user !!!!!!!!!!
    user_pdf = open(f'pdf_files/{message.from_user.id}.pdf', 'rb')
    bot.send_document(message.chat.id, user_pdf)
    user_pdf.close()
    time.sleep(10)
    user.delete_file()


# pre checkout  (must be answered in 10 seconds)
@bot.pre_checkout_query_handler(lambda query: True)
def pre_checkout_query(pre_checkout_q):
    bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    bot.send_message(message.chat.id,
                     f"Payment of {message.successful_payment.total_amount // 100} {message.successful_payment.currency} is successfully done!!!")


@bot.message_handler(commands=['get_pdf'])
def get_pdf(message):
    edit_user(user_id=str(message.from_user.id),
              data=usersall[message.from_user.id])
    try:
        if usersall[message.from_user.id]['full_name'] and usersall[message.from_user.id]['position'] and usersall[message.from_user.id]['residence'] and usersall[message.from_user.id]['email'] and usersall[message.from_user.id]['portfolio'] and usersall[message.from_user.id]['about_me'] and usersall[message.from_user.id]['work_exp'] and usersall[message.from_user.id]['edu_exp'] and usersall[message.from_user.id]['skills'] and usersall[message.from_user.id]['flag'] and usersall[message.from_user.id]['cw'] and usersall[message.from_user.id]['ce'] and usersall[message.from_user.id]['skil']:
            bot.send_message(
                message.chat.id, f"{'_' * 63}\n\n\n{'.' * 15}Please wait 15-20 seconds and you will receive your CV{'.' * 15}\n\n\n{'_' * 63}")

            create_pdf_for_user(
                message=message, final_dict=usersall[message.from_user.id])
        else:
            bot.send_message(
                message.chat.id, f"{'_'*43}\n\n\n\n\n{'.'*15}Please fill in all sections in the CV{'.'*15}\n\n\n\n\n{'_'*43}")
            menu_options(message)
    except:
        bot.send_message(
            message.chat.id, f"{'_'*43}\n\n\n\n\n{'.'*15}Please fill in all fields in the CV{'.'*15}\n\n\n\n\n{'_'*43}")
        menu_options(message)


def edit_user(user_id: str, data: dict):
    connection = get_connection()
    database.edit_data(connection, user_id=str(user_id), data=data)
    comments = '''
    # database.inser_user_data(connection, user_id=str(user_id), data=data)
    # user_data_from_db = database.get_user_data(connection, user_id=1)
    # Get user data from the Database
    # get_user_data(user_id="gdhudhuehwufewuihfiuer") If [] empty list then  => New user, else => Existing user
    # Update user data within the Database

    # user_data_from_db = [{}]
    # if len(user_data_from_db) == 0:
    #     print("New user")
    # else:
    #     print("Existing user")
# fun => edit
    # Currently creating Resume Process => dict user data completed => Do you wanna edit something? no => Creating PDF => DB
    # I want to edit the PDF file info =>  Get user data from the DB => dict use data => editing process => Creating PDF => Insert Update data into DB
    # database.edit_data(connection, user_id=1, data=1
    '''

# Used for looping work (infinite work if there are no errors in the code)
bot.polling(none_stop=True)

if __name__ == '__main__':
     menu_options()
