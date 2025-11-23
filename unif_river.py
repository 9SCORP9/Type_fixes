import pandas as pd
import json
import re
#from spellchecker import SpellChecker

# Чтение файла
number = 17
file = "types"
fil0 = f"{file}_{number-1}"
#fil0 = f"full_file_cuted_4_without_spaces_Проект судна_{number}"

file_path = f"{fil0}.xlsx"


#dfs = (pd.read_excel(file_path, sheet_name=0)).copy()
dfr = (pd.read_excel(file_path, sheet_name=0)).copy()

type_sokr = None
with open('type_sokr.json', 'r', encoding='utf-8') as fil:
    type_sokr = json.load(fil)

'''
type_main = None
with open('type_main.json', 'r', encoding='utf-8') as fill:
    type_main = json.load(fill)

type_pod = None
with open('type_pod.json', 'r', encoding='utf-8') as filll:
    type_pod = json.load(filll)

new_type_pod = {'не ' + key: value for key, value in type_pod.items()}
type_pod = {**type_pod, **new_type_pod}
'''

type_main_list = None
with open('type_main_list.json', 'r', encoding='utf-8') as fill:
    type_main_list = json.load(fill)

type_pod_list = None
with open('type_pod_list.json', 'r', encoding='utf-8') as filll:
    type_pod_list = json.load(filll)

type_pod_list += [('не' + tp) for tp in type_pod_list]

type_pod_rod = None
with open('rod_pod_list.json', 'r', encoding='utf-8') as fillll:
    type_pod_rod = json.load(fillll)
type_pod_rod.update({('не' + tp):v for tp, v in type_pod_rod.items()})

type_main_rod = None
with open('rod_main_list.json', 'r', encoding='utf-8') as filllll:
    type_main_rod = json.load(filllll)

