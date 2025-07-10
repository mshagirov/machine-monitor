import re

column_names_ = {
    "HOST"    : "hostname",
    "OS"      : "os",
    "ARCH"    : "arch",
    "NCPU"    : "cpu_count",
    "CPU%"    : "cpu_usage",
    "LOAD%"   : "cpu_load",
    "TOTMEM"  : "mem_tot",
    "MEM%"    : "mem_usage",
    "STORAGE" : "disk_usage",
    "NETSTAT" : "network_stats",
    "CONN"    : "connections",
    "TSTAMP"  : "timestamp",
}

col_LUT_ = {v:k for k, v in column_names_.items()}

def clean_string(s:str, )->str:
    out = []
    for item in map(
        lambda val: val.split(" : "), s.replace("%", "").split("; ")
    ):
        if len(item) < 2:
            for m in re.findall(r"( \([^()]*\))", item[0]):
                item[0] = item[0].replace(m, "")
            out.append(item[0])
            continue
        if ("_ERROR " in item[1]) or (" down" in item[1]):
            out.append(f"ERROR:{item[0]}")
            continue
        out.append("OK")
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
        row[col_LUT_[k]] = clean_string(v)
    for k, v in metrics.items():
        if col_LUT_.get(k) == None:
            continue
        row[col_LUT_[k]] = clean_string(v)
    return row #[row[k] for k in column_names_]
