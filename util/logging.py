import json

log_filename = "logging.json"
dataset_filename = "dataset.json"
result_filename = "result.json"
class LogIO:
    def __init__(self):
        self.log_filename = log_filename
        self.dataset_filename = dataset_filename
        self.result_filename = result_filename

    def get_list_log(self, load_dataset=False, load_result=False):
        list_log = []

        #Open log file
        f = open(self.log_filename)
        #Read list log
        lines = f.readlines()
        for line in lines:
            log_json = json.loads(line)
            log_object = Log(log_json["key"],log_json["name"], log_json["algorithm"],
                             log_json["number_of_point"],log_json["created_date"], log_json["parameter"])
            list_log.append(log_object)
        #Close log file
        f.close()

        #Load dataset and result
        for i in range(len(list_log)):
            if load_dataset:
                list_log[i].dataset = self.get_dataset_by_log_key(list_log[i].key)
            if load_result:
                list_log[i].result = self.get_result_by_log_key(list_log[i].key)
        return list_log

    def get_dataset_by_log_key(self, log_key):
        dataset = []
        # Open dataset file
        f = open(self.dataset_filename)
        # Read list dataset
        lines = f.readlines()
        for line in lines:
            log_json = json.loads(line)
            if log_json["log_key"] == log_key:
                dataset = log_json["dataset"]
        # Close dataset file
        f.close()
        return dataset

    def get_result_by_log_key(self, log_key):
        result = []
        # Open result file
        f = open(self.result_filename)
        # Read list result
        lines = f.readlines()
        for line in lines:
            log_json = json.loads(line)
            if log_json["log_key"] == log_key:
                result = log_json["result"]
        # Close result file
        f.close()
        return result

    def get_new_log_key(self):
        key = 0
        # Open log file
        f = open(self.log_filename)
        # Read list log
        lines = f.readlines()
        for line in lines:
            log_json = json.loads(line)
            if log_json["key"] > key:
                key = log_json["key"]
        # Close log file
        f.close()
        return (key + 1)

    def add_new_log(self, log):
        log_json = log.to_dict()
        dataset_json = {}
        dataset_json["log_key"] = log.key
        dataset_json["dataset"] = log.dataset
        result_json = {}
        result_json["log_key"] = log.key
        result_json["result"] = log.result

        # Write log file
        f = open(self.log_filename, "a+")
        json.dump(log_json, f)
        f.write("\n")
        f.close()

        #Write dataset file
        f = open(self.dataset_filename, "a+")
        json.dump(dataset_json, f)
        f.write("\n")
        f.close()

        #Write result file
        f = open(self.result_filename, "a+")
        json.dump(result_json, f)
        f.write("\n")
        f.close()

    def rename_log(self, log_key, log_new_name):
        #Load logs
        f = open(self.log_filename)
        lines = f.readlines()
        f.close()

        #Rename
        for i in range(len(lines)):
            log_json = json.loads(lines[i])
            if log_json["key"] == log_key:
                log_json["name"] = log_new_name
                lines[i] = json.dumps(log_json)

        #Save to file
        f = open(self.log_filename, "w")
        for line in lines:
            f.write(line)
        f.close()

    def remove_log(self, log_key):
        #Remove in log file
        f = open(self.log_filename)
        lines = f.readlines()
        f.close()

        f = open(self.log_filename, "w")
        for line in lines:
            log_json = json.loads(line)
            if log_json["key"] != log_key:
                json.dump(log_json, f)
        f.close()

        # Remove in dataset file
        f = open(self.dataset_filename)
        lines = f.readlines()
        f.close()

        f = open(self.dataset_filename, "w")
        for line in lines:
            log_json = json.loads(line)
            if log_json["log_key"] != log_key:
                json.dump(log_json, f)
        f.close()

        # Remove in result file
        f = open(self.result_filename)
        lines = f.readlines()
        f.close()

        f = open(self.result_filename, "w")
        for line in lines:
            log_json = json.loads(line)
            if log_json["log_key"] != log_key:
                json.dump(log_json, f)
        f.close()

class Log:
    def __init__(self, key, name, algorithm, number_of_point, created_date, parameter, dataset=None, result=None):
        self.key=key
        self.name=name
        self.algorithm=algorithm
        self.number_of_point=number_of_point
        self.created_date=created_date
        self.parameter=parameter
        self.dataset=dataset
        self.result=result

    def to_dict(self):
        log_dict = {}
        log_dict["key"] = self.key
        log_dict["name"] = self.name
        log_dict["algorithm"] = self.algorithm
        log_dict["number_of_point"] = self.number_of_point
        log_dict["created_date"] = self.created_date
        log_dict["parameter"] = self.parameter
        return log_dict


