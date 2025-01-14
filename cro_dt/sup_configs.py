import sys
sys.path.append(".")

import csv
import pdb

import numpy as np

config_BC = {
    "code": "breast_cancer",
    "name": "Breast cancer",
    "filepath": "datasets/breast-cancer-wisconsin.data",
    "n_attributes": 9,
    "attributes": [
        "Clump Thickness", "Uniformity of Cell Size", "Uniformity of Cell Shape",
        "Marginal Adhesion", "Single Epithelial Cell Size", "Bare Nuclei",
        "Bland Chromatin", "Normal Nucleoli", "Mitoses"],
    "n_classes": 2,
    "classes": [(2, "Benign"), (4, "Malignant")]
}

config_CE = {
    "code": "car",
    "name": "Car evaluation",
    "filepath": "datasets/car.data",
    "n_attributes": 6,
    "attributes": ["buying", "maint", "doors", "persons", "lug_boot", "safety"],
    "n_classes": 4,
    "classes": [(0, "Unacceptable"), (1, "Acceptable"), (2, "Good"), (3, "Very good")]
}

config_BN = {
    "code": "banknote",
    "name": "Banknote authentication",
    "filepath": "datasets/data_banknote_authentication.txt",
    "n_attributes": 4,
    "attributes": ["variance", "skewness", "curtosis", "entropy"],
    "n_classes": 4,
    "classes": [(0, "Authentic"), (1, "Forged")]
}

config_BS = {
    "code": "balance",
    "name": "Balance scale",
    "filepath": "datasets/balance-scale.data",
    "n_attributes": 4,
    "attributes": ["left weight", "left distance", "right weight", "right distance"],
    "n_classes": 3,
    "classes": [(0, "Left"), (1, "Balanced"), (2, "Right")]
}

config_AI1 = {
    "code": "acute-1",
    "name": "Acute inflammations 1",
    "filepath": "datasets/acute-inflammations-1.data",
    "n_attributes": 6,
    "attributes": ["temperature", "nausea", "lumbar pain", "urine pushing", "micturition", "burning urethra"],
    "n_classes": 2,
    "classes": [(0, "No inflammation"), (1, "Inflammation")]
}

config_AI2 = {
    "code": "acute-2",
    "name": "Acute inflammations 2",
    "filepath": "datasets/acute-inflammations-2.data",
    "n_attributes": 6,
    "attributes": ["temperature", "nausea", "lumbar pain", "urine pushing", "micturition", "burning urethra"],
    "n_classes": 2,
    "classes": [(0, "No nephritis"), (1, "Nephritis")]
}

config_BT = {
    "code": "transfusion",
    "name": "Blood transfusion",
    "filepath": "datasets/blood-transfusion.data",
    "n_attributes": 4,
    "attributes": ["recency", "frequency", "monetary", "time"],
    "n_classes": 2,
    "classes": [(0, "Not donor"), (1, "Donor")]
}

config_CC = {
    "code": "climate",
    "name": "Climate model crashes",
    "filepath": "datasets/climate-crashes.data",
    "n_attributes": 18,
    "attributes": ["vconst_corr", "vconst_2", "vconst_3", "vconst_4", "vconst_5", "vconst_7", "ah_corr", "ah_bolus",
                   "slm_corr", "efficiency_factor", "tidal_mix_max", "vertical_decay_scale", "convect_corr",
                   "bckgrnd_vdc1", "bckgrnd_vdc_ban", "bckgrnd_vdc_eq", "bckgrnd_vdc_psim", "Prandtl"],
    "n_classes": 2,
    "classes": [(0, "Failure"), (1, "Success")]
}

config_CB = {
    "code": "sonar",
    "name": "Connectionist bench sonar",
    "filepath": "datasets/sonar.all-data",
    "n_attributes": 60,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15",
                   "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29",
                   "x30", "x31", "x32", "x33", "x34", "x35", "x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43",
                   "x44", "x45", "x46", "x47", "x48", "x49", "x50", "x51", "x52", "x53", "x54", "x55", "x56", "x57",
                   "x58", "x59", "x60"],
    "n_classes": 2,
    "classes": [(0, "Rock"), (1, "Mine")]
}

config_OC = {
    "code": "optical",
    "name": "Optical recognition",
    "filepath": "datasets/optdigits.tra",
    "n_attributes": 64,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15",
                   "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29",
                   "x30", "x31", "x32", "x33", "x34", "x35", "x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43",
                   "x44", "x45", "x46", "x47", "x48", "x49", "x50", "x51", "x52", "x53", "x54", "x55", "x56", "x57",
                   "x58", "x59", "x60", "x61", "x62", "x63", "x64"],
    "n_classes": 10,
    "classes": [(0, "Number 0"), (1, "Number 1"), (2, "Number 2"), (3, "Number 3"), (4, "Number 4"), (5, "Number 5"),
                (6, "Number 6"), (7, "Number 7"), (8, "Number 8"), (9, "Number 9")]
}

config_DB = {
    "code": "drybean",
    "name": "Drybeans",
    "filepath": "datasets/drybean_data.txt",
    "n_attributes": 16,
    "attributes": ["Area", "Perimeter", "MajorAxisLength", "MinorAxisLength", "AspectRation", "Eccentricity",
                   "ConvexArea", "EquivDiameter", "Extent", "Solidity", "roundness", "Compactness", "ShapeFactor1",
                   "ShapeFactor2", "ShapeFactor3", "ShapeFactor4"],
    "n_classes": 7,
    "classes": [(0, "Seker"), (1, "Barbunya"), (2, "Bombay"), (3, "Cali"), (4, "Dermosan"), (5, "Horoz"), (6, "Sira")]
}

