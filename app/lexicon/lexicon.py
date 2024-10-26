LEXICON: dict[str, str] = {
    "ascii_art":
r"""
 ____  _     ____  ____  _  __   _____  _     ____  _____  _     _____
/  _ \/ \   /  _ \/   _\/ |/ /  /__ __\/ \ /\/  __\/__ __\/ \   /  __/
| | //| |   | / \||  /  |   /     / \  | | |||  \/|  / \  | |   |  \  
| |_\\| |_/\| |-|||  \_ |   \     | |  | \_/||    /  | |  | |_/\|  /_ 
\____/\____/\_/ \|\____/\_|\_\    \_/  \____/\_/\_\  \_/  \____/\____\
    """,

    "/start": 
"""✋ Привет! Я помогу узнать вам расписание <b>ГАПОУ КПК</b>!
Для начала, давайте выберем, чьи пары вы хотите смотреть.""",

    "reg_group_or_teacher":
        "❔ Вы хотите смотреть пары <b>группы</b> или <b>преподавателя</b>?",

    "reg_enter_group":
        "❔ Введите номер группы",

    "reg_enter_teacher":
        "❔ Введите фамилию преподавателя",

    "reg_cancel":
        """ℹ️ Хорошо! Вы можете зарегистрироваться в другой раз, прописав <b>регистрация</b>.
Чтобы узнать, что я могу, пропишите <b>помощь</b>!""",

    "reg_group_not_found":
                """⚠️ <b>Такой группы нет...</b>

Отправьте номер своей группы еще раз.""",

    "reg_group_selected":
                """✅ Отлично, группа выбрана! Теперь вы можете смотреть пары своей группы!
Чтобы узнать, что я могу, пропишите <b>помощь</b>!""",

    "reg_teacher_not_found":
        """⚠️ <b>Такого преподавателя нет...</b>

Отправьте фамилию еще раз.""",

    "reg_teacher_selected":
        """✅ Отлично, преподаватель выбран! Теперь вы можете смотреть его пары!
Чтобы узнать, что я могу, пропишите <b>помощь</b>!""",

    "cancel": "Отмена",

    "no_lessons": """————| <b>Нет расписания</b> |————

<b>На этот день распиания пока нет...</b>""",

    "bells_weekdays": 
"""   <b>Расписание звонков</b>
      <i>пн — пт</i>

<b>1 урок</b>    8:00 — 8:45
<b>2 урок</b>    8:50 — 9:35
<b>3 урок</b>    9:40 — 10:25
<b>4 урок</b>    10:45 — 11:30
<b>5 урок</b>    11:50 — 12:35
<b>6 урок</b>    12:55 — 13:40
<b>7 урок</b>    14:00 — 14:45
<b>8 урок</b>    15:00 — 15:45
<b>9 урок</b>    16:05 — 16:50
<b>10 урок</b>   16:55 — 17:40
<b>11 урок</b>   17:45 — 18:30
""",

    "bells_saturday": 
"""   <b>Расписание звонков</b>
      <i>суббота</i>

<b>1 урок</b>    8:00 — 8:45
<b>2 урок</b>    8:50 — 9:35
<b>3 урок</b>    9:45 — 10:30
<b>4 урок</b>    10:40 — 11:25
<b>5 урок</b>    11:35 — 12:20
<b>6 урок</b>    12:30 — 13:15
<b>7 урок</b>    13:20 — 14:05
<b>8 урок</b>    14:10 — 14:45
<b>9 урок</b>    15:00 — 15:45
<b>10 урок</b>   15:50 — 16:35
""",

    "help_generic": 
"""❓ На данный момент доступны команды:

        <b>Пары</b> - отправляет расписание пар на выбранный день
        <i>Подробнее: <u>помощь пары</u></i>

        <b>Фио</b> - отправляет ФИО преподавателя
        <i>Подробнее: <u>помощь фио</u></i>

        <b>Звонки</b> - отправляет расписание звонков
        <i>Подробнее: <u>помощь звонки</u></i>

        <b>Регистрация</b> - позволяет выбрать свою группу и удобнее смотреть пары

        <b>Клавиатура показать</b> - показывает клавиатуру внизу

        <b>Клавиатура убрать</b> - убирает клавиатуру внизу

Если возникнут трудности, в любое время можно написать в техподдержку! 😉""",

    "help_lessons": 
"""❓ <b>Пары:</b>    <i>пары   [ группа ]   [ день ]   [ неделя ]</i>

<b>Примеры:</b>
      -  пары 921
      -  пары 921 завтра 
      -  пары 921 вчера 
      -  пары 921 понедельник
      -  пары 921 вт
      -  пары 921 ср след
      -  пары 921 чт эта
      -  пары 921 пт прош
      -  пары 921 10.09.2024
      -  пары димитриев
      -  пары димитриев завтра
      -  пары димитриев понедельник
      -  пары александр олегович понедельник
      -  пары олегович понедельник
      -  пары димитриев александр олегович 24.10.2024

<b>Важно:</b> дату надо вводить в формате чч.мм.гггг, например <b>10.09.2024</b>. Позже мы сделаем так, чтобы можно было вводить и в других форматах

<i>Примечание:   если вы зарегистрировались, то номер писать необязательно, например <b>пары завтра</b></i>""",

    "help_fio": 
"""❓ <b>Фио:</b>     <i>фио   [ фамилия | имя | отчество ]</i>

<b>Примеры:</b>
        - фио Димитриев
        - фио Александр
        - фио Олегович

<i>Примечание:   информация может быть неправильной или устаревшей. Если что-то не так, пишите в техподдержку</i>""",

    "help_bells": 
"""❓ <b>Звонки:</b> <i>звонки   [ будни | суббота ]</i>

<b>Примеры:</b>
        - звонки
        - звонки будни
        - звонки суббота
        - звонки сб

<i>Примечание:   если написать просто <b>звонки</b>, то отправится расписание звонков на сегодня</i>""",

    "exception":
        """🚫 Что-то пошло не так...
Пропишите <b>помощь</b> для вывода списка команд""",

    "kb_hide":
        """✅ Убрал клавиатуру!""",

    "kb_show":
        """✅ Показываю клавиатуру!""",

    "not_available_in_groups":
        """🚫 Данная команда недоступна в групповых чатах!""",

    "err_se_not_selected":
        """🚫 Вы не выбрали чье расписание хотите смотреть!

Для этого пропишите <b>регистрация</b>""",

}
