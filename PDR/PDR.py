from tkinter.filedialog import askopenfilename
from tkinter import *
from os import path
from tkinter.ttk import Progressbar
from tkinter import ttk
import time
import threading
import subprocess
from tkinter import scrolledtext
from tkinter.ttk import *
import tkinter.font
from tkinter import messagebox
import time

from Bio.Blast import NCBIWWW
from Bio import AlignIO
from Bio import SeqIO
from Bio import SearchIO
import Bio.SearchIO.BlastIO
import os
import sys
from Bio.Align.Applications import ClustalwCommandline
import xlrd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import shutil
from Bio.Align.Applications import MuscleCommandline
import os.path
from os import path
from xlwt import Workbook


def findfile():
        problem_label.configure(text = "")
        filename = askopenfilename()
        lbl1.configure(text = filename)
        if(lbl1['text'] != ""):
                bttn2.configure(state=NORMAL)

def start():
        global currentThread
        bttn1.configure(state=DISABLED)
        bttn2.configure(state=DISABLED)
        bttn3.configure(state=NORMAL)
        combo1.configure(state = DISABLED) ###
        combo2.configure(state = DISABLED)
        combo3.configure(state = DISABLED)
        combo4.configure(state = DISABLED)

        currentThread = myThread()
        currentThread.start()

def openfolder():
	test_thread = TestThread()
	test_thread.start()	

def find_C(sequence):
        c_list = []
        for s in range(len(sequence)):
                if sequence[s] == "C":
                        c_list.append(s)
                        
        return c_list #here index starts from 0!!!!


def Check_Monkey(description_list):
        monkey_count = 0
        for name in description_list:
                for monkey in monkey_list:
                        if monkey.split()[0].lower() in name.lower():
                                monkey_count += 1
                                break
        if(len(description_list) != 0):
                percentage = round(100.0 * monkey_count / len(description_list), 1)
        else:
                return True, 100.0, 0, 0
        return (percentage >= int(combo3.get())), percentage, monkey_count, len(description_list) ###### you put equal sign here ####80.0%

def activate_muscle(protein_name):
        #t0 = time.time() ########test
        cline = MuscleCommandline(input="{}/{}.faa".format(folder_name, protein_name), out="{}/{}.aln".format(folder_name, protein_name), clwstrict=True) 
        stdout, stderr = cline() # we use the muscle software to do the multiple alignments
        #t1 = time.time() ########test
        #print("muscle: {}\n".format(t1 - t0)) ######test

def Restart():
        lbl1.configure(text = "")
        info_txt.delete(1.0,END)
        bttn1.configure(state = NORMAL)
        bttn2.configure(state = DISABLED)
        bttn3.configure(state = DISABLED)
        bar['value'] = 0
        new_button.configure(state = DISABLED)
        combo1.configure(state = NORMAL) ####
        combo2.configure(state = NORMAL)
        combo3.configure(state = NORMAL)
        combo4.configure(state = NORMAL)
        lbl2.configure(text = "")

def Open_Info():
        os.system('start README.txt')

currentThread = None
window = Tk()

window.title("Primate Differential Redoxome (PDR)")
window.geometry('950x620')

default_font = tkinter.font.nametofont("TkDefaultFont")
default_font.configure(size=11)

f5 = Frame(window)
bttn1 = Button(f5, text="Choose input file", command=findfile)
bttn4 = Button(f5, text="Info", command=Open_Info)
f5.grid(row = 0, column = 0, pady = 10)
bttn1.pack(side = RIGHT, padx = 20)
bttn4.pack(side = LEFT, padx = 20)

lbl1 = Label(window)
lbl1.grid(row = 0, column = 1)

f1 = Frame(window)
lbl4 = Label(f1, text = "               Orthologs number : ")
combo1 = Combobox(f1)
f1.grid(row = 1, column = 0, pady = 10)
lbl4.pack(side = LEFT)
combo1.pack(side = LEFT)
combo1['values']= (250, 300, 350, 400, 450, 500)
combo1.current(0) #set to default

f2 = Frame(window)
lbl5 = Label(f2, text = "     Sequence identity, >(%) : ")
combo2 = Combobox(f2)
f2.grid(row = 2, column = 0, pady = 10)
lbl5.pack(side = LEFT)
combo2.pack(side = LEFT)
combo2['values']= (70, 80, 90)
combo2.current(1) #set to default

