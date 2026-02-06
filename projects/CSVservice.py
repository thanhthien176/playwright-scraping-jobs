import csv


class HelperFileCSV:
    @staticmethod
    def save_single_column_list(data_list, path_file):
        with open(path_file, "w", encoding="UTF-8", newline="") as f:
            writer = csv.writer(f)
            for row in data_list:
                writer.writerow([row])
    
    @staticmethod
    def save_dict_list(dict_list, path_file):
        if not dict_list:
            print("The list does not exist!")
            return
        
        with open(path_file, "w", encoding="UTF-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=dict_list[0].keys())
            writer.writeheader()
            writer.writerows(dict_list)
    
    @staticmethod
    def load_list_from_file(path_file):
        list_data = []
        with open(path_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                list_data.append(row)
        return list_data
    
    @staticmethod
    def load_dict_list_from_file(path_file):
        list_dict = []
        with open(path_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                list_dict.append(row)
                            
    