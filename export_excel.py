# -*- coding: utf-8 -*-
"""
Xuat toan bo bao gia da thu thap tu website ra file Excel, dung DUNG cau truc
sheet Tong_hop_bao_gia da duoc xay dung thu cong truoc do (bang chi tiet A-M,
vung tham chieu O-R, bang tong hop/chot gia du toan ben duoi) - de NCC noi tiep
dung 1 quy trinh voi cac dot truoc.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
from openpyxl.worksheet.datavalidation import DataValidation

HEADER_FILL = PatternFill("solid", fgColor="305496")
HEADER_FONT = Font(bold=True, color="FFFFFF")
THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

DETAIL_START_ROW = 5
DETAIL_END_ROW = 5 + 300  # du cho nhieu bao gia hon cac dot truoc


def build_workbook(vendor_by_id, all_items, all_maint, categories):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tong_hop_bao_gia"

    ws["A1"] = "TỔNG HỢP BÁO GIÁ - GÓI THẦU TBYT (xuất tự động từ Cổng thu thập báo giá trực tuyến)"
    ws["A2"] = ("Nền XANH = NCC chào giá THẤP NHẤT | Nền ĐỎ = NCC chào giá CAO NHẤT | Cột L,M tham khảo (bảo trì mở rộng) | "
                "Cột M/O bảng tổng hợp bên dưới do Bệnh viện tự quyết định")

    headers = ["STT", "Danh mục thiết bị y tế", "Tên nhà cung cấp", "Ký/mã/nhãn hiệu/Model", "Hãng sản xuất",
               "Xuất xứ", "Số lượng", "ĐVT", "Đơn giá\n(đã bao gồm thuế, phí, lệ phí)", "Thành tiền", "Ngày báo giá",
               "Giá bảo trì/bảo hành\nmở rộng - gói 12 tháng\n(1 thiết bị, đã VAT)", "Thành tiền bảo trì\nmở rộng (toàn bộ SL)"]
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = BORDER

    # vung tham chieu danh muc O-R
    ws["O4"] = "STT"
    ws["P4"] = "Danh mục thiết bị y tế (Vùng tham chiếu - KHÔNG XOÁ)"
    ws["Q4"] = "ĐVT"
    ws["R4"] = "SL yêu cầu"
    for c in ["O4", "P4", "Q4", "R4"]:
        ws[c].font = HEADER_FONT
        ws[c].fill = HEADER_FILL
        ws[c].alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

    for i, cat in enumerate(categories):
        r = 5 + i
        ws.cell(row=r, column=15, value=i + 1)  # O
        ws.cell(row=r, column=16, value=cat["ten"])  # P
        ws.cell(row=r, column=17, value=cat["dvt"])  # Q
        ws.cell(row=r, column=18, value=cat["sl"])  # R
    ref_last_row = 4 + len(categories)

    # build detail rows tu du lieu NCC da nop
    r = DETAIL_START_ROW
    stt = 1
    for item in all_items:
        v = vendor_by_id.get(item["vendor_id"])
        if not v:
            continue
        ws.cell(row=r, column=1, value=stt)
        ws.cell(row=r, column=2, value=next((c["ten"] for c in categories if c["ma"] == item["ma_danh_muc"]), item["ma_danh_muc"]))
        ws.cell(row=r, column=3, value=v["ten_ncc"])
        ws.cell(row=r, column=4, value=item["model"])
        ws.cell(row=r, column=5, value=item["hang_sx"])
        ws.cell(row=r, column=6, value=item["xuat_xu"])
        ws.cell(row=r, column=7, value=f"=IF($B{r}=\"\",\"\",VLOOKUP($B{r},$P$5:$R${ref_last_row},3,0))")
        ws.cell(row=r, column=8, value=f"=IF($B{r}=\"\",\"\",VLOOKUP($B{r},$P$5:$R${ref_last_row},2,0))")
        ws.cell(row=r, column=9, value=item["don_gia"])
        ws.cell(row=r, column=10, value=f"=IF(OR($G{r}=\"\",$I{r}=\"\"),\"\",$G{r}*$I{r})")
        ws.cell(row=r, column=11, value=item["ngay_bao_gia"])

        maint_match = next((m for m in all_maint if m["vendor_id"] == item["vendor_id"] and m["ma_danh_muc"] == item["ma_danh_muc"]), None)
        if maint_match:
            ws.cell(row=r, column=12, value=maint_match["don_gia_baotri"])
        ws.cell(row=r, column=13, value=f"=IF(OR($G{r}=\"\",$L{r}=\"\"),\"\",$G{r}*$L{r})")
        r += 1
        stt += 1

    # dien cong thuc rong cho cac dong con lai den DETAIL_END_ROW (de sau nay add them thu cong van chay dung)
    for rr in range(r, DETAIL_END_ROW + 1):
        ws.cell(row=rr, column=1, value=stt)
        ws.cell(row=rr, column=7, value=f"=IF($B{rr}=\"\",\"\",VLOOKUP($B{rr},$P$5:$R${ref_last_row},3,0))")
        ws.cell(row=rr, column=8, value=f"=IF($B{rr}=\"\",\"\",VLOOKUP($B{rr},$P$5:$R${ref_last_row},2,0))")
        ws.cell(row=rr, column=10, value=f"=IF(OR($G{rr}=\"\",$I{rr}=\"\"),\"\",$G{rr}*$I{rr})")
        ws.cell(row=rr, column=13, value=f"=IF(OR($G{rr}=\"\",$L{rr}=\"\"),\"\",$G{rr}*$L{rr})")
        stt += 1

    last_detail_row = DETAIL_END_ROW

    dv = DataValidation(type="list", formula1=f"$P$5:$P${ref_last_row}", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"B{DETAIL_START_ROW}:B{last_detail_row}")

    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    rng = f"A{DETAIL_START_ROW}:M{last_detail_row}"
    b1 = DETAIL_START_ROW
    e1 = last_detail_row
    rule_min = Rule(
        type="expression",
        formula=[f'AND($B{b1}<>"",COUNTIFS($B${b1}:$B${e1},$B{b1})>1,$I{b1}=MINIFS($I${b1}:$I${e1},$B${b1}:$B${e1},$B{b1}))'],
        dxf=DifferentialStyle(fill=green_fill),
        stopIfTrue=False,
    )
    rule_max = Rule(
        type="expression",
        formula=[
            f'AND($B{b1}<>"",COUNTIFS($B${b1}:$B${e1},$B{b1})>1,$I{b1}=MAXIFS($I${b1}:$I${e1},$B${b1}:$B${e1},$B{b1}),'
            f'MINIFS($I${b1}:$I${e1},$B${b1}:$B${e1},$B{b1})<>MAXIFS($I${b1}:$I${e1},$B${b1}:$B${e1},$B{b1}))'
        ],
        dxf=DifferentialStyle(fill=red_fill),
        stopIfTrue=False,
    )
    ws.conditional_formatting.add(rng, rule_min)
    ws.conditional_formatting.add(rng, rule_max)

    # bang tong hop & chot gia du toan
    sum_start = last_detail_row + 3
    ws.cell(row=sum_start - 2, column=1, value="BẢNG TỔNG HỢP GIÁ & CHỐT GIÁ DỰ TOÁN THEO TỪNG DANH MỤC").font = Font(bold=True, size=12)
    hdr2 = ["STT", "Danh mục thiết bị y tế", "ĐVT", "SL\nyêu cầu", "Số báo\ngiá nhận\nđược", "Giá thấp nhất\n(đã VAT)",
            "NCC chào\ngiá thấp nhất", "Giá cao nhất\n(đã VAT)", "NCC chào\ngiá cao nhất", "Giá trung bình\n(đã VAT)",
            "% Chênh\nlệch", "Cảnh báo", "Giá dự toán\nCHỐT (đã VAT)", "Thành tiền\ndự toán", "Căn cứ chọn giá"]
    for i, h in enumerate(hdr2, start=1):
        c = ws.cell(row=sum_start, column=i, value=h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

    for i, cat in enumerate(categories):
        r = sum_start + 1 + i
        refrow = 5 + i
        ws.cell(row=r, column=1, value=i + 1)
        ws.cell(row=r, column=2, value=f"=P{refrow}")
        ws.cell(row=r, column=3, value=f"=Q{refrow}")
        ws.cell(row=r, column=4, value=f"=R{refrow}")
        ws.cell(row=r, column=5, value=f'=COUNTIF($B${DETAIL_START_ROW}:$B${last_detail_row},$B{r})')
        ws.cell(row=r, column=6, value=f'=IF($E{r}=0,"",MINIFS($I${DETAIL_START_ROW}:$I${last_detail_row},$B${DETAIL_START_ROW}:$B${last_detail_row},$B{r}))')
        ws.cell(row=r, column=7, value=(
            f'=IF($E{r}=0,"",INDEX($C${DETAIL_START_ROW}:$C${last_detail_row},'
            f'SUMPRODUCT(($B${DETAIL_START_ROW}:$B${last_detail_row}=$B{r})*($I${DETAIL_START_ROW}:$I${last_detail_row}=$F{r})*'
            f'ROW($B${DETAIL_START_ROW}:$B${last_detail_row}))-{DETAIL_START_ROW - 1})'
        ))
        ws.cell(row=r, column=8, value=f'=IF($E{r}=0,"",MAXIFS($I${DETAIL_START_ROW}:$I${last_detail_row},$B${DETAIL_START_ROW}:$B${last_detail_row},$B{r}))')
        ws.cell(row=r, column=9, value=(
            f'=IF($E{r}=0,"",INDEX($C${DETAIL_START_ROW}:$C${last_detail_row},'
            f'SUMPRODUCT(($B${DETAIL_START_ROW}:$B${last_detail_row}=$B{r})*($I${DETAIL_START_ROW}:$I${last_detail_row}=$H{r})*'
            f'ROW($B${DETAIL_START_ROW}:$B${last_detail_row}))-{DETAIL_START_ROW - 1})'
        ))
        ws.cell(row=r, column=10, value=f'=IF($E{r}=0,"",AVERAGEIF($B${DETAIL_START_ROW}:$B${last_detail_row},$B{r},$I${DETAIL_START_ROW}:$I${last_detail_row}))')
        ws.cell(row=r, column=11, value=f'=IF(OR($E{r}<2,$J{r}=""),"",($H{r}-$F{r})/$J{r})')
        ws.cell(row=r, column=12, value=f'=IF($K{r}="","",IF($K{r}>0.2,"⚠ Chênh lệch cao","OK"))')
        ws.cell(row=r, column=14, value=f'=IF(OR($D{r}="",$M{r}=""),"",$D{r}*$M{r})')

    warn_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    l_first = sum_start + 1
    l_last = sum_start + len(categories)
    ws.conditional_formatting.add(
        f"L{l_first}:L{l_last}",
        Rule(type="expression", formula=[f'$L{l_first}="⚠ Chênh lệch cao"'], dxf=DifferentialStyle(fill=warn_fill)),
    )

    total_row = sum_start + 1 + len(categories)
    ws.cell(row=total_row, column=2, value="TỔNG DỰ TOÁN GÓI THẦU").font = Font(bold=True)
    ws.cell(row=total_row, column=14, value=f"=SUM(N{sum_start+1}:N{total_row-1})").font = Font(bold=True)

    widths = {1: 6, 2: 30, 3: 26, 4: 16, 5: 18, 6: 12, 7: 10, 8: 8, 9: 16, 10: 16, 11: 12, 12: 16, 13: 16,
              15: 6, 16: 34, 17: 10, 18: 10}
    for col, w in widths.items():
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

    return wb
