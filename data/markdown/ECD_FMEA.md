<!-- FMEA_ROW_START id=ECD-0001 -->

## ECD-0001

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 2
- process: 晶圓傳送 模組
- functional_requirement: 傳送 100片無問題
- potential_failure_mode: 1.FOUP 無法辨識<br>2.無法pre-align<br>3.robot失靈/wafer抓取高度錯誤
- potential_failure_effect: 1.無法進行製程<br>2.wafer破片
- severity_before: 10
- potential_causes: 1.HW和SW間訊號出問題<br>2.robot故障
- occurrence_before: 6
- current_process_controls: robot定期初始化
- detection_before: 1
- rpn_before: 60
- recommended_actions: Robot定期PM/上油和進行韌體更新
- severity_after: 10
- occurrence_after: 6
- detection_after: 1
- rpn_after: 60
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0002 -->

## ECD-0002

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 3
- process: 晶圓傳送 模組
- functional_requirement: contact ring 要符合pin對在seed layer，Seal蓋在PR上
- potential_failure_mode: 1.seal 因EBR不符合造成汙染(被電鍍)<br>2.seal彈性疲乏，無法緊壓PR
- potential_failure_effect: 1.contact ring附近區電流密度不均，影響整個wafer膜厚均勻<br>2.contact ring區藥水外滲，影響整個wafer膜厚均勻度
- severity_before: 10
- potential_causes: 1. EBR不符合規範<br>2.PR厚度>300um，contact ring老化
- occurrence_before: 6
- current_process_controls: 目前有兩組SRM，在contact ring和wafer壓合後會進行檢查
- detection_before: 1
- rpn_before: 60
- recommended_actions: 1.每批lot在電鍍前先OM確認EBR是否in spec<br>1.目前有兩組SRM檢測模組，加上四個contact ring自行更換<br>2.定期進行contact ring清潔，有必要需委外送洗
- severity_after: 10
- occurrence_after: 6
- detection_after: 1
- rpn_after: 60
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0003 -->

## ECD-0003

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 4
- process: Prewet 模組
- functional_requirement: 帶有光阻的pattern需要有好的wetting效果
- potential_failure_mode: 1.電鍍失效<br>2.包孔<br>3.膜成形出問題
- potential_failure_effect: 接下來的製程受影響/電性
- severity_before: 10
- potential_causes: 1.真空pump損壞<br>2.噴水頭故障<br>3.廠務供水系統出狀況
- occurrence_before: 4
- current_process_controls: 有HW控制和偵測
- detection_before: 3
- rpn_before: 120
- recommended_actions: 1.定期PM/Bump定期檢測<br>2.定期使用pattern wafer進行電鍍，確認是否有狀況
- severity_after: 10
- occurrence_after: 4
- detection_after: 3
- rpn_after: 120
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0004 -->

## ECD-0004

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 5
- process: 電鍍 模組
- functional_requirement: 電鍍溶液要符合酮酸氯濃度/添加劑要符合濃度規範<br>(B:10, C:12, L:10)
- potential_failure_mode: 酮酸氯濃度不對/添加劑濃度比例不正確
- potential_failure_effect: 1.產生by product，造成電鍍溶液汙染<br>2.鍍膜厚度完全跑掉
- severity_before: 10
- potential_causes: 建槽時陰陽級母液加錯，添加劑濃度加錯
- occurrence_before: 4
- current_process_controls: 電鍍陰極及楊極母液體分桶且標示清楚，添加劑濃度計算要正確
- detection_before: 3
- rpn_before: 120
- recommended_actions: 在建完槽後過貨前先進行CVS濃度分析，沒問題再過貨
- severity_after: 10
- occurrence_after: 4
- detection_after: 3
- rpn_after: 120
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0005 -->

## ECD-0005

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 6
- process: 電鍍 模組
- functional_requirement: 銅顆粒要長黑膜(CuPx)
- potential_failure_mode: 陽極銅顆粒黑膜不完整
- potential_failure_effect: 電鍍膜厚U%不好
- severity_before: 8
- potential_causes: PM酸鹼洗後burning不完整
- occurrence_before: 2
- current_process_controls: 在酸鹼洗後會做dummy鍍膜10分鐘
- detection_before: 1
- rpn_before: 16
- recommended_actions: 1.將burning步驟納入PM SOP<br>2.重要產品前dummy run 一片NPW
- severity_after: 8
- occurrence_after: 2
- detection_after: 1
- rpn_after: 16
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0006 -->

