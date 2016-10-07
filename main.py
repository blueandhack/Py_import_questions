import os
from pymongo import MongoClient

if __name__ == '__main__':
    filename_list = os.listdir("./")

    client = MongoClient('localhost', 27017)
    db = client.acbs160
    collection = db.quiz

    for filename in filename_list:
        filename_quiz = 'quiz'
        if filename.find(filename_quiz) != -1:
            enc = 'iso-8859-15'
            quiz_file = open(filename, 'r', encoding=enc)
            question_begin = 0
            question = ''
            question_correct_answer = ''
            answer_list = []
            while 1:
                line = quiz_file.readline()
                if not line:
                    break

                if line.find('---') != -1:
                    question_begin = 1

                if question_begin == 1 and line.find('---') == -1:
                    question = line
                    question_begin = 0
                elif line.find('---') == -1 and line.find('*') == -1 and question != '':
                    answer_list.append(line)

                if line.find('*') != -1:
                    question_correct_answer = line[1:]

                    # print information
                    print(question)
                    print(answer_list)
                    print(question_correct_answer)

                    # insert to database
                    per_question = {
                        "question": question,
                        "answer_list": answer_list,
                        "bingo": question_correct_answer
                    }
                    if collection.find({"question": question}).count() == 0:
                        collection.insert_one(per_question)

                    # clean all
                    question = ''
                    answer_list.clear()
                    question_correct_answer = ''
