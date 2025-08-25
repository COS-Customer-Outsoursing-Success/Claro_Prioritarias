WITH base AS (
    SELECT *,
        CASE 
            WHEN excluir = 1
              OR placa IN (
                  SELECT placa 
                  FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos 
                  WHERE periodo = 202508
              )
            THEN 1 ELSE 0 
        END AS exclusiones_general
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    WHERE periodo = 202508
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

-- ---------------------------------------------------------------------------- --
-- Sin gestion : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- ---------------------------------------------------------------------------- --

/*
	AND tipo_phone = 'telefono1'
	AND (vicidial_calls = 0 OR vicidial_calls IS NULL)
*/

-- ---------------------------------------------------------------------------- --
-- No Contacto : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- ---------------------------------------------------------------------------- --

/*
    AND vicidial_calls <= 5
	AND (tipo_mejor_gestion = 'No Contacto'
	OR tipificacion_mejor_gestion_soul IN ('No Contestan', 'Grabadora o Buzon', 'Cliente Cuelga La Llamada')
    )

	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%m%d') 
	BETWEEN  DATE_FORMAT(CURDATE() - INTERVAL 10 DAY, '%m%d') AND DATE_FORMAT(CURDATE(), '%m%d')
*/

-- ---------------------------------------------------------------------------- --
-- Seguimientos: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- ---------------------------------------------------------------------------- --

/*
    AND vicidial_calls <= 10
	AND (tipificacion_mejor_gestion_soul IN ('Cliente solicita envío de cotización', 'Llamar después')
    )
*/  

-- ---------------------------------------------------------------------------- --
-- Fechas De Vigencia: Descomentar colocando un # al inicio de los simbolos "/*" -
-- ---------------------------------------------------------------------------- --

/*
	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN  DATE_FORMAT(CURDATE() + INTERVAL 1 DAY, '%%m%%d') AND DATE_FORMAT(CURDATE() + INTERVAL 15 DAY, '%%m%%d')
*/

-- ---------------------------------------------------------------------------- --
-- No comentar esta parte, evita que se marquen registros marcados entre hoy y ayer
-- ---------------------------------------------------------------------------- --

    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)
	AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)

ORDER BY fecha_fin_vigencia_actual DESC, vicidial_calls ASC, tipo_phone ASC;