import sys,json

for fname in sys.argv[1:]:

    with open(fname) as f:
        data = []
        rawdata = f.read().split("}")
        for i in range(len(rawdata)):
            if rawdata[i]:
                rawdata[i] += "}"
        rawdata = rawdata[:-1]
        for i in rawdata:
            x = json.loads(i)
            data.append(x)
        
        keys = data[0].keys()
        #check for missing records
        print(fname, file = sys.stderr)
        warnings = []
        for i in data:
            for k in keys:
                if not i[k]:
                    warnings.append(data.index(i))
                    print(data.index(i), ":", k, i[k], file = sys.stderr)
    
        print(fname, " warning:", len(warnings), " / ", len(keys) * len(data), "records seem to have data missing")
