import xml_parser
import resourses.constants
from tkinter import *


def testing(parsed):
    win = Toplevel()
    win.minsize(width=600, height=500)
    root.withdraw()

    # print(1)

    main_frame = Frame(win)
    main_frame.config(bg="#FFF")
    main_frame.pack(expand=YES, fill=BOTH)

    nav_frame = Frame(main_frame)
    nav_frame.config(bg="gray")
    for item_id in range(len(parsed)):
        btn = Button(nav_frame)
        btn.config(text=str(item_id + 1), font=resourses.constants.button_font)
        btn.config(height=1, width=3)
        btn.pack(side=LEFT, padx=10, pady=10)
    nav_frame.pack(expand=YES, fill=BOTH)

    msg = Message(main_frame)
    msg.config(font=resourses.constants.message_font, justify=CENTER, width=700)
    msg.config(bg="#FFF")
    msg.pack(expand=YES, fill=BOTH)

    variants_frame = Frame(main_frame)
    variants_frame.pack(expand=YES, fill=BOTH)

    footer_frame = Frame(main_frame)
    footer_frame.config(bg='gray', height=30)
    footer_frame.pack(expand=YES, fill=BOTH)

    btn_prev = Button(footer_frame)
    btn_prev.config(text='Предыдущий', font=resourses.constants.button_font)
    btn_prev.config(height=1, state=DISABLED)
    btn_prev.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_comfirm = Button(footer_frame)
    btn_comfirm.config(text='Подтвердить ответ', font=resourses.constants.button_font)
    btn_comfirm.config(height=1)
    btn_comfirm.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_next = Button(footer_frame)
    btn_next.config(text='Следующий', font=resourses.constants.button_font)
    btn_next.config(height=1, state=DISABLED)
    btn_next.pack(side=RIGHT, expand=YES, fill=BOTH, padx=20, pady=20)

    for item_id in map(str, range(len(parsed))):
        item = parsed[item_id]
        item_type = item['type']
        question = item['question']
        question_text = question['text']

        variants = question['variants']
        answers = item['answers']

        msg.config(text=question_text)

        variants_frame

        if False:
            print('id :', item['id'])
            print('type :', item['type'])
            print('question :', item['question'])
            print('answer :', item['answer'])

    # win.protocol('WM_DELETE_WINDOW', win.quit)
    win.focus_set()
    # win.grab_set()
    win.wait_window()
    root.deiconify()


if __name__ == '__main__':
    path = 'resourses/questions.xml'
    parsed = xml_parser.parse(path)

    root = Tk()
    root.minsize(width=600, height=500)
    # root.maxsize(width=300, height=300)
    root.title('Тестирование')

    main_frame = Frame(root)
    main_frame.config(bg="#FFF")
    main_frame.pack(expand=YES, fill=BOTH)

    # label = Label(f, text=resourses.constants.intro_label)
    # label.config(height=5, width=30)
    # label.config(font=resourses.constants.label_font)
    # label.pack()

    msg = Message(main_frame, text=resourses.constants.intro_message)
    msg.config(font=resourses.constants.message_font, justify=CENTER)
    msg.config(bg="#FFF")
    msg.pack(expand=YES, fill=BOTH, padx=50, pady=20)

    footer_frame = Frame(main_frame)
    footer_frame.config(bg="#FFF")
    footer_frame.pack(expand=YES, fill=BOTH)

    btn_start = Button(footer_frame, text='Начать тестирование', command=(lambda: testing(parsed)))
    btn_start.config(font=resourses.constants.button_font, bg="#BBB")
    btn_start.config(width=15, height=1)
    btn_start.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_quit = Button(footer_frame, text='Завершить', command=footer_frame.quit)
    btn_quit.config(font=resourses.constants.button_font, bg='#BBB')
    btn_quit.config(width=15, height=1)
    btn_quit.pack(side=RIGHT, expand=YES, fill=BOTH, padx=20, pady=20)

    root.mainloop()
