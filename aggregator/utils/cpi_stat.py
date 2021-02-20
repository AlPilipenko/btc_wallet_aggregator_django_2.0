import json

def cpi_stat_arg():
    with open(r"aggregator/cpi.json") as f:
        #print(v)
        my_dict = json.load(f)

        cpi_d = my_dict.get("d")
        cpi_w = my_dict.get("w")
        cpi_m = my_dict.get("m")

        with open(r"aggregator/daily_stat_data.json") as d:
            my_dict2 = json.load(d)
            daily = my_dict2.get("total")

            #print(daily)
            #print(cpi_d)
            #print(cpi_w)
            #print(cpi_m)

            with open('aggregator/cpi.json', 'w') as data_file:

                cpi_d.append(daily[0])
                cpi_w.append(daily[1])
                cpi_m.append(daily[2])
                #my_dict["d"] = cpi_d
                #my_dict["w"] = cpi_w
                #my_dict["m"] = cpi_m
                #players["So"] = 2780
                my_dict = json.dump(my_dict, data_file)

    with open(r"aggregator/cpi.json") as f:
        #print(v)
        my_dict = json.load(f)
        #print(my_dict)
        #print(my_dict[0],my_dict[1],my_dict[2])

        d = my_dict.get("d")
        w = my_dict.get("w")
        m = my_dict.get("m")

        cpi_d = 100
        cpi_w = 100
        cpi_m = 100
        cpi = 100
        #k = 1
        for i, n in enumerate(d):


            if i == 0:
                print("D\tW\t M")
                print(round(cpi_d,1), round(cpi_w,1), round(cpi_m,1))
                pass
            else:
                cpi_d = ((d[i]/d[i-1])*cpi_d)
                cpi_w = ((w[i]/w[i-1])*cpi_w )
                cpi_m = ((m[i]/m[i-1])*cpi_m)
                print(round(cpi_d,1), round(cpi_w,1), round(cpi_m,1))
        #print(daily)
        #print(d)
        #print(w)
        #print(m)
