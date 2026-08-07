<!-- FMEA_ROW_START id=DESCUM-0001 -->

## DESCUM-0001

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 3
- process: 1. 晶圓進料
- functional_requirement: 晶片表面的particle數量合乎規格
- potential_failure_mode: 被particle遮蔽區域形成未鍍膜
- potential_failure_effect: 線路斷路
- severity_before: 8
- potential_causes: 來料particle數值太高
- occurrence_before: 4
- current_process_controls: camtek、CS-10、OM
- detection_before: 1
- rpn_before: 32
- recommended_actions: 請QC提供目前批次Shuttle Particle level
- severity_after: 8
- occurrence_after: 4
- detection_after: 1
- rpn_after: 32
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0002 -->

## DESCUM-0002

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 4
- process: 1. 晶圓進料
- functional_requirement: 晶片翹曲度過大(>2mm)
- potential_failure_mode: 設備傳送異常
- potential_failure_effect: 發生破片、製程中斷
- severity_before: 10
- potential_causes: 來料warpage大於2mm
- occurrence_before: 4
- current_process_controls: Fogal
- detection_before: 1
- rpn_before: 40
- recommended_actions: 請QC提供目前批次warp數值
- severity_after: 10
- occurrence_after: 4
- detection_after: 1
- rpn_after: 40
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0003 -->

## DESCUM-0003

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 5
- process: 1. 晶圓進料
- functional_requirement: Wafer背面無汙染
- potential_failure_mode: 設備傳送異常
- potential_failure_effect: 發生破片
- severity_before: 10
- potential_causes: Wafer背面有光阻、膠材汙染
- occurrence_before: 2
- current_process_controls: 目視檢驗
- detection_before: 6
- rpn_before: 120
- recommended_actions: 前站完成後或本站進貨時進行檢驗
- severity_after: 10
- occurrence_after: 2
- detection_after: 6
- rpn_after: 120
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0004 -->

## DESCUM-0004

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 6
- process: 1. 晶圓進料
- functional_requirement: 機台環境Particle監測
- potential_failure_mode: Particle high
- potential_failure_effect: Yield loss
- severity_before: 8
- potential_causes: 廠務系統變異/HEPA失效
- occurrence_before: 2
- current_process_controls: Particle counter
- detection_before: 3
- rpn_before: 48
- recommended_actions: 定期進行無塵室環境/Loadport環境量測
- severity_after: 8
- occurrence_after: 2
- detection_after: 3
- rpn_after: 48
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0005 -->

## DESCUM-0005

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 7
- process: 2. DESCUM製程
- functional_requirement: 蝕刻深度符合規格
- potential_failure_mode: 蝕刻深度不符合規格
- potential_failure_effect: 線路斷路、電路阻抗不符合設計值、Yield loss
- severity_before: 7
- potential_causes: 1.電漿系統功率輸出失效<br>2.氣體供應系統異常<br>3.晶圓翹曲度過大<br>4.製程轉換時造成Descum腔體汙染<br>5.選擇錯誤的製程recipe
- occurrence_before: 3
- current_process_controls: 1.設備軟體設定電漿功率誤差允許值<br>2.設備軟體設定氣體流量誤差允許值<br>3.Fogal<br>4.製程轉換時進行大PM並進行測機<br>5.操作者目視確認
- detection_before: 3
- rpn_before: 63
- recommended_actions: 1.請設備部門定期進行電漿系統保養<br>2.請設備部門定期檢查氣體供應系統<br>3.請QC提供目前批次warp數值<br>4.請設備部門在轉換製程時執行大PM<br>5.請操作者確實確認
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0006 -->

## DESCUM-0006

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 8
- process: 2. DESCUM製程
- functional_requirement: 均勻性符合規格(U%<10%)
- potential_failure_mode: 均勻性不符合規格
- potential_failure_effect: 線路斷路、電路阻抗不符合設計值、Yield loss
- severity_before: 6
- potential_causes: 1.晶圓底座高度動作誤差<br>2.晶圓翹曲度過大
- occurrence_before: 3
- current_process_controls: 1.設備軟體設定底座高度值<br>2.Fogal量測
- detection_before: 3
- rpn_before: 54
- recommended_actions: 1.請設備部門定期檢查底座系統<br>2.請QC提供目前批次warp數值
- severity_after: 6
- occurrence_after: 3
- detection_after: 3
- rpn_after: 54
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0007 -->

## DESCUM-0007

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 9
- process: 2. DESCUM製程
- functional_requirement: 銅Via區域表面無PI殘留
- potential_failure_mode: 銅Via區域表面殘留PI
- potential_failure_effect: 線路斷路、電路阻抗不符合設計值、Yield loss
- severity_before: 6
- potential_causes: 1.電漿系統功率輸出失效<br>2.晶圓翹曲度過大<br>3.黃光製程未能形成良好Via開孔
- occurrence_before: 3
- current_process_controls: 1.設備軟體設定電漿功率誤差允許值<br>2.Fogal量測<br>2.黃光製程定期測機
- detection_before: 3
- rpn_before: 54
- recommended_actions: 1.請設備部門定期進行電漿系統保養<br>2.請QC提供目前批次warp數值<br>2.請QC進行每批次檢驗
- severity_after: 6
- occurrence_after: 3
- detection_after: 3
- rpn_after: 54
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0008 -->

## DESCUM-0008

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 10
- process: 2. DESCUM製程
- functional_requirement: 銅Via區域表面無髒污/表面異常
- potential_failure_mode: 銅Via區域表面髒污/變色/腐蝕
- potential_failure_effect: 晶圓報廢
- severity_before: 10
- potential_causes: 製程轉換時造成Descum腔體汙染
- occurrence_before: 3
- current_process_controls: 製程轉換時進行大PM並進行測機
- detection_before: 3
- rpn_before: 90
- recommended_actions: 請設備部門在轉換製程時執行大PM
- severity_after: 10
- occurrence_after: 3
- detection_after: 3
- rpn_after: 90
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=DESCUM-0009 -->

## DESCUM-0009

- source_excel: DESCUM_FMEA.xlsx
- source_sheet: 天虹Descum_逸書
- source_excel_row: 11
- process: 2. DESCUM製程
- functional_requirement: 晶圓完整無損傷
- potential_failure_mode: 晶圓損傷、缺角、破裂
- potential_failure_effect: 晶圓報廢
- severity_before: 10
- potential_causes: 1.玻璃晶圓與底座發生沾黏<br>2. 來料warpage大於2mm
- occurrence_before: 4
- current_process_controls: 1.調整底座升降參數與dechuck除靜電參數降低沾黏發生率<br>2.Fogal量測
- detection_before: 7
- rpn_before: 280
- recommended_actions: 1.請原廠檢討底座設計並加上表面粗糙度設計<br>2.請QC提供目前批次warp數值
- severity_after: 10
- occurrence_after: 4
- detection_after: 7
- rpn_after: 280
- owner_date: 

<!-- FMEA_ROW_END -->