config_AB = {
    "code": "avila",
    "name": "Avila bible",
    "filepath": "datasets/avila-tr.txt",
    "n_attributes": 10,
    "attributes": ["intercolumnar distance", "upper margin", "lower margin", "exploitation", "row number",
                   "modular ratio", "interlinear spacing", "weight", "peak number",
                   "modular ratio/ interlinear spacing"],
    "n_classes": 12,
    "classes": [(0, "A"), (1, "B"), (2, "C"), (3, "D"), (4, "E"), (5, "F"), (6, "G"), (7, "H"), (8, "I"), (9, "W"),
                (10, "X"), (11, "Y")]
}

config_WQ1 = {
    "code": "wine-red",
    "name": "Wine quality red",
    "filepath": "datasets/winequality-red.csv",
    "n_attributes": 11,
    "attributes": ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides",
                   "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"],
    "n_classes": 6,
    "classes": [(3, "Score 3"), (4, "Score 4"), (5, "Score 5"), (6, "Score 6"), (7, "Score 7"), (8, "Score 8")]
}

config_WQ2 = {
    "code": "wine-white",
    "name": "Wine quality white",
    "filepath": "datasets/winequality-white.csv",
    "n_attributes": 11,
    "attributes": ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides",
                   "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"],
    "n_classes": 7,
    "classes": [(3, "Score 3"), (4, "Score 4"), (5, "Score 5"), (6, "Score 6"), (7, "Score 7"), (8, "Score 8"),
                (9, "Score 9")]
}

config_ART1 = {
    "code": "artificial_100_3_2",
    "name": "Artificial N=100, C=3, P=2",
    "filepath": "datasets/artificial/scikit_N-100_C-3_P-2.csv",
    "n_attributes": 2,
    "attributes": ["x1", "x2"],
    "n_classes": 3,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2")]
}

config_ART2 = {
    "code": "artificial_1000_3_2",
    "name": "Artificial N=1000, C=3, P=2",
    "filepath": "datasets/artificial/scikit_N-1000_C-3_P-2.csv",
    "n_attributes": 2,
    "attributes": ["x1", "x2"],
    "n_classes": 3,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2")]
}

config_ART3 = {
    "code": "artificial_1000_3_10",
    "name": "Artificial N=1000, C=3, P=10",
    "filepath": "datasets/artificial/scikit_N-1000_C-3_P-10.csv",
    "n_attributes": 10,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"],
    "n_classes": 3,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2")]
}

config_ART4 = {
    "code": "artificial_1000_10_10",
    "name": "Artificial N=1000, C=10, P=10",
    "filepath": "datasets/artificial/scikit_N-1000_C-10_P-10.csv",
    "n_attributes": 10,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"],
    "n_classes": 10,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2"), (3, "Class 3"), (4, "Class 4"), (5, "Class 5"),
                (6, "Class 6"), (7, "Class 7"), (8, "Class 8"), (9, "Class 9")]
}

config_ART5 = {
    "code": "artificial_10000_3_2",
    "name": "Artificial N=10000, C=3, P=2",
    "filepath": "datasets/artificial/scikit_N-10000_C-3_P-2.csv",
    "n_attributes": 2,
    "attributes": ["x1", "x2"],
    "n_classes": 3,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2")]
}

config_ART6 = {
    "code": "artificial_10000_3_10",
    "name": "Artificial N=10000, C=3, P=10",
    "filepath": "datasets/artificial/scikit_N-10000_C-3_P-10.csv",
    "n_attributes": 10,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"],
    "n_classes": 3,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2")]
}

config_ART7 = {
    "code": "artificial_100000_10_10",
    "name": "Artificial N=100000, C=10, P=10",
    "filepath": "datasets/artificial/scikit_N-100000_C-10_P-10.csv",
    "n_attributes": 10,
    "attributes": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"],
    "n_classes": 10,
    "classes": [(0, "Class 0"), (1, "Class 1"), (2, "Class 2"), (3, "Class 3"), (4, "Class 4"), (5, "Class 5"),
                (6, "Class 6"), (7, "Class 7"), (8, "Class 8"), (9, "Class 9")]
}

real_dataset_list = ["breast_cancer", "car", "banknote", "balance", "acute-1", "acute-2", "transfusion", "climate",
                     "sonar", "optical", "drybean", "avila", "wine-red", "wine-white"]
artificial_dataset_list = ["artificial_100_3_2", "artificial_1000_3_2", "artificial_1000_3_10", "artificial_1000_10_10",
                           "artificial_10000_3_2", "artificial_10000_3_10", "artificial_100000_10_10"]


def get_config(dataset_code):
    for config in [config_BC, config_CE, config_BN, config_BS,
                   config_AI1, config_AI2, config_BT, config_CC, config_CB,
                   config_OC, config_AB, config_DB, config_WQ1, config_WQ2,
                   config_ART1, config_ART2, config_ART3, config_ART4,
                   config_ART5, config_ART6, config_ART7]:

        if config["code"] == dataset_code:
            return config

    raise Exception(f"Invalid dataset code {dataset_code}.")


def load_dataset(config):
    try:
        Xy = np.loadtxt(open(config["filepath"], "r"), delimiter=",")
    except:
        pdb.set_trace()
    X = Xy[:, :-1]
    y = Xy[:, -1]
    y = [[i for i, (c, _) in enumerate(config["classes"]) if c == y_i][0] for y_i in y]
    return np.array(X), np.array(y)


if __name__ == "__main__":
    pdb.set_trace()