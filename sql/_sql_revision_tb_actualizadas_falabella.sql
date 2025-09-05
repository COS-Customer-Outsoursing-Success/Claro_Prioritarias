SELECT 
max(call_date), 
'Soul' AS tb 
FROM bbdd_cos_bog_grupo_axa.tb_soul_desgloce_falabella_v2

UNION ALL

SELECT 
max(call_date),
'Vicidial' AS tb
FROM bbdd_cos_bog_grupo_axa.tb_marcaciones_desgloce_dts_v2;
;