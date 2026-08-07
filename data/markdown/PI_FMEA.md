<!-- FMEA_ROW_START id=PI-0001 -->

## PI-0001

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 3
- process: 1.Wafer check/ handling
- functional_requirement: 晶圓進料檢查
- potential_failure_mode: 晶片表面異常
- potential_failure_effect: 塗佈後造成濺影,氣泡,<br>PI後薄不均,顯影後via open太大或不開
- severity_before: 5
- potential_causes: 晶片表面刮痕、顆粒、凹凸過大,背面太髒
- occurrence_before: 2
- current_process_controls: 目視/OM檢查
- detection_before: 3
- rpn_before: 30
- recommended_actions: 要求前站增加檢查樣本數, 並出示檢測證明
- severity_after: 5
- occurrence_after: 2
- detection_after: 3
- rpn_after: 30
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0002 -->

## PI-0002

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 4
- process: 1.Wafer check/ handling
- functional_requirement: 晶片表面無刮痕、顆粒、凹凸過大(<1.66um)
- potential_failure_mode: 濺影產生造成PI塗佈不均
- potential_failure_effect: 線路斷路或殘留
- severity_before: 7
- potential_causes: 進貨無抽樣到
- occurrence_before: 7
- current_process_controls: camtek、NANO、CS-10、OM
- detection_before: 3
- rpn_before: 147
- recommended_actions: 進貨檢驗片數全檢確認<br>1.請QC提供目前批次Shuttle Particle level<br>2.請QC提供目前批次Warp level
- severity_after: 7
- occurrence_after: 7
- detection_after: 3
- rpn_after: 147
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0003 -->

## PI-0003

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 5
- process: 1.Wafer check/ handling
- functional_requirement: 翹曲warp
- potential_failure_mode: 機台警示(真空度過低無法抓取)
- potential_failure_effect: 晶片內外受熱不均，開孔大小不均
- severity_before: 7
- potential_causes: 
- occurrence_before: 
- current_process_controls: 目視、Fogale
- detection_before: 
- rpn_before: 
- recommended_actions: Fogale檢測warp前值
- severity_after: 7
- occurrence_after: 0
- detection_after: 0
- rpn_after: 0
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0004 -->

## PI-0004

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 6
- process: 1.Wafer check/ handling
- functional_requirement: Wafer背面無汙染<br>基板吸取真空度
- potential_failure_mode: 機台警示(真空度過低無法抓取)
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

<!-- FMEA_ROW_START id=PI-0005 -->

## PI-0005

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 7
- process: 1.Wafer check/ handling
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

<!-- FMEA_ROW_START id=PI-0006 -->

## PI-0006

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 8
- process: 1.Wafer check/ handling
- functional_requirement: 晶片取放/傳送
- potential_failure_mode: 晶片偵測異常
- potential_failure_effect: 需人工確認處裡
- severity_before: 7
- potential_causes: 晶片斜插,凸片,sensor異常
- occurrence_before: 5
- current_process_controls: 機台發出警報
- detection_before: 1
- rpn_before: 35
- recommended_actions: 定期進行晶片傳送/取放測試
- severity_after: 7
- occurrence_after: 5
- detection_after: 1
- rpn_after: 35
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0007 -->

## PI-0007

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 9
- process: 1.Wafer check/ handling
- functional_requirement: 晶片取放/傳送
- potential_failure_mode: 取放失誤
- potential_failure_effect: 需人工確認處裡
- severity_before: 7
- potential_causes: 手臂之真空異常
- occurrence_before: 3
- current_process_controls: 機台發出警報
- detection_before: 1
- rpn_before: 21
- recommended_actions: 定期進行晶片傳送/取放測試
- severity_after: 7
- occurrence_after: 3
- detection_after: 1
- rpn_after: 21
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0008 -->

