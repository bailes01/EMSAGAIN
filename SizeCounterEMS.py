import csv
from os import error, getcwd
import re
import shutil
from collections import Counter
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import DISABLED, NORMAL, messagebox


class SizeCounter:
    SHOE_SIZES = [
        "Junior 1 - EU 32",
        "Junior 2 - EU 33",
        "Junior 3 - EU 34",
        "Adult 4 - 3XS - EU 35/36",
        "Adult 5 - 2XS - EU 36/37",
        "Adult 6 - XS - EU 38",
        "Adult 7 - S - EU 39/40",
        "Adult 8 - M - EU 40/41",
        "Adult 9 - L - EU 41/42",
        "Adult 10 - XL - EU 43",
        "Adult 11 - 2XL - EU 44/45",
        "Adult 12 - 3XL - EU 45/46",
        "Adult 13 - 4XL - EU 47",
        "Adult 14 - 5XL - EU 48",
    ]

    WETSUIT_SIZES = [
        "0 - XXS - Mens 26 - Womens 4-6",
        "1- XS - Mens 28 - Womens 6-8",
        "2 - S - Mens 30 - Womens 8-10",
        "3 - M - Mens 32 - Womens 10-12",
        "4 - L - Mens 34 - Womens 12-14",
        "5 - XL - Mens 36 - Womens 14-16",
        "6 - 2XL - Mens 38 - Womens 16-18",
        "7 - 3XL - Mens 40 - Womens 18-20",
        "8 - 4XL - Mens 42 - Womens 20-22",
        "9 - 5XL - Mens 44 - Womens 22-24",
        "4 - Junior - Height 110 cm - Waist 57 cm",
        "6 - Junior - Height 120 cm - Waist 60 cm",
        "8 - Junior - Height 130 cm - Waist 62.5 cm",
        "10 - Junior - Height 140 cm - Waist 65 cm",
        "12 - Junior - Height 150 cm - Waist 67.5 cm",
        "14 - Junior - Height 160 cm - Waist 70 cm",
    ]
    BRINGING_OWN_WETSUIT = "I will bring my own wetsuit"
    BRINGING_OWN_FINS = "I will bring my own fins"
    SIZE_ISSUE_WETSUIT = "My clothes size is larger or smaller than above sizing please contact me to discuss"
    # SIZE_ISSUE_FINS = ""

    def __init__(self, input_dir, output_dir="./manifest.csv"):
        self.used_sizes = {}
        self.raw_data = []
        self.to_count = []
        self.sizes = {"wetsuit": self.WETSUIT_SIZES, "shoe": self.SHOE_SIZES}
        self.data = {}
        self.by_time = {}
        self.max_counts = {}
        self.data_length = 0
        self.size_issue = {"wetsuit": [], "shoe": []}
        self.bringing_own = {"wetsuit": [], "shoe": []}
        self.others = {"wetsuit": [], "shoe": []}
        self.output_dir = output_dir
        with open(input_dir, "r", errors="ignore") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                if row != []:
                    self.raw_data.append(row)

        # self.by_time = self.getByTime()

    def find_data(self):
        self.columns = self.raw_data.pop(0)
        for column, value in enumerate(self.columns):
            if "name" in self.columns[column].lower():
                self.data["name"] = [row[column] for row in self.raw_data]

            if "wetsuit" in self.columns[column].lower():
                self.data["wetsuit"] = [row[column] for row in self.raw_data]
                if not self.check_empty(self.data["wetsuit"]):
                    self.to_count.append("wetsuit")
            if (
                "shoe" in self.columns[column].lower()
                or "fin" in self.columns[column].lower()
            ):
                self.data["shoe"] = [row[column] for row in self.raw_data]
                if not self.check_empty(self.data["wetsuit"]):
                    self.to_count.append("shoe")

            if "session" in self.columns[column].lower():
                self.data["time"] = [row[column] for row in self.raw_data]

    def check_empty(self, list_):
        return all([row == "" for row in list_])

    def find_exceptions(self):
        for row in range(self.data_length):
            if "wetsuit" in self.to_count:
                if self.data["wetsuit"][row] == self.BRINGING_OWN_WETSUIT:
                    self.bringing_own["wetsuit"].append(self.data["name"][row])
                if self.data["wetsuit"][row] == self.SIZE_ISSUE_WETSUIT:
                    self.size_issue["wetsuit"].append(self.data["name"][row])
                if self.data["wetsuit"][row] not in self.WETSUIT_SIZES + [
                    self.BRINGING_OWN_WETSUIT,
                    self.SIZE_ISSUE_WETSUIT,
                    "",
                ]:
                    print("Excluding '" + self.data["wetsuit"][row] + "'")
                    self.others["wetsuit"].append(self.data["name"][row])
                    self.data["wetsuit"][row] = ""
            if "shoe" in self.to_count:
                if self.data["shoe"][row] == self.BRINGING_OWN_FINS:
                    self.bringing_own["shoe"].append(self.data["name"][row])
                # if self.data["shoe"][row] == self.SIZE_ISSUE_FINS:
                #     self.fin_size_issue.append(self.data["name"][row])
                if self.data["shoe"][row] not in self.SHOE_SIZES + [
                    self.BRINGING_OWN_FINS,
                    "",
                    # self.SIZE_ISSUE_FINS
                ]:
                    print("Excluding '" + self.data["shoe"][row] + "'")
                    self.others["shoe"].append(self.data["name"][row])
                    self.data["shoe"][row] = ""

    def validate_dict(self):
        data_length_set = set([len(self.data[key]) for key in self.data.keys()])
        self.data_length = list(data_length_set)[0]
        if len(data_length_set) == 1:
            print(
                "Dict valid: "
                + str(list(self.data.keys()))
                + ", counting: "
                + str(self.to_count)
            )
            return "Valid"
        else:
            raise error("DATA NOT CORRECT")

    def sort_by_time(self):
        group_c = 0
        time = self.data["time"][0]
        self.by_time = {item: {group_c: []} for item in self.to_count}
        for row in range(self.data_length):
            if self.data["time"][row] == time or self.data["time"][row] == "":
                if "shoe" in self.to_count:
                    self.by_time["shoe"][group_c].append(self.data["shoe"][row])
                if "wetsuit" in self.to_count:
                    self.by_time["wetsuit"][group_c].append(self.data["wetsuit"][row])
            else:
                time = self.data["time"][row]
                group_c += 1
                if "wetsuit" in self.to_count:
                    self.by_time["wetsuit"][group_c] = []
                    self.by_time["wetsuit"][group_c].append(self.data["wetsuit"][row])
                if "shoe" in self.to_count:
                    self.by_time["shoe"][group_c] = []
                    self.by_time["shoe"][group_c].append(self.data["shoe"][row])

    def count_gear(self):
        if "wetsuit" in self.to_count:
            self.count_sizes("wetsuit")
        if "shoe" in self.to_count:
            self.count_sizes("shoe")

    def count_sizes(self, key):
        used_sizes = [
            size for size in self.sizes[key] if size in list(set(self.data[key]))
        ]
        self.used_sizes[key] = used_sizes
        counts_by_time = {
            k: dict(Counter(self.by_time[key][k])) for k in self.by_time[key].keys()
        }
        counts_list = list(counts_by_time.values())
        all_counts = {
            k: [d[k] for d in counts_list if k in d.keys()] for k in used_sizes
        }
        self.max_counts[key] = dict(
            sorted(
                {k: max(all_counts[k]) for k in all_counts.keys()}.items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

    def process_data(self):
        self.find_data()
        self.validate_dict()
        self.find_exceptions()
        self.sort_by_time()
        self.count_gear()
        return self.max_counts

    # def merge_multiple(*args):
    #     merged = {"wetsuit": [], "shoe": []}
    #     data = [c for c in args]
    #     for size in SizeCounter.WETSUIT_SIZES:
    #         merged["wetsuit"][size] = []
    #         for dataset in data:
    #             try:
    #                 merged["wetsuit"][size].append(dataset.max_counts["wetsuit"][size])
    #             except KeyError:
    #                 merged["wetsuit"][size].append(0)
    #     for size in SizeCounter.SHOE_SIZES:
    #         merged["shoe"][size] = []
    #         for dataset in data:
    #             try:
    #                 merged["shoe"][size].append(dataset.max_counts["shoe"][size])
    #             except KeyError:
    #                 merged["shoe"][size].append(0)
    #     size_issue = {"wetsuit": [], "shoe": []}
    #     bringing_own = {"wetsuit": [], "shoe": []}
    #     others = {
    #         "wetsuit": [p for p in dataset.others["wetsuit"] for dataset in data],
    #         "shoe": [[p for p in dataset.others["wetsuit"] for dataset in data]],
    #     }
    #     print(others)
    #     print((merged))


class FileIO:
    def __init__(self, *args):
        self.data = [
            {
                "input": arg[0],
                "output": self.gen_output_dir(arg),
                "date": self.get_date(arg[0]),
                "counter": SizeCounter(arg[0]),
            }
            for arg in args
        ]

    def get_date(self, in_dir):
        try:
            return re.search(r"\d{4}-\d{2}-\d{2}", in_dir).group()
        except:
            return "No Date"

    def gen_output_dir(self, arg):
        return arg[1] + "Manifest " + self.get_date(arg[0]) + ".csv"

    def make_copy(self, file):
        shutil.copyfile(file["input"], file["output"])

    # def write_all(self):
    #     data = [file["counter"].process_data() for file in self.data]

    #     formatted = self.format_data(data)
    #     with open("Multiple events.csv", "w", newline="") as f:
    #         writer = csv.writer(f)
    #         writer.writerows(formatted)

    def write_all_seperate(self, include_original=True):
        for file in self.data:
            self.write_single(file=file, include_original=include_original)

    def write_single(self, file=None, include_original=True):
        if file == None:
            file = self.data[0]
        self.make_copy(file)
        formatted = self.format_data(file)
        with open(file["output"], "a" if include_original else "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(formatted)

    def format_data(self, file):
        data = file["counter"].process_data()
        formatted = [[" "], [file["date"]], [" "]]
        for key in data.keys():
            formatted += (
                [[key + " size counts"]]
                + [[size, data[key][size]] for size in file["counter"].used_sizes[key]]
                + [" "]
                + [
                    [
                        f"Bringing own {'fins' if key == 'shoe' else key}",
                        *file["counter"].bringing_own[key],
                    ]
                    if len(file["counter"].bringing_own[key]) != 0
                    else " "
                ]
                + [
                    [
                        f"{key} size issue",
                        *file["counter"].size_issue[key],
                    ]
                    if len(file["counter"].size_issue[key]) != 0
                    else ""
                ]
                + [
                    [
                        f"Unsorted {key} size",
                        *file["counter"].others[key],
                    ]
                    if len(file["counter"].others[key]) != 0
                    else ""
                ]
            )
        for line in formatted:
            print(line)
        return formatted


class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SizeCounterEMS")
        self.separate = tk.IntVar(self.root, 1)
        self.inc_og = tk.IntVar(self.root, 1)
        self.mult = False
        self.file_io = None
        self.browseButton = tk.Button(
            self.root, text="Select Files", command=self.open_file
        )
        self.browseButton.pack()
        self.includeOriginalButton = tk.Checkbutton(
            self.root,
            text="Include Original Spreadsheet",
            variable=self.inc_og,
            onvalue=1,
            offvalue=0,
        )
        self.includeOriginalButton.pack()
        self.separateButton = tk.Checkbutton(
            self.root,
            text="Separate files",
            variable=self.separate,
            onvalue=1,
            offvalue=0,
            command=self.sep_check,
        )
        self.writeButton = tk.Button(
            self.root, text="write to file/s", state=DISABLED, command=self.write
        )
        self.writeButton.pack()
        self.root.mainloop()

    def sep_check(self):
        if self.separate.get() == 0 and self.mult:
            self.inc_og.set(0)
            self.includeOriginalButton.config(state=DISABLED)
        else:
            self.includeOriginalButton.config(state=NORMAL)

    def inc_check(self):
        pass

    def open_file(self):
        files = fd.askopenfilenames(
            parent=self.root, title="Choose a File", initialdir=getcwd()
        )
        self.file_io = FileIO(*files)
        if len(files) > 1:
            self.mult = True
            self.writeButton.pack_forget()
            self.separateButton.pack()
            self.writeButton.pack()
        self.writeButton.config(state=NORMAL)

    def write(self):
        inc_og = True if self.inc_og.get() == 1 else False
        if self.mult:
            if self.separate.get() == 1:
                self.file_io.write_all_seperate(inc_og)
            else:
                self.file_io.write_all()
        else:
            self.file_io.write_single(include_original=inc_og)
        messagebox.showinfo("Done", "New file/s created.")
        self.quit()

    def quit(self):
        self.root.destroy()


if __name__ == "__main__":
    app = AppWindow()
# gogo = FileIO(
#     "gear-sizing-manifest-to-print-2022-01-06 (1).csv",
#     "gear-sizing-manifest-to-print-2022-01-07.csv",
#     "gear-sizing-manifest-to-print-2022-01-08.csv",
#     "gear-sizing-manifest-to-print-2022-01-14.csv",
#     "gear-sizing-manifest-to-print-2022-01-15.csv",
# )
# gogo.write_all()
# counter = SizeCounter("raw/gear-sizing-manifest-to-print-2022-01-06 (1).csv")
# counter.process_data()
def convert(file):
    file_io = FileIO(file)
    file_io.write_single()
