import pandas as pd
from scipy import stats
import utils
import numpy;

def convertToUnixtime(df, datetime):
    datetime = df[datetime]
    unixtime = utils.datetime_timestamp(datetime)
    return unixtime

def makeSenarioData(df,index):
    data_s = df[df['scenarioId'] == index]
    #print（data_s）
    #data_s.rename(columns= lambda x:(x=='dateTime'?x), inplace=True)
    filename = "data/request-unix-"+str(index) +".csv"
    data_s.to_csv(filename, index=False)
    return data_s

def addPrefix(str, pre):
    if str =='dateTime':
        return str
    else:
        return pre+str

    #(result)

#data = pd.read_csv("data/request-new-unix.csv")
#print(data['dateTime'])
#data['dateTime'] = data['dateTime'].apply(utils.removeMillis)
#data.to_csv("data/request-new-unix-modified.csv", index=False)

#data2 = data['dateTime'].apply(utils.datetime_timestamp)

# data = pd.read_csv("data/request-new-unix-modified.csv")
# monitoring_data = pd.read_csv("data/result-5-cleaned.csv")
#
# data_s1 = makeSenarioData(data, 1)
# data_s2 = makeSenarioData(data, 2)
# data_s3 = makeSenarioData(data, 3)
# data_s4 = makeSenarioData(data, 4)
#
# data_s_mixed = pd.merge(data_s1, data_s2, on = 'dateTime', suffixes = ('_s1','_s2') , how = 'outer')
# data_s_mixed = pd.merge(data_s_mixed,data_s3, on = 'dateTime', suffixes = ('','_s3') , how = 'outer')
# data_s_mixed = pd.merge(data_s_mixed,data_s4, on = 'dateTime', suffixes = ('','_s4') , how = 'outer')
# #print(data_s_mixed)
#
# data_mixed = pd.merge(data_s_mixed, monitoring_data, on = 'dateTime', how = 'outer')
# print("merege finished")
# data_mixed.to_csv("data/test_mixed.csv", index=False)



# for index in services.columns.values:
#     series = services[index];
#     print(series)


#services.to_csv("data/sock-results-all_6-10-services.csv", index=False)