## PI-0008

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 10
- process: 1.Wafer check/ handling
- functional_requirement: 晶片取放/傳送
- potential_failure_mode: Particle
- potential_failure_effect: 晶片表面有particle
- severity_before: 3
- potential_causes: 手臂/吸盤未清潔
- occurrence_before: 3
- current_process_controls: 定期擦拭手臂/吸盤
- detection_before: 5
- rpn_before: 45
- recommended_actions: 定期擦拭手臂/吸盤,進行晶片傳送/取放測試
- severity_after: 3
- occurrence_after: 3
- detection_after: 5
- rpn_after: 45
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0009 -->

## PI-0009

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 11
- process: 1.Wafer check/ handling
- functional_requirement: 晶片中心化
- potential_failure_mode: 晶片未置中
- potential_failure_effect: 後續高速旋轉時晶片吸不住而飛離破裂
- severity_before: 7
- potential_causes: 機械故障,校正不完全
- occurrence_before: 2
- current_process_controls: 在晶片於塗佈/顯影旋轉時肉眼觀察是否偏心
- detection_before: 3
- rpn_before: 42
- recommended_actions: 定期進行晶片旋轉測試,以回推是否偏心需校正
- severity_after: 7
- occurrence_after: 2
- detection_after: 3
- rpn_after: 42
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0010 -->

## PI-0010

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 12
- process: 2. PI旋轉塗佈
- functional_requirement: PI原料品質
- potential_failure_mode: 變質或厚度變異
- potential_failure_effect: 解析度不佳及CD變異
- severity_before: 7
- potential_causes: 過期或環境影響
- occurrence_before: 1
- current_process_controls: NANO厚度量測及CD量測
- detection_before: 1
- rpn_before: 7
- recommended_actions: 1.二周一次更換材料，測試<br>2.Nano-測厚度<br>3.CD解析度-OM<br>4.產品Camtek
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0011 -->

## PI-0011

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 13
- process: 2. PI旋轉塗佈
- functional_requirement: 下料量<br>SPEC.=18 ± 0.5㏄
- potential_failure_mode: 下料量不足
- potential_failure_effect: 塗佈厚度不足,厚度不均，產生箭影
- severity_before: 5
- potential_causes: N2加壓異常
- occurrence_before: 1
- current_process_controls: NANO，目視
- detection_before: 1
- rpn_before: 5
- recommended_actions: 1.設備檢修<br>2.空跑第一片
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0012 -->

## PI-0012

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 14
- process: 2. PI旋轉塗佈
- functional_requirement: 厚度均勻無氣泡產生
- potential_failure_mode: 濺影產生造成PI塗佈不均
- potential_failure_effect: via處嚴重殘留，斷路
- severity_before: 7
- potential_causes: 加壓罐N2溶入PI，管路/閥件接縫處產生<br>管路無排泡或回吸失效
- occurrence_before: 3
- current_process_controls: 機台內建重力除泡罐<br>NANO，目視或OM
- detection_before: 3
- rpn_before: 63
- recommended_actions: 1.設備檢修<br>2.增加管路Cycle Purge次數
- severity_after: 7
- occurrence_after: 3
- detection_after: 3
- rpn_after: 63
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0013 -->

## PI-0013

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 15
- process: 2. PI旋轉塗佈
- functional_requirement: 吐料口PI: 0<回吸<3mm
- potential_failure_mode: 吐料口PI回吸異常
- potential_failure_effect: 手臂移動路線上均有PI弄髒其他地方,<br>吐出PI帶有氣泡
- severity_before: 3
- potential_causes: 回吸閥異常,回吸調整不適當
- occurrence_before: 3
- current_process_controls: 調整適當之回吸量
- detection_before: 2
- rpn_before: 18
- recommended_actions: 每次使用前檢查吐料口
- severity_after: 3
- occurrence_after: 3
- detection_after: 2
- rpn_after: 18
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0014 -->

