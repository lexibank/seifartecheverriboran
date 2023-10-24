import csv
from collections import defaultdict
import re
from lingpy import Wordlist
from pysem.glosses import to_concepticon


wl = Wordlist("raw/parsed_bora.tsv")
proto_concepts = [[
    "CONCEPT",
    "CONCEPTICON_ID",
    "CONCEPTICON_GLOSS",
    "PROTO_ID"
    ]]

concept_exists = []
concept_count = 0
concept_ids = defaultdict()

for i in wl:
    concept = re.sub("  ", " ", wl[i, "concept"]).lower()

    ID = wl[i, "protoset"]
    # Proto-Concepts
    if wl[i, "doculect"] == "PBoM":
        mapped = to_concepticon([{"gloss": concept}], language="en")
        if mapped[concept]:
            cid, cgl = mapped[concept][0][:2]
        else:
            cid, cgl = "", ""

        proto_concepts.append([
            concept, cid, cgl, ID
        ])

with open("etc/concepts.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(proto_concepts)
