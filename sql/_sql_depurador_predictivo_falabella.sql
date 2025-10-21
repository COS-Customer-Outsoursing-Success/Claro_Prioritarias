WITH base AS (
    SELECT *,
        CASE 
            WHEN excluir = 1        
              OR placa IN (
					SELECT placa 
					FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_no_aptos 
					WHERE periodo = 202510)
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
    FROM bbdd_cos_bog_grupo_axa.tb_asignacion_falabella_v2_coalesce
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
# and tasa < 0.03
# and prima_temporario_plus > 2500000

-- -----------------------------------------------------------------------------------------
-- Consultar Placas													  -- 
-- -----------------------------------------------------------------------------------------
/*
and placa IN (
'LOW543',
'GST854',
'NLR314',
'NFN449',
'KXM356',
'LMR092',
'LRS420',
'KQS442',
'PIR958',
'NQR344',
'NUL691',
'LWZ920',
'NUZ923',
'JYU088',
'LTT030',
'NMS933',
'NXQ271',
'LMQ007',
'LQL425',
'JXW904',
'DUR341',
'GHY162',
'KRW564',
'JRP716',
'JHV180',
'LMS619',
'KVT922',
'FKL652',
'EPP754',
'NLS493',
'NLS917',
'LZR262',
'JOS850',
'LMR677',
'JXT207',
'LTT189',
'NXR662',
'LYW314',
'NXQ870',
'LFN842',
'LFO138',
'NTX087',
'LYV617',
'LOV605',
'NXT869',
'KOM663',
'NQR189',
'NUL736',
'KNP993',
'FVW094',
'JHL234',
'LMQ909',
'HTY098',
'NQN398',
'KXW001',
'JJQ824',
'NFN887',
'KNX572',
'NFN761',
'LMU435',
'GZO781',
'FOZ021',
'FXR189',
'EPS603',
'EGM737',
'DXM532',
'KRP964',
'LMT437',
'MXY187',
'GWP090',
'NIO891',
'KQZ143',
'LKU072',
'LLK186',
'HFQ221',
'JLM662',
'JXV325',
'NBL354',
'KPV040',
'NXU735',
'NML862',
'DON364',
'JXQ738',
'FZU061',
'LQT762',
'FRU269',
'NGU871',
'GRL769',
'IGO637',
'PHR875',
'HRW487',
'IEP915',
'DJP960',
'NXU693',
'MCQ966',
'JNQ411',
'GWT631',
'IMW417',
'KUP036',
'NHZ179',
'IXW701',
'NHX213',
'LOZ490',
'KTT593',
'FNX172',
'GWW289',
'LRU981',
'EGZ187',
'KUQ935',
'LMX009',
'NTX493',
'EPU816',
'FIW863',
'NVX207',
'KOP362',
'LRY923',
'LIM540',
'KRR465',
'NLZ837',
'JVO301',
'IJX371',
'GSZ631',
'KOM504',
'KVX295',
'JDX924',
'NMV022',
'JMV120',
'MYK641',
'KSL882',
'IKT821',
'JSO210',
'IFV751',
'DJY042',
'FUV145',
'LMX762',
'JPV443',
'LRO999',
'NUL920',
'KQN233',
'KRU019',
'JQU733',
'JCR763',
'NLT554',
'LOM771',
'NON118',
'KTY913',
'EOO822',
'NKZ491',
'GPN056',
'LQV114',
'NLV601',
'JMT274',
'JSR149',
'GLY050',
'NUM021',
'NTX639',
'NTY033',
'NWL753',
'NPQ811',
'HRW469',
'NTW486',
'NYL133',
'LGX173',
'LYZ484',
'NTY033',
'NWL753',
'NPQ811',
'HRW469',
'LKY797',
'NTW486',
'NYL133',
'LGX173',
'LYZ484'
)

*/
-- -----------------------------------------------------------------------------------------
-- Consultar seguimientos sin gestion													  -- 
-- -----------------------------------------------------------------------------------------
/*
and placa in (
	select address2
	FROM bbdd_cos_bog_grupo_axa.tb_marcaciones_desgloce_dts_v2
	where DATE_FORMAT(call_date, '%%Y%%m%%d') 
	BETWEEN  DATE_FORMAT("2025-10-01", "%%Y%%m%%d") AND DATE_FORMAT("2025-10-17", "%%Y%%m%%d")
	and tipificacion = 'Volver A Llamar'
	and campaign_id IN ('AXA_FA10', 'AXA_FAL4', 'AXA_FAL2', 'AXA_FAL5', 'AXA_FAL3')
	) 

*/

#and left(no_temporario_plus, 5) = 16181
#AND tipo_phone IN ("telefono1") #,"telefono2"
#AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
#	BETWEEN  DATE_FORMAT("2025-10-10", "%%m%%d") AND DATE_FORMAT("2025-10-13", "%%m%%d");


-- -----------------------------------------------------------------------------------------
-- Predictivo Sin Gestion: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------
#and left(no_temporario_plus,5) = 16181
#and placa = 'EOM395'
/*
    #AND aseguradora_actual IN ("ALLIANZ", "HDI-LIBERTY")
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND (
		vicidial_calls = 0 
        OR 
        vicidial_calls IS NULL
        )
    
    AND tipificacion_mejor_gestion_soul IS NULL
          
	AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") #= DATE_FORMAT('2025-10-10', "%%m%%d")	 
	BETWEEN  DATE_FORMAT("2025-10-08", "%%m%%d") AND DATE_FORMAT("2025-10-12", "%%m%%d")
     
#   AND prioridad = "POTENCIAL PREMIUM"
#	AND prioridad IN ("ALTO POTENCIAL")
#   AND prioridad IN ("NORMAL")


*/

-- -----------------------------------------------------------------------------------------
-- Predictivo No Contacto: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------
#and left(no_temporario_plus, 5 ) = 16181
#and placa NOT IN ('KOV619')
#/*

	and tipo_phone IN ("telefono1") #,"telefono2"
		
		AND ( 
		vicidial_calls <= 6
		AND 
		vicidial_calls IS NOT NULL 
		)

		AND Tipificacion_mejor_gestion_soul IN ("No Contestan") #or
        #Tipificacion_mejor_gestion_soul IS NULL)#


		AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
		BETWEEN  DATE_FORMAT("2025-10-21", "%%m%%d") AND DATE_FORMAT("2025-10-31", "%%m%%d")
		
	#	AND tipificacion_mejor_gestion IN ("Agent Not Available", "Agent Altnum", "No Contacto","ADAIR")    
	#	AND tipificacion_mejor_gestion NOT IN ("Agent Not Available", "Agent Altnum", "No Contacto","ADAIR")
		
	#     AND prioridad NOT IN ("POTENCIAL PREMIUM") #   
		 AND prioridad IN ("BUEN POTENCIAL") #, "BUEN POTENCIAL"
	#    AND prioridad IN ("NORMAL")

#*/

-- -----------------------------------------------------------------------------------------
-- Blaster : Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- --------------------------------------b---------------------------------------------------

/*
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND ( 
    vicidial_calls <= 3
    AND 
    vicidial_calls IS NOT NULL 
    )

    AND (
    tipificacion_mejor_gestion_soul = "No Contestan" 
    OR 
    tipificacion_mejor_gestion_soul IS NULL
    )
    
    AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
	BETWEEN  DATE_FORMAT("2025-09-01", "%%m%%d") AND DATE_FORMAT("2025-09-14", "%%m%%d")

    AND tipo_ultima_gestion <> "Blaster - Contacto"
    AND tipo_mejor_gestion <> "Blaster - Contacto"
*/

-- -----------------------------------------------------------------------------------------
-- Seguimientos Manuales: Descomentar colocando un # al inicio de los simbolos "/*" ---- --
-- -----------------------------------------------------------------------------------------

/*
    AND vicidial_calls <= 10
	AND (tipificacion_ultima_gestion_soul IN ("Cliente solicita envío de cotización", "Llamar después")
	
    AND DATE_FORMAT(fecha_ultima_gestion_soul, "%%m%%d") 
	BETWEEN  DATE_FORMAT(CURDATE() - INTERVAL 5 DAY, "%%m%%d") AND DATE_FORMAT(CURDATE(), "%%m%%d")
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
	AND tipo_phone IN ("telefono1") #,"telefono2"
	AND (vicidial_calls = 0 OR vicidial_calls IS NULL)
	AND DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") 
	BETWEEN DATE_FORMAT("2025-09-11", "%%m%%d") AND DATE_FORMAT("2025-09-25", "%%m%%d")
*/
-- ---------------------------------------------------------------------------- --
-- No comentar esta parte, evita que se marquen registros marcados entre hoy y ayer
-- ---------------------------------------------------------------------------- --
#/*
    AND (
		fecha_ultima_gestion IS NULL OR DATE(fecha_ultima_gestion) < CURDATE() - INTERVAL 1 DAY
	)
	AND (
		fecha_ultima_gestion_soul IS NULL OR DATE(fecha_ultima_gestion_soul) < CURDATE() - INTERVAL 1 DAY
	)


#*/
ORDER BY DATE_FORMAT(fecha_fin_vigencia_actual, "%%m%%d") ASC, prima_temporario_plus DESC, tasa ASC, vicidial_calls ASC, tipo_phone ASC, prioridad ASC
;