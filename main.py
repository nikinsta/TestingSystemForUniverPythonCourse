import xml_parser
import resourses.constants
from tkinter import *


def disable_item(user_answers, item_id):
    user_answers[item_id]['disabled'] = True


def go_to_question(item_id, parsed, nav_buttons, msg, variants_frame, btn_prev, btn_comfirm, btn_next, user_answers):
    print('go to question ', item_id)
    print('user_answers', user_answers)
    # print(nav_buttons)

    if item_id > 0:
        btn_prev.config(state=NORMAL)
        btn_prev.config(command=(lambda: go_to_question(item_id - 1, parsed,
                                                        nav_buttons, msg, variants_frame,
                                                        btn_prev, btn_comfirm, btn_next, user_answers)))
    else:
        btn_prev.config(state=DISABLED)

    # btn_comfirm.config(state=nav_buttons[item_id]['state'])
    # btn_comfirm.config(
    #     command=(lambda: nav_buttons[item_id].config(bg='green', disabledforeground='black',
    #                                                 state=DISABLED) or btn_comfirm.config(state=DISABLED)))
    if user_answers[item_id]['disabled']:
        btn_comfirm.config(state=DISABLED)
    else:
        btn_comfirm.config(state=NORMAL)
        btn_comfirm.config(
            command=(lambda: nav_buttons[item_id].config(bg='green')
                             or disable_item(user_answers, item_id) or btn_comfirm.config(state=DISABLED)))

    if item_id + 1 < len(parsed):
        btn_next.config(state=NORMAL)
        btn_next.config(
            command=(
                lambda: go_to_question(item_id + 1, parsed, nav_buttons, msg, variants_frame, btn_prev, btn_comfirm,
                                       btn_next, user_answers)))
    else:
        btn_next.config(state=DISABLED)

    item = parsed[str(item_id)]
    item_type = item['type']
    question = item['question']
    question_text = question['text']

    variants = question['variants']
    answers = item['answers']

    msg.config(text=question_text)

    return

    if item_type == 'entry':
        entry = Entry(variants_frame)
        entry.config(font=resourses.constants.ENTRY_FONT)
        entry.config(width=5)
        entry.pack(expand=YES, fill=BOTH, padx=10, pady=10)
    elif item_type == 'checkbutton':
        for variant_id in map(str, range(len(variants))):
            variant = variants[variant_id]
            checkbutton = Checkbutton(variants_frame)
            checkbutton.config(text=variant)
            checkbutton.pack()

    if False:
        print('id :', item['id'])
        print('type :', item['type'])
        print('question :', item['question'])
        print('answer :', item['answer'])


def testing(root, parsed):
    user_answers = {i: {'disabled': False, 'answers': {}} for i in range(len(parsed))}
    # user_answers[0]['disabled'] = True
    # user_answers[1]['answers'] = {1, 2}
    # user_answers[2] = {'disabled': False, 'answers': {3, 4, 5}}

    win = Toplevel()
    win.minsize(width=750, height=500)
    win.maxsize(width=750, height=500)
    root.withdraw()

    # print(1)

    main_frame = Frame(win)
    main_frame.config(bg="#FFF")
    main_frame.pack(expand=YES, fill=BOTH)

    nav_frame = Frame(main_frame)
    nav_frame.config(bg="gray")
    nav_buttons = []
    for item_id in range(len(parsed)):
        btn = Button(nav_frame)
        btn.config(text=str(item_id + 1), font=resourses.constants.BUTTON_FONT)
        btn.config(height=1, width=3)
        btn.config(overrelief=RAISED, activebackground='#DDD')
        btn.config(command=(lambda item_id=item_id: go_to_question(item_id, parsed, nav_buttons, \
                                                                   msg, variants_frame, btn_prev, btn_comfirm, \
                                                                   btn_next, user_answers)))
        btn.pack(side=LEFT, padx=10, pady=10)
        nav_buttons.append(btn)
    nav_frame.pack(expand=NO, fill=BOTH)
    print(nav_buttons[0] is nav_buttons[1])

    msg = Message(main_frame)
    msg.config(font=resourses.constants.MESSAGE_FONT, justify=CENTER, width=700)
    msg.config(bg="#FFF")
    msg.pack(expand=YES, fill=BOTH)

    variants_frame = Frame(main_frame)
    variants_frame.pack(expand=YES, fill=BOTH)

    footer_frame = Frame(main_frame)
    footer_frame.config(bg='gray', height=30)
    footer_frame.pack(side=BOTTOM, expand=NO, fill=BOTH)

    btn_prev = Button(footer_frame)
    btn_prev.config(text='Предыдущий', font=resourses.constants.BUTTON_FONT)
    btn_prev.config(height=1, state=DISABLED)
    btn_prev.config(overrelief=RAISED, activebackground='#DDD')
    btn_prev.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_comfirm = Button(footer_frame)
    btn_comfirm.config(text='Подтвердить ответ', font=resourses.constants.BUTTON_FONT)
    btn_comfirm.config(height=1)
    btn_comfirm.config(overrelief=RAISED, activebackground='#DDD')
    btn_comfirm.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_next = Button(footer_frame)
    btn_next.config(text='Следующий', font=resourses.constants.BUTTON_FONT)
    btn_next.config(height=1, state=DISABLED)
    btn_next.config(overrelief=RAISED, activebackground='#DDD')
    btn_next.pack(side=RIGHT, expand=YES, fill=BOTH, padx=20, pady=20)

    go_to_question(0, parsed, nav_buttons, msg, variants_frame, btn_prev, btn_comfirm, btn_next, user_answers)

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
    # root.maxsize(width=600, height=500)
    root.title('Тестирование')

    main_frame = Frame(root)
    main_frame.config(bg="#FFF")
    main_frame.pack(expand=YES, fill=BOTH)

    # label = Label(f, text=resourses.constants.intro_label)
    # label.config(height=5, width=30)
    # label.config(font=resourses.constants.label_font)
    # label.pack()

    welcome_msg = Message(main_frame, text=resourses.constants.intro_message)
    welcome_msg.config(font=resourses.constants.MESSAGE_FONT, justify=CENTER)
    welcome_msg.config(bg="#FFF")
    welcome_msg.pack(expand=YES, fill=BOTH, padx=50, pady=20)

    footer_frame = Frame(main_frame)
    footer_frame.config(bg="#FFF")
    footer_frame.pack(expand=YES, fill=BOTH)

    btn_start = Button(footer_frame, text='Начать тестирование', command=(lambda: testing(root, parsed)))
    btn_start.config(font=resourses.constants.BUTTON_FONT, bg="#BBB")
    btn_start.config(width=15, height=1)
    btn_start.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_quit = Button(footer_frame, text='Завершить', command=footer_frame.quit)
    btn_quit.config(font=resourses.constants.BUTTON_FONT, bg='#BBB')
    btn_quit.config(width=15, height=1)
    btn_quit.pack(side=RIGHT, expand=YES, fill=BOTH, padx=20, pady=20)

    root.mainloop()