## PI-0014

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 16
- process: 2. PI旋轉塗佈
- functional_requirement: 供料pump正常
- potential_failure_mode: 供料pump
- potential_failure_effect: PI吐料異常,厚度不均
- severity_before: 5
- potential_causes: 供料Pump故障造成PI吐料異常
- occurrence_before: 1
- current_process_controls: 目前機台無此pump
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0015 -->

## PI-0015

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 17
- process: 2. PI旋轉塗佈
- functional_requirement: PI供料溫控 (<±1℃)
- potential_failure_mode: PI供料溫控
- potential_failure_effect: PI厚度不對
- severity_before: 5
- potential_causes: 供料之溫控失效,吐出之PI溫度過高或過低,黏度跑掉,PI厚度不對
- occurrence_before: 1
- current_process_controls: 目前機台無供料溫控<br>定期檢查溫控裝置
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0016 -->

## PI-0016

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 18
- process: 2. PI旋轉塗佈
- functional_requirement: 吐料手臂擺動正常
- potential_failure_mode: 吐料手臂擺動異常
- potential_failure_effect: PI, Pre-wet, EBR供料位置異常
- severity_before: 7
- potential_causes: 馬達/控制器異常
- occurrence_before: 1
- current_process_controls: 機台自動偵測
- detection_before: 1
- rpn_before: 7
- recommended_actions: 請原廠保養/檢測
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0017 -->

## PI-0017

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 19
- process: 2. PI旋轉塗佈
- functional_requirement: Pre-wet正常
- potential_failure_mode: Pre-wet
- potential_failure_effect: 晶片表面潤濕不足
- severity_before: 5
- potential_causes: 控制閥異常, N2異常
- occurrence_before: 1
- current_process_controls: 人工觀察
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0018 -->

## PI-0018

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 20
- process: 2. PI旋轉塗佈
- functional_requirement: EBR洗邊正常
- potential_failure_mode: EBR洗邊
- potential_failure_effect: 晶邊沒洗乾淨
- severity_before: 3
- potential_causes: 控制閥異常, N2異常
- occurrence_before: 1
- current_process_controls: 人工觀察
- detection_before: 1
- rpn_before: 3
- recommended_actions: 請原廠保養/檢測
- severity_after: 3
- occurrence_after: 1
- detection_after: 1
- rpn_after: 3
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0019 -->

## PI-0019

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 21
- process: 2. PI旋轉塗佈
- functional_requirement: BSR背洗正常
- potential_failure_mode: BSR背洗
- potential_failure_effect: 晶背不乾淨
- severity_before: 5
- potential_causes: 控制閥異常, N2異常
- occurrence_before: 1
- current_process_controls: 人工觀察
- detection_before: 5
- rpn_before: 25
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 5
- rpn_after: 25
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0020 -->

## PI-0020

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 22
- process: 2. PI旋轉塗佈
- functional_requirement: N2壓力正常
- potential_failure_mode: N2壓力異常
- potential_failure_effect: PI吐料不穩, pre-wet/EBR/BSR異常
- severity_before: 5
- potential_causes: N2壓力不穩定造成吐料量變化
- occurrence_before: 3
- current_process_controls: 機台已設定最低操作壓力
- detection_before: 3
- rpn_before: 45
- recommended_actions: 定期確認壓力錶
- severity_after: 5
- occurrence_after: 3
- detection_after: 3
- rpn_after: 45
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0021 -->

## PI-0021

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 23
- process: 2. PI旋轉塗佈
- functional_requirement: 轉速正常 ±3rpm
- potential_failure_mode: 轉速異常
- potential_failure_effect: PI厚度不對
- severity_before: 5
- potential_causes: 旋轉馬達異常,轉速不對,造成PI厚度不對
- occurrence_before: 1
- current_process_controls: 機台自動偵測轉速<br>NANO厚度量測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 1.設備檢修<br>2.每次上料測試後略微調整
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0022 -->

