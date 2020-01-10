import pandas as pd
import json
import glob
import os

def pos_tags(df_data, sentence):
    pos_tags = []
    with open('sick2pd.json') as data_file:
        data = json.load(data_file)
        counter = 0

        for line in df_data["pair_ID"]:
            file_id = data[str(line)][sentence]
            if not os.path.isfile('pmb_SICK/data/silver/'+file_id+"/en.pos.noncorr.cols") and not os.path.isfile('pmb_SICK/data/gold/'+file_id+"/en.pos.noncorr.cols") and not os.path.isfile('pmb_SICK/data/bronze/'+file_id+"/en.pos.noncorr.cols") :
                pos_tags.append(" ")
            else:
                for path in glob.glob("pmb_SICK/data/*/" + file_id):
                    filename = (path + "/en.pos.noncorr.cols").replace("\\", "/")
                    pos = ""
                    for line in open(filename, "r"):
                        line = line.split("\t")
                        pos = pos + line[0] + " "
                    pos_tags.append(pos)
    return pos_tags


def create_csv(file_name, df_data):
    """creates a csv file for the data + the features """
    # df_data['sent'] = sentiment_score(df_data)
    df_data['SenA_pos'] = pos_tags(df_data,0)
    df_data['SenB_pos'] = pos_tags(df_data,1)
    df_data.to_csv(file_name, sep='\t', encoding='utf-8')

    # Resets the used dataframe to the one with added features and preprocessing
    return pd.read_csv(file_name, sep='\t')


def main():
    data = pd.read_csv('SICK/SICK_train.txt', sep="\t")
    df_data = create_csv('test.csv', data)


if __name__ == "__main__":
    main()
