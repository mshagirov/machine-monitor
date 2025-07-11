import re
from datetime import datetime

# can change the column name (key) but NOT API name (value)
column_names_ = {
    "HOST"       : "hostname",
    "OS"         : "os",
    "ARCH"       : "arch",
    "NCPU(LOG)"  : "cpu_count",
    "CPU%"       : "cpu_usage",
    "LOAD%"      : "cpu_load",
    "TOTMEM"     : "mem_tot",
    "MEM%"       : "mem_usage",
    "STORAGE"    : "disk_usage",
    "NETSTATS"   : "network_stats",
    "CONNECTIONS": "connections",
    "TIMESTAMP"  : "timestamp",
}

col_LUT_ = {v:k for k, v in column_names_.items()}


def strip_alpha(s: str, rmspace=True) -> str:
    for alpha in re.findall(r"[a-zA-Z]+", s):
        s = s.replace(alpha, "")
    if rmspace:
        s = s.replace(" ", "")
    return s


def clean_string(s:str, alphaonly=False)->str:
    out = []
    for item in map(
        lambda val: val.split(" : "), s.replace("%", "").split("; ")
    ):
        if len(item) < 2:
            for m in re.findall(r"( \([^()]*\))", item[0]):
                if alphaonly:
                    item[0] = item[0].replace(m, strip_alpha(m))
                else:
                    item[0] = item[0].replace(m, "")
            out.append(item[0])
            continue
        if ("_ERROR " in item[1]) or (" down" in item[1]):
            out.append(f"ERROR:{item[0][:5]}")
            continue
        out.append(f"{item[0][:5]}:OK")
    num_errors = sum(map(lambda item: "ERROR" in item, out))
    if num_errors < 1:
        return "/".join(out)
    else :
        return "W: " + ("/".join(
            filter(lambda v: "ERROR" in v, out)
        )).replace("ERROR:", "")

def make_row(info    : dict = {},
             metrics : dict = {},
             template : bool= True)->dict:
    if template:
        row = { c: "" for c in column_names_}
    else:
        row = {}
    for k, v in info.items():
        if col_LUT_.get(k) == None:
            continue
        if k == 'cpu_count':
            row[col_LUT_[k]] = clean_string(v, alphaonly=True)
            continue
        row[col_LUT_[k]] = clean_string(v)
    for k, v in metrics.items():
        if col_LUT_.get(k) == None:
            continue
        row[col_LUT_[k]] = clean_string(v)
    # reformat timestamp
    if (None != row.get(col_LUT_["timestamp"])) and row[col_LUT_["timestamp"]].strip():
        row[col_LUT_["timestamp"]] = datetime.strptime( row[col_LUT_["timestamp"]],
                                                   "%d-%m-%Y %H:%M:%S.%f"
                                                   ).strftime("%d%b %H:%M:%S")
    return row

