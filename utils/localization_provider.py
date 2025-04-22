import arc
import hikari

COMMAND_LOCALES = {
    "cutie": {
        hikari.Locale.EN_US: arc.LocaleResponse("cutie", "So cuute!"),
        hikari.Locale.RU:  arc.LocaleResponse("мило",  "Такая милота!"),
        hikari.Locale.UK:  arc.LocaleResponse("мило",  "Таке миле"),
    },
    "cutie meow": {
        hikari.Locale.EN_US: arc.LocaleResponse("meow", "Meow-meow-meow"),
        hikari.Locale.RU:  arc.LocaleResponse("мяу",  "Мяу-мяу-мяу"),
        hikari.Locale.UK:  arc.LocaleResponse("мяу",  "Мяу-Мяу-Мяу"),
    },
    "cutie bark": {
        hikari.Locale.EN_US: arc.LocaleResponse("bark", "Bark-bark-bark"),
        hikari.Locale.RU:  arc.LocaleResponse("фыр",  "Фыр-фыр-фыр"),
        hikari.Locale.UK:  arc.LocaleResponse("фрр",  "фир-фир-фря"),
    },
    "cutie ribbit": {
        hikari.Locale.EN_US: arc.LocaleResponse("ribbit", "Ribbit-ribbit-ribbit"),
        hikari.Locale.RU:  arc.LocaleResponse("ква",    "Ква-ква-ква"),
        hikari.Locale.UK:  arc.LocaleResponse("ква",    "Ква-ква-ква"),
    },
    "cutie honk": {
        hikari.Locale.EN_US: arc.LocaleResponse("honk",   "Hooooonk"),
        hikari.Locale.RU:  arc.LocaleResponse("га",     "Гаааааа"),
        hikari.Locale.UK:  arc.LocaleResponse("га",     "Гаааааа"),
    },
    "emotions": {
        hikari.Locale.EN_US: arc.LocaleResponse("emotions", "Express your feelings!"),
        hikari.Locale.RU:  arc.LocaleResponse("эмоции",    "Выразите свои чувства!"),
        hikari.Locale.UK:  arc.LocaleResponse("емоції",    "Виразіть свої почуття!"),
    },
    "emotions hug": {
        hikari.Locale.EN_US: arc.LocaleResponse("hug",       "Give someone a hug"),
        hikari.Locale.RU:  arc.LocaleResponse("обнять",    "Обнимите кого-нибудь"),
        hikari.Locale.UK:  arc.LocaleResponse("обійняти",  "Обійміть когось"),
    },
    "emotions kick": {
        hikari.Locale.EN_US: arc.LocaleResponse("kick",      "Kick someone."),
        hikari.Locale.RU:  arc.LocaleResponse("пнуть",     "Пнуть кого-нибудь."),
        hikari.Locale.UK:  arc.LocaleResponse("вдарити",   "Вдарити когось."),
    },
    "emotions greet": {
        hikari.Locale.EN_US: arc.LocaleResponse("greet",          "Greet someone."),
        hikari.Locale.RU:  arc.LocaleResponse("приветствие",    "Поздоровайтесь с кем-нибудь"),
        hikari.Locale.UK:  arc.LocaleResponse("привітання",     "Привітайтеся з кимось"),
    },
    "emotions kiss": {
        hikari.Locale.EN_US: arc.LocaleResponse("kiss",       "Kiss your lover"),
        hikari.Locale.RU:  arc.LocaleResponse("поцеловать", "Поцелуйте свою вторую половинку"),
        hikari.Locale.UK:  arc.LocaleResponse("поцілувати", "Поцілуйте свою другу половинку"),
    },
    "emotions pet": {
        hikari.Locale.EN_US: arc.LocaleResponse("pet",         "Pet someone!"),
        hikari.Locale.RU:  arc.LocaleResponse("погладить",    "Погладьте кого-нибудь!"),
        hikari.Locale.UK:  arc.LocaleResponse("погладити",    "Погладьте когось!"),
    },
    "emotions smile": {
        hikari.Locale.EN_US: arc.LocaleResponse("smile",      "That's what it means."),
        hikari.Locale.RU:  arc.LocaleResponse("улыбка",     "Вот что это значит."),
        hikari.Locale.UK:  arc.LocaleResponse("посмішка",   "Ось що це означає."),
    },
    "emotions cry": {
        hikari.Locale.EN_US: arc.LocaleResponse("cry",        "Cry about it?"),
        hikari.Locale.RU:  arc.LocaleResponse("плакать",    "Поплакать об этом?"),
        hikari.Locale.UK:  arc.LocaleResponse("плакати",    "Поплакати про це?"),
    },
    "emotions sorry": {
        hikari.Locale.EN_US: arc.LocaleResponse("sorry",     "Sorry to whoever you screwed up!"),
        hikari.Locale.RU:  arc.LocaleResponse("извиниться","Извинитесь перед тем, кого подвели!"),
        hikari.Locale.UK:  arc.LocaleResponse("вибачитися","Вибачтеся перед тим, кого підвели!"),
    },
    "emotions handshake": {
        hikari.Locale.EN_US: arc.LocaleResponse("handshake", "Shake hands with someone."),
        hikari.Locale.RU:  arc.LocaleResponse("рукопожатие","Пожмите кому-нибудь руку."),
        hikari.Locale.UK:  arc.LocaleResponse("рукостискання","Потисніть комусь руку."),
    },
    "emotions tickle": {
        hikari.Locale.EN_US: arc.LocaleResponse("tickle",    "Tickle someone."),
        hikari.Locale.RU:  arc.LocaleResponse("щекотать",  "Пощекочите кого-нибудь."),
        hikari.Locale.UK:  arc.LocaleResponse("лоскотати", "Полоскочіть когось."),
    },
    "emotions midfinger": {
        hikari.Locale.EN_US: arc.LocaleResponse("midfinger","Fun third finger."),
        hikari.Locale.RU:  arc.LocaleResponse("средний-палец","Весёлый третий палец."),
        hikari.Locale.UK:  arc.LocaleResponse("середній-палець","Веселий третій палець."),
    },
    "anime": {
        hikari.Locale.EN_US: arc.LocaleResponse("anime", "Anime images."),
        hikari.Locale.RU:  arc.LocaleResponse("аниме", "Анимешные картинки."),
        hikari.Locale.UK:  arc.LocaleResponse("аніме", "Аніме картинки."),
    },
    "anime neko": {
        hikari.Locale.EN_US: arc.LocaleResponse("neko", "Cat-girls"),
        hikari.Locale.RU:  arc.LocaleResponse("неко", "Кошкодевочки"),
        hikari.Locale.UK:  arc.LocaleResponse("неко", "Кішкодівчата"),
    },
    "anime kitsune": {
        hikari.Locale.EN_US: arc.LocaleResponse("kitsune",       "Foxy girls, huh?"),
        hikari.Locale.RU:  arc.LocaleResponse("лиса",      "Лисички, да?"),
        hikari.Locale.UK:  arc.LocaleResponse("лисиця",    "Лисички, так?"),
    },
    "anime waifu": {
        hikari.Locale.EN_US: arc.LocaleResponse("waifu",     "Yours and not just wafu!"),
        hikari.Locale.RU:  arc.LocaleResponse("вайфу",     "Твоя и не только вайфу!"),
        hikari.Locale.UK:  arc.LocaleResponse("вайфу",     "Твоя і не тільки вайфу!"),
    },
    "anime husbando": {
        hikari.Locale.EN_US: arc.LocaleResponse("husbando", "Yours and not just men!"),
        hikari.Locale.RU:  arc.LocaleResponse("хусбандо", "Твой и не только мужчины!"),
        hikari.Locale.UK:  arc.LocaleResponse("хусбандо", "Твій і не тільки чоловіки!"),
    },
    "suicide": {
        hikari.Locale.EN_US: arc.LocaleResponse("suicide", "Press F."),
        hikari.Locale.RU:  arc.LocaleResponse("суицид",  "Нажмите F."),
        hikari.Locale.UK:  arc.LocaleResponse("суїцид",  "Натисніть F."),
    },
    "arsenal": {
        hikari.Locale.EN_US: arc.LocaleResponse("arsenal", "Nukes, Mivinki - do you need it?"),
        hikari.Locale.RU:  arc.LocaleResponse("арсенал","Ядерки, мивинки – тебе оно нужно?"),
        hikari.Locale.UK:  arc.LocaleResponse("арсенал","Ядерки, мівінки – тобі воно нужно?"),
    },
    "nuclear": {
        hikari.Locale.EN_US: arc.LocaleResponse("nuclear", "Nuke a man."),
        hikari.Locale.RU:  arc.LocaleResponse("ядерка",   "Запустить ядерку в человека."),
        hikari.Locale.UK:  arc.LocaleResponse("ядерка",   "Запустити ядерку в людину."),
    },
    "mivina": {
        hikari.Locale.EN_US: arc.LocaleResponse("mivina",  "Use mivinka for treatment."),
        hikari.Locale.RU:  arc.LocaleResponse("мивина",   "Используйте мивинку для лечения."),
        hikari.Locale.UK:  arc.LocaleResponse("мівіна",   "Використовуйте мівінку для лікування."),
    },
    "case": {
        hikari.Locale.EN_US: arc.LocaleResponse("case",   "Issuing nukes and mivinas."),
        hikari.Locale.RU:  arc.LocaleResponse("кейс",   "Выдача ядерок и мивинок."),
        hikari.Locale.UK:  arc.LocaleResponse("кейс",   "Видача ядерок і мівінок."),
    },
    "top": {
        hikari.Locale.EN_US: arc.LocaleResponse("top", "Top users."),
        hikari.Locale.RU:  arc.LocaleResponse("топ", "Топ пользователей."),
        hikari.Locale.UK:  arc.LocaleResponse("топ", "Топ користувачів."),
    },
    "top bumps": {
        hikari.Locale.EN_US: arc.LocaleResponse("bumps",    "Top users by bump."),
        hikari.Locale.RU:  arc.LocaleResponse("бампы",     "Топ пользователи по бампам."),
        hikari.Locale.UK:  arc.LocaleResponse("бампи",     "Топ користувачів за бампи."),
    },
    "top messages": {
        hikari.Locale.EN_US: arc.LocaleResponse("messages",    "Top users by messages."),
        hikari.Locale.RU:  arc.LocaleResponse("сообщения",    "Топ пользователи по сообщениям."),
        hikari.Locale.UK:  arc.LocaleResponse("топ-повідомлення", "Топ користувачів за повідомленнями."),
    },
    "top voice": {
        hikari.Locale.EN_US: arc.LocaleResponse("voice",    "Top users by length of time in voice channel."),
        hikari.Locale.RU:  arc.LocaleResponse("голос",     "Топ пользователи по времени в голосовом канале."),
        hikari.Locale.UK:  arc.LocaleResponse("голос",     "Топ користувачів за часом у голосовому каналі."),
    },
    "profile": {
        hikari.Locale.EN_US: arc.LocaleResponse("profile", "User Profile."),
        hikari.Locale.RU:  arc.LocaleResponse("профиль", "Профиль пользователя."),
        hikari.Locale.UK:  arc.LocaleResponse("профіль", "Профіль користувача."),
    },
    "biography": {
        hikari.Locale.EN_US: arc.LocaleResponse("bio", "Learn the story of one of the heroines!"),
        hikari.Locale.RU:  arc.LocaleResponse("био", "Узнайте историю одной из героинь!"),
        hikari.Locale.UK:  arc.LocaleResponse("біо", "Дізнайтесь історію однієї з героїнь!"),
    },
    "biography marmeladkabio": {
        hikari.Locale.EN_US: arc.LocaleResponse("marmeladka", "Find out more about Marmeladka!"),
        hikari.Locale.RU:  arc.LocaleResponse("мармеладка", "Узнайте больше о Мармеладке!"),
        hikari.Locale.UK:  arc.LocaleResponse("мармеладка", "Дізнайтесь більше про Мармеладку!"),
    },
    "biography zefirkabio": {
        hikari.Locale.EN_US: arc.LocaleResponse("zefirka", "Find out more about Zefirka!"),
        hikari.Locale.RU:  arc.LocaleResponse("зефирка", "Узнайте больше о Зефирке!"),
        hikari.Locale.UK:  arc.LocaleResponse("зефірка", "Дізнайтесь більше про Зефірку!"),
    },
    "biography shocomelkabio": {
        hikari.Locale.EN_US: arc.LocaleResponse("shocomelka", "Find out more about Shocomelka!"),
        hikari.Locale.RU:  arc.LocaleResponse("шокомелка",  "Узнайте больше о Шокомелке!"),
        hikari.Locale.UK:  arc.LocaleResponse("шокомелка",  "Дізнайтесь більше про Шокомелку!"),
    },
    "biography milkabio": {
        hikari.Locale.EN_US: arc.LocaleResponse("milka", "Find out more about Milka!"),
        hikari.Locale.RU:  arc.LocaleResponse("милка", "Узнайте больше о Милке!"),
        hikari.Locale.UK:  arc.LocaleResponse("мілка", "Дізнайтесь більше про Мілку!"),
    },
    "help": {
        hikari.Locale.EN_US: arc.LocaleResponse("help", "A quick tour of the server."),
        hikari.Locale.RU:  arc.LocaleResponse("помощь",  "Быстрая экскурсия по серверу."),
        hikari.Locale.UK:  arc.LocaleResponse("допомога","Швидка екскурсія по серверу."),
    },
    "randomnumber": {
        hikari.Locale.EN_US: arc.LocaleResponse("random-number", "A random number from and to."),
        hikari.Locale.RU:  arc.LocaleResponse("случайное-число","Случайное число от и до."),
        hikari.Locale.UK:  arc.LocaleResponse("випадкове-число","Випадкове число від і до."),
    },
    "clear": {
        hikari.Locale.EN_US: arc.LocaleResponse("clear", "Clears a specified number of messages."),
        hikari.Locale.RU:  arc.LocaleResponse("очистить","Очищает заданное количество сообщений."),
        hikari.Locale.UK:  arc.LocaleResponse("очистити","Очищає вказану кількість повідомлень."),
    },
    "setup-private-voice": {
        hikari.Locale.EN_US: arc.LocaleResponse("setup-private-voice", "Set up a private voice channel."),
        hikari.Locale.RU:  arc.LocaleResponse("setup-private-voice", "Настройка приватного голосового канала."),
        hikari.Locale.UK:  arc.LocaleResponse("setup-private-voice", "Налаштування приватного голосового канала."),
    }
}

