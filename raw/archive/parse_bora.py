import csv

cogid = 0
id = 0
full_data = [[
    "ID",
    "DOCULECT",
    "FORM",
    "CONCEPT",
    "COGID",
    "MORPHEMES",
    "NOTE",
    "PROTOSET",
    "PROTOFORM",
    "APBM",
    "BASICVOCABULARY"
]]

bora_phones = []
muinane_phones = []

text = open('proto_bora.txt', 'r', encoding="utf8").read()
text = text.split("\n")
for line in text:
    proto_set = line.split("\t")[0].replace(".", "")
    entry = line.split("\t")[1]
    entry = entry.split("|")
    proto_entry = entry[0].replace("PBoM ", "")
    proto_entry = proto_entry.replace(", ", ",")
    proto_form = proto_entry.split(" ")[0]
    proto_concept = " ".join(proto_entry.split(" ")[1:])

    bora = entry[1].split(";")[0].replace(" Bo ", "")
    muin = entry[1].split(";")[1].replace(" Mu ", "")

    apbm = ""
    if "APBM" in muin:
        muin = muin.split("[")
        apbm = muin[1].replace("APBM ", "").replace("]", "")
        muin = muin[0]

    cogid += 1
    id += 1
    bv = []

    if "‡" in proto_concept:
        bv.append("Leipzig-Jakarta")  # add conceptlist well!
        proto_concept = proto_concept.replace("‡", "")
    if "†" in proto_concept:
        bv.append("Swadesh")
        proto_concept = proto_concept.replace("†", "")
    bv = ", ".join(bv)

    bora_s = bora.split("(")
    bora_comment = bora_s[1].replace(")", "") if len(bora_s) > 1 else ""

    bora_f = bora_s[0].split("‘")
    bora_form = bora_f[0]
    bora_gloss = bora_f[1].replace("’", "") if len(bora_f) > 1 else ""

    full_proto = [
        id,
        "PBoM",
        proto_form.replace("*", ""),
        proto_concept,
        cogid,
        "",  # gloss
        "",  # comment
        proto_set,
        proto_form,
        apbm,
        bv
    ]

    id += 1
    full_bora = [
        id,
        "Bora",
        bora_form,
        proto_concept,
        cogid,
        bora_gloss,
        bora_comment,
        proto_set,
        proto_form,
        "",
        bv
    ]

    muin_s = muin.split("(")
    muin_comment = muin_s[1].replace(")", "") if "(" in muin else ""

    muin_f = muin_s[0].split("‘")
    muin_form = muin_f[0]
    muin_gloss = muin_f[1].replace("’", "") if len(muin_f) > 1 else ""

    id += 1
    full_muin = [
        id,
        "Muinane",
        muin_form,
        proto_concept,
        cogid,
        muin_gloss,
        muin_comment,
        proto_set,
        proto_form,
        "",
        bv
    ]

    full_data.append(full_proto)
    full_data.append(full_bora)
    full_data.append(full_muin)

    for char in bora_form:
        if char not in bora_phones:
            bora_phones.append(char)
    for char in muin_form:
        if char not in muinane_phones:
            muinane_phones.append(char)


with open('../parsed_bora.tsv', 'w', encoding="utf8") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(full_data)

with open('../../etc/bora.tsv', 'w', encoding="utf8") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(bora_phones)

with open('../../etc/muinane.tsv', 'w', encoding="utf8") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(muinane_phones)
