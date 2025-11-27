# xyz_Vbur_BiteAngle_combined_fixed2.py
import os
import csv
from morfeus import BuriedVolume, BiteAngle, read_xyz

# 配置
FOLDER_PATH = "."  # 放 xyz 文件的文件夹
OUTPUT_CSV = "combined_vbur_biteangle_results.csv"

# 需要计算 buried volume 的球半径
RADII = [3.0, 4.0, 5.0]

# 所有金属元素（用于 donor 判断：金属 = 潜在 donor）
METALS_ALL = {"Pd", "Pt", "Ni", "Co", "Rh", "Ir", "Fe", "Cu", "Zn", "Au", "Ag"}

# 优先作为“配位中心金属”的元素（排除配体金属，例如常见的 Fe-茂体系）
# 可以根据你的体系自己再增删
CENTER_METALS = {"Pd", "Pt", "Ni", "Co", "Rh", "Ir", "Cu", "Zn", "Au", "Ag"}

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

    # === 自动识别配位中心金属原子索引（1-based） ===
    # 1. 优先在 CENTER_METALS 中寻找（Ir、Rh、Pd、Pt 等）
    primary_candidates = [i + 1 for i, e in enumerate(elements) if e in CENTER_METALS]

    # 2. 如果找不到，在所有金属中寻找（包括 Fe）
    if primary_candidates:
        metal_idx_1b = primary_candidates[0]
    else:
        all_metal_candidates = [i + 1 for i, e in enumerate(elements) if e in METALS_ALL]
        if not all_metal_candidates:
            print(f"{file_name} 中未找到金属元素 {METALS_ALL}，跳过该结构")
            continue
        metal_idx_1b = all_metal_candidates[0]

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
    # donor 自动选：除中心金属原子外，前两个“非金属”原子
    donor_indices = [
        i + 1
        for i, e in enumerate(elements)
        if (i + 1) != metal_idx_1b and e not in METALS_ALL
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
            f"Metal idx = {metal_idx_1b}, Donors = ({donor1_idx}, {donor2_idx}), "
            f"Bite Angle = {angle}, Inverted = {inverted}"
        )

    rows.append(row)

# === 3. 写出到一个 CSV ===
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"所有计算完成，结果已保存到 {OUTPUT_CSV}")