## PI-0022

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 24
- process: 2. PI旋轉塗佈
- functional_requirement: 沒有PI gel產生
- potential_failure_mode: PI gel產生
- potential_failure_effect: PI表面凸起
- severity_before: 5
- potential_causes: PI管路不潔淨,<br>吐料口材料乾掉
- occurrence_before: 5
- current_process_controls: 定期洗管<br>定時吐料,保濕盒
- detection_before: 5
- rpn_before: 125
- recommended_actions: 定期洗管(每月)<br>定時吐料,保濕盒
- severity_after: 5
- occurrence_after: 5
- detection_after: 5
- rpn_after: 125
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0023 -->

## PI-0023

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 25
- process: 2. PI旋轉塗佈
- functional_requirement: exhaust排氣正常
- potential_failure_mode: exhaust排氣異常
- potential_failure_effect: PI表面particle增加, 溶劑異味增加
- severity_before: 5
- potential_causes: 排氣異常
- occurrence_before: 1
- current_process_controls: 定期檢查排氣是否正常
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期檢查排氣是否正常
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0024 -->

## PI-0024

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 26
- process: 2. PI旋轉塗佈
- functional_requirement: 無Particle在晶片表面
- potential_failure_mode: Particle在晶片表面
- potential_failure_effect: PI表面凸起,<br>造成濺影使PI厚度不均
- severity_before: 5
- potential_causes: CUP壁不乾淨在晶片旋轉時捲回晶片表面
- occurrence_before: 5
- current_process_controls: 定期送洗CUP
- detection_before: 5
- rpn_before: 125
- recommended_actions: 增加送洗頻率
- severity_after: 5
- occurrence_after: 5
- detection_after: 5
- rpn_after: 125
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0025 -->

## PI-0025

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 27
- process: 3.軟烤 HP+CP
- functional_requirement: HP溫度異常<±1.5℃
- potential_failure_mode: HP溫度異常
- potential_failure_effect: PI烤不夠或太久，CD變異
- severity_before: 5
- potential_causes: HP故障溫度不對
- occurrence_before: 1
- current_process_controls: 機台內有偵測溫度上下限
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期TC wafer 測溫，設備檢修
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0026 -->

## PI-0026

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 28
- process: 3.軟烤 HP+CP
- functional_requirement: HP溫度均勻性 <±1.5℃
- potential_failure_mode: HP溫度均勻性
- potential_failure_effect: 造成PI受熱不均
- severity_before: 5
- potential_causes: HP故障溫度不均勻
- occurrence_before: 1
- current_process_controls: 製程結果有問題才處理
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期TC wafer 測溫
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0027 -->

## PI-0027

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 29
- process: 3.軟烤 HP+CP
- functional_requirement: Gap 正常 依設定值
- potential_failure_mode: Gap 異常
- potential_failure_effect: PI烤不夠或太久
- severity_before: 5
- potential_causes: 頂pin異常
- occurrence_before: 1
- current_process_controls: 依機台內設定
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0028 -->

## PI-0028

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 30
- process: 3.軟烤 HP+CP
- functional_requirement: exhaust排氣正常
- potential_failure_mode: exhaust排氣異常
- potential_failure_effect: PI烤不乾
- severity_before: 5
- potential_causes: 排氣異常造成solvent充滿HP腔內
- occurrence_before: 3
- current_process_controls: 打開腔門,定期檢查排氣
- detection_before: 5
- rpn_before: 75
- recommended_actions: 設備商-更有效之排氣設計
- severity_after: 5
- occurrence_after: 3
- detection_after: 5
- rpn_after: 75
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0029 -->

## PI-0029

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 31
- process: 3.軟烤 HP+CP
- functional_requirement: HP上板溫度正常
- potential_failure_mode: HP上板溫度異常
- potential_failure_effect: Solvent凝結滴落至PI表面而烤不乾
- severity_before: 5
- potential_causes: HP上板故障
- occurrence_before: 1
- current_process_controls: 機台內有偵測溫度上下限
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0030 -->

