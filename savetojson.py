import sys, json

def writeLines(lines, entry, key, start):
    i = start
    running = 1
    while running:
        for term in parsingTerms:
            try:
                x = term.replace(" ","")
                l = lines[i].lower()
                if (term in l or x in l):
                    running = 0
                    break
            except IndexError:
                return start - 1
        else:
            entry[key] += "" + processVal(lines[i])
            i+=1
    return i-1

def processVal(val):
    val = "".join(char for char in val if 0 < ord(char) < 128)
    val = val.strip()
    if val in ["-", "nil", "none"]:
        val = ""
    val = val.title()
    return val

def resetEntry():
    return {"course code": "", "course title": "", "prerequisites": "", "course type": "", "course learning objectives":"", "course content":"", "course outcomes":"", "credits":"", "reference books": ""}

parsingTerms = ["course code", "course title", "prerequisites", "credits", "course type", "course content", "course learning objectives",  "course outcomes", "reference books"]
entry = resetEntry()
fname = sys.argv[1]
outname = fname + ".json"
output = open(outname,"w")

with open(fname) as f:
    lines = f.readlines()
    n = len(lines) 
    lineno = 0
    while lineno < n:
        line = lines[lineno]
        flag = 0
        lline = line.lower()
        for term in parsingTerms:
            flag = term in lline
            
            if flag:
                lline = lline.partition(":")[-1]
                if not lline:
                    lline = lline.replace(term,"")
                if (parsingTerms.index(term) >= 5):
                    lineno = writeLines(lines, entry, term, lineno + 1)
                    continue
                else:
                    entry[term] = processVal(lline)
            else:
                orig = term
                term = term.replace(" ","")
                flag = term in lline
                if flag:
                    lline = lline.partition(":")[-1]
                    if not lline:
                        lline = lline.replace(term, "")
                    if (parsingTerms.index(orig) >= 5):
                        lineno = writeLines(lines, entry, orig, lineno + 1)
                        continue
                    else:
                        entry[orig] = processVal(lline)
           
        if flag:
            try:
                entry["credits"] = (entry["credits"].replace("0",""))[0]
            except IndexError:
                pass
            output.write(json.dumps(entry, indent = 2))
            output.write("\n")
            entry = resetEntry()
            flag = 0

        lineno+=1

output.close()
