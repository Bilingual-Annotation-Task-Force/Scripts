from praatio import tgio
import pandas as pd
import numpy as np

def parse_textgrid_to_csv(src_path = "DanishVoices_BSK_RevisedTextGrid_080219", dest_path = "Danish.csv"):
    assert type(src_path) == type("string")
    assert type(dest_path) == type("string")
    assert dest_path[-4: ] == ".csv" # make sure the output is to a csv file
    tg = tgio.openTextgrid(src_path)


    max_len = max([len(tg.tierDict[str(name)].entryList) for name in tg.tierNameList])

    temp_dict = {}
    cur = pd.DataFrame()
    for name in tg.tierNameList:
        tier = tg.tierDict[str(name)]
        temp_arr_0 = []
        temp_arr_1 = []
        temp_arr_2 = []

        for start, stop, label in tier.entryList:
            temp_arr_0.append(start)
            temp_arr_1.append(stop)
            temp_arr_2.append(label)
        while(len(temp_arr_0) <max_len):
            temp_arr_0.append(None)
            temp_arr_1.append(None)
            temp_arr_2.append(None)
        temp_dict[name + "Start"] = tuple(temp_arr_0)
        temp_dict[name + "Stop"] = tuple(temp_arr_1)
        temp_dict[name + "Label"] = tuple(temp_arr_2)
    cur = pd.DataFrame(data = temp_dict)
    cur.to_csv(dest_path)

if __name__ == "__main__":
    parse_textgrid_to_csv()


