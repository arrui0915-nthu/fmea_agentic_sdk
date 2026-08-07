<!-- FMEA_ROW_START id=PILITHO-0001 -->

## PILITHO-0001

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 3
- process: 1.產品Pattern驗證
- functional_requirement: 曝光Pattern無異常
- potential_failure_mode: 圖形異常
- potential_failure_effect: 產品功能失效
- severity_before: 7
- potential_causes: 曝光圖形/光罩異常
- occurrence_before: 3
- current_process_controls: OM、camtek
- detection_before: 3
- rpn_before: 63
- recommended_actions: 1.廠商出圖DRC確認<br>2.請QC帶貨時，產品驗證前導批驗證，前導測方式(可Rework光阻)
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0002 -->

## PILITHO-0002

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 4
- process: 1.產品Pattern驗證
- functional_requirement: Criticle pattern define
- potential_failure_mode: 圖形異常
- potential_failure_effect: 產品功能失效
- severity_before: 7
- potential_causes: 曝光圖形/光罩異常
- occurrence_before: 3
- current_process_controls: OM、camtek
- detection_before: 3
- rpn_before: 63
- recommended_actions: 1.Camtek全檢、Criticle pattern check OM抽檢
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0003 -->

## PILITHO-0003

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 5
- process: 1.產品Pattern驗證
- functional_requirement: EBR(??um)、切割道(120um)定義
- potential_failure_mode: Warp Control
- potential_failure_effect: Warp過大，無法曝光
- severity_before: 3
- potential_causes: 曝光圖形/光罩異常
- occurrence_before: 3
- current_process_controls: OM
- detection_before: 3
- rpn_before: 27
- recommended_actions: 1.請QC出圖前定義確認<br>2.OM Chcek
- severity_after: 3
- occurrence_after: 3
- detection_after: 3
- rpn_after: 27
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0004 -->

## PILITHO-0004

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 6
- process: 1.產品Pattern驗證
- functional_requirement: 光罩進料檢查(無 particle汙染)
- potential_failure_mode: Repeat defect
- potential_failure_effect: particle 會遮光造成曝光局部失效
- severity_before: 3
- potential_causes: 包裝或製作過程汙染
- occurrence_before: 1
- current_process_controls: 強光燈檢測<br>OM抽測
- detection_before: 1
- rpn_before: 3
- recommended_actions: 1.異常退回給光罩廠處理<br>2.測試片驗證
- severity_after: 3
- occurrence_after: 1
- detection_after: 1
- rpn_after: 3
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0005 -->

## PILITHO-0005

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 7
- process: 2. 晶圓進料檢查
- functional_requirement: 晶片表面無刮痕、顆粒、凹凸過大(<1.66um)、warp(<300um?)
- potential_failure_mode: 濺影產生造成光阻塗佈不均
- potential_failure_effect: PI殘留填孔失敗造成斷路
- severity_before: 7
- potential_causes: 進貨無抽樣到
- occurrence_before: 7
- current_process_controls: camtek、NANO、CS-10、OM、Fogal
- detection_before: 3
- rpn_before: 147
- recommended_actions: 進貨檢驗片數全檢確認<br>1.請QC提供目前批次Shuttle Particle level<br>2.請QC提供目前批次Warp level
- severity_after: 7
- occurrence_after: 7
- detection_after: 3
- rpn_after: 147
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0006 -->

## PILITHO-0006

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 8
- process: 2. 晶圓進料檢查
- functional_requirement: wafer notch 辨識
- potential_failure_mode: notch 誤認
- potential_failure_effect: 機台無法辨識進行取放片
- severity_before: 5
- potential_causes: 玻璃wafer邊緣不正常透光
- occurrence_before: 3
- current_process_controls: 目視檢<br>機台alarm
- detection_before: 3
- rpn_before: 45
- recommended_actions: 前程邊緣蝕刻需要乾淨
- severity_after: 5
- occurrence_after: 3
- detection_after: 3
- rpn_after: 45
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0007 -->

## PILITHO-0007

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 9
- process: 2. 晶圓進料檢查
- functional_requirement: Wafer背面無汙染<br>基板吸取真空度
- potential_failure_mode: 機台警示(真空度過低)
- potential_failure_effect: 部分位置失焦，無法進行曝光
- severity_before: 5
- potential_causes: 進貨無抽樣到
- occurrence_before: 1
- current_process_controls: 目視檢
- detection_before: 3
- rpn_before: 15
- recommended_actions: 1.進貨檢驗片數全檢擦拭<br>2.清chuck
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0008 -->

