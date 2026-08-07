<!-- FMEA_ROW_START id=PRLITHO-0001 -->

## PRLITHO-0001

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 3
- process: 1. 晶圓進料檢查
- functional_requirement: 晶片表面無刮痕、顆粒、凹凸過大(<1.66um)、warp(<300um?)
- potential_failure_mode: 濺影產生造成光阻塗佈不均
- potential_failure_effect: 線路斷路或殘留
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

<!-- FMEA_ROW_START id=PRLITHO-0002 -->

## PRLITHO-0002

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 4
- process: 1. 晶圓進料檢查
- functional_requirement: wafer notch 辨識
- potential_failure_mode: notch 誤認
- potential_failure_effect: 機台無法辨識進行取放片
- severity_before: 7
- potential_causes: 玻璃wafer邊緣不正常透光
- occurrence_before: 3
- current_process_controls: 目視檢<br>機台alarm
- detection_before: 3
- rpn_before: 63
- recommended_actions: 前程邊緣蝕刻需要乾淨
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0003 -->

## PRLITHO-0003

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 5
- process: 1. 晶圓進料檢查
- functional_requirement: Wafer背面無汙染<br>基板吸取真空度
- potential_failure_mode: 機台警示(真空度過低)
- potential_failure_effect: 部分位置失焦，無法進行曝光
- severity_before: 7
- potential_causes: 進貨無抽樣到
- occurrence_before: 1
- current_process_controls: 目視檢
- detection_before: 3
- rpn_before: 21
- recommended_actions: 1.進貨檢驗片數全檢擦拭<br>2.清chuck
- severity_after: 7
- occurrence_after: 1
- detection_after: 3
- rpn_after: 21
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0004 -->

## PRLITHO-0004

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 6
- process: 1. 晶圓進料檢查
- functional_requirement: 機台環境Particle監測
- potential_failure_mode: Particle high
- potential_failure_effect: Yield loss
- severity_before: 7
- potential_causes: 廠務系統變異
- occurrence_before: 1
- current_process_controls: CS-10
- detection_before: 3
- rpn_before: 21
- recommended_actions: 環境擺測試控片，前後值分析
- severity_after: 7
- occurrence_after: 1
- detection_after: 3
- rpn_after: 21
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0005 -->

## PRLITHO-0005

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 7
- process: 2. 光阻塗佈
- functional_requirement: 光阻原料品質
- potential_failure_mode: 變質或厚度變異
- potential_failure_effect: 解析度不佳及CD變異
- severity_before: 7
- potential_causes: 過期或環境影響
- occurrence_before: 1
- current_process_controls: NANO厚度量測及CD量測
- detection_before: 1
- rpn_before: 7
- recommended_actions: 1.一周兩次測試   2.Nano-測厚度<br>3.CD解析度-OM<br>4.產品Camtek
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0006 -->

## PRLITHO-0006

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 8
- process: 2. 光阻塗佈
- functional_requirement: HMDS 塗佈均勻
- potential_failure_mode: 光阻接著不良
- potential_failure_effect: 光阻塗佈不均，光阻顯影後peeling
- severity_before: 7
- potential_causes: N2 purge 壓力不足或 stage 溫控異常
- occurrence_before: 1
- current_process_controls: 機台alarm
- detection_before: 1
- rpn_before: 14
- recommended_actions: 設備檢修
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 14
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0007 -->

## PRLITHO-0007

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 9
- process: 2. 光阻塗佈
- functional_requirement: 厚度均勻無氣泡產生
- potential_failure_mode: 濺影產生造成光阻塗佈不均
- potential_failure_effect: 線路斷路或殘留
- severity_before: 7
- potential_causes: 管路無排泡或回吸失效
- occurrence_before: 1
- current_process_controls: NANO，目視或OM
- detection_before: 3
- rpn_before: 42
- recommended_actions: 1.設備檢修<br>2.增加管路Cycle Purge次數
- severity_after: 7
- occurrence_after: 1
- detection_after: 3
- rpn_after: 42
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0008 -->

## PRLITHO-0008

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 10
- process: 2. 光阻塗佈
- functional_requirement: chuck轉速<br>SPEC.=1950 ±-50rpm
- potential_failure_mode: 厚度變厚或變薄
- potential_failure_effect: CD變異
- severity_before: 5
- potential_causes: 馬達轉速有異常
- occurrence_before: 1
- current_process_controls: NANO厚度量測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0009 -->

## PRLITHO-0009

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 11
- process: 2. 光阻塗佈
- functional_requirement: 下料量<br>SPEC.=11± 0.5 cc
- potential_failure_mode: 下料量不足
- potential_failure_effect: 塗佈厚度不足,厚度不均，產生箭影
- severity_before: 5
- potential_causes: 定量pump異常
- occurrence_before: 1
- current_process_controls: NANO，目視
- detection_before: 1
- rpn_before: 5
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0010 -->

## PRLITHO-0010

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 12
- process: 2. 光阻塗佈
- functional_requirement: 軟烤 HP+CP溫控<br>SPEC.=110±1◦C
- potential_failure_mode: 溫控過高或過低
- potential_failure_effect: CD變異
- severity_before: 5
- potential_causes: 溫控器異常
- occurrence_before: 1
- current_process_controls: 設備自動偵測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0011 -->

