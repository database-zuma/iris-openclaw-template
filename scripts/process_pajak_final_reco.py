import pdfplumber
import pandas as pd
import os
import re

def extract_pajak_items(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
            
            # Extract Global Info
            supplier = "N/A"
            match_sup = re.search(r'Nama\s*:\s*(.*?)\nAlamat', all_text)
            if match_sup:
                supplier = match_sup.group(1).strip()
            
            no_faktur = "N/A"
            match_no = re.search(r'Kode dan Nomor Seri Faktur Pajak:\s*(\d+)', all_text)
            if match_no:
                no_faktur = match_no.group(1).strip()
            
            tgl_faktur = "N/A"
            match_tgl = re.search(r'([A-Z.\s]+),\s+(\d+\s+[A-Za-z]+\s+\d{4})', all_text)
            if match_tgl:
                tgl_faktur = match_tgl.group(2).strip()

            no_ref = "N/A"
            match_ref = re.search(r'\(Referensi:\s*(.*?)\)', all_text)
            if match_ref:
                no_ref = match_ref.group(1).strip()

            # Global Totals for distribution
            dpp_global = 0
            match_dpp = re.search(r'Dasar Pengenaan Pajak\s+([\d.,]+)', all_text)
            if match_dpp:
                dpp_global = float(match_dpp.group(1).replace(".", "").replace(",", "."))
            
            ppn_global = 0
            match_ppn = re.search(r'Jumlah PPN \(Pajak Pertambahan Nilai\)\s+([\d.,]+)', all_text)
            if match_ppn:
                ppn_global = float(match_ppn.group(1).replace(".", "").replace(",", "."))

            # Extract Items
            items = []
            lines = all_text.split("\n")
            
            # Find all item lines
            item_raw_data = []
            for i, line in enumerate(lines):
                match_p_q = re.search(r'Rp\s+([\d.,]+)\s+x\s+([\d.,]+)\s+([A-Za-z]+)', line)
                if match_p_q:
                    price = float(match_p_q.group(1).replace(".", "").replace(",", "."))
                    qty = float(match_p_q.group(2).replace(".", "").replace(",", "."))
                    unit = match_p_q.group(3)
                    item_name = lines[i-1].strip() if i > 0 else "N/A"
                    item_name = re.sub(r'^\d+\s+', '', item_name)
                    item_raw_data.append({"name": item_name, "price": price, "qty": qty, "unit": unit, "subtotal": price * qty})
            
            total_subtotal = sum(d["subtotal"] for d in item_raw_data)
            
            for d in item_raw_data:
                # DPP item = Price per unit * Actual Qty (per Lia's request #1)
                dpp_item = d["price"] * d["qty"]
                # PPN-M remains proportional to the original total for accuracy if possible, 
                # but to be consistent with Lia's calculation:
                ppn_item = dpp_item * 0.11 # Using standard 11% PPN rate
                
                items.append({
                    "SUPPLIER": supplier,
                    "RINCIAN": d["name"],
                    "Satuan": d["unit"],
                    "Tanggal Invoice": tgl_faktur,
                    "NO INVOICE": no_ref,
                    "Tgl Faktur Pajak": tgl_faktur,
                    "No Seri Faktur Pajak": no_faktur,
                    "Harga/ Qty": d["price"],
                    "DPP": dpp_item,
                    "PPN-M": ppn_item,
                    "Jumlah": dpp_item + ppn_item,
                    "QTY_ACTUAL": d["qty"]
                })
            
            return items
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return []

base_dir = "/Users/database-zuma/.openclaw/workspace/temp_pajak/PPNM JAN 2026"
all_items_flat = []
for file in os.listdir(base_dir):
    if file.endswith(".pdf"):
        pdf_items = extract_pajak_items(os.path.join(base_dir, file))
        all_items_flat.extend(pdf_items)

df_results = pd.DataFrame(all_items_flat)

# Load Updated Template (with Sheet2)
template_path = "/Users/database-zuma/.openclaw/workspace/Rekapan_PPNM_Januari_2026_ITEMIZED_UPDATED.xlsx"
xl = pd.ExcelFile(template_path)
df1_template = xl.parse(sheet_name='Sheet1', header=None)
df2_lia = xl.parse(sheet_name='Sheet2', header=None)

headers = df1_template.iloc[1].tolist()
data_rows = []
for _, row in df_results.iterrows():
    new_row = [None] * len(headers)
    for i, h in enumerate(headers):
        if h in row:
            new_row[i] = row[h]
    data_rows.append(new_row)

df1_final = pd.concat([df1_template.iloc[0:2], pd.DataFrame(data_rows)], ignore_index=True)
df1_final["Qty Actual"] = [None, "Qty Actual"] + df_results["QTY_ACTUAL"].tolist()

# Reconciliation logic
df1_agg = df_results.groupby('No Seri Faktur Pajak').agg({'DPP': 'sum', 'PPN-M': 'sum'}).reset_index()
df2_data = df2_lia.iloc[2:].copy()
df2_data.columns = df2_lia.iloc[1]
df2_data['NOMOR FP'] = df2_data['NOMOR FP'].astype(str).str.strip()
df2_data['DPP_LIA'] = pd.to_numeric(df2_data['Harga Jual/Penggantian/DPP'], errors='coerce').fillna(0) + pd.to_numeric(df2_data['DPP Nilai Lain/DPP'], errors='coerce').fillna(0)
df2_data['PPN_LIA'] = pd.to_numeric(df2_data['PPN'], errors='coerce').fillna(0)

# 1. Missing in Sheet 1
fakturs_df1 = set(df1_agg['No Seri Faktur Pajak'])
fakturs_df2 = set(df2_data['NOMOR FP'])
missing_in_s1 = df2_data[df2_data['NOMOR FP'].isin(fakturs_df2 - fakturs_df1)][['NAMA', 'NOMOR FP', 'DPP_LIA', 'PPN_LIA']]

# Update DPP_LIA to use only 'Harga Jual/Penggantian/DPP' per Lia's request
df2_data['DPP_LIA'] = pd.to_numeric(df2_data['Harga Jual/Penggantian/DPP'], errors='coerce').fillna(0)
# Note: PPN remains the same
merged = pd.merge(df1_agg, df2_data, left_on='No Seri Faktur Pajak', right_on='NOMOR FP')
merged['Diff_DPP'] = merged['DPP'] - merged['DPP_LIA']
merged['Diff_PPN'] = merged['PPN-M'] - merged['PPN_LIA']
mismatches = merged[(merged['Diff_DPP'].abs() > 2) | (merged['Diff_PPN'].abs() > 2)][['NOMOR FP', 'DPP', 'DPP_LIA', 'Diff_DPP', 'PPN-M', 'PPN_LIA', 'Diff_PPN']]

# Create Reconciliation Sheet
reco_data = [
    ["RINGKASAN REKONSILIASI", "", "", ""],
    ["Keterangan", "Sheet 1 (Iris)", "Sheet 2 (Sistem Pajak)", "Selisih"],
    ["Total DPP", df1_agg['DPP'].sum(), df2_data['DPP_LIA'].sum(), df1_agg['DPP'].sum() - df2_data['DPP_LIA'].sum()],
    ["Total PPN", df1_agg['PPN-M'].sum(), df2_data['PPN_LIA'].sum(), df1_agg['PPN-M'].sum() - df2_data['PPN_LIA'].sum()],
    ["", "", "", ""],
    ["FAKTUR DI SISTEM TAPI TIDAK ADA DI PDF (FILE ZIP)", "", "", ""]
]
reco_df_header = pd.DataFrame(reco_data)
reco_df_missing = missing_in_s1.copy()
reco_df_mismatch_title = pd.DataFrame([["", "", "", ""], ["PERBEDAAN NILAI (DATA PDF VS SISTEM)", "", "", ""]])
reco_df_mismatch = mismatches.copy()

# Writing to Excel
output_path = "/Users/database-zuma/.openclaw/workspace/Rekapan_PPNM_Januari_2026_FINAL_RECO.xlsx"
with pd.ExcelWriter(output_path) as writer:
    df1_final.to_excel(writer, sheet_name='Rekapan_Iris', index=False, header=False)
    df2_lia.to_excel(writer, sheet_name='Data_Sistem_Lia', index=False, header=False)
    # Reconcile sheet
    reco_df_header.to_excel(writer, sheet_name='Reconsiliasi', index=False, header=False, startrow=0)
    missing_in_s1.to_excel(writer, sheet_name='Reconsiliasi', index=False, startrow=len(reco_data))
    reco_df_mismatch_title.to_excel(writer, sheet_name='Reconsiliasi', index=False, header=False, startrow=len(reco_data) + len(missing_in_s1) + 1)
    mismatches.to_excel(writer, sheet_name='Reconsiliasi', index=False, startrow=len(reco_data) + len(missing_in_s1) + 4)

print(f"DONE: {output_path}")
