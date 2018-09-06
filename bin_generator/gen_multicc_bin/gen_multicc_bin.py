# -*-coding：utf-8 -*-
import re
import os
import time
origin_list  = []
bin_folder_list = []
file_list = []
tv_bin_find_cnt = 0  #initial
cc_num = 0

case_re = re.compile(r"Case\d+")
final_folder_name = ""
cfg_dict = {}
bin_re_str = ""
input_combine_case_num = 0
output_combined_case_num = 0
cfg_txt_line_num = 0


# 读取cfg文件中的参数，包括原始输入文件，输出文件，各个CC的向量偏移地址
def read_cfg_file():
    global cfg_dict
    with open("cfg_file.txt","r") as f:
        lines = f.readlines()
        for item in lines:
            item_k,item_v = item.strip("\n").split("=")
            cfg_dict[item_k.strip()] = item_v.strip()



def process_multicc_bin():
    global cfg_dict
    global bin_re_str
    global tv_bin_find_cnt
    global input_combine_case_num
    global output_combined_case_num
    global cfg_txt_line_num

    #使用正则表达式进行编译，用于后面搜索相应的case
    bin_re_str = cfg_dict["search_bin_name"]
    bin_re = re.compile(bin_re_str)
    try:
        if not os.path.exists(cfg_dict["output_multcc_bin_foldername"]):
            os.makedirs(cfg_dict["output_multcc_bin_foldername"])
    except Exception as e:
        print("output_multcc_bin_foldername in cfg_file.txt is wrong\n")


    multicc_case_file_name = cfg_dict["output_multcc_bin_foldername"] + "multicc_case.txt"
    if os.path.exists(multicc_case_file_name):
        os.remove(multicc_case_file_name)
    multicc_case_f = open(multicc_case_file_name, "w")

    with open("fpga_test_case_list-CA.txt","r") as f:
        origin_list = f.readlines()
        input_combine_case_num = 0
        output_combined_case_num = 0
        for item in origin_list:
            tv_bin_find_cnt = 0 #每一行处理时都要清0
            item = item.strip("\n").strip(" ") #排除掉某一行中有空格的问题
            cfg_txt_line_num = cfg_txt_line_num + 1
            if 0 != len(item):
                input_bin_folder_list = item.strip( ).split(" ")#读出来一行，确定几个CC的case需要合并
                path_length = len(input_bin_folder_list)
                cc_num = path_length - 2
               #generate the new folder name
                final_folder_name_list = []
                final_folder_prefix_list = []
                final_floder_prefix_set = []
                bin_folder_list = []

                #检查路径的个数是否合理

                if (cc_num < 2):
                    print("input path's format in fpga_test_case_list-CA.txt linenum:{} is wrong，pls refer to the userguide Ch 3.1!\n".format(cfg_txt_line_num))
                    continue
                try:
                    int(input_bin_folder_list[path_length - 1])
                except Exception as e:
                    print("the last string in fpga_test_case_list-CA.txt linenum:{} should be a number".format(cfg_txt_line_num))
                    continue

                input_combine_case_num = input_combine_case_num + 1
                for i in range(cc_num ):
                    bin_folder_list.append(input_bin_folder_list[i])


                
                final_folder_name = ""
                final_folder_name_prefix = ""
                final_file_path = ""
                '''
                #通过每个合并CASE中的Case关键字匹配相应的Case,如果找到了，保留Case****，作为后续文件夹的字段
                for item in bin_folder_list:
                    floder_name_item_list = item.split("\\")
                    for case_name_search in  floder_name_item_list:
                        case_match = re.match(case_re,case_name_search)
                        if (case_match is not None):
                            case_name = case_match.group()
                            flolder_prefix_index = floder_name_item_list.index(case_name)-1 #找到Case****前面的字段作为前缀
                
                            final_folder_name_list.append(case_name)
                            final_folder_prefix_list.append(floder_name_item_list[flolder_prefix_index])
                #每个case按照原来的输入顺序保留CASE名
                #final_folder_prefix_set =  list(set(final_folder_prefix_list))
                #final_folder_prefix_set.sort(key=final_folder_prefix_list.index)
                
                #生成文件夹的前缀和名字
                final_folder_name_tuple = zip(final_folder_prefix_list,final_folder_name_list)
                for i in final_folder_name_tuple:
                    for j in i:
                        final_folder_name = final_folder_name + j
                    final_folder_name = final_folder_name+"_"
                
                
                final_folder_name = final_folder_name[0:len(final_folder_name)-1]
                final_folder_name = cfg_dict["output_multcc_bin_foldername"] + final_folder_name
                '''
                #检查输入的目录是否正确
                try:
                    for dir_path in bin_folder_list:
                        if not os.path.exists(dir_path):
                            raise Exception(dir_path)
                except Exception as e:
                    print("input path {0} in fpga_test_case_list-CA.txt linenum:{1} is not exist!\n".format(e,cfg_txt_line_num))
                    continue

                final_folder_name = input_bin_folder_list[len(input_bin_folder_list) - 2]
                final_folder_name = final_folder_name + "ONL\\"
                # 生成输出文件夹
                try:
                    if not os.path.exists(final_folder_name):
                        os.makedirs(final_folder_name)
                except Exception as e:
                    print("{0} in fpga_test_case_list-CA.txt linenum:{1} is wrong\n".format(final_folder_name,cfg_txt_line_num))
                    continue

                # 在每个文件夹下面打开一个log文件，记录每次合并TV时的log
                f_log = open(final_folder_name + "/case_combine.log", "a")
                
                
                print("\n\ntime:{0},----START TO GENERATE MULTICC BIN ----".format(time.ctime()),file =f_log)
                print("output_folder_name = {0},detect_cc_num = {1}".format(final_folder_name,cc_num), file=f_log)
                
                
                #开始处理不同CASE下面的向量，进行合并
                try:
                    final_file_path = final_folder_name + "\\"+ cfg_dict["output_multicc_bin_name"]
                    final_f = open(final_file_path,"wb") #final file
                
                    for folder_name in bin_folder_list:
                        folder_name = folder_name.strip("\n").strip()
                        folder_name = folder_name + "ONL\\" #在输入目录下的ONL文件夹下寻找要合并的文件
                        print("process folder:{0}".format(folder_name),file = f_log)
                        if os.path.exists(folder_name):      #检查目录是否正确
                            file_list = (os.listdir(folder_name))     #find the folder's file list
                            for file_name in file_list:
                                m = re.match(bin_re,file_name)     #find the dp_fpga.case
                                if m is not None:
                                    case_path = folder_name + m.group()   #form the path
                                    print("find match file path = {0}".format(case_path),file = f_log)
                                    tv_bin_find_cnt= tv_bin_find_cnt +1
                                    with open(case_path,"rb") as f_bin:
                                        print("fill the bin to the output file at address:{0}\n".format(hex(final_f.tell())), file=f_log)
                                        final_f.write(f_bin.read())
                                        final_f.seek(int(cfg_dict["byte_offset_for_cc"]) * tv_bin_find_cnt,0)
                        else:
                            print("linenum:{0},input_path:{1} is wrong!".format(cfg_txt_line_num,folder_name))
                    if (cc_num == tv_bin_find_cnt):
                        output_combined_case_num = output_combined_case_num + 1
                        print("cc_num = {0},detect valid bin num = {1}".format(cc_num,tv_bin_find_cnt),file=f_log)
                        print(final_folder_name ,file = multicc_case_f)
                        print("--------------------------------PASS--------------------------------",file = f_log)
                    else:
                        print("****error****,cc_num = {0},detect valid bin num = {1}".format(cc_num, tv_bin_find_cnt),file=f_log)
                        print("--------------------------------FAIL--------------------------------", file=f_log)
                        print("linenum:{0},{1} can't find enough bin file to combine, pls check it!\n".format(cfg_txt_line_num,final_folder_name))
                except Exception as e:
                    print("******exception,pls check the input case folder path************", file=f_log)
                    print("******linenum:{},{} exception occurs,pls check the input case folder************\n".format(cfg_txt_line_num, final_folder_name))
                
                f_log.close()
    #写完关闭
    multicc_case_f.close()



if __name__ == "__main__":
    print("gen_multi_cc: version:2018-09-06,author:brain.liu")
    print("start to process,pls wait for a moment.....\n")
    read_cfg_file()
    process_multicc_bin()

    print("input_combine_case_num:{},output_combined_case_num:{}\n".format(input_combine_case_num,
                                                                         output_combined_case_num))
    if (input_combine_case_num == output_combined_case_num):
        print("---------------Combine CA Case PASS------------------\n")
    else:
        print("***************Combine CA Case FAIL******************\n")

    os.system("pause")