## PILITHO-0008

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 10
- process: 2. 晶圓進料檢查
- functional_requirement: 機台環境Particle監測
- potential_failure_mode: Particle high
- potential_failure_effect: Yield loss
- severity_before: 5
- potential_causes: 廠務系統變異
- occurrence_before: 1
- current_process_controls: CS-10
- detection_before: 3
- rpn_before: 15
- recommended_actions: 環境擺測試控片，前後值分析
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0009 -->

## PILITHO-0009

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 11
- process: 3. 光阻對位曝光
- functional_requirement: 厚度曝光變異符合產品需求<br>SPEC.=5±0.5um
- potential_failure_mode: 電性異常
- potential_failure_effect: Via hole形狀不佳
- severity_before: 7
- potential_causes: 曝光sensor異常
- occurrence_before: 5
- current_process_controls: 光學顯微鏡
- detection_before: 3
- rpn_before: 105
- recommended_actions: 1.設備校正及調整機台曝光均勻度
- severity_after: 7
- occurrence_after: 5
- detection_after: 3
- rpn_after: 105
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0010 -->

## PILITHO-0010

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 12
- process: 3. 光阻對位曝光
- functional_requirement: 符合產品OL需求±1um的需求<br>SPEC.標準wafer為±0.5um
- potential_failure_mode: Overlay 超出設計範圍
- potential_failure_effect: 線路斷路或短路
- severity_before: 7
- potential_causes: 對位key模糊機台無法辨識,或wafer warp
- occurrence_before: 1
- current_process_controls: 1.Camtek<br>2.光學顯微鏡
- detection_before: 3
- rpn_before: 21
- recommended_actions: 1.OL量測<br>2.Alignment Mark(SPEC.±1um)及WARP控制在允許範圍內
- severity_after: 7
- occurrence_after: 1
- detection_after: 3
- rpn_after: 21
- owner_date: -

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0011 -->

## PILITHO-0011

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 13
- process: 3. 光阻對位曝光
- functional_requirement: chuck X、Y軸移動精度<br>SPEC.=±1um
- potential_failure_mode: Overlay over SPC.
- potential_failure_effect: 對位異常,CD變異
- severity_before: 7
- potential_causes: 機台stage異常
- occurrence_before: 1
- current_process_controls: 光學顯微鏡
- detection_before: 1
- rpn_before: 7
- recommended_actions: 設備校正及調整
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0012 -->

## PILITHO-0012

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 14
- process: 3. 光阻對位曝光
- functional_requirement: chuck Z軸移動精度<br>SPEC.=±1um
- potential_failure_mode: Focus 異常
- potential_failure_effect: CD變異
- severity_before: 7
- potential_causes: 機台stage異常
- occurrence_before: 1
- current_process_controls: 光學顯微鏡
- detection_before: 1
- rpn_before: 7
- recommended_actions: 設備校正及調整
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0013 -->

## PILITHO-0013

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 15
- process: 3. 光阻對位曝光
- functional_requirement: 曝光整面均勻度為3%
- potential_failure_mode: 過高或過低造成profile異常
- potential_failure_effect: 線路形狀不佳，CD變異
- severity_before: 5
- potential_causes: 曝光sensor異常,laser decay
- occurrence_before: 1
- current_process_controls: 1.光學顯微鏡OM<br>2.Camtek
- detection_before: 3
- rpn_before: 15
- recommended_actions: 1.設備校正及調整機台曝光均勻度<br>2.更換laser 源
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0014 -->

## PILITHO-0014

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 16
- process: 3. 光阻對位曝光
- functional_requirement: 符合曝邊的需求<br>1.8um± 0.5um
- potential_failure_mode: 影響邊緣Not/Good Die影響
- potential_failure_effect: 電鍍爬坡搭接問題
- severity_before: 5
- potential_causes: 機台中心點設定跑掉
- occurrence_before: 2
- current_process_controls: 目視<br>光學顯微鏡
- detection_before: 2
- rpn_before: 20
- recommended_actions: 重新校正WAFER中心點以符合規範
- severity_after: 5
- occurrence_after: 2
- detection_after: 2
- rpn_after: 20
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PILITHO-0015 -->

## PILITHO-0015

- source_excel: PILITHO_FMEA.xlsx
- source_sheet: PI_Litho_良全
- source_excel_row: 17
- process: 3. 光阻對位曝光
- functional_requirement: 產品Stiching確認<br>SPEC.=no residue 無彩紋…
- potential_failure_mode: 外觀異常
- potential_failure_effect: 產品影響未知
- severity_before: 5
- potential_causes: 曝光量異常
- occurrence_before: 1
- current_process_controls: 1.目視<br>2.電性驗證<br>3.OM量測
- detection_before: 3
- rpn_before: 15
- recommended_actions: OM量測
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->
