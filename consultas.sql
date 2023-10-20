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

-- ANALISIS DIAS DE LA SEMANA CON MAS RESERVAS Y PROVEEDOR.
WITH ReservasPorSemana AS (
    SELECT
        id_origen_reserva,
        dia_visita,
        SUM(pax_real) AS reservas_por_semana,
        RANK() OVER (PARTITION BY YEARWEEK(dia_visita) ORDER BY SUM(pax_real) DESC) AS ranking
    FROM data_barkeno_transformado
    WHERE realitzat = 1
    GROUP BY id_origen_reserva, dia_visita
)

SELECT
    id_origen_reserva,
    dia_visita,
    reservas_por_semana
FROM ReservasPorSemana
WHERE ranking = 1
ORDER BY reservas_por_semana DESC;

