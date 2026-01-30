import json
import sys
from lxml import etree
import Evtx.Evtx as evtx

def xml_to_dict(elem):
    # Convierte XML a dict manejando namespaces y repeticiones
    tag = etree.QName(elem).localname
    node = {}
    # atributos
    if elem.attrib:
        node["@"] = {etree.QName(k).localname: v for k, v in elem.attrib.items()}
    # hijos
    children = list(elem)
    if children:
        kids = {}
        for c in children:
            k, v = xml_to_dict(c)
            if k in kids:
                if not isinstance(kids[k], list):
                    kids[k] = [kids[k]]
                kids[k].append(v)
            else:
                kids[k] = v
        if elem.text and elem.text.strip():
            kids["#text"] = elem.text.strip()
        node.update(kids)
    else:
        text = (elem.text or "").strip()
        node = text if text else node
    return tag, node

def main(evtx_path, out_json):
    out = []
    with evtx.Evtx(evtx_path) as log:
        for r in log.records():
            x = r.xml().encode("utf-8", "ignore")
            root = etree.fromstring(x)
            k, v = xml_to_dict(root)
            out.append({k: v})

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[+] OK: {len(out)} events -> {out_json}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evtx_to_json.py <file.evtx> <out.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
