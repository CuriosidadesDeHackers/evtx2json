import json
import glob
import os
import sys
from lxml import etree
import Evtx.Evtx as evtx

def xml_to_dict(elem):
    tag = etree.QName(elem).localname
    node = {}
    if elem.attrib:
        node["@"] = {etree.QName(k).localname: v for k, v in elem.attrib.items()}

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
        text = (elem.text or "").strip()
        if text:
            kids["#text"] = text
        node.update(kids)
    else:
        text = (elem.text or "").strip()
        node = text if text else node

    return tag, node

def parse_one_evtx(path):
    events = []
    with evtx.Evtx(path) as log:
        for r in log.records():
            x = r.xml().encode("utf-8", "ignore")
            root = etree.fromstring(x)
            k, v = xml_to_dict(root)

            # Por si por alguna razón aparece _evtx_file dentro del XML/dict
            if isinstance(v, dict) and "_evtx_file" in v:
                del v["_evtx_file"]

            # NO añadimos "_evtx_file"
            events.append({k: v})

    return events

def main(folder, out_json):
    folder = os.path.abspath(folder)
    pattern = os.path.join(folder, "*.evtx")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"[!] No .evtx files found in: {folder}")
        sys.exit(2)

    out = {}
    event_counter = 1
    total_files = len(files)

    for i, f in enumerate(files, 1):
        try:
            evs = parse_one_evtx(f)
            for ev in evs:
                out[f"Event_{event_counter:06d}"] = ev
                event_counter += 1

            print(f"[+] {i}/{total_files} OK: {os.path.basename(f)} ({len(evs)} events)")
        except Exception as e:
            print(f"[!] {i}/{total_files} FAIL: {os.path.basename(f)} -> {e}")

    with open(out_json, "w", encoding="utf-8") as out_f:
        json.dump(out, out_f, ensure_ascii=False, indent=2)

    print(f"\n[+] DONE: {len(out)} total events -> {out_json}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evtx_folder_to_json.py <folder_with_evtx> <out.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
