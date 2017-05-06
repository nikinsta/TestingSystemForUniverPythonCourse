import xml.dom.minidom
from xml.dom.minidom import Node


def parse(path):
    doc = xml.dom.minidom.parse('resourses/questions.xml')

    parsed = {}
    for item_tag in doc.getElementsByTagName("item"):  # обход объекта DOM
        # <item id type>
        item = {}
        item_id = item_tag.getAttribute("id")
        item_type = item_tag.getAttribute("type")
        item["id"] = item_id
        item["type"] = item_type

        # <question>
        question_tag = item_tag.getElementsByTagName("question")
        question = {}

        # <text>
        text_tag = question_tag[0].getElementsByTagName("text")
        question_text = text_tag[0].childNodes[0].data
        question["text"] = question_text

        # <variants>
        variants_tag = question_tag[0].getElementsByTagName("variants")
        variants = {}
        for variant_tag in variants_tag[0].getElementsByTagName("variant"):
            # <variant id>
            variant_id = variant_tag.getAttribute("id")
            variants[variant_id] = variant_tag.childNodes[0].data
        question["variants"] = variants

        item["question"] = question

        # <answers>
        answers_tag = item_tag.getElementsByTagName("answers")
        answers = {}

        for answer_tag in answers_tag[0].getElementsByTagName("answer"):
            # <answer id>
            answer_id = answer_tag.getAttribute("id")
            answers[answer_id] = answer_tag.childNodes[0].data

        item["answers"] = answers

        parsed[item_id] = item
    return parsed

if __name__ == '__main__':
    path = 'resourses/questions.xml'
    parsed = parse(path)
    for key, value in parsed.items():
        # print("item id :", key)
        for key2, value2 in value.items():
            print("-" * 50)
            print(key2)
            print(value2)
        print('=' * 50)
        # return parsed
        # for key, value in parsed.items():
        # print(key, value)
