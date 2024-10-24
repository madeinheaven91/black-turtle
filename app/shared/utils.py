def lessons_declension(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return "урок"
    elif 2 <= (count % 10) <= 4 and not 12 <= count <= 14:
        return "урока"
    else:
        return "уроков"