## PI-0030

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 32
- process: 3.軟烤 HP+CP
- functional_requirement: CP溫度正常
- potential_failure_mode: CP溫度異常
- potential_failure_effect: 每片之間回溫情況略有差異
- severity_before: 5
- potential_causes: CP回溫速度太慢
- occurrence_before: 1
- current_process_controls: 無控制 (目前CP為自然冷卻,回溫速度較慢)
- detection_before: 5
- rpn_before: 25
- recommended_actions: 拉長晶片進入CP時間,<br>設備商-使用水冷控制之CP
- severity_after: 5
- occurrence_after: 1
- detection_after: 5
- rpn_after: 25
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0031 -->

## PI-0031

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 33
- process: 3.軟烤 HP+CP
- functional_requirement: 無particle
- potential_failure_mode: particle
- potential_failure_effect: 造成PI表面凸起,<br>造成濺影使PI厚度不均
- severity_before: 5
- potential_causes: HP,CP腔壁particle掉落
- occurrence_before: 3
- current_process_controls: 定期清潔
- detection_before: 5
- rpn_before: 75
- recommended_actions: 定期清潔
- severity_after: 5
- occurrence_after: 3
- detection_after: 5
- rpn_after: 75
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0032 -->

## PI-0032

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 34
- process: 4.對位<br>SUSS, K&S, LDI
- functional_requirement: 
- potential_failure_mode: 
- potential_failure_effect: 
- severity_before: 
- potential_causes: 
- occurrence_before: 
- current_process_controls: 
- detection_before: 
- rpn_before: 
- recommended_actions: 
- severity_after: 0
- occurrence_after: 0
- detection_after: 0
- rpn_after: 0
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0033 -->

## PI-0033

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 35
- process: 4.對位<br>SUSS, K&S, LDI
- functional_requirement: 
- potential_failure_mode: 
- potential_failure_effect: 
- severity_before: 
- potential_causes: 
- occurrence_before: 
- current_process_controls: 
- detection_before: 
- rpn_before: 
- recommended_actions: 
- severity_after: 0
- occurrence_after: 0
- detection_after: 0
- rpn_after: 0
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0034 -->

## PI-0034

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 36
- process: 5. PI顯影
- functional_requirement: 顯影條件正常
- potential_failure_mode: 顯影條件不對
- potential_failure_effect: PI恐底殘留太嚴重,<br>PI peeling
- severity_before: 5
- potential_causes: 顯影時間不足或過長
- occurrence_before: 1
- current_process_controls: OM檢查,OP定期測機
- detection_before: 1
- rpn_before: 5
- recommended_actions: OP定期測機,<br>不同設計需要先做測試片確認顯影條件
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0035 -->

## PI-0035

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 37
- process: 5. PI顯影
- functional_requirement: 供料幫鋪正常
- potential_failure_mode: 供料幫鋪
- potential_failure_effect: 局部區顯影液不足,顯不乾淨
- severity_before: 5
- potential_causes: pump故障,無法吐顯影液
- occurrence_before: 1
- current_process_controls: 目前機台無此pump
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠固定保養/檢測<br>設備商-加上此pump
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0036 -->

## PI-0036

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 38
- process: 5. PI顯影
- functional_requirement: 顯影液溫控<±1.5℃
- potential_failure_mode: 顯影液溫控
- potential_failure_effect: 顯影不夠或超過,CD太大或不開
- severity_before: 5
- potential_causes: 顯影液溫控故障,溫度太高或太低
- occurrence_before: 1
- current_process_controls: 目前機台無此溫控<br>CD以OM檢測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠固定保養/檢測,<br>設備商-加上溫控功能
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0037 -->

## PI-0037

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 39
- process: 5. PI顯影
- functional_requirement: 顯影液需全面覆蓋
- potential_failure_mode: 部分PI殘留
- potential_failure_effect: CD變異, Via不開
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
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0038 -->

## PI-0038

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 40
- process: 5. PI顯影
- functional_requirement: C260(PGMEA) rinse<br>SPEC.=no residue 無彩紋…
- potential_failure_mode: 部分PI殘留
- potential_failure_effect: CD變異, Via不開
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

