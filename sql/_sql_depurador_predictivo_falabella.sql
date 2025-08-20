with base as (
    select *,
        case 
            when excluir = 1
			OR placa IN ( SELECT placa FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos WHERE periodo IN (
            202508
				)
            )
            then 1 
            else 0 
        end as exclusiones_general
    from bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
    where 
    periodo IN (
    202508
    )
),
consolidados as (
    select *,
        max(exclusiones_general) over(partition by placa) as exclusion_total,
        row_number() over(partition by placa order by fecha_ultima_gestion asc) as orden
    from base
)

SELECT 
*
FROM consolidados
WHERE 1 = 1
	AND orden = 1
	AND exclusion_total = 0
    
-- Seleccion de telefonos a marcar    
	AND tipo_phone IN (
    'telefono1'
#   'telefono2'
#   'telefono3'
	)
    
-- Seleccion de cantidad de intentos a marcar
	AND (
		vicidial_calls <= 0
		OR vicidial_calls IS NULL
	)
        
-- Eleccion si se marca no contacto y sin gestion
	AND (
        tipificacion_mejor_gestion_soul IS NULL
        OR tipo_mejor_gestion IS NULL
        
#        OR tipo_mejor_gestion = 'No Contacto'
#        OR tipificacion_mejor_gestion_soul IN ('No Contestan', 'Grabadora o Buzon', 'Cliente Cuelga La Llamada')
	)

-- De aca para abajo no cambia, solo en casos especiales
	AND DATE_FORMAT(fecha_fin_vigencia_actual, '%%m%%d') 
	BETWEEN  DATE_FORMAT(CURDATE() + INTERVAL 1 DAY, '%%m%%d') AND DATE_FORMAT(CURDATE() + INTERVAL 15 DAY, '%%m%%d')
	
    AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 1 DAY
	)
	AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)
    
ORDER BY  fecha_asignacion DESC, vicidial_calls asc, tipificacion_ultima_gestion_soul ASC, tipo_phone asc