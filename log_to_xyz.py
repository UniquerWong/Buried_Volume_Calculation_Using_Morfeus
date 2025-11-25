# log_to_xyz.py
# 作用：将当前文件夹下所有 .log 文件转换成同名 .xyz 文件（自动识别全部元素）

import os

# 全元素周期表（1-118）
PERIODIC_TABLE = {
    1: 'H', 2: 'He',
    3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
    11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar',
    19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe',
    27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se',
    35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo',
    43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
    51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce',
    59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy',
    67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W',
    75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb',
    83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th',
    91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf',
    99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
    106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn',
    113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'
}

def extract_xyz_from_log(logfile):
    """从 Gaussian log 中提取 Input orientation 坐标"""
    with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    atoms = []
    for i, line in enumerate(lines):
        if "Input orientation:" in line:
            atoms = []
            for j in range(i + 5, len(lines)):
                if '-----' in lines[j]:
                    break
                parts = lines[j].split()
                if len(parts) < 6:
                    continue
                atomic_num = int(parts[1])
                x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                atom = PERIODIC_TABLE.get(atomic_num, str(atomic_num))
                atoms.append((atom, x, y, z))
    return atoms

def write_xyz(atoms, xyzfile):
    """写 xyz 文件"""
    with open(xyzfile, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write("Generated from Gaussian log file\n")
        for atom, x, y, z in atoms:
            f.write(f"{atom:<3} {x:>12.6f} {y:>12.6f} {z:>12.6f}\n")

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))  # 脚本所在文件夹
    log_files = [f for f in os.listdir(current_folder) if f.lower().endswith('.log')]

    if not log_files:
        print("当前文件夹没有 .log 文件")
    else:
        for log in log_files:
            log_path = os.path.join(current_folder, log)
            xyz_path = os.path.join(current_folder, os.path.splitext(log)[0] + ".xyz")
            atoms = extract_xyz_from_log(log_path)
            if atoms:
                write_xyz(atoms, xyz_path)
                print(f"已处理：{log} -> {os.path.basename(xyz_path)}")
            else:
                print(f" 未在 {log} 中找到坐标")