<!-- FMEA_ROW_START id=PI-0039 -->

## PI-0039

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 41
- process: 5. PI顯影
- functional_requirement: N2壓力正常
- potential_failure_mode: N2壓力異常
- potential_failure_effect: 局部區顯影液不足,顯不乾淨
- severity_before: 5
- potential_causes: N2壓力不穩定造成吐出之顯影液量變化
- occurrence_before: 1
- current_process_controls: 機台已設定最低操作壓力
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期確認壓力錶
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0040 -->

## PI-0040

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 42
- process: 5. PI顯影
- functional_requirement: 轉速正常 ±3rpm
- potential_failure_mode: 轉速異常
- potential_failure_effect: 局部區域顯影不夠或超過,via open太大或不開
- severity_before: 5
- potential_causes: 旋轉馬達異常,轉速不對
- occurrence_before: 1
- current_process_controls: 機台自動偵測轉速
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0041 -->

## PI-0041

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 43
- process: 5. PI顯影
- functional_requirement: 吐料手臂擺動正常
- potential_failure_mode: 吐料手臂擺動異常
- potential_failure_effect: 局部區域顯影不夠或超過,via open太大或不開
- severity_before: 5
- potential_causes: 馬達/控制器 異常
- occurrence_before: 1
- current_process_controls: 機台自動偵測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 請原廠保養/檢測
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0042 -->

## PI-0042

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 44
- process: 5. PI顯影
- functional_requirement: exhaust排氣正常
- potential_failure_mode: exhaust排氣異常
- potential_failure_effect: 機台附近溶劑異味增加
- severity_before: 7
- potential_causes: 排氣異常
- occurrence_before: 1
- current_process_controls: 機台自動偵測
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期確認排氣錶正常
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0043 -->

## PI-0043

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 45
- process: 5. PI顯影
- functional_requirement: 無particle
- potential_failure_mode: particle
- potential_failure_effect: 顯影後晶片表面帶有particle
- severity_before: 5
- potential_causes: CUP/腔壁沾黏材料粉塵/particle,顯影時掉回晶片表面
- occurrence_before: 3
- current_process_controls: 不定期清潔
- detection_before: 3
- rpn_before: 45
- recommended_actions: 定期清潔
- severity_after: 5
- occurrence_after: 3
- detection_after: 3
- rpn_after: 45
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0044 -->

## PI-0044

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 46
- process: 6. Oven cure
- functional_requirement: Q-time
- potential_failure_mode: 吸水,吸氨
- potential_failure_effect: via顯不開、profile變形
- severity_before: 7
- potential_causes: 吸水,吸氨
- occurrence_before: 1
- current_process_controls: Q-time
- detection_before: 1
- rpn_before: 7
- recommended_actions: 1.Q-time控制<br>2.環境NH3檢測
- severity_after: 7
- occurrence_after: 1
- detection_after: 1
- rpn_after: 7
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0045 -->

## PI-0045

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 47
- process: 6. Oven cure
- functional_requirement: 溫度控制 <±2℃
- potential_failure_mode: 溫度控制
- potential_failure_effect: 溫度不夠PI物性化性改變,溫度太高影響前層材料
- severity_before: 5
- potential_causes: sensor故障,加熱器/溫度控制器異常
- occurrence_before: 1
- current_process_controls: 定期TC wafer測溫
- detection_before: 3
- rpn_before: 15
- recommended_actions: 定期TC wafer測溫
- severity_after: 5
- occurrence_after: 1
- detection_after: 3
- rpn_after: 15
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0046 -->

## PI-0046

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 48
- process: 6. Oven cure
- functional_requirement: 溫度控制 <±2℃
- potential_failure_mode: cure 不夠，PI 沒有完全故化
- potential_failure_effect: 物化性改變
- severity_before: 10
- potential_causes: 溫度不足，時間不足
- occurrence_before: 1
- current_process_controls: 依烤箱內設定之參數
- detection_before: 1
- rpn_before: 10
- recommended_actions: 
- severity_after: 
- occurrence_after: 
- detection_after: 
- rpn_after: 
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0047 -->