## ECD-0006

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 7
- process: 電鍍 模組
- functional_requirement: 電鍍chamber液位要在spec內
- potential_failure_mode: 1.電鍍膜厚和均勻度完全不對<br>2.水揮發到membrane裸露，membrane乾掉
- potential_failure_effect: 接下來的製程受影響
- severity_before: 10
- potential_causes: 1.自動補水系統故障<br>2.廠務供水系統出狀況
- occurrence_before: 4
- current_process_controls: 有sensor偵測水位系統，oos會Alarm
- detection_before: 1
- rpn_before: 40
- recommended_actions: 電鍍前確認機台有無水位過低的Alarm，定期更換水位sensor
- severity_after: 10
- occurrence_after: 4
- detection_after: 1
- rpn_after: 40
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0007 -->

## ECD-0007

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 8
- process: 電鍍 模組
- functional_requirement: 鍍液溫度在常溫
- potential_failure_mode: 1.電鍍厚度不正確<br>2.晶粒結構大小不同
- potential_failure_effect: 1.接下來的製程受影響<br>2.電性和機械性質改變
- severity_before: 8
- potential_causes: 冷水機/恆溫系統故障
- occurrence_before: 4
- current_process_controls: 1.現有的藥水是在常溫下進行電鍍<br>2.有恆溫系統
- detection_before: 3
- rpn_before: 96
- recommended_actions: 1.電鍍前再次確認目前藥水溫度(機台是否有跳Alarm)<br>2.冰水機/恆溫系統定期檢查
- severity_after: 8
- occurrence_after: 4
- detection_after: 3
- rpn_after: 96
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0008 -->

## ECD-0008

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 9
- process: 電鍍 模組
- functional_requirement: 鍍液流速 (3.6 LPM)
- potential_failure_mode: 1.電鍍厚度不正確<br>2.電鍍膜厚U%不好
- potential_failure_effect: 1.接下來的製程受影響<br>2.Die間/不同Die的厚度不均勻，接下來的製程受影響
- severity_before: 8
- potential_causes: 1.控制系統失靈<br>2.管路汙染阻塞
- occurrence_before: 4
- current_process_controls: 1.有HW控制<br>2.chamber有paddle攪拌
- detection_before: 3
- rpn_before: 96
- recommended_actions: 1.電鍍前確認前再次確認流速(機台是否有跳Alarm)<br>2.定期PM/清理管路/換藥水
- severity_after: 8
- occurrence_after: 4
- detection_after: 3
- rpn_after: 96
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0009 -->

## ECD-0009

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 10
- process: 電鍍 模組
- functional_requirement: filter功能正常
- potential_failure_mode: 電鍍液流速受影響，影響膜厚和U%
- potential_failure_effect: 接下來的製程受影響
- severity_before: 10
- potential_causes: 1.電鍍溶液汙染阻塞<br>2.filter老舊
- occurrence_before: 4
- current_process_controls: 定期更換filter和電鍍溶液
- detection_before: 1
- rpn_before: 40
- recommended_actions: 定期更換電鍍溶液和filter(不論是否電鍍溶液life time還未過)
- severity_after: 10
- occurrence_after: 4
- detection_after: 1
- rpn_after: 40
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0010 -->

## ECD-0010

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 11
- process: 電鍍 模組
- functional_requirement: membrane需要有阻止添加劑擴散的作用
- potential_failure_mode: 添加劑從電鍍陰極滲透至陽極
- potential_failure_effect: 膜厚均勻度跑掉，Die間/不同Die的厚度不均勻，接下來的製程受影響
- severity_before: 8
- potential_causes: membrane老舊
- occurrence_before: 4
- current_process_controls: 每周送測添加劑濃度分析
- detection_before: 1
- rpn_before: 32
- recommended_actions: 1.備料membrane<br>2.組建藥水濃度自動分析及添加系統(已接洽廠商看是否能用租借方式)<br>3.持續維持每周藥水分析，owner不在時backup幫忙取藥水並送分析
- severity_after: 8
- occurrence_after: 4
- detection_after: 1
- rpn_after: 32
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0011 -->

## ECD-0011

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 12
- process: 電鍍 模組
- functional_requirement: 分散板功能正常
- potential_failure_mode: 被汙染物阻塞或是汙染
- potential_failure_effect: 影響wafer模厚均勻度
- severity_before: 8
- potential_causes: 電鍍溶液汙染
- occurrence_before: 4
- current_process_controls: 只過特定且化學性穩定的PR
- detection_before: 3
- rpn_before: 96
- recommended_actions: 定期PM/清理管路/換藥水
- severity_after: 8
- occurrence_after: 4
- detection_after: 3
- rpn_after: 96
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0012 -->

