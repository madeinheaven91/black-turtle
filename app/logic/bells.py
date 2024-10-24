from datetime import date
from lexicon import LEXICON

def bells_logic(specifier: str):
    match specifier:
        case "сб" | "суббота":
            result = LEXICON["bells_saturday"]
        case "будни":
            result = LEXICON["bells_weekdays"]
        case _:
            weekday = date.today().weekday()
            if weekday == 5:
                result = LEXICON["bells_saturday"]
            else:
                result = LEXICON["bells_weekdays"]
    return result