## PI-0047

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 49
- process: 6. Oven cure
- functional_requirement: 溫度控制 <±2℃
- potential_failure_mode: cure 太多，PI裂解
- potential_failure_effect: peeling, 物化性改變
- severity_before: 10
- potential_causes: 溫度過高，時間過久
- occurrence_before: 1
- current_process_controls: 依烤箱內設定之參數
- detection_before: 1
- rpn_before: 10
- recommended_actions: 
- severity_after: 
- occurrence_after: 
- detection_after: 
- rpn_after: 
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0048 -->

## PI-0048

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 50
- process: 6. Oven cure
- functional_requirement: N2正常
- potential_failure_mode: N2異常
- potential_failure_effect: 造成O2含量太高,PI固化後變質,物性化性改變
- severity_before: 7
- potential_causes: 廠務供應異常, 管路破裂/阻塞, 控制閥件故障
- occurrence_before: 1
- current_process_controls: 有02偵測,超量時自動烤箱alarm停止,手動烤箱僅顯示數值。
- detection_before: 5
- rpn_before: 35
- recommended_actions: 手動烤箱執行後,等待10分鐘確認O2含量
- severity_after: 7
- occurrence_after: 1
- detection_after: 5
- rpn_after: 35
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0049 -->

## PI-0049

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 51
- process: 6. Oven cure
- functional_requirement: 排氣功能正常
- potential_failure_mode: 排氣功能
- potential_failure_effect: 排氣太強烤箱溫度上不去PI固化不完全,<br>物性化性改變
- severity_before: 5
- potential_causes: 排氣太強烤箱溫度上不去,排氣不足
- occurrence_before: 1
- current_process_controls: 自動烤箱自動偵測,<br>手動烤箱人為調整好排氣閥門
- detection_before: 1
- rpn_before: 5
- recommended_actions: 定期確認排氣錶正常
- severity_after: 5
- occurrence_after: 1
- detection_after: 1
- rpn_after: 5
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0050 -->

## PI-0050

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 52
- process: 6. Oven cure
- functional_requirement: 溫度均勻性 <±2℃
- potential_failure_mode: 溫度均勻性
- potential_failure_effect: 不同晶片之PI固化的程度不同
- severity_before: 5
- potential_causes: 部分加熱器異常
- occurrence_before: 1
- current_process_controls: 定期TC wafer測溫<br>自動烤箱可測三位置<br>手動烤箱僅一位置
- detection_before: 5
- rpn_before: 25
- recommended_actions: 定期TC wafer測溫
- severity_after: 5
- occurrence_after: 1
- detection_after: 5
- rpn_after: 25
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0051 -->

## PI-0051

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 53
- process: 6. Oven cure
- functional_requirement: 無particle
- potential_failure_mode: particle
- potential_failure_effect: particle掉至晶片表面無法清除
- severity_before: 5
- potential_causes: 烤箱清潔度不足
- occurrence_before: 3
- current_process_controls: 定期清潔oven
- detection_before: 5
- rpn_before: 75
- recommended_actions: 定期清潔oven
- severity_after: 5
- occurrence_after: 3
- detection_after: 5
- rpn_after: 75
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=PI-0052 -->

## PI-0052

- source_excel: PI_FMEA.xlsx
- source_sheet: PI_煥鈞
- source_excel_row: 54
- process: 7. Descum
- functional_requirement: 
- potential_failure_mode: 
- potential_failure_effect: 
- severity_before: 
- potential_causes: 
- occurrence_before: 
- current_process_controls: 
- detection_before: 
- rpn_before: 
- recommended_actions: 
- severity_after: 
- occurrence_after: 
- detection_after: 
- rpn_after: 
- owner_date: 

<!-- FMEA_ROW_END -->
