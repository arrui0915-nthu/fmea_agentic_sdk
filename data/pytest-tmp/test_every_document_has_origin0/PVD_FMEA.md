<!-- FMEA_ROW_START id=PVD-0001 -->

## PVD-0001

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
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
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":10,"button_2":20,"button_3":30}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0002 -->

## PVD-0002

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 4
- process: 1. 晶圓進料
- functional_requirement: 晶片翹曲度過大(>2mm)
- potential_failure_mode: 設備傳送異常
- potential_failure_effect: 發生破片
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
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":15,"button_2":25,"button_3":35}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0003 -->

## PVD-0003

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
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
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":20,"button_2":30,"button_3":40}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0004 -->

## PVD-0004

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
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
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":25,"button_2":35,"button_3":45}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0005 -->

## PVD-0005

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 7
- process: 2. PVD製程
- functional_requirement: 鍍膜厚度符合需求
- potential_failure_mode: 厚度不符合需求
- potential_failure_effect: 後續蝕刻製程失效、電路阻抗不符合設計值
- severity_before: 7
- potential_causes: 1.電漿系統功率輸出失效<br>2.靶材壽命用盡<br>3.選擇錯誤的製程recipe
- occurrence_before: 3
- current_process_controls: 1.設備軟體設定電漿功率誤差允許值<br>2.設備軟體設定警戒值<br>3.操作者目視確認
- detection_before: 3
- rpn_before: 63
- recommended_actions: 1. 請設備部門定期進行保養<br>2. 請設備部門定期檢查靶材用量<br>3. 請操作者確實確認
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":30,"button_2":40,"button_3":50}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0006 -->

## PVD-0006

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 8
- process: 2. PVD製程
- functional_requirement: 鍍膜電阻率符合需求
- potential_failure_mode: 鍍膜電阻率不符合需求
- potential_failure_effect: 電路阻抗不符合設計值
- severity_before: 6
- potential_causes: 1. 晶片表面材質outgas<br>2. 塗佈製程未能完全固化<br>3. Degas功率未達設定值<br>4. 機台真空度不佳
- occurrence_before: 3
- current_process_controls: 1.設備軟體設定入料真空允許值<br>2.設備軟體設定入料真空允許值<br>3.設備軟體設定加熱功率誤差允許值<br>4.設備軟體設定各腔體IDLE真空允許值
- detection_before: 3
- rpn_before: 54
- recommended_actions: 1.新材料進行製程前需要先進行製程相容性評估<br>2.固化製程需定期執行製程驗證測機<br>3.請設備部門定期進行加熱器保養<br>4.請設備部門定期進行真空pump保養
- severity_after: 6
- occurrence_after: 3
- detection_after: 3
- rpn_after: 54
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":35,"button_2":45,"button_3":55}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0007 -->

## PVD-0007

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 9
- process: 2. PVD製程
- functional_requirement: 鍍膜均勻性符合規格(U%<6%)
- potential_failure_mode: 鍍膜均勻性不符合規格
- potential_failure_effect: 後續蝕刻製程失效、良率損失
- severity_before: 6
- potential_causes: 1.晶圓翹曲度過大<br>2.靶材磁場系統故障
- occurrence_before: 3
- current_process_controls: 1.Fogal量測<br>2.設備軟體偵測故障訊號
- detection_before: 3
- rpn_before: 54
- recommended_actions: 1.請QC提供目前批次warp數值<br>2.請設備部門定期進行系統檢查
- severity_after: 6
- occurrence_after: 3
- detection_after: 3
- rpn_after: 54
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":40,"button_2":50,"button_3":60}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0008 -->

## PVD-0008

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 10
- process: 2. PVD製程
- functional_requirement: 鍍膜附著性達到5B
- potential_failure_mode: 鍍膜附著性不佳/表面起泡
- potential_failure_effect: 晶圓報廢
- severity_before: 10
- potential_causes: 1. 晶片表面材質outgas<br>2. 塗佈製程未能完全固化<br>3. Degas功率未達設定值<br>4. 機台真空度不佳<br>5. ICP參數與表面材料未能匹配<br>6. ICP電漿功率未達設定值
- occurrence_before: 4
- current_process_controls: 1.設備軟體設定入料真空允許值<br>2.設備軟體設定入料真空允許值<br>3.設備軟體設定加熱功率誤差允許值<br>4.設備軟體設定各腔體IDLE真空允許值<br>5.針對新材料進行參數優化<br>6.設備軟體設定電漿功率誤差允許值
- detection_before: 3
- rpn_before: 120
- recommended_actions: 1.新材料進行製程前需要先進行製程相容性評估<br>2.固化製程需定期執行製程驗證測機<br>3.請設備部門定期進行加熱器保養<br>4.請設備部門定期進行真空pump保養<br>5.請QC提供新材料完整資料並進行完整測試<br>6.請設備部門定期進行電漿系統保養
- severity_after: 10
- occurrence_after: 4
- detection_after: 3
- rpn_after: 120
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":45,"button_2":55,"button_3":65}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0009 -->

## PVD-0009

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 11
- process: 2. PVD製程
- functional_requirement: 製程後particle增加量符合規範
- potential_failure_mode: Particle high
- potential_failure_effect: Yield loss
- severity_before: 8
- potential_causes: 1.機台擋板使用需進行清洗<br>2.電漿系統發生異常放電<br>3.來料汙染
- occurrence_before: 4
- current_process_controls: 1.設備軟體設定擋板lifetime上限<br>2.電源供應系統設定異常放電消除機制<br>3.camtek、CS-10、OM
- detection_before: 3
- rpn_before: 96
- recommended_actions: 1.請設備部門依據lifetime更換機台擋板<br>2.請設備部門定期進行電漿系統保養<br>3.請QC提供目前批次Shuttle Particle level
- severity_after: 8
- occurrence_after: 4
- detection_after: 3
- rpn_after: 96
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":50,"button_2":60,"button_3":70}}

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PVD-0010 -->

## PVD-0010

- source_excel: PVD_FMEA.xlsx
- source_sheet: fmea_pvd
- source_excel_row: 12
- process: 2. PVD製程
- functional_requirement: 晶圓完整無損傷
- potential_failure_mode: 晶圓損傷、缺角、破裂
- potential_failure_effect: 晶圓報廢
- severity_before: 10
- potential_causes: 1.玻璃晶圓與底座發生沾黏<br>2. 來料warpage大於2mm
- occurrence_before: 2
- current_process_controls: 1.調整底座升降參數與dechuck除靜電參數降低沾黏發生率<br>2.Fogal量測
- detection_before: 10
- rpn_before: 200
- recommended_actions: 1.請原廠檢討底座設計並加上表面粗糙度設計<br>2.請QC提供目前批次warp數值
- severity_after: 10
- occurrence_after: 2
- detection_after: 10
- rpn_after: 200
- owner_date: 
- machine_action: {"machine_id":"PVD-DEMO-01","setpoints":{"button_1":55,"button_2":65,"button_3":75}}

<!-- FMEA_ROW_END -->
