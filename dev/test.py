data = """
1,2,3
4,5,6\u001B
7,8,9
"""

def csv_to_asv(text):
    rows = []
    for line in text.splitlines():
        row = "\u001f".join(line.split(','))
        rows.append(row)
    return "\u001d" + "\u001e".join(rows)


print(csv_to_asv(data))