admin_ids: set[str] = {"2087648271"}

group_url = "https://schedule.mstimetables.ru/api/publications/group/lessons"
teacher_url = "https://schedule.mstimetables.ru/api/publications/teacher/lessons"
req_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Content-Type": "application/json",
    "Accept": "*/*",
}