f3 = Frame(window)
lbl7 = Label(f3, text = "      Cys conservation, <(%) : ")
combo4 = Combobox(f3)
f3.grid(row = 3, column = 0, pady = 10)
lbl7.pack(side = LEFT)
combo4.pack(side = LEFT)
combo4['values']= (10, 20, 30, 40, 50)
combo4.current(2) #set to default

f4 = Frame(window)
lbl6 = Label(f4, text = "            Cys primates, >(%) : ")
combo3 = Combobox(f4)
f4.grid(row = 4, column = 0, pady = 10)
lbl6.pack(side = LEFT)
combo3.pack(side = LEFT)
combo3['values']= (70, 80, 90)
combo3.current(1) #set to default

bttn2 = Button(window, text="Start", command=start, state = DISABLED)
bttn2.grid(row = 5, column = 0, pady = 10)

lbl6 = Label(window, text = "Progress:")
lbl6.grid(row = 6, column = 0)

bar = Progressbar(window, length=350, style='black.Horizontal.TProgressbar')
bar.grid(row = 7, column = 0)

lbl2 = Label(window)
lbl2.grid(row = 7, column = 1)

info_txt = scrolledtext.ScrolledText(window, width=40,height=10)
info_txt.grid(row = 8, column = 0)

bttn3 = Button(window, text="Open results", command=openfolder, state = DISABLED)
bttn3.grid(row = 9, column = 0, pady = 10)

problem_label = Label(window)
problem_label.grid(row = 9, column = 1, pady = 10)

new_button = Button(window, text="New", command=Restart, state = DISABLED)
new_button.grid(row = 10, column = 0, pady = 10)

folder_path = ""
folder_name = ""

class myThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.killed = False

        def run(self):
                global row_count
                row_count = 1
                try:
                        sheet = ReadExcel()
                        CreateFolders(sheet) #final_sheet,
                except Exception as e:
                        print(str(e))
                        Restart()
                        problem_label.configure(text = "There has been a problem with the excel file chosen")
                        return

                if("(" in folder_name or ")" in folder_name):
                        Restart()
                        problem_label.configure(text = "There cant be '(' or ')' in folder name")
                        return

                log_file = open("{}/{}_log.log".format(folder_name, folder_name), 'w') # file in which we will record all progress, log file
                log_file.close()
                
                summary = open("{}/Summary.txt".format(folder_name), 'w') 
                summary.close()

                lbl2.configure(text = "Status : Running")
                for i in range(0, sheet.nrows):
                        bar['value'] = int((1 + i) * 100 / sheet.nrows)
                        protein_name = str(sheet.cell_value(i,0))
                        sequence = str(sheet.cell_value(i,1))

                        log_file = open("{}/{}_log.log".format(folder_name, folder_name), 'a+') # file in which we will record all progress, log file
                        log_file.write("{}      {}      ".format(i + 1, protein_name))
                        info_txt.insert(INSERT, "{}) {} : Started\n".format(i+1, protein_name))

                        summary = open("{}/Summary.txt".format(folder_name), 'a+') 
                        
                        check = create_files_per_protein(protein_name, sequence, log_file, summary, True, i) #final_sheet, 
                        if(check[0] != 0):
                                info_txt.insert(INSERT, "Error {}:\n{}\n{}) {} : Trying again\n".format(check[0], check[1], i+1, protein_name))
                                log_file.write("Trying again\n")

                                check = create_files_per_protein(protein_name, sequence, log_file, summary, False, i) #final_sheet, 
                                if(check[0] == 1):
                                        info_txt.insert(INSERT, "Problem with BLAST: {}\n".format(check[1]))
                                        
                                        summary.write("{}\tProblem with BLAST: {}\n".format(protein_name, check[1])) ###
                                        
                                        info_txt.insert(INSERT, "{}) {} : Aborted\n-------------------------------------\n".format(i+1, protein_name))
                                        log_file.write("Aborted\n")
                                        
                                elif(check[0] == 2):
                                        info_txt.insert(INSERT, "No relevant hits found: {}\n".format(check[1]))

                                        summary.write("{}\tNo relevant hits found: {}\n".format(protein_name, check[1])) ###
                                        
                                        info_txt.insert(INSERT, "{}) {} : Aborted\n-------------------------------------\n".format(i+1, protein_name))
                                        log_file.write("Aborted\n")

                                elif(check[0] == 3):
                                        info_txt.insert(INSERT, "Problem with reading .aln file: {}\n".format(check[1]))

                                        summary.write("{}\tProblem with reading .aln file: {}\n".format(protein_name, check[1])) ###
                                        
                                        info_txt.insert(INSERT, "{}) {} : Aborted\n-------------------------------------\n".format(i+1, protein_name))
                                        log_file.write("Aborted\n")

                                else:
                                        info_txt.insert(INSERT, "{}) {} : Finished\n-------------------------------------\n".format(i+1, protein_name))
                        else:
                                info_txt.insert(INSERT, "{}) {} : Finished\n-------------------------------------\n".format(i+1, protein_name))
                                
                        log_file.close()
                        summary.close()
                        row_count += 1

                lbl2.configure(text = "Status : Finished")
                new_button.configure(state = NORMAL)

        def kill(self): 
                self.killed = True

class TestThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                global folder_name
                try:
                        see = os.path.abspath(os.path.dirname(sys.argv[0]))
                        path = (see + "\\" + folder_name + "\\").replace("/", "\\")
                        os.startfile(path) ###for windows only! ####test
                        ####subprocess.call("nautilus -- {}".format(path), shell = True) ### for linux
                        return
                except Exception as e:
                        return

monkeys_file = "Primates.xlsx"
book1 = xlrd.open_workbook(monkeys_file)
sheet1 = book1.sheet_by_index(0)

monkey_list = []

row_count = 1

for i in range(sheet1.nrows):
	monkey_list.append(sheet1.cell_value(i, 0).split()[0])
book1.release_resources()

def ReadExcel():
        excel_file = lbl1['text']
        book = xlrd.open_workbook(excel_file)
        sheet = book.sheet_by_index(0)
        book.release_resources()
        return sheet

def CreateFolders(sheet):
        global folder_path
        global folder_name
        folder_name = lbl1['text']
        temp = folder_name.split('.')
        temp = temp[0].split('/')
        folder_name = temp[len(temp) - 1]
        folder_path = "/".join(temp) + "/"

        if(not path.exists(folder_name)):
                os.mkdir(folder_name)
        if(not path.exists("{}/hits".format(folder_name))):
                os.mkdir("{}/hits".format(folder_name))
                os.mkdir("{}/hits/primate_hits".format(folder_name))

def activate_blast(protein_name, sequence):
        max_seq_num = combo1.get()
        #print(max_seq_num)
        #t0 = time.time() ########test
        result_handle = NCBIWWW.qblast("blastp", "nr", sequence, hitlist_size = int(max_seq_num), entrez_query = \
"Mammalia[ALL] NOT (humans[ALL] OR 'Homo sapiens'[ALL])") #######change sequence!
        #t1 = time.time() ########test
        #print("blast: {}".format(t1 - t0)) ######test
        
        file_name = "{}/{}.xml".format(folder_name, protein_name)
        with open("{}/{}.xml".format(folder_name, protein_name), "w") as out_handle:
                out_handle.write(result_handle.read())
        result_handle.close()
        out_handle.close()

