WITH base AS (
    SELECT *,
        CASE 
            WHEN excluir = 1        
              OR placa IN (
					SELECT placa 
					FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos 
					WHERE periodo = 202509
              )
/*
              OR phone IN ( 
					SELECT 
						phone_number_dialed 
                    FROM bbdd_cos_bog_grupo_axa.tb_markings_2300_daily
					WHERE campana = 'Falabella'
                    )
*/
            THEN 1 ELSE 0 
        END AS exclusiones_general
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    WHERE periodo = 202509
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

-- -----------------------------------------------------------------------------------------
-- Predictivo Sin Gestion: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
	AND tipo_phone IN ('telefono1') #,'telefono2'
	AND (
		vicidial_calls = 0 
        OR 
        vicidial_calls IS NULL
        )
    
    AND tipificacion_mejor_gestion_soul IS NULL
    
	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN  DATE_FORMAT('2025-09-24', '%%m%%d') AND DATE_FORMAT('2025-09-30', '%%m%%d')
    
#    AND prioridad = 'POTENCIAL PREMIUM'
#	 AND prioridad IN ('ALTA GAMA BUEN POTENCIAL', 'ALTO POTENCIAL')
#    AND prioridad = 'NORMAL'
    
*/

-- -----------------------------------------------------------------------------------------
-- Predictivo No Contacto: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

#/*
	AND tipo_phone IN ('telefono1') #,'telefono2'
    
	AND ( 
    vicidial_calls <= 1
    AND 
    vicidial_calls IS NOT NULL 
    )

    AND (
    tipificacion_mejor_gestion_soul IN ('No Contestan')#, 'Cliente Cuelga La Llamada')
    OR 
    tipificacion_mejor_gestion_soul IS NULL
    )

	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN  DATE_FORMAT('2025-09-23', '%%m%%d') AND DATE_FORMAT('2025-09-30', '%%m%%d')
    
#	AND tipificacion_mejor_gestion IN ('Agent Not Available', 'Agent Altnum', 'No Contacto','ADAIR')    
#	AND tipificacion_mejor_gestion NOT IN ('Agent Not Available', 'Agent Altnum', 'No Contacto','ADAIR')
    
#     AND prioridad = 'POTENCIAL PREMIUM'
#	 AND prioridad IN ('ALTA GAMA BUEN POTENCIAL', 'ALTO POTENCIAL')
#    AND prioridad = 'NORMAL'
    
#*/

-- -----------------------------------------------------------------------------------------
-- Blaster : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
	AND tipo_phone IN ('telefono1') #,'telefono2'
	AND ( 
    vicidial_calls <= 3
    AND 
    vicidial_calls IS NOT NULL 
    )

    AND (
    tipificacion_mejor_gestion_soul = 'No Contestan' 
    OR 
    tipificacion_mejor_gestion_soul IS NULL
    )
    
    AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN  DATE_FORMAT('2025-09-01', '%%m%%d') AND DATE_FORMAT('2025-09-14', '%%m%%d')

    AND tipo_ultima_gestion <> 'Blaster - Contacto'
    AND tipo_mejor_gestion <> 'Blaster - Contacto'
*/

-- -----------------------------------------------------------------------------------------
-- Seguimientos Manuales: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
    AND vicidial_calls <= 10
	AND (tipificacion_ultima_gestion_soul IN ('Cliente solicita envío de cotización', 'Llamar después')
	
    AND DATE_FORMAT(fecha_ultima_gestion_soul, '%%m%%d') 
	BETWEEN  DATE_FORMAT(CURDATE() - INTERVAL 5 DAY, '%%m%%d') AND DATE_FORMAT(CURDATE(), '%%m%%d')
    )
	
    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 2 DAY
	)
	AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 2 DAY
	)
    
*/  

-- -----------------------------------------------------------------------------------------
-- SMS : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
	AND tipo_phone IN ('telefono1') #,'telefono2'
	AND (vicidial_calls = 0 OR vicidial_calls IS NULL)
	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN DATE_FORMAT('2025-09-11', '%%m%%d') AND DATE_FORMAT('2025-09-25', '%%m%%d')
*/
-- ---------------------------------------------------------------------------- --
-- No comentar esta parte, evita que se marquen registros marcados entre hoy y ayer
-- ---------------------------------------------------------------------------- --

    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)
	AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 1 DAY
	)

ORDER BY DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') ASC, vicidial_calls ASC, tipo_phone ASC, prioridad ASC
;