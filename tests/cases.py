token_test_cases = [
    (["пары", "921", "", "", "", "", "", "", "", ""], ["пары", "921", "", ""]),
    (["пары", "921", "пт", "", "", "", "", "", "", ""], ["пары", "921", "пт", ""]),
    (["пары", "921", "пт", "след", "", "", "", "", "", ""], ["пары", "921", "пт", "след"]),
    (["пары", "921", "след", "", "", "", "", "", "", ""], ["пары", "921", "", "след"]),
    (["пары", "", "", "", "", "", "", "", "", ""], ["пары", "", "", ""]),
    (["пары", "пт", "", "", "", "", "", "", "", ""], ["пары", "", "пт", ""]),
    (["пары", "пт", "след", "", "", "", "", "", "", ""], ["пары", "", "пт", "след"]),
    (["пары", "след", "", "", "", "", "", "", "", ""], ["пары", "", "", "след"]),
    (["пары", "димитриев", "", "", "", "", "", "", "", ""], ["пары", "димитриев", "", ""]),
    (["пары", "димитриев", "пт", "", "", "", "", "", "", ""], ["пары", "димитриев", "пт", ""]),
    (["пары", "димитриев", "пт", "след", "", "", "", "", "", ""], ["пары", "димитриев", "пт", "след"]),
    (["пары", "димитриев", "след", "", "", "", "", "", "", ""], ["пары", "димитриев", "", "след"]),
    (["пары", "димитриев", "александр", "", "", "", "", "", "", ""], ["пары", "димитриев александр", "", ""]),
    (["пары", "димитриев", "александр", "пт", "", "", "", "", "", ""], ["пары", "димитриев александр", "пт", ""]),
    (["пары", "димитриев", "александр", "пт", "след", "", "", "", "", ""], ["пары", "димитриев александр", "пт", "след"]),
    (["пары", "димитриев", "александр", "след", "", "", "", "", "", ""], ["пары", "димитриев александр", "", "след"]),
    (["пары", "димитриев", "александр", "олегович", "", "", "", "", "", ""], ["пары", "димитриев александр олегович", "", ""]),
    (["пары", "димитриев", "александр", "олегович", "пт", "", "", "", "", ""], ["пары", "димитриев александр олегович", "пт", ""]),
    (["пары", "димитриев", "александр", "олегович", "пт", "след", "", "", "", ""], ["пары", "димитриев александр олегович", "пт", "след"]),
    (["пары", "димитриев", "александр", "олегович", "след", "", "", "", "", ""], ["пары", "димитриев александр олегович", "", "след"]),
]