def create_files_per_protein(protein_name, sequence, log_file, summary, write_error, protein_index): #, final_sheet
        global row_count
        global folder_name
        
        try:
                activate_blast(protein_name, sequence)
        except Exception as e:
                """
                if(write_error == True):
                        final_sheet.write(row_count, 1, str(e))
                """
                log_file.write("Error while using blast: {}\n".format(str(e)))
                return [1, str(e)]
        
                
        blast_qresult = SearchIO.read("{}/{}.xml".format(folder_name, protein_name), "blast-xml")
        
        query_sec = SeqRecord(Seq(sequence), "query_seq") #try this

        record = []

        record.append(query_sec)

        for hit in blast_qresult:
                if len(hit) == 1:
                        identity = 100.0 * hit[0].ident_num / len(sequence)
                        if identity > int(combo2.get()): ###80.0
                                if "homo sapiens" in hit[0].hit.description.lower(): #we exclude humans
                                        pass
                                elif "multispecies" in hit[0].hit.description.lower(): #we exclude multispecies (bacteria)
                                        pass
                                elif "hypothetical protein" in hit[0].hit.description.lower():
                                        pass
                                else:
                                        record.append(hit[0].hit)
        if len(record) == 1: ##### if no hits are left, end program for current protein  
                log_file.write("No relevant orthologs returned by blast\n")
                return [2, "No relevant orthologs returned by blast"]

        

        protein_dict = {}
        for protein in record:
                protein_dict[protein.id] = protein.description # { id : description }
        
        SeqIO.write(record, "{}/{}.faa".format(folder_name, protein_name), "fasta") # write records to fasta file
        
        activate_muscle(protein_name)
        
        
        
        alignment = []
        
        try:
                alignment = AlignIO.read("{}/{}.aln".format(folder_name, protein_name), "clustal")
        except Exception as e:
                log_file.write("Error while opening .aln file\n")
                return [3, str(e)]

        stat_file = open("{}/{}_stat.txt".format(folder_name, protein_name), 'w') # file in which we will write all our statistics

        stat_file.write("{}\n{}\n".format(protein_name, sequence)) # write first the protein name and the sequence into the stat file
        
        original_c_list = find_C(sequence) # find locations of Cys on the original query sequence (with no gaps)
        if sequence[0] != "M":
                original_c_list = [i + 1 for i in original_c_list]

        stat_file.write("Locations of Cys in original query sequence: ")
        if len(original_c_list) == 0:
                stat_file.write("None") # in case we found no Cys

        for i, c in enumerate(original_c_list):
                
                stat_file.write("%s" % c)
                
                if i == len(original_c_list) - 1:
                        stat_file.write(".")
                else:
                        stat_file.write(", ")
        stat_file.write("\n\n")

        c_list = find_C(next(i for i in alignment if i.id == "query_seq").seq) # find locations of Cys on the aligned query sequence (with gaps)
        count_list = [0] * len(c_list)
        protein_matrix = []

        for i in range(len(c_list)):
                protein_list = []
                for protein in alignment:
                        if protein.id == "query_seq":
                                continue

                        if protein.seq[c_list[i]] == "C":
                                count_list[i] += 1
                                protein_list.append(protein.id)
                        

                protein_matrix.append(protein_list)

        text = "Cys {}: {} % identical, ({} / {})\n"

        for j in range(len(count_list)):
                stat_file.write(text.format(original_c_list[j], round(count_list[j] * 100.0 / (len(alignment)-1), 1), count_list[j], len(alignment)-1))


        suspect = False
        monkey_suspect = False
        special_suspect = False
        monkey_suspect_list = []

        for j in range(len(count_list)):
                if round(count_list[j] * 100.0 / (len(alignment)-1), 1) < int(combo4.get()):
                        suspect = True
                        is_monkey, percentage, monkey_count, length = Check_Monkey([protein_dict[i] for i in protein_matrix[j]])
                        if is_monkey or len(protein_matrix[j]) < 6:
                                monkey_suspect = True
                                monkey_suspect_list.append(str(original_c_list[j]))
                        
                        stat_file.write("\n########################################Cys {}: {} % are primates ({}/{})########################################\n\n".format(original_c_list[j], percentage, monkey_count, length))

                        for protein_id in protein_matrix[j]:
                                stat_file.write("{}\n".format(protein_dict[protein_id]))

        stat_file.close()

        if suspect:
                shutil.copyfile("{}/{}_stat.txt".format(folder_name, protein_name), "{}/hits/{}_stat.txt".format(folder_name, protein_name))

        if monkey_suspect:
                shutil.copyfile("{}/{}_stat.txt".format(folder_name, protein_name), "{}/hits/primate_hits/{}_stat.txt".format(folder_name, protein_name))
                summary.write("{}\t{}\n".format(protein_name, ",".join(monkey_suspect_list)) )
        else:
                summary.write("{}\n".format(protein_name))

        os.remove("{}/{}.xml".format(folder_name, protein_name)) #erase unneccesary files
        os.remove("{}/{}.faa".format(folder_name, protein_name))
        os.remove("{}/{}.aln".format(folder_name, protein_name))
        log_file.write("Finished\n")
        return [0, "Finished"]

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()




