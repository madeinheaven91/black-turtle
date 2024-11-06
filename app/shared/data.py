api_url = "https://schedule.mstimetables.ru/api/publications/" # + "group/lessons/"
req_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Content-Type": "application/json",
    "Accept": "*/*",
}

relative_day_tokens: set[str] = {
    "позавчера",
    "вчера",
    "сегодня",
    "завтра",
    "послезавтра"
}
absolute_day_tokens: set[str] = {
    "послезавтра",
    "пн",
    "понедельник",
    "вт",
    "вторник",
    "ср",
    "среда",
    "чт",
    "четверг",
    "пт",
    "пятница",
    "сб",
    "суббота",
    "вс",
    "воскресенье",
}
day_tokens = relative_day_tokens.union(absolute_day_tokens)
week_tokens: set[str] = {
    "эта",
    "этот",
    "текущая",
    "текущий",
    "след",
    "следующий",
    "следующая",
    "пред",
    "предыдущий",
    "предыдущая",
}

command_tokens: set[str] = {
    "пары",
    "помощь",
    "/start",
    "звонки",
    "фио",
    "регистрация",
    "клавиатура",
    "/kill",
    "/send",
    "/send_all",
    "/ban",
    "/unban",
    "/promote",
    "/stat"

}
