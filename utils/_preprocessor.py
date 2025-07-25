##############################################################
#Project Name : BFSI
#File Name : _preprocessor.py
#Team Name : ThunderBolt
#Description : This will preprocess the data 
##############################################################

class DataPreprocessor:
    def split_waiting_indemnity(data):
        result = []
        for item in data:
            if isinstance(item, str) and '/' in item:
                waiting, indemnity = item.split('/')
                result.append([waiting, indemnity])
            else:
                result.append([None, None])
        return result