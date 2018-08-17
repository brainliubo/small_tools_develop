import re
import os
origin_list  = []
bin_folder_list = []
file_list = []

case_re = re.compile(r"Case\d+")
final_folder_name = ""
cfg_dict = {}
bin_re_str = ""

def read_cfg_file():
    global cfg_dict
    with open("cfg_file.txt","r") as f:
        lines = f.readlines()
        for item in lines:
            item_k,item_v = item.strip("\n").split(":")
            cfg_dict[item_k] = item_v



def process_multicc_bin():
    global cfg_dict
    global bin_re_str
    bin_re_str = cfg_dict["search_file_name"]
    bin_re = re.compile(bin_re_str);

    with open("multi_cc_bin_list.txt","r") as f:
        origin_list = f.readlines()
        for item in origin_list:
            find_idx = 0 #initial
            bin_folder_list = (item.strip("\n").split(";"))
            #generate the new folder name
            final_folder_name_list = []
            final_folder_name = ""
            final_file_path = ""
            for item in bin_folder_list:
               for case_name_search in  item.split("\\") :
                   case_match = re.match(case_re,case_name_search)
                   if (case_match is not None):
                       case_name = case_match.group()
                       final_folder_name_list.append(case_name)
            for ut in (final_folder_name_list):
                final_folder_name = final_folder_name + ut + "_"

            final_folder_name = final_folder_name[0:len(final_folder_name)-1]
            print(final_folder_name)
            os.mkdir(final_folder_name)
            final_file_path = final_folder_name + "\\"+ cfg_dict["generate_file_name"]
            final_f = open(final_file_path,"wb") #final file

            for folder_name in bin_folder_list:
                print(folder_name)
                folder_name = folder_name.strip()
                print(folder_name)
                if (len(folder_name) > 0):      #each cc's folder
                    file_list = (os.listdir(folder_name))     #find the folder's file list
                    for file_name in file_list:
                        m = re.match(bin_re,file_name)     #find the dp_fpga.case
                        if m is not None:
                            case_path = folder_name + m.group()   #form the path
                            print("find match file path = {0}".format(case_path))
                            find_idx= find_idx +1
                            with open(case_path,"rb") as f_bin:
                                print(final_f.tell())
                                final_f.write(f_bin.read())
                                final_f.seek(int(cfg_dict["tv_bin_OffsetofCc"]) * find_idx,0)



if __name__ == "__main__":
    read_cfg_file()
    process_multicc_bin()