class Ship_Type:
    def __init__(self, df, type_sokr, type_main, type_pod, type_main_rod, type_pod_rod):
        self.df = df
        self.sokr_dict = type_sokr
        #self.main_dict=type_main
        #self.pod_dict=type_pod
        self.pod_key_dict = {}
        self.main_list=type_main
        self.pod_list=type_pod
        self.main_rod=type_main_rod
        self.pod_rod=type_pod_rod
        self.word_end_list = ['.', ',', '|', ':', '/', ';']

    def get_pod_key_dict(self):
        first=['ы', 'и', 'о', 'а', 'я', 'е']
        second=['й', 'я', 'е']
        # ый, ий, ой
        # ая, яя
        # ое, ее
        for key in self.pod_list:
            self.pod_key_dict[key]=key
            for f in first:
                for s in second:
                    self.pod_key_dict[f"{key[:-2]}{f}{s}"]=key
        '''
        for key, val in self.pod_dict:
            self.pod_key_dict[key]=key
            for f in first:
                for s in second:
                    self.pod_key_dict[f"{key[:-2]}{f}{s}"]=key
        '''

    def pp(self, row):
        #if row % 200 == 0:
            # break
            #print(row)
        return 0
    def strip_spaces(self, row_ii = 0):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, row_ii]).strip()
            self.df.iloc[row, row_ii] = value0
            self.pp(row)

    def del_point_comma(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace(';', ' ').strip()
            self.df.iloc[row, 0] = value0
            self.pp(row)

    def unsokr(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_words = value0.split(' ')
            #found_keys=[[key,  for key in self.sokr_dict if key in value0]
            for key in self.sokr_dict:
                for i in range(len(value0_words)):
                    if any(f"{key}{s}" == value0_words[i].lower() for s in self.word_end_list + ['']):
                        value0_words[i] = self.sokr_dict[key]

            value0 = ' '.join(value0_words)

            self.df.iloc[row, 0] = value0
            self.pp(row)

    '''
    def get_found_keys(self, self_dict, value0, mode = False):
        def main_ifs(value_lower, key):
            if mode:
                key_list=[k for k, v in self.pod_key_dict.items() if v == key]
                for key0 in key_list:
                    if key0.lower() in value_lower:
                        key = key0
                        break

            if key.lower() in value_lower:
                bool1 = True
                if value_lower.find(key.lower())>0:
                    if value_lower[value_lower.find(key.lower()) - 1] not in [' ', '.', ',', '|']:
                        bool1 = False
                bool2=True
                if value_lower.find(key.lower())+ len(key.lower()) < len(value_lower)-1:
                    if value_lower[value_lower.find(key.lower()) + len(key.lower())] not in [' ', '.', ',', '|']:
                        bool2=False

                return [bool1 and bool2, key]

            else:
                return [False, None]
        found_keys=[main_ifs(value0.lower(), key)[1] for key, val in self_dict if main_ifs(value0.lower(), key)[0]]

        for i in range(len(found_keys)):
            if any(found_keys[i].lower() in found_keys[j].lower() and i != j for j in range(len(found_keys))):
                found_keys[i]='-1'
        while '-1' in found_keys:
            found_keys.remove('-1')

        return found_keys
    '''


    def get_found_key(self, self_list, value_word, mode=False):
        def main_ifs(value_lower, key):
            if mode:
                key_list=[k for k, v in self.pod_key_dict.items() if v == key]
                for key0 in key_list:
                    if key0.lower() in value_lower:
                        key=key0
                        break

            if key.lower() in value_lower:
                bool2=True
                if len(key.lower()) < len(value_lower) - 1:
                    bool2 = False
                return [bool2, key]

            else:
                return [False, None]

        found_key=None
        for key in self_list:
            if main_ifs(value_word.lower(), key)[0]:
                #print(f"{value_word} == {key}")
                found_key=main_ifs(value_word.lower(), key)[1]
                break
        return found_key


    def delete_point_rule(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()

            def main_point_main(text):
                first_index=text.find('|')
                if first_index == -1:
                    return -1  # Первой палки нет
                second_index=text.find('|', first_index + 1)
                if second_index != -1:
                    if '.' in text[:second_index]:
                        if len(text[:second_index].split('.', 1))>1:
                            fm, sm=text[:second_index].split('.', 1)
                            fm, sm=fm.strip(), sm.strip()
                            if fm[-1] == '|':
                                fm=fm[:-1]
                            found_key_1=self.get_found_key(self.main_list, fm)
                            found_key_2=self.get_found_key(self.main_list, sm)

                            if found_key_1 is not None and found_key_2 is not None:
                                text=f"{found_key_1}|{found_key_2}{text[second_index:]}"
                return text
            value0 = main_point_main(value0)
            self.df.iloc[row, 1]=value0

    def correct_point_split(self, value0):
        value0_pred_list=value0.split('.')
        value0_pred_list=[vi.strip() for vi in value0_pred_list]
        vi = 0
        while vi<len(value0_pred_list):
            if vi<len(value0_pred_list)-1:
                if value0_pred_list[vi].split(' ')[-1].lower() not in [mt.lower() for mt in self.main_list]:
                    if re.findall(r"\b\d+[a-zA-Zа-яА-Я]{1,4}\b", value0_pred_list[vi].split(' ')[-1]) or re.findall(r"\b[a-zA-Zа-яА-Я]{1,4}\b", value0_pred_list[vi].split(' ')[-1]):
                        value0_pred_list[vi] += '. ' + value0_pred_list[vi+1]
                        del value0_pred_list[vi+1]
                        vi-=1
            vi+=1
        return value0_pred_list

    def main_pod_analyze(self):
        for row in range(len(self.df)):
            print('=======')
            print(f"row: {row}")
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list = self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                type_main_split=[]  # внутри [['строка до', 'доп в конце'], 'type_main']
                #main
                last_pos = 0
                value0_pred_words = value0_pred_list[vi].split()
                wi = 0
                main_first = False
                while wi<len(value0_pred_words):
                    #print(f"vi: {vi}, wi: {value0_pred_words[wi]}")
                    if wi!=len(value0_pred_words)-1:
                        found_key = self.get_found_key(self.main_list, f"{value0_pred_words[wi]} {value0_pred_words[wi+1]}")
                        if found_key is not None:
                            if wi == 0:
                                main_first = True
                            end_pos = len(' '.join([value0_pred_words[wii] for wii in range(wi)]))
                            type_main_split.append([[value0_pred_list[vi][last_pos:end_pos], None], found_key])
                            last_pos = end_pos+len(f" {value0_pred_words[wi]} {value0_pred_words[wi+1]}")
                            wi+=2
                            continue
                    found_key=self.get_found_key(self.main_list, value0_pred_words[wi])
                    if found_key is not None:
                        if wi == 0:
                            main_first=True
                        end_pos=len(' '.join([value0_pred_words[wii] for wii in range(wi)]))
                        type_main_split.append([[value0_pred_list[vi][last_pos:end_pos], None],found_key])
                        last_pos=end_pos + len(f" {value0_pred_words[wi]}")
                    wi+=1
                if len(value0_pred_list[vi])!=last_pos and type_main_split:
                    type_main_split[-1][0][1] = value0_pred_list[vi][last_pos:]

                if len(type_main_split)==0:
                    type_main_split.append([[value0_pred_list[vi][:], None], 'Судно'])

                #pod
                value0_pred_list[vi] = ""
                for tpi in range(len(type_main_split)):
                    pod_str = ""
                    type_main_split[tpi][0][0] = type_main_split[tpi][0][0].strip()
                    type_main_split_words=type_main_split[tpi][0][0].split()
                    pi=0
                    last_pos = 0
                    while pi < len(type_main_split_words):
                        if pi != len(type_main_split_words) - 1:
                            found_key=self.get_found_key(self.pod_list,f"{type_main_split_words[pi]} {type_main_split_words[pi + 1]}", True)
                            if found_key is not None:
                                end_pos=len(' '.join([type_main_split_words[pii] for pii in range(pi)]))
                                pod_str=f"{str(found_key).capitalize().strip()}|{type_main_split[tpi][0][0][last_pos:end_pos].capitalize().strip()}|{pod_str}"
                                last_pos=end_pos + len(f" {type_main_split_words[pi]} {type_main_split_words[pi + 1]}")
                                pi+=2
                                continue
                        found_key=self.get_found_key(self.pod_list, type_main_split_words[pi], True)
                        if found_key is not None:
                            end_pos=len(' '.join([type_main_split_words[pii] for pii in range(pi)]))
                            pod_str=f"{str(found_key).capitalize().strip()}|{type_main_split[tpi][0][0][last_pos:end_pos].capitalize().strip()}|{pod_str}"
                            last_pos=end_pos + len(f" {type_main_split_words[pi]}")
                        pi+=1
                    if len(type_main_split[tpi][0][0]) != last_pos:
                        pod_str += '|' + type_main_split[tpi][0][0][last_pos:].capitalize().strip()

                    pod_str1 = ""
                    if  main_first:
                        if type_main_split[tpi][0][1] is not None:
                            type_main_split_words=type_main_split[tpi][0][1].strip().split()
                            pi=0
                            last_pos=0
                            while pi < len(type_main_split_words):
                                if pi != len(type_main_split_words) - 1:
                                    found_key=self.get_found_key(self.pod_list,
                                                                 f"{type_main_split_words[pi]} {type_main_split_words[pi + 1]}",
                                                                 True)
                                    if found_key is not None:
                                        end_pos=len(' '.join([type_main_split_words[pii] for pii in range(pi)]))
                                        pod_str1=f"{str(found_key).capitalize().strip()}|{type_main_split[tpi][0][1][last_pos:end_pos].capitalize().strip()}|{pod_str1}"
                                        last_pos=end_pos + len(
                                            f" {type_main_split_words[pi]} {type_main_split_words[pi + 1]}")
                                        pi+=2
                                        continue
                                found_key=self.get_found_key(self.pod_list, type_main_split_words[pi], True)
                                if found_key is not None:
                                    end_pos=len(' '.join([type_main_split_words[pii] for pii in range(pi)]))
                                    pod_str1=f"{str(found_key).capitalize().strip()}|{type_main_split[tpi][0][1][last_pos:end_pos].capitalize().strip()}|{pod_str1}"
                                    last_pos=end_pos + len(f" {type_main_split_words[pi]}")
                                pi+=1
                            if len(type_main_split[tpi][0][1]) != last_pos:
                                pod_str1+='|' + type_main_split[tpi][0][1][last_pos:].capitalize().strip()
                    else:
                        pod_str1 = type_main_split[tpi][0][1].capitalize().strip() if type_main_split[tpi][0][1] is not None else ""

                    value0_pred_list[vi]+= f"{type_main_split[tpi][1].capitalize().strip()}|{pod_str.strip()}|{pod_str1.capitalize().strip() if pod_str1 != "" else ""}"
            self.df.iloc[row, 0]='. '.join(value0_pred_list)

    def pod_razdel_pod(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list = self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words = value0_pred_list[vi].split()
                for wi in range(len(value0_pred_words)):
                    if '-' in value0_pred_words[wi] or '/' in value0_pred_words[wi]:
                        raz_symbol = '-'
                        if '/' in value0_pred_words[wi]:
                            raz_symbol = '/'
                        last_symbol = ''
                        if value0_pred_words[wi][-1] in self.word_end_list:
                            last_symbol = value0_pred_words[wi][-1]
                            value0_pred_words[wi] = value0_pred_words[wi][:-1]
                        if len(value0_pred_words[wi].split(raz_symbol, 1)) > 1:
                            pod_1, pod_2 = value0_pred_words[wi].split(raz_symbol, 1)
                            if len(pod_1)>1:
                                if pod_1[-1] == 'о':
                                    pod_1 = pod_1[:-1] + pod_2[-2:]
                            found_key_1=self.get_found_key(self.pod_list, pod_1, True)
                            found_key_2=self.get_found_key(self.pod_list, pod_2, True)
                            if found_key_1 is not None and found_key_2 is not None:
                                value0_pred_words[wi] = f"{found_key_1} {found_key_2}{last_symbol}"
                value0_pred_list[vi] = ' '.join(value0_pred_words)
            self.df.iloc[row, 0]='. '.join(value0_pred_list)

    def main_razdel_pod(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split()
                for wi in range(len(value0_pred_words)):
                    if '-' in value0_pred_words[wi] or '/' in value0_pred_words[wi]:
                        raz_symbol='-'
                        if '/' in value0_pred_words[wi]:
                            raz_symbol='/'
                        last_symbol=''
                        if value0_pred_words[wi][-1] in self.word_end_list:
                            last_symbol=value0_pred_words[wi][-1]
                            value0_pred_words[wi]=value0_pred_words[wi][:-1]
                        if len(value0_pred_words[wi].split(raz_symbol, 1))>1:
                            pod_1, pod_2=value0_pred_words[wi].split(raz_symbol, 1)
                            found_key_1=self.get_found_key(self.main_list, pod_1)
                            found_key_2=self.get_found_key(self.pod_list, pod_2, True)
                            if found_key_1 is not None and found_key_2 is not None:
                                value0_pred_words[wi]=f"{found_key_1} {found_key_2}{last_symbol}"
                value0_pred_list[vi]=' '.join(value0_pred_words)
            self.df.iloc[row, 0]='. '.join(value0_pred_list)

    def main_razdel_main(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split()
                for wi in range(len(value0_pred_words)):
                    if '-' in value0_pred_words[wi] or '/' in value0_pred_words[wi]:
                        raz_symbol='-'
                        if '/' in value0_pred_words[wi]:
                            raz_symbol='/'
                        last_symbol=''
                        if value0_pred_words[wi][-1] in self.word_end_list:
                            last_symbol=value0_pred_words[wi][-1]
                            value0_pred_words[wi]=value0_pred_words[wi][:-1]
                        if len(value0_pred_words[wi].split(raz_symbol, 1)) > 1:
                            pod_1, pod_2=value0_pred_words[wi].split(raz_symbol, 1)
                            found_key_1=self.get_found_key(self.main_list, pod_1)
                            found_key_2=self.get_found_key(self.main_list, pod_2)
                            if found_key_1 is not None and found_key_2 is not None:
                                #value0_pred_words[wi]=f"{found_key_1} {found_key_2}{last_symbol}"
                                if f"{found_key_1}-{found_key_2}" not in self.main_list:
                                    self.main_list.append(f"{found_key_1}-{found_key_2}")
                                    print(f"{found_key_1}-{found_key_2}")
                #value0_pred_list[vi]=' '.join(value0_pred_words)
            #self.df.iloc[row, 0]='. '.join(value0_pred_list)

    def make_upper(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                for wi in range(len(value0_pred_words)):
                    if len(value0_pred_words[wi])>=1:
                        value0_pred_words[wi] = value0_pred_words[wi][0].upper() + value0_pred_words[wi][1:]

                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def summ_mains(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()

            def main_eq_main(text):
                text_words=text.split('|')
                text_words=[tw.strip() for tw in text_words]
                for ti in range(len(text_words) - 1):
                    found_key_1=self.get_found_key(self.main_list, text_words[ti])
                    found_key_2=self.get_found_key(self.main_list, text_words[ti+1])
                    if found_key_1 is not None and found_key_2 is not None:
                        if '-' in text_words[ti]:
                            if text_words[ti + 1].lower() in [twi.lower() for twi in text_words[ti].split('-')]:
                                text_words[ti + 1]=''
                        elif '-' in text_words[ti + 1]:
                            if text_words[ti].lower() in [twi.lower() for twi in text_words[ti + 1].split('-')]:
                                text_words[ti]=''
                        else:
                            if text_words[ti].lower() == text_words[ti + 1].lower():
                                text_words[ti + 1]=''
                            elif text_words[ti] == 'Судно' and text_words[ti+1] != 'Судно':
                                text_words[ti]=''
                            elif text_words[ti+1] == 'Судно' and text_words[ti] != 'Судно':
                                text_words[ti+1]=''

                result='|'.join(text_words)
                if result[0] == '|':
                    result=result[1:]
                return result

            value0 = main_eq_main(value0)
            self.df.iloc[row, 1]=value0


    def summ_if_second_sudno(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            if len(value0_pred_list)>1:
                vi = 1
                while vi < len(value0_pred_list):
                    if value0_pred_list[vi].startswith('Судно'):
                        value0_pred_list[vi-1] += "|" + value0_pred_list[vi][5:]
                        del value0_pred_list[vi]
                    else:
                        vi+=1
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def summ_if_first_sudno(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            if len(value0_pred_list)==2:
                if value0_pred_list[0].startswith('Судно'):
                    value0_pred_words_0=value0_pred_list[0].split('|')
                    vpl0 = []
                    for word in value0_pred_words_0:
                        found_main_0=self.get_found_key(self.main_list, word)
                        if found_main_0 is not None:
                            vpl0.append(found_main_0)
                    if len(vpl0)==1:
                        value0_pred_words_1=value0_pred_list[1].split('|', 1)
                        if len(value0_pred_words_1)==1:
                            value0_pred_words_1.append('')
                        found_main_1=self.get_found_key(self.main_list, value0_pred_words_1[0])
                        if found_main_1 is not None:
                            value0_pred_words_0[0] = found_main_1
                            value0_pred_list[0] = '|'.join(value0_pred_words_0) + '|' + value0_pred_words_1[1]
                            del value0_pred_list[1]

            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def summ_if_first_sudno_1(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            if len(value0_pred_list)==2:
                value0_pred_words_0=value0_pred_list[0].split('|')
                vpl0 = []
                for word in value0_pred_words_0:
                    found_main_0=self.get_found_key(self.main_list, word)
                    if found_main_0 is not None:
                        vpl0.append(found_main_0)
                if len(vpl0)==1:
                    value0_pred_words_1=value0_pred_list[1].split('|', 1)
                    if len(value0_pred_words_1)==1:
                        value0_pred_words_1.append('')
                    found_main_1=self.get_found_key(self.main_list, value0_pred_words_1[0])
                    if found_main_1 is not None:
                        if found_main_1.lower() == vpl0[0].lower():
                            #value0_pred_words_0[0] = found_main_1
                            value0_pred_list[0] = '|'.join(value0_pred_words_0) + '|' + value0_pred_words_1[1]
                            del value0_pred_list[1]
                        else:
                            if '-' in found_main_1 and vpl0[0].lower() in [found_main_1_l.lower() for found_main_1_l in found_main_1.split('-')]:
                                value0_pred_words_0[0] = found_main_1
                                value0_pred_list[0] = '|'.join(value0_pred_words_0) + '|' + value0_pred_words_1[1]
                                del value0_pred_list[1]
                            elif '-' in vpl0[0] and found_main_1.lower() in [vpl0_0_l.lower() for vpl0_0_l in vpl0[0].split('-')]:
                                #value0_pred_words_0[0] = found_main_1
                                value0_pred_list[0] = '|'.join(value0_pred_words_0) + '|' + value0_pred_words_1[1]
                                del value0_pred_list[1]
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def sudno_zam_first(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                sudno_index = -1
                for wi in range(len(value0_pred_words)):
                    if value0_pred_words[wi].lower() == 'судно':
                        sudno_index = wi
                    if sudno_index!=-1 and sudno_index!=wi:
                        found_main=self.get_found_key(self.main_list, value0_pred_words[wi])
                        if found_main is not None:
                            value0_pred_words[sudno_index] = value0_pred_words[wi]
                            value0_pred_words[wi] = ''
                            sudno_index=-1
                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def del_similar_pot(self):
        for row in range(len(self.df)):
            print(f"row: {row}")
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                current_pod_list = []
                for wi in range(1, len(value0_pred_words)):
                        if self.get_found_key(self.main_list, value0_pred_words[wi]) is not None:
                            current_pod_list = []
                        else:
                            pod_key = self.get_found_key(self.pod_list, value0_pred_words[wi], True)
                            if pod_key is not None:
                                if pod_key.lower()[:-2] in current_pod_list:
                                    value0_pred_words[wi] = ''
                                else:
                                    current_pod_list.append(pod_key.lower()[:-2])
                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def skob_fix(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                for wi in range(len(value0_pred_words)):
                    if len(value0_pred_words[wi]) >= 1:
                        if value0_pred_words[wi][0] == '(':
                            if len(value0_pred_words[wi]) >= 2:
                                if value0_pred_words[wi][-1] == ')':
                                    value0_pred_words[wi] = value0_pred_words[wi][1:-1]
                                if value0_pred_words[wi][-2] == ')':
                                    value0_pred_words[wi]=value0_pred_words[wi][1:-2]
                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def rod_fix(self):
        for row in range(len(self.df)):
            print(f"row: {row}")
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                current_main_rod = 0
                for wi in range(0, len(value0_pred_words)):
                        if self.get_found_key(self.main_list, value0_pred_words[wi]) is not None:
                            current_main_rod = self.main_rod[self.get_found_key(self.main_list, value0_pred_words[wi])]-1
                        else:
                            pod_key = self.get_found_key(self.pod_list, value0_pred_words[wi], True)
                            if pod_key is not None:
                                if len(pod_key) >= 3:
                                    pod_rod_result=[k for k in self.pod_rod.keys() if pod_key[:-2] in k and len(pod_key) == len(k)]
                                    if len(pod_rod_result) > 0:
                                        if len(self.pod_rod[pod_rod_result[0]])>0:
                                            value0_pred_words[wi] = pod_rod_result[0][:-2] + self.pod_rod[pod_rod_result[0]][current_main_rod]
                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def sort_pod(self):
        for row in range(len(self.df)):
            print(f"row: {row}")
            value0=str(self.df.iloc[row, 1]).strip()
            value0_pred_list=self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                value0_pred_words=value0_pred_list[vi].split('|')
                current_main_index = 0
                current_pod_list = [[], []]
                for wi in range(1, len(value0_pred_words)):
                        if (self.get_found_key(self.main_list, value0_pred_words[wi]) is not None or wi == len(value0_pred_words)-1) and current_main_index!=wi:
                            current_pod_list[0] = sorted(current_pod_list[0])
                            value0_pred_words[current_main_index+1:wi] = [''] * (wi-current_main_index)
                            if current_main_index+1 != wi:
                                value0_pred_words[current_main_index+1] = '|'.join(current_pod_list[0]) + '|' + '|'.join(current_pod_list[1])
                            current_main_index=wi
                            current_pod_list = [[], []]
                        else:
                            pod_key = self.get_found_key(self.pod_list, value0_pred_words[wi], True)
                            if pod_key is not None:
                                current_pod_list[0].append(value0_pred_words[wi])
                            else:
                                current_pod_list[1].append(value0_pred_words[wi])
                value0_pred_list[vi]='|'.join(value0_pred_words)
            self.df.iloc[row, 1]='. '.join(value0_pred_list)

    def get_non_pod_main(self):
        nonpodmain_list = []
        for row in range(len(self.df)):
            print(f"row: {row}")
            value0=str(self.df.iloc[row, 1]).strip()
            value0_palka_list=value0.split('|')
            for vpl in value0_palka_list:
                if self.get_found_key(self.main_list, vpl) is None and self.get_found_key(self.pod_list, vpl, True) is None:
                    nonpodmain_list.append(vpl)
        nonpodmain_str = '\n'.join(nonpodmain_list)

        with open("nonpodmain.txt", 'w') as nonpodmain_file_object:
            nonpodmain_file_object.write(nonpodmain_str)

    '''
    def main_pos(self):
        def move_substring(s, start, substr, insert_at, plus_sub):
            substring = substr + plus_sub
            remaining_str=s[:start] + s[start + len(substring):]
            new_str=remaining_str[:insert_at] + substring + remaining_str[insert_at:]
            return new_str


        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list = self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                #print('===============', row)
                #print(value0_pred_list[vi])

                found_keys =  self.get_found_keys(self.main_dict, value0_pred_list[vi])

                #print(found_keys)

                if len(found_keys) == 0:
                    value0_pred_list[vi]= 'Судно|'+ value0_pred_list[vi]
                    #print(f"str:{value0_pred_list[vi]}")
                else:
                    last_pos = 0
                    for key in found_keys:
                        plus_sub = '|'
                        start = value0_pred_list[vi].lower().find(key.lower())
                        value0_pred_list[vi] = move_substring(value0_pred_list[vi], start, key, last_pos, plus_sub)
                        #print(f"lp:{last_pos}   st:{start}  str:{value0_pred_list[vi]}")
                        last_pos = start + len(plus_sub) + len(key)

            self.df.iloc[row, 0]='. '.join(value0_pred_list)

    def pod_pos(self):
        def move_substring(s, start, substr, insert_at, plus_sub):
            substring = substr + plus_sub
            remaining_str=s[:start] + s[start + len(substring):]
            new_str=remaining_str[:insert_at] + substring + remaining_str[insert_at:]
            return new_str


        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0_pred_list = self.correct_point_split(value0)
            for vi in range(len(value0_pred_list)):
                #print('===============', row)
                #print(value0_pred_list[vi])

                found_keys_main = self.get_found_keys(self.main_dict, value0_pred_list[vi])
                found_keys = self.get_found_keys(self.pod_dict, value0_pred_list[vi], True)

                found_keys = [key for key in  found_keys if not any(key.lower() in keym.lower() for keym in found_keys_main)]

                #print(found_keys_main)
                #print(found_keys)

                if '|' in value0_pred_list[vi]:
                    for key in found_keys:
                        plus_sub = '|'
                        start = value0_pred_list[vi].lower().find(key.lower())
                        last_pos=value0_pred_list[vi].lower()[:start].rfind('|')+1
                        value0_pred_list[vi] = move_substring(value0_pred_list[vi], start, self.pod_key_dict[key], last_pos, plus_sub)
                        #print(f"lp:{last_pos}   st:{start}  str:{value0_pred_list[vi]}")
                        last_pos = start + len(plus_sub) + len(key)

            self.df.iloc[row, 0]='.'.join(value0_pred_list)
    '''
    def comma_end(self):# . , в конце
        for row in range(1, len(self.df)):

            value0=str(self.df.iloc[row, 0]).strip()
            if value0[-1] == ',' or value0[-1] == '.':
                # print(value0, "__", value0[:-1])
                self.df.iloc[row, 0]=value0[:-1]
            self.pp(row)

    def comma_similar(self):
        value_with_comma=[]
        value_without_comma=[]

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count(',') == 1:
                value_with_comma.append(value0)  # .replace(',', ''))
                value_without_comma.append(value0.replace(',', ''))
            self.pp(row)

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count(',') == 0:
                if value0 in value_without_comma:
                    index=value_without_comma.index(value0)
                    self.df.iloc[row, 0]=value_with_comma[index]
            self.pp(row)

    def defis(self): # -
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0])
            if '- ' in value0 and ' - ' not in value0:
                value1 = value0.replace('- ', '-')
                self.df.iloc[row, 0] = value1
            elif ' -' in value0 and ' - ' not in value0:
                value1 = value0.replace(' -', '-')
                self.df.iloc[row, 0] = value1

            self.pp(row)

    def vert_last(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 1])
            if value0[-1] == '|':
                value0 =value0[:-1]
            self.df.iloc[row, 1] = value0

    def some_fixes(self, row_ii=0): # < <= >= > .
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, row_ii])
            
            def replace_val(value0, old, new):
                while old in value0:
                    value0 = value0.replace(old, new)
                return value0
            
            def replace_val1(value0, old, new):
                value0 = value0.replace(old, new)
                return value0

            def rep_grad(value0):
                value0=replace_val(value0, 'гр. С', 'гр.c')
                value0=replace_val(value0, 'гр. с', 'гр.c')
                value0=replace_val(value0, 'гр. C', 'гр.c')
                value0=replace_val(value0, 'гр. c', 'гр.c')

                value0=replace_val(value0, 'гр С', 'гр.c')
                value0=replace_val(value0, 'гр с', 'гр.c')
                value0=replace_val(value0, 'гр C', 'гр.c')
                value0=replace_val(value0, 'гр c', 'гр.c')

                value0=replace_val(value0, 'гр.С', 'гр.c')
                value0=replace_val(value0, 'гр.с', 'гр.c')
                value0=replace_val(value0, 'гр.C', 'гр.c')

                value0=replace_val(value0, 'грС', 'гр.c')
                value0=replace_val(value0, 'грс', 'гр.c')
                value0=replace_val(value0, 'грC', 'гр.c')
                value0=replace_val(value0, 'грc', 'гр.c')

                value0=replace_val(value0, 'град. С', 'гр.c')
                value0=replace_val(value0, 'град. с', 'гр.c')
                value0=replace_val(value0, 'град. C', 'гр.c')
                value0=replace_val(value0, 'град. c', 'гр.c')

                value0=replace_val(value0, 'град С', 'гр.c')
                value0=replace_val(value0, 'град с', 'гр.c')
                value0=replace_val(value0, 'град C', 'гр.c')
                value0=replace_val(value0, 'град c', 'гр.c')

                value0=replace_val(value0, 'град.С', 'гр.c')
                value0=replace_val(value0, 'град.с', 'гр.c')
                value0=replace_val(value0, 'град.C', 'гр.c')
                value0=replace_val(value0, 'град.c', 'гр.c')

                value0=replace_val(value0, 'градС', 'гр.c')
                value0=replace_val(value0, 'градс', 'гр.c')
                value0=replace_val(value0, 'градC', 'гр.c')
                value0=replace_val(value0, 'градc', 'гр.c')

                value0=replace_val(value0, 'градусов С', 'гр.c')
                value0=replace_val(value0, 'градусов с', 'гр.c')
                value0=replace_val(value0, 'градусов C', 'гр.c')
                value0=replace_val(value0, 'градусов c', 'гр.c')
                value0=replace_val(value0, 'градусовС', 'гр.c')
                value0=replace_val(value0, 'градусовс', 'гр.c')
                value0=replace_val(value0, 'градусовC', 'гр.c')
                value0=replace_val(value0, 'градусовc', 'гр.c')
                value0=replace_val(value0, 'градусов', 'гр.c')
                value0=replace_val(value0, 'градусо', 'гр.c')

                value0=replace_val1(value0, 'гр ', 'гр.')
                value0=replace_val(value0, 'град ', 'град.')
                value0=replace_val1(value0, 'гр.', 'гр.c')
                value0=replace_val(value0, 'град.', 'гр.c')


                def grad_zam(zam, value0):
                    if zam in value0[-len(zam)-2:]:
                        value0 = value0[:-len(zam)-2] + value0[-len(zam)-2:].replace(zam, 'гр.c')
                    return value0

                value0 = grad_zam('гр', value0)
                value0 = grad_zam('град', value0)

                value0=replace_val(value0, 'гр.cc', 'гр.c')

                value0=replace_val(value0, ' гр.c', 'гр.c')
                value0=replace_val(value0, 'гр.c', '°c')

                value0=replace_val(value0, '° С', '°c')
                value0=replace_val(value0, '° с', '°c')
                value0=replace_val(value0, '° C', '°c')
                value0=replace_val(value0, '° c', '°c')
                value0=replace_val(value0, ' °c', '°c')
                value0=replace_val(value0, '°c ', '°c')
                value0=replace_val1(value0, '°c', '°c ')

                return value0

            def rep_Tsvp(value0):
                value0=replace_val(value0, 'Твсп', 'Tвсп')
                value0=replace_val(value0, 'tвсп', 'Tвсп')
                value0=replace_val(value0, 'tсвп', 'Tвсп')
                value0=replace_val(value0, 'Tсвп.', 'Tвсп')
                value0=replace_val(value0, 'Tсвп', 'Tвсп.')
                return value0

            def rep_other(value0):
                value0=replace_val(value0, '..', '.')
                value0=replace_val(value0, '60р.', '60°c')
                return value0

            def rep_symbols(value0):
                value0=replace_val(value0, '> ', '>')
                value0=replace_val(value0, ' >', '>')
                value0=replace_val(value0, '< ', '<')
                value0=replace_val(value0, ' <', '<')

                value0=replace_val(value0, '= ', '=')
                value0=replace_val(value0, ' =', '=')

                value0=replace_val(value0, '>= ', '>=')
                value0=replace_val(value0, ' >=', '>=')
                value0=replace_val(value0, '<= ', '<=')
                value0=replace_val(value0, ' <=', '<=')

                value0=replace_val1(value0, '=', ' = ')
                value0=replace_val1(value0, '>', ' > ')
                value0=replace_val1(value0, '<', ' < ')

                value0=replace_val(value0, '> =', '>=')
                value0=replace_val(value0, '< =', '<=')
                return value0

            value0 = rep_Tsvp(value0)
            value0 = rep_other(value0)
            value0 = rep_symbols(value0)
            value0 = rep_grad(value0)

            self.df.iloc[row, row_ii] = value0

    def vert_0(self, row_ii=0): # -
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, row_ii])
            if '| ' in value0:
                value1 = value0.replace('| ', '|')
                self.df.iloc[row, row_ii] = value1
            if ' |' in value0:
                value1 = value0.replace(' |', '|')
                self.df.iloc[row, row_ii] = value1

            self.pp(row)
    def vert_1(self, row_ii = 0): # -
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, row_ii])
            while '||' in value0:
                value0 = value0.replace('||', '|')
            self.df.iloc[row, row_ii] = value0
            self.pp(row)

    def defis_similar(self):
        value_with_comma=[]
        value_without_comma=[]

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count('-') == 1:
                value_with_comma.append(value0)  # .replace(',', ''))
                value_without_comma.append(value0.replace('-', ''))
            self.pp(row)

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count('-') == 0:
                if value0 in value_without_comma:
                    index=value_without_comma.index(value0)
                    self.df.iloc[row, 0]=value_with_comma[index]
            self.pp(row)

    def defis_similar_2(self):
        value_with_comma=[]
        value_without_comma=[]

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count('-') == 1:
                value_with_comma.append(value0)  # .replace(',', ''))
                value_without_comma.append(value0.replace('-', ', '))
            self.pp(row)

        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if value0.count('-') == 0:
                if value0 in value_without_comma:
                    index=value_without_comma.index(value0)
                    self.df.iloc[row, 0]=value_with_comma[index]
            self.pp(row)

    def first_dlya(self):# , для первое
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if ', для ' in value0 and value0.find(',') == value0.find(', для'):
                self.df.iloc[row, 0] = value0.replace(', для ', '|', 1)
            self.pp(row)

    def first_chosen(self, chosen):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if f', {chosen}' in value0 and value0.find(',') == value0.find(f', {chosen}'):
                self.df.iloc[row, 0] = value0.replace(f', {chosen}', f'|{chosen}', 1)
            self.pp(row)

    def comma_chosen(self, chosen):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if f' {chosen}' in value0 and value0[value0.find(f' {chosen}')-1] != ',':
                self.df.iloc[row, 0] = value0.replace(f' {chosen}', f', {chosen}', 1)
            self.pp(row)

    def delete_double_spaces(self, row_ii = 0):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, row_ii]).strip()
            while '  ' in value0:
                value0=value0.replace('  ', ' ')
            self.df.iloc[row, row_ii] = value0.strip()
            self.pp(row)

    def yo_to_ye(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('ё', 'е')
            self.df.iloc[row, 0] = value0.strip()
            self.pp(row)

    #секция наплавного моста
    def SNM(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('секция наплавного моста', 'СН_М')
            value0=value0.replace('Секция наплавного моста', 'СН_М')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)
    def unSNM(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('СН_М', 'Секция наплавного моста')
            value0=value0.replace('Сн_м', 'Секция наплавного моста')
            value0=value0.replace('сн_м', 'Секция наплавного моста')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)

    def PSM(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('переходный стыковочный модуль', 'ПС_М')
            value0=value0.replace('Переходный стыковочный модуль', 'ПС_М')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)
    def unPSM(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('ПС_М', 'Переходный стыковочный модуль')
            value0=value0.replace('Пс_м', 'Переходный стыковочный модуль')
            value0=value0.replace('пс_м', 'Переходный стыковочный модуль')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)

    def SVP(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('судно на воздушной подушке', 'С_НА_ВП')
            value0=value0.replace('Судно на воздушной подушке', 'С_НА_ВП')
            value0=value0.replace('на воздушной подушке', 'НА_ВП')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)
    def unSVP(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('С_НА_ВП', 'Судно на воздушной подушке')
            value0=value0.replace('С_на_вп', 'Судно на воздушной подушке')
            value0=value0.replace('с_на_вп', 'Судно на воздушной подушке')
            value0=value0.replace('НА_ВП', 'на воздушной подушке')
            value0=value0.replace('На_вп', 'на воздушной подушке')
            value0=value0.replace('на_вп', 'на воздушной подушке')

            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)

    def first_point(self):
        def get_find(value0, ch):
            if value0.find(f'{ch} ') == -1:
                return 1000
            else:
                return value0.find(f'{ch} ')
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if '. ' in value0:
                if ', ' or ': ' or '; ' in value0:
                    if value0.find('. ') < min([get_find(value0, ch) for ch in [', ', ': ', '; ']]):
                        value0=value0.replace('. ', '|')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)

    def first_s(self):# , с первое
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            if ', с ' in value0 and value0.find(',') == value0.find(', с '):
                self.df.iloc[row, 0] = value0.replace(', с ', '|', 1)
            self.pp(row)
    def give_vert(self):
        for row in range(len(self.df)):
            value0=str(self.df.iloc[row, 0]).strip()
            value0=value0.replace('судно снабжения', 'Cудно|снабжения')
            value0=value0.replace('Cудно снабжения', 'Cудно|снабжения')
            value0=value0.replace('_С_Н_', '|Специального назначения')
            value0=value0.replace('_с_н_', '|Специального назначения')
            self.df.iloc[row, 0]=value0.strip()
            self.pp(row)
        #судно снабжения
#stys = Ship_Type(dfs)
#styr = Ship_Type(dfr, type_sokr, sorted(type_main.items(), key=lambda x: x[1]), sorted(type_pod.items(), key=lambda x: x[1]))
styr = Ship_Type(dfr, type_sokr, type_main_list, type_pod_list, type_main_rod, type_pod_rod)
styr.get_pod_key_dict()
def type_5():
    print('strip_spaces')
    styr.strip_spaces(1)

    print('make_upper')
    styr.make_upper()
    print('summ_if_second_sudno')
    styr.summ_if_second_sudno()

    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_6():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('skob_fix')
    styr.skob_fix()
    print('some_fixes')
    styr.some_fixes(1)


    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_7():
    print('strip_spaces')
    styr.strip_spaces(1)

    print('vert_last')
    styr.vert_last()

    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_8():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('sudno_zam')
    styr.sudno_zam()
    print('sudno_zam')
    styr.sudno_zam()
    print('sudno_zam')
    styr.sudno_zam()
    print('sudno_zam')
    styr.sudno_zam()
    print('sudno_zam')
    styr.sudno_zam()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_10():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('summ_if_first_sudno')
    styr.summ_if_first_sudno()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_11():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('summ_if_first_sudno_1')
    styr.summ_if_first_sudno_1()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_14():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('del_similar_pot')
    styr.del_similar_pot()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_15():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('sort_pod')
    styr.sort_pod()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

def type_16():
    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

    print('rod_fix')
    styr.rod_fix()

    print('strip_spaces')
    styr.strip_spaces(1)
    print('vert_0')
    styr.vert_0(1)
    print('vert_1')
    styr.vert_1(1)
    print('delete_double_spaces')
    styr.delete_double_spaces(1)
    print('strip_spaces')
    styr.strip_spaces(1)

'''
print('strip_spaces')
styr.strip_spaces()
print('del_point_comma')
styr.del_point_comma()
print('comma_end')
styr.comma_end()
print('comma_similar')
styr.comma_similar()
print('math_symbols')
styr.math_symbols()
print('defis')
styr.defis()
print('defis_similar')
styr.defis_similar()
print('defis_similar_2')
styr.defis_similar_2()
print('delete_double_spaces')
styr.delete_double_spaces()
print('unsokr')
styr.unsokr()
print('SVP')
styr.SVP()
print('PSM')
styr.PSM()
print('SNM')
styr.SNM()
print('strip_spaces')
styr.strip_spaces()
print('delete_double_spaces')
styr.delete_double_spaces()
print('yo_to_ye')
styr.yo_to_ye()


print('main_razdel_main')
styr.main_razdel_main()

print('main_razdel_pod')
styr.main_razdel_pod()

print('pod_razdel_pod')
styr.pod_razdel_pod()
'''
'''
print('main_pod_analyze')
styr.main_pod_analyze()

print('unSVP')
styr.unSVP()
print('unPSM')
styr.unPSM()
print('unSNM')
styr.unSNM()
print('give_vert')
styr.give_vert()
print('vert_0')
styr.vert_0()
print('vert_1')
styr.vert_1()

print('delete_double_spaces')
styr.delete_double_spaces()
print('strip_spaces')
styr.strip_spaces()
'''
'''
print('strip_spaces')
styr.strip_spaces()

print('delete_point_rule')
styr.delete_point_rule()
print('summ_mains')
styr.summ_mains()

print('vert_0')
styr.vert_0()
print('vert_1')
styr.vert_1()
print('delete_double_spaces')
styr.delete_double_spaces()
print('strip_spaces')
styr.strip_spaces()
'''

type_14()

#styr.get_non_pod_main()

def save_file():
    with pd.ExcelWriter(f"{file}_{number}.xlsx", engine="openpyxl") as writer:
        #stys.df.to_excel(writer, sheet_name="sea", index=False)
        styr.df.to_excel(writer, sheet_name="river", index=False)
save_file()