import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.logic import extract_lessons_tokens
# пары, имя, день, неделя
queries = [
    "пары 921",
    "пары 921 пт",
    "пары 921 пт след",
    "пары 921 след",
    "пары",
    "пары пт",
    "пары пт след",
    "пары след",
    "пары димитриев александр",
    "пары димитриев александр пт",
    "пары димитриев александр пт след",
    "пары димитриев александр след",
    
] 

def up_to_ten(str):
    array = str.split(" ")
    while len(array) < 10:
        array.append("")
    return array

queries = list(map(up_to_ten, queries))

assert extract_lessons_tokens(queries[0]) == ["пары", "921", "", ""]
assert extract_lessons_tokens(queries[1]) == ["пары", "921", "пт", ""]
assert extract_lessons_tokens(queries[2]) == ["пары", "921", "пт", "след"]
# assert extract_lessons_tokens(queries[3]) == ["пары", "921", "", "след"]
assert extract_lessons_tokens(queries[4]) == ["пары", "", "", ""]
assert extract_lessons_tokens(queries[5]) == ["пары", "", "пт", ""]
assert extract_lessons_tokens(queries[6]) == ["пары", "", "пт", "след"]
# assert extract_lessons_tokens(queries[7]) == ["пары", "", "", "след"]
assert extract_lessons_tokens(queries[8]) == ["пары", "димитриев александр", "", ""]
assert extract_lessons_tokens(queries[9]) == ["пары", "димитриев александр", "пт", ""]
assert extract_lessons_tokens(queries[10]) == ["пары", "димитриев александр", "пт", "след"]
# assert extract_lessons_tokens(queries[11]) == ["пары", "димитриев александр", "", "след"]
