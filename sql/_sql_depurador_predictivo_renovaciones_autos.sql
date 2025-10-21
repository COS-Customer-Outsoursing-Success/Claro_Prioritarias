WITH base AS (
    SELECT *,
        CASE 
            WHEN excluir = 1        
              OR placa IN (
					SELECT placa 
					FROM bbdd_cos_bog_grupo_axa.tb_asignacion_renovados_autos_v2_no_aptos 
					WHERE periodo = 202510
              )
/*
              OR phone IN ( 
					SELECT 
						phone_number_dialed 
                    FROM bbdd_cos_bog_grupo_axa.tb_markings_2300_daily
					WHERE campana = "Falabella"
                    )
*/
            THEN 1 ELSE 0 
        END AS exclusiones_general
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_renovados_autos_v2_coalesce
    WHERE periodo = 202510
)
, consolidados AS (
    SELECT *,
           MAX(exclusiones_general) OVER(PARTITION BY placa) AS exclusion_total
    FROM base
)
SELECT 
	*
FROM consolidados 
WHERE exclusion_total = 0
and tipo_phone = 'no_celular'
and nombre_base = 'Base call center renovados 700 reg 20 Octubre 2025 Aptos'
and oneroso = 'NO ONEROSO'

#AND DATE_FORMAT(inicio_renovacion, "%m%d") 
#	BETWEEN  DATE_FORMAT("2025-09-01", "%m%d") AND DATE_FORMAT("2025-09-14", "%m%d")
ORDER BY DATE_FORMAT(inicio_renovacion, "%m%d") ASC, oneroso DESC