OPTION_LOCALES = {
    "emotions hug": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who to hug?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь", "Кого обнять?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Кого обійняти?"),
        },
    },
    "emotions kick": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Kick who?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь", "Кого пнуть?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Кого вдарити?"),
        },
    },
    "emotions greet": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who are you greeting?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","С кем здороваешься?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",  "З ким вітаєшся?"),
        },
    },
    "emotions kiss": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who to kiss?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь", "Кого поцеловать?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Кого поцілувати?"),
        },
    },
    "emotions pet": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who to pet?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","Кого погладить?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Кого погладити?"),
        },
    },
    "emotions sorry": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Screwed up in front of who?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","Перед кем провинился?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Перед ким провинився?"),
        },
    },
    "emotions handshake": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who are you shaking hands with?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","С кем пожимаешь руку?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "З ким тиснеш руку?"),
        },
    },
    "emotions tickle": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Who to tickle?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","Кого щекотать?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Кого лоскотати?"),
        },
    },
    "nuclear": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Launch at who?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","В кого запустить?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "В кого запустити?"),
        },
        "name": {
            hikari.Locale.EN_US: arc.LocaleResponse("name",     "What is the name of the nuclear bomb?"),
            hikari.Locale.RU:  arc.LocaleResponse("название", "Название запускаемого боезаряда."),
            hikari.Locale.UK:  arc.LocaleResponse("назва",    "Назва запусканого боєзаряду."),
        },
    },
    "profile": {
        "user": {
            hikari.Locale.EN_US: arc.LocaleResponse("user", "Whose profile are you looking at?"),
            hikari.Locale.RU:  arc.LocaleResponse("пользователь","Чей профиль вы хотите посмотреть?"),
            hikari.Locale.UK:  arc.LocaleResponse("користувач",   "Чий профіль ви хочете подивитися?"),
        },
    },
    "randomnumber": {
        "first_number": {
            hikari.Locale.EN_US: arc.LocaleResponse("first_number", "Start point."),
            hikari.Locale.RU:  arc.LocaleResponse("первое_число","Точка старта."),
            hikari.Locale.UK:  arc.LocaleResponse("перше_число",  "Точка старту."),
        },
        "second_number": {
            hikari.Locale.EN_US: arc.LocaleResponse("second_number","End point."),
            hikari.Locale.RU:  arc.LocaleResponse("второе_число","Точка конца."),
            hikari.Locale.UK:  arc.LocaleResponse("друге_число",  "Точка кінця."),
        },
    },
    "clear": {
        "amount": {
            hikari.Locale.EN_US: arc.LocaleResponse("amount", "Number of messages to delete."),
            hikari.Locale.RU:  arc.LocaleResponse("количество", "Количество сообщений для удаления."),
            hikari.Locale.UK:  arc.LocaleResponse("кількість",  "Кількість повідомлень для видалення."),
        },
    },
}