## ECD-0012

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 13
- process: 電鍍 模組
- functional_requirement: Power supply供應穩定
- potential_failure_mode: power supply出問題會影響電流不穩定
- potential_failure_effect: 造成鍍膜不均勻和薄膜品質不佳(電性和機械性質不好)
- severity_before: 10
- potential_causes: 損壞/電流密度設定過高
- occurrence_before: 4
- current_process_controls: 1.有HW monitor spec，超過會Alarm
- detection_before: 3
- rpn_before: 120
- recommended_actions: 1.recipe要設定正確，電流設定不超標(第二人double check)<br>2.定期維護和更換
- severity_after: 10
- occurrence_after: 4
- detection_after: 3
- rpn_after: 120
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0013 -->

## ECD-0013

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 14
- process: 電鍍 模組
- functional_requirement: 添加劑濃度符合規格，L濟濃度要保持高>10 ml/L
- potential_failure_mode: 1.電鍍膜厚U%不好<br>2.無法cover前程問題，導致大量Cu nodule出現
- potential_failure_effect: 1.Nodule defect區差排多，影響電性<br>2.Nodule defect區旁，其厚度會低於實際厚度
- severity_before: 6
- potential_causes: 添加劑濃度低於規範
- occurrence_before: 3
- current_process_controls: 每周進行藥水濃度檢測，電鍍前添加不足的藥水劑量
- detection_before: 3
- rpn_before: 54
- recommended_actions: 1.組建藥水濃度自動分析及添加系統(已接洽廠商看是否能用租借方式)<br>2.建立藥水濃度模擬，預測濃度(已告知R3進行合作)<br>3.持續維持每周藥水分析，owner不在時backup幫忙取藥水並送分析
- severity_after: 6
- occurrence_after: 3
- detection_after: 3
- rpn_after: 54
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0014 -->

## ECD-0014

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 15
- process: 電鍍 模組
- functional_requirement: recipe選擇要正確
- potential_failure_mode: 選錯recipe
- potential_failure_effect: 膜厚完全不對，接下來的製程受影響
- severity_before: 10
- potential_causes: 人為疏失
- occurrence_before: 6
- current_process_controls: 將recipe名字區隔清楚
- detection_before: 1
- rpn_before: 60
- recommended_actions: 選recipe時有另一個人double check
- severity_after: 10
- occurrence_after: 6
- detection_after: 1
- rpn_after: 60
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0015 -->

## ECD-0015

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 16
- process: SRD 模組
- functional_requirement: 電鍍後殘留化合物要沖水旋乾
- potential_failure_mode: 1.轉盤出問題，無法旋乾<br>2.噴水頭出問題
- potential_failure_effect: 1.表面殘留chemical無法完全去除，影響正常膜厚。影響後續製程<br>2.汙染電鍍厚表面。影響後續製程
- severity_before: 10
- potential_causes: 1.function故障<br>2.噴水頭故障<br>3.廠務供水系統出狀況
- occurrence_before: 4
- current_process_controls: 1.有HW控制和偵測<br>2.電鍍完目視
- detection_before: 3
- rpn_before: 120
- recommended_actions: 1.定期PM<br>2.定期用NPW驗機，後目視
- severity_after: 10
- occurrence_after: 4
- detection_after: 3
- rpn_after: 120
- owner_date: 

<!-- FMEA_ROW_END -->

<!-- FMEA_ROW_START id=ECD-0016 -->

## ECD-0016

- source_excel: ECD_FMEA.xlsx
- source_sheet: Nokota_ECD_肅競
- source_excel_row: 17
- process: TSV洗邊
- functional_requirement: TSV洗邊功能正常
- potential_failure_mode: 洗邊不完整，殘留Cu residul
- potential_failure_effect: 影響CMP製程
- severity_before: 8
- potential_causes: 洗邊溶液life time過了
- occurrence_before: 4
- current_process_controls: 定期更換洗邊液體
- detection_before: 3
- rpn_before: 96
- recommended_actions: 1.不論過貨量多少，定期更換洗邊溶液<br>2.洗邊後目視，必要時進行OM/alpha-step確認
- severity_after: 8
- occurrence_after: 4
- detection_after: 3
- rpn_after: 96
- owner_date: 

<!-- FMEA_ROW_END -->
