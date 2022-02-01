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
            entry[key] += "\n" + processVal(lines[i])
            i+=1
    return i-1

def processVal(val):

    val = "".join(char for char in val if 0 < ord(char) < 128)
    val = val.strip()
    if val in ["-", "nil", "none"]:
        val = ""
    val = val.title()
    return val

def isextraLine(line):
    
    out = line != "\n"
    out = out or line != "---"
    out = out or "B. Tech" in line or "Semester" in line
    out = out or "(2017-18 onwards)" in line
    return out

def write2dict(lines, entry, lline, term, lineno):
    
    x = lline.partition(":")[-1]
    if not x:
        lline = lline.replace(term,"")
        lline = lline.replace(term.replace(" ",""),"")
    else:
        lline = x
    #put all multiline entries AFTER course content so this works
    if (parsingTerms.index(term) >= 5):
        lineno = writeLines(lines, entry, term, lineno + 1)
        return lineno
    else:
        entry[term] = processVal(lline)
        return 0

fname = sys.argv[1]
parsingTerms = ["course code", "course title", "prerequisites", "credits", "course type", "course content", "course learning objectives",  "course outcomes", "books"]
entry = {"course code": "", "course title": "", "prerequisites": "", "course type": "", "course learning objectives":"", "course content":"", "course outcomes":"", "credits":"", "books": ""}
outname = fname + ".json"
output = open(outname,"w")

with open(fname) as f:
    lines = list(f.readlines())
    nlines = []
    for l in lines:
        if isextraLine(l):
            l = l.lower()
            for term in parsingTerms:
                if term in l or term.replace(" ","") in l:
                    l = (l.replace(term, "\n" + term + "\n") if parsingTerms.index(term) >= 5 else l)
            nlines.append(l)
    lines = nlines
    lineno = 0
    iters = 1 
    while lineno < len(lines):
        line = lines[lineno]
        for term in parsingTerms:
            if term in line or term.replace(" ","") in line:
                x = write2dict(lines, entry, line, term, lineno)
                if x:
                    lineno = x

        if not iters % 9:
            try:
                entry["credits"] = (entry["credits"].replace("0",""))[0]
            except IndexError:
                entry["credits"] = "0"
            output.write(json.dumps(entry, indent = 2))
            output.write("\n")
            entry = entry.fromkeys(entry,"")
            iters = 0

        lineno += 1
        iters += 1

output.close()
