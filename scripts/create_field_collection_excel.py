#!/usr/bin/env python3
"""
scripts/create_field_collection_excel.py
========================================
Generates 'FIELD_COLLECTION_FORM.xlsx' for field researchers.
Includes multi-tab data entry forms with validation rules, formatting,
and clear column guides.
"""

from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_XLSX = PROJECT_ROOT / "FIELD_COLLECTION_FORM.xlsx"

def create_excel_workbook():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    subhead_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    subhead_font = Font(name="Calibri", size=10, bold=True, color="1F497D")
    
    thin_border = Border(
        left=Side(style='thin', color='BFBFBF'),
        right=Side(style='thin', color='BFBFBF'),
        top=Side(style='thin', color='BFBFBF'),
        bottom=Side(style='thin', color='BFBFBF')
    )
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------
    # TAB 1: Dispatch_Metadata
    # -------------------------------------------------------------
    ws1 = wb.create_sheet(title="1_Dispatch_Metadata")
    ws1.views.sheetView[0].showGridLines = True
    
    headers1 = [
        "Shipment UID", "Corridor ID", "Origin Packhouse / FPO", "Destination Terminal Mandi",
        "Crop Commodity", "Cultivar Variety", "Dispatch Date & Time (ISO)", "Vehicle Reg. Number",
        "Driver Contact Phone", "Vehicle Transport Mode (1-4)", "Cold Chain Active? (1/0)",
        "Reefer Setpoint (°C)", "Packaging Type", "Total Shipment Crates",
        "Harvest Date", "Harvest-to-Loading (Hours)", "Fungicide Dip Applied? (Y/N)",
        "Dispatch Field Officer Name", "Field Notes / Traffic Outlook"
    ]
    ws1.append(headers1)
    
    # Sample row
    sample_row_1 = [
        "SHP-20261115-JAL-01", "COR_JALGAON", "Jalgaon Banana Farmer Co-op Hub", "APMC Vashi, Navi Mumbai",
        "Banana", "Grand Naine (Cavendish)", "2026-11-15 06:30:00", "MH-19-BM-4421",
        "+91-98220-XXXXX", 2, 0,
        "", "CFB_Telescopic", 350,
        "2026-11-14", 14.5, "Y (1% Alum + Fungicide)",
        "Abhinay Pande", "Standard NH53 route; clear weather; driver briefed on logger protocol"
    ]
    ws1.append(sample_row_1)

    # -------------------------------------------------------------
    # TAB 2: Fruit_Specimens_Dispatch
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="2_Fruit_Dispatch_Assay")
    ws2.views.sheetView[0].showGridLines = True
    
    headers2 = [
        "Shipment UID", "Specimen Tag UID", "Crate Position (Core/Periphery)",
        "Photo Dorsal Filepath", "Photo Ventral Filepath", "von Loesecke Stage (1-7)",
        "Defect Area (%)", "AgriRoute V Score (0-100)", "Calibrated Confidence",
        "Selective Abstain? (1/0)", "Initial Weight W0 (g)", "Initial Pulp Firmness (kg/cm²)",
        "Rater 1 ID", "Rater 2 ID (if dual-graded)", "Specimen Notes"
    ]
    ws2.append(headers2)
    
    for i in range(1, 11):
        ws2.append([
            "SHP-20261115-JAL-01", f"FRT-{i:02d}", "Core_Bottom" if i <= 5 else "Periphery_Top",
            f"data/photos/SHP-20261115-JAL-01_FRT-{i:02d}_D.jpg",
            f"data/photos/SHP-20261115-JAL-01_FRT-{i:02d}_V.jpg",
            1 if i != 3 else 2, 0.0 if i != 4 else 2.5, 94.2, 0.965, 0,
            165.4 + (i * 2.1), 11.2 - (i * 0.1), "EP_Rater", "AP_Rater" if i <= 2 else "",
            "Firm green mature hand"
        ])

    # -------------------------------------------------------------
    # TAB 3: Logistics_Telemetry
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="3_Logistics_Telemetry")
    ws3.views.sheetView[0].showGridLines = True
    
    headers3 = [
        "Shipment UID", "Arrival Date & Time (ISO)", "Actual Transit Duration (Hours)",
        "Actual Road Distance (km)", "Logger A Core UID", "Logger B Periphery UID",
        "Mean Core Temp (°C)", "Max Core Temp (°C)", "Min Core Temp (°C)",
        "Degree-Hours Above 15°C", "Mean Relative Humidity (%)", "Min Relative Humidity (%)",
        "AgriRoute Route Score G", "AgriRoute Dynamic Fusion R", "En Route Interruptions / Remarks"
    ]
    ws3.append(headers3)
    ws3.append([
        "SHP-20261115-JAL-01", "2026-11-15 18:45:00", 12.25, 418.5,
        "ELT-RC4-88412", "ELT-RC4-88419", 24.8, 31.4, 21.2,
        119.5, 78.4, 62.1,
        28.4, 31.8, "2-hour traffic hold at Kasara Ghat; no refrigeration failure"
    ])

    # -------------------------------------------------------------
    # TAB 4: Fruit_Specimens_Arrival
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="4_Fruit_Arrival_Assay")
    ws4.views.sheetView[0].showGridLines = True
    
    headers4 = [
        "Shipment UID", "Specimen Tag UID", "Arrival Photo Dorsal Path", "Arrival Photo Ventral Path",
        "Arrival von Loesecke Stage (1-7)", "Arrival Defect Area (%)", "Arrival Weight W_arr (g)",
        "Physiological Loss in Weight PLW (%)", "Arrival Pulp Firmness (kg/cm²)",
        "Firmness Loss ΔF (kg/cm²)", "Pulp TSS (°Brix) [Sacrifice Fruit]",
        "COMMERCIAL SPOILAGE BINARY Y (1=Spoiled / 0=Marketable)",
        "Commercial Marketability Grade (0-100)", "Rater 1 ID", "Rater 2 ID",
        "Inter-Rater Consensus", "Final Specimen Disposition"
    ]
    ws4.append(headers4)
    
    for i in range(1, 11):
        spoil = 1 if i == 7 else 0
        w0 = 165.4 + (i * 2.1)
        w_arr = w0 * (0.96 if spoil == 0 else 0.89)
        plw = ((w0 - w_arr) / w0) * 100.0
        ws4.append([
            "SHP-20261115-JAL-01", f"FRT-{i:02d}",
            f"data/photos/SHP-20261115-JAL-01_FRT-{i:02d}_ARR_D.jpg",
            f"data/photos/SHP-20261115-JAL-01_FRT-{i:02d}_ARR_V.jpg",
            2 if spoil == 0 else 6, 1.0 if spoil == 0 else 18.5,
            round(w_arr, 1), round(plw, 2),
            9.5 if spoil == 0 else 2.1, round(11.2 - (9.5 if spoil == 0 else 2.1), 2),
            6.5 if i <= 2 else "", spoil, 88.0 if spoil == 0 else 25.0,
            "BN_Rater", "VP_Rater" if i <= 2 else "", "Full Consensus",
            "Wholesale Grade A Lot" if spoil == 0 else "Severe Crown Rot Salvage Cull"
        ])

    # -------------------------------------------------------------
    # TAB 5: Codebook_Definitions
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="5_Codebook_Reference")
    ws5.views.sheetView[0].showGridLines = True
    
    headers5 = ["Field Name", "Sheet Location", "Format / Type", "Permissible Values", "Operational Instructions for Field Researchers"]
    ws5.append(headers5)
    
    codebook_items = [
        ("Shipment UID", "All sheets", "String", "SHP-YYYYMMDD-[COR]-[NUM]", "Use standard corridor code (JAL, NAS, SOL, GUN) and sequential two-digit batch number"),
        ("Transport Mode", "Dispatch", "Integer [1-4]", "1=Open trailer, 2=Covered truck, 3=Insulated, 4=Reefer", "Inspect cargo compartment directly; verify tarpaulin tie-down or refrigeration unit serial"),
        ("Cold Chain Active?", "Dispatch", "Binary [0,1]", "1 = Active cooling; 0 = Ambient", "Must verify reefer engine running and check dashboard display at departure"),
        ("von Loesecke Stage", "Dispatch/Arrival", "Integer [1-7]", "1=All green, 2=Trace yellow, 3=More green, 4=More yellow, 5=Green tips, 6=Full yellow, 7=Brown flecked", "Compare against laminated standard color chart under 5500K LED lighting"),
        ("Defect Area (%)", "Dispatch/Arrival", "Float [0.0 - 100.0]", "0.0% to 100.0%", "Visually estimate surface necrosis, latex staining, or mechanical crush; use grid overlay if uncertain"),
        ("Initial Weight (g)", "Dispatch", "Float (0.1g res)", "80.0 to 350.0 g", "Tare scale before each measurement; wipe any surface mud with dry cloth before weighing"),
        ("Pulp Firmness", "Dispatch/Arrival", "Float (kg/cm²)", "0.5 to 15.0 kg/cm²", "Hold penetrometer perpendicular to fruit cheek; drive plunger smoothly to 10mm scribed ring"),
        ("Commercial Spoilage Y", "Arrival", "Binary [0,1]", "1 = Cull / Distress; 0 = Marketable", "PRIMARY OUTCOME: Set to 1 if stage >= 6.5, rot > 15%, or rupture; otherwise 0"),
        ("Selective Abstain?", "Dispatch", "Binary [0,1]", "1 = Abstain; 0 = Accept", "AgriRoute safety flag: set to 1 if MobileNetV2 calibrated confidence < 0.90")
    ]
    for row in codebook_items:
        ws5.append(row)

    # Apply formatting across all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        # Header formatting
        for col_num in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center_align
            cell.border = thin_border
            
        # Data formatting
        for row_num in range(2, ws.max_row + 1):
            for col_num in range(1, ws.max_column + 1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.border = thin_border
                cell.font = Font(name="Calibri", size=10)
                if isinstance(cell.value, (int, float)):
                    cell.alignment = center_align
                else:
                    cell.alignment = left_align

        # Auto-adjust column widths
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)
            
        ws.row_dimensions[1].height = 28

    print(f"💾 Saving workbook to {OUTPUT_XLSX}...")
    wb.save(str(OUTPUT_XLSX))
    print(f"✅ Excel field collection workbook successfully created: {OUTPUT_XLSX}")

if __name__ == "__main__":
    create_excel_workbook()

