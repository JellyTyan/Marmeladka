import lightbulb
import hikari


localization_provider = lightbulb.DictLocalizationProvider({
    hikari.Locale.EN_US: {
        # Cutie commands
        "commands.cutie.name": "cutie",
        "commands.cutie.description": "So cuute!",

        "commands.frogimage.name": "ribbit",
        "commands.frogimage.description": "Ribbit-ribbit-ribbit",

        "commands.catimage.name": "meow",
        "commands.catimage.description": "Meow-meow-meow",

        "commands.foximage.name": "bark",
        "commands.foximage.description": "Bark-bark-bark",

        "commands.gooseimage.name": "honk",
        "commands.gooseimage.description": "Hooooonk",
        # Emotion commands
        "commands.emotions.name": "emotions",
        "commands.emotions.description": "Express your feelings!",

        "commands.hug.name": "hug",
        "commands.hug.description": "Give someone a hug",
        "commands.hug.options.user.name": "user",
        "commands.hug.options.user.description": "Who to hug?",

        "commands.kick.name": "kick",
        "commands.kick.description": "Kick someone.",
        "commands.kick.options.user.name": "user",
        "commands.kick.options.user.description": "Kick who?",

        "commands.hi.name": "greet",
        "commands.hi.description": "Greet someone",
        "commands.hi.options.user.name": "user",
        "commands.hi.options.user.description": "Who are you greeting?",

        "commands.kiss.name": "kiss",
        "commands.kiss.description": "Kiss your lover",
        "commands.kiss.options.user.name": "user",
        "commands.kiss.options.user.description": "Who to kiss?",

        "commands.pet.name": "pet",
        "commands.pet.description": "Pet someone!",
        "commands.pet.options.user.name": "user",
        "commands.pet.options.user.description": "Who to pet?",

        "commands.smile.name": "smile",
        "commands.smile.description": "That's what it means.",

        "commands.cry.name": "cry",
        "commands.cry.description": "Cry about it?",

        "commands.sorry.name": "sorry",
        "commands.sorry.description": "Sorry to whoever you screwed up!",
        "commands.sorry.options.user.name": "user",
        "commands.sorry.options.user.description": "Screwed up in front of who?",

        "commands.handshake.name": "handshake",
        "commands.handshake.description": "Shake hands with someone.",
        "commands.handshake.options.user.name": "user",
        "commands.handshake.options.user.description": "Who are you shaking hands with?",

        "commands.tickle.name": "tickle",
        "commands.tickle.description": "Tickle someone.",
        "commands.tickle.options.user.name": "user",
        "commands.tickle.options.user.description": "Who to tickle?",

        "commands.midfinger.name": "midfinger",
        "commands.midfinger.description": "Fun third finger.",
        # Neko commands
        "commands.anime.name": "anime",
        "commands.anime.description": "anime images.",

        "commands.neko.name": "neko",
        "commands.neko.description": "Cat-girls",

        "commands.fox.name": "fox",
        "commands.fox.description": "Foxy girls, huh?",

        "commands.waifu.name": "waifu",
        "commands.waifu.description": "Yours and not just wafu!",

        "commands.husbando.name": "husbando",
        "commands.husbando.description": "Yours and not just men!",
        # Nuclear commands
        "commands.suicide.name": "suicide",
        "commands.suicide.description": "Press F.",

        "commands.arsenal.name": "arsenal",
        "commands.arsenal.description": "Nukes, Mivinki - do you need it?",

        "commands.startbomb.name": "nuclear",
        "commands.startbomb.description": "Nuke a man.",
        "commands.startbomb.options.user.name": "user",
        "commands.startbomb.options.user.description": "Launch at who?",
        "commands.startbomb.options.string.name": "name",
        "commands.startbomb.options.string.description": "Название пускаемого бое-заряда.",

        "commands.startmivina.name": "mivina",
        "commands.startmivina.description": "Use mivinka for treatment.",

        "commands.nuclearcase.name": "case",
        "commands.nuclearcase.description": "Issuing nukes and mivinas.",
        # Top commands
        "commands.topbumps.name": "top-bumps",
        "commands.topbumps.description": "Top users by bump.",

        "commands.topmessages.name": "top-messages",
        "commands.topmessages.description": "Top users by messages.",

        "commands.topvoice.name": "top-voice",
        "commands.topvoice.description": "Top users by length of time in voice channel.",

        "commands.userprofile.name": "profile",
        "commands.userprofile.description": "User Profile.",
        "commands.userprofile.options.user.name": "user",
        "commands.userprofile.options.user.description": "Whose profile are you looking at?",
        # Information commands
        "commands.biography.name": "bio",
        "commands.biography.description": "Learn the story of one of the heroines!",

        "commands.marmeladkabio.name": "marmeladka",
        "commands.marmeladkabio.description": "Find out more about Marmeladka!",

        "commands.zefirkabio.name": "zefirka",
        "commands.zefirkabio.description": "Find out more about Zefirka!",

        "commands.shocomelkabio.name": "shocomelka",
        "commands.shocomelkabio.description": "Find out more about Shocomelka!",

        "commands.milkabio.name": "milka",
        "commands.milkabio.description": "Find out more about Milka!",
        # Tech commands
        "commands.help.name": "help",
        "commands.help.description": "A quick tour of the server.",

        "commands.randomnumber.name": "randomnumber",
        "commands.randomnumber.description": "A random number from and to.",
        "commands.randomnumber.options.first_number.name": "first_number",
        "commands.randomnumber.options.first_number.description": "Start point.",
        "commands.randomnumber.options.second_number.name": "second_number",
        "commands.randomnumber.options.second_number.description": "End point.",

        "commands.clear.name": "clear",
        "commands.clear.description": "Clears a specified number of messages.",
        "commands.clear.options.amount.name": "amount",
        "commands.clear.options.amount.description": "Number of messages to delete.",
    },
    hikari.Locale.RU: {
        # Cutie commands
        "commands.cutie.name": "мило",
        "commands.cutie.description": "Такая милота!",

        "commands.frogimage.name": "ква",
        "commands.frogimage.description": "Ква-ква-ква",

        "commands.catimage.name": "мяу",
        "commands.catimage.description": "Мяу-мяу-мяу",

        "commands.foximage.name": "фыр",
        "commands.foximage.description": "Фыр-фыр-фыр",

        "commands.gooseimage.name": "га",
        "commands.gooseimage.description": "Гааааааа",
        # Emotions commands
        "commands.emotions.name": "эмоции",
        "commands.emotions.description": "Выразите свои чувства!",

        "commands.hug.name": "обнять",
        "commands.hug.description": "Обнимите кого-нибудь",
        "commands.hug.options.user.name": "пользователь",
        "commands.hug.options.user.description": "Кого обнять?",

        "commands.kick.name": "пнуть",
        "commands.kick.description": "Пнуть кого-нибудь.",
        "commands.kick.options.user.name": "пользователь",
        "commands.kick.options.user.description": "Кого пнуть?",

        "commands.hi.name": "приветствие",
        "commands.hi.description": "Поздоровайтесь с кем-нибудь",
        "commands.hi.options.user.name": "пользователь",
        "commands.hi.options.user.description": "С кем здороваешься?",

        "commands.kiss.name": "поцеловать",
        "commands.kiss.description": "Поцелуйте свою вторую половинку",
        "commands.kiss.options.user.name": "пользователь",
        "commands.kiss.options.user.description": "Кого поцеловать?",

        "commands.pet.name": "погладить",
        "commands.pet.description": "Погладьте кого-нибудь!",
        "commands.pet.options.user.name": "пользователь",
        "commands.pet.options.user.description": "Кого погладить?",

        "commands.smile.name": "улыбка",
        "commands.smile.description": "Вот что это значит.",

        "commands.cry.name": "плакать",
        "commands.cry.description": "Поплакать об этом?",

        "commands.sorry.name": "извиниться",
        "commands.sorry.description": "Извинитесь перед тем, кого подвели!",
        "commands.sorry.options.user.name": "пользователь",
        "commands.sorry.options.user.description": "Перед кем провинился?",

        "commands.handshake.name": "рукопожатие",
        "commands.handshake.description": "Пожмите кому-нибудь руку.",
        "commands.handshake.options.user.name": "пользователь",
        "commands.handshake.options.user.description": "С кем пожимаешь руку?",

        "commands.tickle.name": "щекотать",
        "commands.tickle.description": "Пощекочите кого-нибудь.",
        "commands.tickle.options.user.name": "пользователь",
        "commands.tickle.options.user.description": "Кого щекотать?",

        "commands.midfinger.name": "средний-палец",
        "commands.midfinger.description": "Весёлый третий палец.",
        # Neko commands
        "commands.anime.name": "аниме",
        "commands.anime.description": "Анимешные картинки.",

        "commands.neko.name": "неко",
        "commands.neko.description": "Кошкодевочки",

        "commands.fox.name": "лиса",
        "commands.fox.description": "Лисички, да?",

        "commands.waifu.name": "вайфу",
        "commands.waifu.description": "Твоя и не только вайфу!",

        "commands.husbando.name": "хусбандо",
        "commands.husbando.description": "Твой и не только мужчины!",
        # Nuclear commands
        "commands.suicide.name": "суицид",
        "commands.suicide.description": "Нажмите F.",

        "commands.arsenal.name": "арсенал",
        "commands.arsenal.description": "Ядерки, мивинки – тебе оно нужно?",

        "commands.startbomb.name": "ядерка",
        "commands.startbomb.description": "Запустить ядерку в человека.",
        "commands.startbomb.options.user.name": "пользователь",
        "commands.startbomb.options.user.description": "В кого запустить?",
        "commands.startbomb.options.string.name": "название",
        "commands.startbomb.options.string.description": "Название запускаемого боезаряда.",

        "commands.startmivina.name": "мивина",
        "commands.startmivina.description": "Используйте мивинку для лечения.",

        "commands.nuclearcase.name": "кейс",
        "commands.nuclearcase.description": "Выдача ядерок и мивинок.",
        # Top commands
        "commands.topbumps.name": "топ-бампы",
        "commands.topbumps.description": "Топ пользователи по бампам.",

        "commands.topmessages.name": "топ-сообщения",
        "commands.topmessages.description": "Топ пользователи по сообщениям.",

        "commands.topvoice.name": "топ-голос",
        "commands.topvoice.description": "Топ пользователи по времени в голосовом канале.",

        "commands.userprofile.name": "профиль",
        "commands.userprofile.description": "Профиль пользователя.",
        "commands.userprofile.options.user.name": "пользователь",
        "commands.userprofile.options.user.description": "Чей профиль вы хотите посмотреть?",
        # Information commands
        "commands.biography.name": "био",
        "commands.biography.description": "Узнайте историю одной из героинь!",

        "commands.marmeladkabio.name": "мармеладка",
        "commands.marmeladkabio.description": "Узнайте больше о Мармеладке!",

        "commands.zefirkabio.name": "зефирка",
        "commands.zefirkabio.description": "Узнайте больше о Зефирке!",

        "commands.shocomelkabio.name": "шокомелка",
        "commands.shocomelkabio.description": "Узнайте больше о Шокомелке!",

        "commands.milkabio.name": "милка",
        "commands.milkabio.description": "Узнайте больше о Милке!",
        # Tech commands
        "commands.help.name": "помощь",
        "commands.help.description": "Быстрая экскурсия по серверу.",

        "commands.randomnumber.name": "случайноечисло",
        "commands.randomnumber.description": "Случайное число от и до.",
        "commands.randomnumber.options.first_number.name": "первое_число",
        "commands.randomnumber.options.first_number.description": "Точка старта.",
        "commands.randomnumber.options.second_number.name": "второе_число",
        "commands.randomnumber.options.second_number.description": "Точка конца.",

        "commands.clear.name": "очистить",
        "commands.clear.description": "Очищает заданное количество сообщений.",
        "commands.clear.options.amount.name": "количество",
        "commands.clear.options.amount.description": "Количество сообщений для удаления.",
    },
    hikari.Locale.UK: {
        # Cutie commands
        "commands.cutie.name": "мило",
        "commands.cutie.description": "Таке миле",

        "commands.frogimage.name": "ква",
        "commands.frogimage.description": "Ква-ква-ква",

        "commands.catimage.name": "мяу",
        "commands.catimage.description": "Мяу-Мяу-Мяу",

        "commands.foximage.name": "фрр",
        "commands.foximage.description": "фир-фир-фря",

        "commands.gooseimage.name": "га",
        "commands.gooseimage.description": "Гаааааа",
        # Emotions commands
        "commands.emotions.name": "емоції",
        "commands.emotions.description": "Виразіть свої почуття!",

        "commands.hug.name": "обійняти",
        "commands.hug.description": "Обійміть когось",
        "commands.hug.options.user.name": "користувач",
        "commands.hug.options.user.description": "Кого обійняти?",

        "commands.kick.name": "вдарити",
        "commands.kick.description": "Вдарити когось.",
        "commands.kick.options.user.name": "користувач",
        "commands.kick.options.user.description": "Кого вдарити?",

        "commands.hi.name": "привітання",
        "commands.hi.description": "Привітайтеся з кимось",
        "commands.hi.options.user.name": "користувач",
        "commands.hi.options.user.description": "З ким вітаєшся?",

        "commands.kiss.name": "поцілувати",
        "commands.kiss.description": "Поцілуйте свою другу половинку",
        "commands.kiss.options.user.name": "користувач",
        "commands.kiss.options.user.description": "Кого поцілувати?",

        "commands.pet.name": "погладити",
        "commands.pet.description": "Погладьте когось!",
        "commands.pet.options.user.name": "користувач",
        "commands.pet.options.user.description": "Кого погладити?",

        "commands.smile.name": "посмішка",
        "commands.smile.description": "Ось що це означає.",

        "commands.cry.name": "плакати",
        "commands.cry.description": "Поплакати про це?",

        "commands.sorry.name": "вибачитися",
        "commands.sorry.description": "Вибачтеся перед тим, кого підвели!",
        "commands.sorry.options.user.name": "користувач",
        "commands.sorry.options.user.description": "Перед ким провинився?",

        "commands.handshake.name": "рукостискання",
        "commands.handshake.description": "Потисніть комусь руку.",
        "commands.handshake.options.user.name": "користувач",
        "commands.handshake.options.user.description": "З ким тиснеш руку?",

        "commands.tickle.name": "лоскотати",
        "commands.tickle.description": "Полоскочіть когось.",
        "commands.tickle.options.user.name": "користувач",
        "commands.tickle.options.user.description": "Кого лоскотати?",

        "commands.midfinger.name": "середній-палець",
        "commands.midfinger.description": "Веселий третій палець.",
        # Neko commands
        "commands.anime.name": "аніме",
        "commands.anime.description": "Аніме картинки.",

        "commands.neko.name": "неко",
        "commands.neko.description": "Кішкодівчата",

        "commands.fox.name": "лисиця",
        "commands.fox.description": "Лисички, так?",

        "commands.waifu.name": "вайфу",
        "commands.waifu.description": "Твоя і не тільки вайфу!",

        "commands.husbando.name": "хусбандо",
        "commands.husbando.description": "Твій і не тільки чоловіки!",
        # Nuclear commands
        "commands.suicide.name": "суїцид",
        "commands.suicide.description": "Натисніть F.",

        "commands.arsenal.name": "арсенал",
        "commands.arsenal.description": "Ядерки, мівінки – тобі воно нужно?",

        "commands.startbomb.name": "ядерка",
        "commands.startbomb.description": "Запустити ядерку в людину.",
        "commands.startbomb.options.user.name": "користувач",
        "commands.startbomb.options.user.description": "В кого запустити?",
        "commands.startbomb.options.string.name": "назва",
        "commands.startbomb.options.string.description": "Назва запусканого боєзаряду.",

        "commands.startmivina.name": "мівіна",
        "commands.startmivina.description": "Використовуйте мівінку для лікування.",

        "commands.nuclearcase.name": "кейс",
        "commands.nuclearcase.description": "Видача ядерок і мівінок.",
        # Top commands
        "commands.topbumps.name": "топ-бампи",
        "commands.topbumps.description": "Топ користувачів за бампи.",

        "commands.topmessages.name": "топ-повідомлення",
        "commands.topmessages.description": "Топ користувачів за повідомленнями.",

        "commands.topvoice.name": "топ-голос",
        "commands.topvoice.description": "Топ користувачів за часом у голосовому каналі.",

        "commands.userprofile.name": "профіль",
        "commands.userprofile.description": "Профіль користувача.",
        "commands.userprofile.options.user.name": "користувач",
        "commands.userprofile.options.user.description": "Чий профіль ви хочете подивитися?",
        # Information commands
        "commands.biography.name": "біо",
        "commands.biography.description": "Дізнайтеся історію однієї з героїнь!",

        "commands.marmeladkabio.name": "мармеладка",
        "commands.marmeladkabio.description": "Дізнайтеся більше про Мармеладку!",

        "commands.zefirkabio.name": "зефірка",
        "commands.zefirkabio.description": "Дізнайтеся більше про Зефірку!",

        "commands.shocomelkabio.name": "шокомелка",
        "commands.shocomelkabio.description": "Дізнайтеся більше про Шокомелку!",

        "commands.milkabio.name": "мілка",
        "commands.milkabio.description": "Дізнайтеся більше про Мілку!",
        # Tech commands
        "commands.help.name": "допомога",
        "commands.help.description": "Швидка екскурсія по серверу.",

        "commands.randomnumber.name": "випадкове_число",
        "commands.randomnumber.description": "Випадкове число від і до.",
        "commands.randomnumber.options.first_number.name": "перше_число",
        "commands.randomnumber.options.first_number.description": "Точка старту.",
        "commands.randomnumber.options.second_number.name": "друге_число",
        "commands.randomnumber.options.second_number.description": "Точка кінця.",

        "commands.clear.name": "очистити",
        "commands.clear.description": "Очищає вказану кількість повідомлень.",
        "commands.clear.options.amount.name": "кількість",
        "commands.clear.options.amount.description": "Кількість повідомлень для видалення."
    }
})
