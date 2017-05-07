"""
Main part of the application.
Uses tkinter and adapted XML parser.
"""

import xml_parser
import resourses.constants
from tkinter import *


def disable_item(user_answers, item_id, variants_frame, parsed):
    """
    Disables all the widgets in variants_frame.

    Temporarily responsible for fixation of entry content in user_answers on confirm button pressed (TODO).
    """

    # TODO Вынести реализацию фиксации текущего содержимого entry в отдельную функцию.

    user_answers[item_id]['disabled'] = True
    vscopy = variants_frame.children.copy()
    for key, widget in vscopy.items():
        widget.config(state=DISABLED)
        # saving widgets state
        item_type = parsed[str(item_id)]['type']
        if item_type == 'entry':
            user_answers[item_id]['answers'].clear()
            user_answers[item_id]['answers'].add(widget.get())
        elif item_type == 'checkbutton':
            continue
        elif item_type == 'radiobutton':
            continue
        else:
            print('ERROR in disable_item')


def destroy_widgets_in_variants_frame(entry, checkbox, radiobox):
    """
    Unnecessary function.
    """

    # destroying widgets in the variants_frame
    if not (entry is None):
        entry.destroy()
        print('entry was destroyed')
    if len(checkbox) != 0:
        for checkbutton in checkbox:
            checkbutton.destroy()
        print('checkbox was destroyed')
    if len(radiobox) != 0:
        for radiobutton in radiobox:
            radiobutton.destroy()
        print('radiobox was destroyed')


def check_all_comfirmed(user_answers, win):
    """
    Destroy the window if all question items confirmed.

    Returns nothing.
    """

    for item in user_answers.values():
        if not item['disabled']:
            return
    win.destroy()


def toggle_checkbutton(checkbutton_var, item_id, variant_id, user_answers):
    """
    Changes user_answer accordingly to the checkbutton state.

    Returns nothing.
    """

    value = checkbutton_var.get()
    print('chkbut value :', value)
    if value == 1:
        user_answers[item_id]['answers'].add(variant_id)
    elif value == 0:
        if variant_id in user_answers[item_id]['answers']:
            user_answers[item_id]['answers'].remove(variant_id)


def select_radiobutton(radiobutton_var, item_id, variant_id, user_answers):
    """
    Changes user_answer accordingly to the radiobutton state.

    Returns nothing.
    """

    value = radiobutton_var.get()
    print('radiobtn value :', value)
    user_answers[item_id]['answers'].clear()
    user_answers[item_id]['answers'].add(variant_id)


def go_to_question(item_id, prev_item_id, parsed, nav_buttons, msg, variants_frame, btn_prev, btn_comfirm, btn_next,
                   user_answers,
                   win):
    """
    Realise jump to item_id-th question.

    Returns nothing.
    """

    print('go to question ', item_id)
    # print('user_answers', user_answers)
    # print(nav_buttons)

    # saving widgets state
    # if parsed[str(item_id)]['type'] == 'entry':
    #   user_answers[item_id]['answers'] = {}

    # print('before', variants_frame.children)
    vscopy = variants_frame.children.copy()
    for key, widget in vscopy.items():
        widget.destroy()
    # print('after', variants_frame.children)

    # destroy_widgets_in_variants_frame(entry, checkbox, radiobox)

    if item_id > 0:
        btn_prev.config(state=NORMAL)
        btn_prev.config(command=(lambda: go_to_question(item_id - 1, item_id, parsed, nav_buttons, msg, variants_frame,
                                                        btn_prev, btn_comfirm, btn_next, user_answers, win)))
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
                             or disable_item(user_answers, item_id, variants_frame, parsed)
                             or btn_comfirm.config(state=DISABLED)
                             or check_all_comfirmed(user_answers, win)))

    if item_id + 1 < len(parsed):
        btn_next.config(state=NORMAL)
        btn_next.config(
            command=(
                lambda: go_to_question(item_id + 1, item_id, parsed, nav_buttons, msg, variants_frame, btn_prev,
                                       btn_comfirm,
                                       btn_next, user_answers, win)))
    else:
        btn_next.config(state=DISABLED)

    item = parsed[str(item_id)]
    item_type = item['type']
    question = item['question']
    question_text = question['text']

    variants = question['variants']
    answers = item['answers']

    msg.config(text=question_text)

    if item_type == 'entry':
        entry = Entry(variants_frame)
        entry.config(font=resourses.constants.ENTRY_FONT)
        entry.config(width=30)
        # http: // infohost.nmt.edu / tcc / help / pubs / tkinter / web / cursors.html
        # cursor ::= 'gumby', 'watch', 'pencil', 'cross', 'hand2'
        entry.config(cursor='xterm')
        entry.config(show='', insertofftime=500, insertontime=500)
        entry.pack(expand=YES, padx=10, pady=10)
        entry.focus_set()

        # entry_text = StringVar()
        # entry.config(variable=entry_text)

        # restore state of the entry
        if len(user_answers[item_id]['answers']) != 0:
            entry.insert(0, list(user_answers[item_id]['answers'])[0])
        else:
            entry.insert(0, '')

        if user_answers[item_id]['disabled']:
            entry.config(state=DISABLED)
        else:
            entry.config(state=NORMAL)

            # user_answers[item_id]['answers']['0'] = entry.get()
            # print(user_answers[item_id]['answers']['0'])

            # root.geometry(newGeometry='300x300+200+200')

            # Button(variants_frame, text='OK', command=win.destroy).pack()

    elif item_type == 'checkbutton':
        # return
        disabled = user_answers[item_id]['disabled']

        checkbox = []
        for variant_id in map(str, range(len(variants))):
            variant = variants[variant_id]
            checkbutton = Checkbutton(variants_frame)
            checkbutton.config(cursor='hand2')
            checkbutton.config(text=variant, font=resourses.constants.CHECKBUTTON_TEXT_FONT, wraplength=400)
            checkbutton_var = IntVar()
            checkbutton.config(variable=checkbutton_var)
            checkbutton.config(command=(
                lambda item_id=item_id, variant_id=variant_id, checkbutton_var=checkbutton_var: toggle_checkbutton(
                    checkbutton_var, item_id, variant_id,
                    user_answers)))
            checkbutton.pack(side=TOP, anchor=NW, padx=150)
            checkbox.append(checkbutton)

            # restore state of the checkbutton
            if variant_id in user_answers[item_id]['answers']:
                checkbutton.toggle()
            # print(user_answers[item_id]['answers'])
            if disabled:
                checkbutton.config(state=DISABLED)
            else:
                checkbutton.config(state=NORMAL)


    elif item_type == 'radiobutton':
        # return
        disabled = user_answers[item_id]['disabled']

        radiobox = []
        radiobutton_var = IntVar()
        radiobutton_var.set(-1)

        for variant_id in map(str, range(len(variants))):
            variant = variants[variant_id]
            radiobutton = Radiobutton(variants_frame)
            radiobutton.config(text=variant, font=resourses.constants.CHECKBUTTON_TEXT_FONT, wraplength=400)
            radiobutton.config(cursor='hand2')
            radiobutton.config(variable=radiobutton_var, value=variant_id)
            radiobutton.config(command=(lambda item_id=item_id, variant_id=variant_id, radiobutton_var=radiobutton_var:
                                        select_radiobutton(radiobutton_var, item_id, variant_id, user_answers)))
            radiobutton.pack(side=TOP, anchor=NW, padx=150)
            radiobox.append(radiobutton)

            # restore state of the radiobutton
            if variant_id in user_answers[item_id]['answers']:
                radiobutton.select()
            else:
                radiobutton.deselect()

            if disabled:
                radiobutton.config(state=DISABLED)
            else:
                radiobutton.config(state=NORMAL)
    else:
        print('UNEXPECTED ITEM TYPE (should be entry or checkbutton or radiobutton)')

    if False:
        print('id :', item['id'])
        print('type :', item['type'])
        print('question :', item['question'])
        print('answer :', item['answer'])


