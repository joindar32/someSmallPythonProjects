import telebot
from datetime import date
from telebot import types
import psycopg2

token = "6296277648:AAHwgP4GmpwPEnXyFBRC6ugrO5J02NBzZ1A"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="schedule",
                        user="postgres",
                        password="jametime2",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
                 'Расписание на следующую неделю')
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def start_message(message):
    date1 = str(date.today().isocalendar())
    try:
        weekodd = int(date1[-14:-12])
    except:
        weekodd = int(date1[-13:-12])
    if weekodd % 2 == 0:
        bot.send_message(message.chat.id, 'четная')
    else:
        bot.send_message(message.chat.id, 'нечетная')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею /week, /mtuci')


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text.lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница']:

        date1 = str(date.today().isocalendar())

        try:
            weekodd = int(date1[-14:-12])
        except:
            weekodd = int(date1[-13:-12])

        if weekodd % 2 == 0:
            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name
                    from (SELECT * FROM public.timetable WHERE day=%s AND week=%s) AS oop
                    inner  join subject
                    on subject.id = oop.subject	
                    inner join teacher
                    on teacher.subject = subject.id''', (message.text, 2))
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
                    {message.text.lower()}
                    ____________
                    '''

            for i in records2:
                day_schedulle += f'''
    
                        {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                        '''

            bot.send_message(message.chat.id, day_schedulle)
        else:
            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name
            from (SELECT * FROM public.timetable WHERE day=%s AND week=%s) AS oop
            inner  join subject
            on subject.id = oop.subject	
            inner join teacher
            on teacher.subject = subject.id''', (message.text, 1))
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
            {message.text.lower()}
            ____________
            '''

            for i in records2:
                day_schedulle += f'''
                
                {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                '''

            bot.send_message(message.chat.id, day_schedulle)

    elif message.text.lower() == 'расписание на текущую неделю':
        date1 = str(date.today().isocalendar())
        try:
            weekodd = int(date1[-14:-12])
        except:
            weekodd = int(date1[-13:-12])
        if weekodd % 2 == 0:
            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name, oop.day
                                    from (SELECT * FROM public.timetable WHERE week=2) AS oop
                                    inner  join subject
                                    on subject.id = oop.subject	
                                    inner join teacher
                                    on teacher.subject = subject.id
                                    order by oop.id_lesson''')
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
                        {message.text.lower()}
                        ____________
                        '''

            for i in records2:
                day_schedulle += f'''
                {str(i[4])}
                {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                '''

            bot.send_message(message.chat.id, day_schedulle)

        else:
            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name, oop.day
                                    from (SELECT * FROM public.timetable WHERE week=1) AS oop
                                    inner  join subject
                                    on subject.id = oop.subject	
                                    inner join teacher
                                    on teacher.subject = subject.id
                                    order by oop.id_lesson''')
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
                                    {message.text.lower()}
                                    ____________
                                    '''

            for i in records2:
                day_schedulle += f'''
                {str(i[4])}

                {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                '''

            bot.send_message(message.chat.id, day_schedulle)
    elif message.text.lower() == 'расписание на следующую неделю':

        date1 = str(date.today().isocalendar())
        try:
            weekodd = int(date1[-14:-12])
        except:
            weekodd = int(date1[-13:-12])

        if weekodd % 2 == 0:
            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name, oop.day
                                            from (SELECT * FROM public.timetable WHERE week=1) AS oop
                                            inner  join subject
                                            on subject.id = oop.subject	
                                            inner join teacher
                                            on teacher.subject = subject.id
                                            order by oop.id_lesson''')
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
                                {message.text.lower()}
                                ____________
                                '''

            for i in records2:
                day_schedulle += f'''
                        {str(i[4])}
                        {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                        '''

            bot.send_message(message.chat.id, day_schedulle)

        else:

            cursor.execute('''select  subject.name, oop.room_numb, oop.start_time, teacher.full_name, oop.day
                                            from (SELECT * FROM public.timetable WHERE week=2) AS oop
                                            inner  join subject
                                            on subject.id = oop.subject	
                                            inner join teacher
                                            on teacher.subject = subject.id
                                            order by oop.id_lesson''')
            records2 = list(cursor.fetchall())

            day_schedulle = f'''
                                            {message.text.lower()}
                                            ____________
                                            '''

            for i in records2:
                day_schedulle += f'''
                        {str(i[4])}

                        {str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3])}  
                        '''
            bot.send_message(message.chat.id, day_schedulle)
    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понял')










bot.polling(none_stop=True)
#help, извините я вас не понял
