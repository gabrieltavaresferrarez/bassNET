import time
import codecs
from datetime import datetime
import os

listString_topicBullets= ['* ', '- ', '+ ', '¢ ', '* ', '- ', '+ ', '¢ ']

class Logger:
    def __init__(self, log_file_name : str = 'log.log', print_log = False):
        self.string_logFileName = log_file_name
        self.bool_print = print_log
        with codecs.open(self.string_logFileName, "w", encoding='utf-8') as file_log:
            string_timestamp = self.get_timestamp()
            string_text = string_timestamp + '########################### START LOG ###########################' + '\n'
            file_log.write(string_text)
            if self.bool_print:
                print(string_text)


    def topic(self, text, sub_level = 0, break_line = True):
        #escreve topico com time stamp
        #subtopicos tem identação
        with codecs.open(self.string_logFileName, "a", encoding='utf-8') as file_log:
            string_timestamp = self.get_timestamp()
            string_text =string_timestamp

            string_text += '\t\t'*sub_level
            string_topicBullet = listString_topicBullets[sub_level]
            string_text += string_topicBullet
            string_text += text

            if break_line:
                file_log.write('\n')

            file_log.write(string_text)
            if self.bool_print:
                print(string_text)

    def write(self, text : str, breakline : bool = False, timestamp : bool = False): # apenas apenda a linha atual do log sem timestamp
        with codecs.open(self.string_logFileName, "a") as file_log:
            if timestamp:
                string_timestamp = self.get_timestamp()

            string_text = string_timestamp
            string_text += text
            if breakline:
                string_text += '\n'

            file_log.write(string_text)
            if self.bool_print:
                print(string_text)


    def erro(self, text, sub_level = 0, breakline : bool = True, timestamp : bool = True):
        with codecs.open(self.string_logFileName, "a") as file_log:
            if timestamp:
                string_timestamp = self.get_timestamp()
                string_text = string_timestamp

            # level
            string_text += '\t\t'*sub_level
            string_topicBullet = listString_topicBullets[sub_level]
            string_text += string_topicBullet

            string_text += '[ERRO] : '
            string_text += text
            if breakline:
                string_text += '\n'

            file_log.write(string_text)
            if self.bool_print:
                print(string_text)

    def breakline(self):
        with codecs.open(self.string_logFileName, "a") as file_log:
            file_log.write('\n')


    def get_timestamp(self):
        date_now = datetime.now()
        string_timestamp = f'{date_now.year:02d}/{date_now.month:02d}/{date_now.day:02d}-{date_now.hour:02d}:{date_now.minute:02d}:{date_now.second:02d} | '
        return string_timestamp

    def __bool__(self):
        return os.path.exists(self.string_logFileName)