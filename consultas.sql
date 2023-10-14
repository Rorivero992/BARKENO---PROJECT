USE barkeno_project;
SELECT SUM(b.pax_real), B.dia_reserva, B.id_visita, B.dia_visita, B.hora_visita, B.id_idioma_visita, B.id_origen_reserva, B.realitzat, M.prec
FROM df_barkeno3 B
JOIN data_metereologico M
ON b.dia_visita = M.fecha
GROUP BY B.dia_reserva, B.dia_reserva, B.id_visita, B.dia_visita, B.hora_visita, B.id_idioma_visita, B.id_origen_reserva, B.realitzat, M.prec
ORDER BY B.dia_reserva; 

-- AGRUPARE POR DIAS LAS RESERVAS DE BARKENO. 
SELECT dia_visita, SUM(pax_real)
FROM df_barkeno2
where realitzat = 0
GROUP BY dia_visita
ORDER BY dia_visita;

-- 	QUERY con datos meteorologicos 

SELECT b.*, M.prec, M.tmed, M.tmin, M.tmax, M.racha
FROM df_barkeno3 B
JOIN data_metereologico M
ON b.dia_visita = M.fecha
ORDER BY B.dia_reserva; 

-- analisis de variables climantologicas. 
SELECT max(racha) FROM data_metereologico;  

-- ANALISIS DIFERENCIA DE DIAS 

SELECT DISTINCT(diferencia_dias) FROM df_barkeno2;


