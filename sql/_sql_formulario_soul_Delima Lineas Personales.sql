SELECT 
	distinct documento0 AS 'Documento',
    `email-tomador2` AS 'Email Tomador',
    nombre1 AS 'Nombre',
    `fecha-final-vigencia3` AS 'Fecha Final Vigencia',
    `telefono-asegurado-215` AS 'Telefono Tomador',
    `ciudad-inmueble17` AS 'Ciudad Inmueble',
    `desc-ramo4` AS 'Desc Ramo',
    `nombre-compania5` AS 'Nombre Compañía',
    `poliza-agrupadora6` AS 'Póliza Agrupadora',
    `poliza-individual7` AS 'Póliza Individual',
    `telefono-tomador-29` 'Telefono Tomador 2',
    `telefono-tomador-310` AS 'Telefono Tomador 3',
    `telefono-tomador8` AS 'Telefono Tomador Res',
    `direccion-inmueble16` AS 'Dirección Inmueble',
    `tipo-bien18` AS 'Tipo Bien',
    `telefono-tomador-oficina12` AS 'Telefono Tomador Oficina',
    `telefono-tomador8` AS 'Celular Tomador',
    `telefono-asegurado-114` AS 'Telefono Asegurado 1',
    `telefono-asegurado-215` AS 'Telefono Asegurado 2'
FROM bbdd_cos_bog_delima.tb_soul2_847_lineas_personales_generales_inbound_crm2
where documento0 = 38867755;