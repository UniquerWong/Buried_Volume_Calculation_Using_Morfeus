# xyz_Vbur_BiteAngle_combined.py
import os
import csv
from morfeus import BuriedVolume, BiteAngle, read_xyz

# 配置
FOLDER_PATH = "."  # 放 xyz 文件的文件夹
OUTPUT_CSV = "combined_vbur_biteangle_results.csv"

# 需要计算 buried volume 的球半径
RADII = [3.0, 4.0, 5.0]

# 金属元素列表（用于自动识别 donor 原子：前两个“非金属”当作 donor）
METALS = {"Pd", "Pt", "Ni", "Co", "Rh", "Ir", "Fe", "Cu", "Zn", "Au", "Ag"}

# 构建 CSV 表头
headers = ["File"]
for r in RADII:
    headers += [
        f"V_bur (%) - {r}",
        f"Buried Volume - {r}",
        f"Free Volume - {r}",
        f"Distal Volume - {r}",
    ]
headers += ["Bite Angle", "Inverted"]

rows = []

for file_name in sorted(os.listdir(FOLDER_PATH)):
    if not file_name.lower().endswith(".xyz"):
        continue

    xyz_path = os.path.join(FOLDER_PATH, file_name)
    try:
        elements, coordinates = read_xyz(xyz_path)
        n_atoms = len(elements)
        if n_atoms == 0:
            print(f"{file_name} 原子数为 0，跳过")
            continue
    except Exception as e:
        print(f"读取 {file_name} 失败: {e}")
        continue

    # 默认金属是最后一个原子（1-based 索引）
    metal_idx_1b = n_atoms

    row = {"File": file_name}

    # === 1. 计算 Buried Volume / %Vbur 等 ===
    for r in RADII:
        try:
            bv = BuriedVolume(elements, coordinates, metal_idx_1b, radius=r)
        except Exception as e:
            print(f"BuriedVolume 初始化失败 {file_name}, radius={r}: {e}")
            row[f"V_bur (%) - {r}"] = None
            row[f"Buried Volume - {r}"] = None
            row[f"Free Volume - {r}"] = None
            row[f"Distal Volume - {r}"] = None
            continue

        # %Vbur
        try:
            vbur_pct = bv.fraction_buried_volume * 100.0
        except Exception:
            vbur_pct = None
        row[f"V_bur (%) - {r}"] = vbur_pct

        # 其他体积
        row[f"Buried Volume - {r}"] = getattr(bv, "buried_volume", None)
        row[f"Free Volume - {r}"] = getattr(bv, "free_volume", None)

        dist_val = getattr(bv, "distal_volume", None)
        if dist_val is None:
            try:
                bv.compute_distal_volume(method="buried_volume")
                dist_val = getattr(bv, "distal_volume", None)
            except Exception:
                dist_val = None
        row[f"Distal Volume - {r}"] = dist_val

    # === 2. 计算 Bite Angle ===
    # donor 自动选：除最后一个金属以外，前两个“非金属”原子
    donor_indices = [
        i + 1
        for i, e in enumerate(elements[:-1])  # 排除最后一个（假定是金属）
        if e not in METALS
    ]

    if len(donor_indices) < 2:
        print(f"{file_name} 找不到足够的非金属原子作为 donor，Bite Angle 记为 None")
        row["Bite Angle"] = None
        row["Inverted"] = None
    else:
        donor1_idx, donor2_idx = donor_indices[:2]
        try:
            ba = BiteAngle(coordinates, metal_idx_1b, donor1_idx, donor2_idx)
            angle = ba.angle
            inverted = getattr(ba, "inverted", False)
        except Exception as e:
            print(f"{file_name} BiteAngle 计算失败: {e}")
            angle = None
            inverted = None

        row["Bite Angle"] = angle
        row["Inverted"] = inverted
        print(
            f"{file_name} 计算完成，"
            f"Bite Angle = {angle}, Inverted = {inverted}"
        )

    rows.append(row)

# === 3. 写出到一个 CSV ===
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"所有计算完成，结果已保存到 {OUTPUT_CSV}")