## PRLITHO-0011

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 13
- process: 3. 光阻洗邊(EBR)
- functional_requirement: 洗邊針頭角度及高度(藥液不能回濺到距離wafer邊緣1 cm)
- potential_failure_mode: 針頭角度及高度偏移
- potential_failure_effect: 洗邊的距離改變及回濺
- severity_before: 2
- potential_causes: 人為碰撞或機台設定跑掉
- occurrence_before: 2
- current_process_controls: 目視
- detection_before: 2
- rpn_before: 8
- recommended_actions: 設備檢修
- severity_after: 2
- occurrence_after: 2
- detection_after: 2
- rpn_after: 8
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0012 -->

## PRLITHO-0012

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 14
- process: 3. 光阻洗邊(EBR)
- functional_requirement: 符合洗邊的需求<br>1.8um± 0.5um
- potential_failure_mode: 電鍍渡液滲出wafer邊緣
- potential_failure_effect: 電鍍環污染,銅環會被電鍍上銅
- severity_before: 2
- potential_causes: 機台中心點設定跑掉
- occurrence_before: 2
- current_process_controls: 目視<br>光學顯微鏡
- detection_before: 2
- rpn_before: 8
- recommended_actions: 重新校正WAFER中心點以符合規範
- severity_after: 2
- occurrence_after: 2
- detection_after: 2
- rpn_after: 8
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0013 -->

## PRLITHO-0013

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 15
- process: 3. 光阻洗邊(EBR)
- functional_requirement: 藥液噴灑穩定(管路不行出現氣泡)
- potential_failure_mode: 噴濺污染
- potential_failure_effect: 光阻受溶劑污染厚度不均
- severity_before: 3
- potential_causes: 管路氣泡
- occurrence_before: 3
- current_process_controls: 目視
- detection_before: 3
- rpn_before: 27
- recommended_actions: 1.設備檢修<br>2.作Cycle Purge
- severity_after: 3
- occurrence_after: 3
- detection_after: 3
- rpn_after: 27
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0014 -->

## PRLITHO-0014

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 16
- process: 4. 光阻對位曝光
- functional_requirement: 光罩進料檢查(無 particle汙染)
- potential_failure_mode: Repeat defect
- potential_failure_effect: particle 會遮光造成曝光局部失效
- severity_before: 7
- potential_causes: 包裝或製作過程汙染
- occurrence_before: 1
- current_process_controls: 強光燈檢測<br>OM抽測
- detection_before: 1
- rpn_before: 7
- recommended_actions: 1.異常退回給光罩廠處理<br>2.測試片驗證
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0015 -->

## PRLITHO-0015

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 17
- process: 4. 光阻對位曝光
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

<!-- FMEA_ROW_START id=PRLITHO-0016 -->

## PRLITHO-0016

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 18
- process: 4. 光阻對位曝光
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

<!-- FMEA_ROW_START id=PRLITHO-0017 -->

## PRLITHO-0017

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 19
- process: 4. 光阻對位曝光
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

<!-- FMEA_ROW_START id=PRLITHO-0018 -->

## PRLITHO-0018

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 20
- process: 4. 光阻對位曝光
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

<!-- FMEA_ROW_START id=PRLITHO-0019 -->

## PRLITHO-0019

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 21
- process: 4. 光阻對位曝光
- functional_requirement: Wafer 厚度量測<br>SPEC.=±8um
- potential_failure_mode: 過高或過低造成profile異常
- potential_failure_effect: CD變異
- severity_before: 5
- potential_causes: 機台量測異常
- occurrence_before: 3
- current_process_controls: 機台log檔
- detection_before: 3
- rpn_before: 45
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 3
- detection_after: 3
- rpn_after: 45
- owner_date: -

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0020 -->

## PRLITHO-0020

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 22
- process: 5. 光阻顯影
- functional_requirement: 顯影液溫控<br>SPEC.=22±1◦C
- potential_failure_mode: 機台警示(溫度過高或過低)
- potential_failure_effect: CD變異
- severity_before: 5
- potential_causes: 溫控器異常
- occurrence_before: 1
- current_process_controls: 光學顯微鏡
- detection_before: 3
- rpn_before: 15
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: -

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0021 -->

## PRLITHO-0021

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 23
- process: 5. 光阻顯影
- functional_requirement: 顯影液需全面覆蓋光阻
- potential_failure_mode: 部分光阻殘留
- potential_failure_effect: 線路斷路或短路
- severity_before: 5
- potential_causes: 顯影液因PI開scribe line而覆蓋不均
- occurrence_before: 1
- current_process_controls: 目視或光學顯微鏡
- detection_before: 3
- rpn_before: 15
- recommended_actions: 增加顯影液的量
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: -

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PRLITHO-0022 -->

## PRLITHO-0022

- source_excel: PRLITHO_FMEA.xlsx
- source_sheet: K&S_PR_Litho
- source_excel_row: 24
- process: 5. 光阻顯影
- functional_requirement: DI water rinse<br>SPEC.=no residue 無彩紋…
- potential_failure_mode: 部分光阻殘留
- potential_failure_effect: 線路斷路或短路
- severity_before: 5
- potential_causes: 管路壓力不足或清洗時間不夠
- occurrence_before: 1
- current_process_controls: 目視或光學顯微鏡
- detection_before: 3
- rpn_before: 15
- recommended_actions: 設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->