def get_results(user_answers, parsed):
    """
    Returns pair of correct answer count and total questions count.
    """

    count = 0
    for i in range(len(user_answers)):
        if user_answers[i]['answers'] == set(parsed[str(i)]['answers'].values()):
            count += 1
    return count, len(parsed)


def testing(root, parsed):
    """
    Creates window with main functionality of the application. Displays results of user testing on main (root) window.
    """

    user_answers = {i: {'disabled': False, 'answers': set()} for i in range(len(parsed))}
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
        btn.config(
            command=(lambda item_id=item_id: go_to_question(item_id, -1, parsed, nav_buttons, msg, variants_frame,
                                                            btn_prev, btn_comfirm, btn_next, user_answers, win)))
        btn.pack(side=LEFT, padx=10, pady=10)
        nav_buttons.append(btn)
    nav_frame.pack(expand=NO, fill=BOTH)
    print(nav_buttons[0] is nav_buttons[1])

    msg = Message(main_frame)
    msg.config(font=resourses.constants.MESSAGE_FONT, justify=CENTER, width=700)
    msg.config(bg="#EEE")
    msg.pack(expand=YES, fill=BOTH)

    variants_frame = Frame(main_frame)
    variants_frame.config(bg='#EEE')
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

    go_to_question(0, -1, parsed, nav_buttons, msg, variants_frame, btn_prev, btn_comfirm, btn_next, user_answers, win)

    # win.protocol('WM_DELETE_WINDOW', win.quit)
    win.focus_set()
    # win.grab_set()
    win.wait_window()

    # Окно тестирования закрыто

    root.deiconify()
    # welcome_msg.config(text=repr(user_answers))
    root.title('Результаты')
    btn_start.config(text='Начать заново')

    user_result, total = get_results(user_answers, parsed)
    # user_result = 9
    welcome_msg_text = str(user_result) + ' / ' + str(total)
    normalized_user_result = user_result / total
    if normalized_user_result <= 0.4:
        welcome_msg_fg_color = 'red'
        welcome_msg_text += '\nПлохой результат'
    elif normalized_user_result <= 0.75:
        welcome_msg_fg_color = 'blue'
        welcome_msg_text += '\nХороший результат'
    else:
        welcome_msg_fg_color = 'green'
        welcome_msg_text += '\nОтличный результат'

    welcome_msg.config(text=welcome_msg_text, fg=welcome_msg_fg_color, font=resourses.constants.TEST_RESULT_FONT)


if __name__ == '__main__':

    path = 'resourses/questions.xml'
    parsed = xml_parser.parse(path)
    # parsed.popitem()

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
    footer_frame.pack(expand=NO, fill=BOTH)

    btn_start = Button(footer_frame, text='Начать тестирование', command=(lambda: testing(root, parsed)))
    btn_start.config(font=resourses.constants.BUTTON_FONT, bg="#BBB")
    btn_start.config(width=15, height=1)
    btn_start.pack(side=LEFT, expand=YES, fill=BOTH, padx=20, pady=20)

    btn_quit = Button(footer_frame, text='Завершить', command=footer_frame.quit)
    btn_quit.config(font=resourses.constants.BUTTON_FONT, bg='#BBB')
    btn_quit.config(width=15, height=1)
    btn_quit.pack(side=RIGHT, expand=YES, fill=BOTH, padx=20, pady=20)

    root.mainloop()
