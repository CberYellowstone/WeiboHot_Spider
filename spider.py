import re
import requests


def get_hot_list() -> tuple[tuple[str, str, str, str]]:
    url = "https://s.weibo.com/top/summary?cate=realtimehot"

    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
        "Cookie": "UOR=,,login.sina.com.cn; ALF=1666445729; SCF=AscEHVE2sTV05zTwYj5M7tduM7Zz3ktqPi21c2dTBB0sGFGcFIldixokcQ1yN8xFwVW-ywKnUt3rugqpWgzVXsE.; SINAGLOBAL=7267933806159.166.1634959444829; SUB=_2AkMW3d0wf8NxqwJRmPERzW_nbIx0yQ7EieKggSzrJRMxHRl-yT9jqhdftRB6PV3z3z21fp5a3CkZMXy5gZcyj15_nia0; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W56DO1wnAXX89yZnIENST5-; _s_tentry=-; Apache=6131946571247.373.1639292770571; ULV=1639292770592:2:1:1:6131946571247.373.1639292770571:1634959444907",
    }
    rep = requests.get(url, headers=_headers, timeout=30)
    rep.raise_for_status()
    rep.encoding = rep.apparent_encoding

    html = rep.text

    pattern = re.compile(
        '<td class="td-01 ranktop ranktop.*?">(.*?)</td>.*?<td class="td-02">.*?<a href="(.*?)" target="_blank">(.*?)</a>.*?<span>(.*?)</span>', re.S
    )
    suffix = "https://s.weibo.com"

    return tuple((rank, suffix + link, keyword, num) for rank, link, keyword, num in re.findall(pattern, html))  # type: ignore


from database import insert_data, export_to_xlsx, init_db

init_db()
insert_data(get_hot_list())
export_to_xlsx()