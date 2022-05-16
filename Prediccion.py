from Functions import *
from Rates import Population
# Para realizar productos cartesianos de muchas listas
from itertools import product
from scipy.stats import t


# Se lee la base de datos
f = "GtoDatOK150322 - GtoDatOK291020.csv"
df = pd.read_csv(f, header=1) #Para Guanajuato: 1; Para México: 0
df.head()

# Se leen las listas de recuperados, difuntos e infectados acumulados
infectados_acumulados = np.array( pd.to_numeric(df["Positivos"]).sort_values() )
recuperados_acumulados = np.array( pd.to_numeric(df["Recuperados"]).sort_values() )
difuntos_acumulados = np.array( pd.to_numeric(df["Muertos"]).sort_values() )
vacunados_acumulados =np.array(pd.to_numeric(df["Vacunados"]).sort_values())


# Se construyen los infectados activos y los inmunes con las listas anteriores
inmunes_acumulados = np.array( recuperados_acumulados + difuntos_acumulados )
infectados_activos = np.array( infectados_acumulados - inmunes_acumulados )


#Si queremos comparar las predicciones con los valores reales, quitamos algunos días de la lista y 
#guardamos los valores eliminados en un diccionario.
dias_de_corte=0
if dias_de_corte!=0:
    numero_de_corte=len(infectados_acumulados)-dias_de_corte
    valores_reales = {"Infectados":[i for i in infectados_acumulados[numero_de_corte:]],
                    "Recuperados":[i for i in recuperados_acumulados[numero_de_corte:]],
                    "Difuntos":[i for i in difuntos_acumulados[numero_de_corte:]],
                    "Inmunes": [i for i in inmunes_acumulados[numero_de_corte:]],
                    "Infectados activos":[i for i in infectados_activos[numero_de_corte:]],
                    "Vacunados acumulados":[i for i in vacunados_acumulados[numero_de_corte:] ] }

for i in range(dias_de_corte):
      infectados_activos=np.delete(infectados_activos,-1)
      recuperados_acumulados=np.delete(recuperados_acumulados,-1)
      difuntos_acumulados=np.delete(difuntos_acumulados,-1)
      inmunes_acumulados=np.delete(inmunes_acumulados,-1)
      infectados_acumulados=np.delete(infectados_acumulados,-1)
      vacunados_acumulados=np.delete(vacunados_acumulados,-1)
      

Poblacion = Population(infected_people=infectados_acumulados,
                        recovered_people=recuperados_acumulados,
                        dead_people=difuntos_acumulados,
                        vaxinated_people=vacunados_acumulados,
                        infection_rate=0.1,
                        population_number=6.137e6)
                        

gamma, gamma_error=Poblacion.effective_infection_rate()
beta, beta_error=Poblacion.transmition_rate_S(gamma)
rho, rho_error=Poblacion.inmune_recovered_relation()
delta, delta_error=Poblacion.inmune_dead_relation()
parametros_vacuna,vacuna_error=Poblacion.vaccunation_vel()



# Parámetros del sistema
poblacion_total = 6.0e6 #Para Guanajuato: 6.0e6; Para México: 128.9e6
tasa_deteccion = 0.1
tasa_deteccion_error = 0.0296

# Parámetros del análisis
dias_a_predecir = 31
dias_de_analisis = 7

# Períodos de predicción y análisis
numero_datos = len (infectados_activos)
beta_log_ajuste = np.poly1d(beta)
periodo_de_prediccion = np.array(range(numero_datos-1,
                                       numero_datos+dias_a_predecir)) #Inicia en el último día

periodo_de_analisis = np.array(range(numero_datos-dias_de_analisis,
                                       numero_datos))
# Se realiza la predicción
infectados_predichos, inmunes_predichos = resolver_SIR(infectados_activos[-1],
                                                       inmunes_acumulados[-1],
                                                       gamma, beta_log_ajuste,
                                                       tasa_deteccion,
                                                       poblacion_total,
                                                       periodo_de_prediccion)
# Se hace un ajuste de los valores predichos
infectados_ajuste = np.poly1d( np.polyfit(periodo_de_prediccion, infectados_predichos, 2) )
inmunes_ajuste = np.poly1d( np.polyfit(periodo_de_prediccion, inmunes_predichos, 2) )

# Se definen las poblaciones de análisis, que incluyen los últimos valores reportados en el dataset
infectados_analisis = infectados_activos[numero_datos-dias_de_analisis:]
inmunes_analisis = inmunes_acumulados[numero_datos-dias_de_analisis:]

# Se realiza el análisis para obtener intervalos de confianza y de predicción del 95%
infectados_confianza, infectados_prediccion = intervalos_confianza_prediccion(periodo_de_analisis,
                                                                              periodo_de_analisis,
                                                                              infectados_analisis,
                                                                              infectados_ajuste(periodo_de_analisis),
                                                                              3)

inmunes_confianza, inmunes_prediccion = intervalos_confianza_prediccion(periodo_de_analisis,
                                                                        periodo_de_analisis,
                                                                              inmunes_analisis,
                                                                              inmunes_ajuste(periodo_de_analisis),
                                                                              3)
# Cotas óptimas
menos_cero_mas = np.array(range(-1,2))


# Vectores de incertidumbres
Gamma = gamma + np.multiply(gamma_error, menos_cero_mas)
Beta_0 = beta[0] + np.multiply(beta_error[0], menos_cero_mas)
Beta_1 = beta[1] + np.multiply(beta_error[1], menos_cero_mas)

Infectados = infectados_activos[-1] + np.multiply(infectados_confianza[-1], menos_cero_mas)
Inmunes = inmunes_acumulados[-1] + np.multiply(inmunes_confianza[-1], menos_cero_mas)

Deteccion = tasa_deteccion + np.multiply(tasa_deteccion_error, menos_cero_mas)

# Cantidades auxiliares para la selección de las cotas más amplias y aptas
infectados_cota_superior = infectados_predichos.copy()
infectados_cota_inferior = infectados_predichos.copy()

inmunes_cota_superior = inmunes_predichos.copy()
inmunes_cota_inferior = inmunes_predichos.copy()

error_inf_up = 0.
error_inf_down = 0.

error_inm_up = 0.
error_inm_down = 0.

# En el for se coloca un producto cartesiano de las listas a iterar
# para no anidar muchos for y mejorar la lectura del código
for inf, inm, g, b0, b1, k in product(Infectados, Inmunes, Gamma,
                                      Beta_0, Beta_1, Deteccion):
  # Se define la función del logaritmo de beta con los errores
  b = np.poly1d([b0, b1])

  # Se evita que los infectados iniciales con los que se evolucionará
  # el modelo sean negativos
  if inf<0:
    inf = 0
  

  # Se hace una predicción con los valores de incertidumbre
  pred_inf, pred_inm = resolver_SIR(inf, inm, g, b, k, poblacion_total, periodo_de_prediccion)
            
  # Se revisa si es una solución razonable, es decir,
  # una solución en la que los inmunes que no crecen demasiado rápido o
  # cotas inferiores inservibles
  tendencia_inmunes = (inmunes_acumulados[-1]-inmunes_acumulados[-dias_de_analisis])/dias_de_analisis
  tendencia_prediccion = (pred_inm[-1]-inmunes_acumulados[-1])/dias_a_predecir

  condicion_arriba_inm = (tendencia_prediccion<np.log2(dias_a_predecir)*tendencia_inmunes and inmunes_predichos[-1]<=pred_inm[-1])
  condicion_abajo_inm =  inmunes_predichos[-1]>=pred_inm[-1] and vector_menor_que_vector(np.zeros(len(pred_inm))-1, pred_inm)
  if condicion_arriba_inm or condicion_abajo_inm: 

    # Se definen los errores de esa predicción
    temp_inm = error_cuadratico_medio(pred_inm, inmunes_predichos)

    # Se revisa si las cotas son mayores e igual de aptas que alguna otra
    # que ya se use
    if ( error_inm_up<temp_inm ) and ( vector_menor_que_vector(inmunes_predichos, pred_inm) ):
      inmunes_cota_superior = pred_inm.copy()
      error_inm_up = temp_inm

    if ( error_inm_down<temp_inm ) and ( vector_menor_que_vector(pred_inm, inmunes_predichos) ):
      # Se evita que los inmunes iniciales con los que se evolucionará el
      # modelo no sean menores al último valor reportado
      if inm>=inmunes_acumulados[-1]:
        inmunes_cota_inferior = pred_inm.copy()
        error_inm_down = temp_inm


  # Se repite lo propio con los infectados
  tendencia_infectados = (infectados_activos[-1]-infectados_activos[-dias_de_analisis])/dias_de_analisis
  tendencia_prediccion = (pred_inf[-1]-infectados_activos[-1])/dias_a_predecir


  ######################################################################
  # HIPOTESIS: EL LOGARITMO NO NECESARIAMENTE ES LOG2, SINO LOG BASE R_0
  ######################################################################

  condicion_arriba_inf = (abs(tendencia_prediccion)<np.log2(dias_a_predecir)*abs(tendencia_infectados) and infectados_predichos[-1]<=pred_inf[-1])
  condicion_abajo_inf = (infectados_predichos[-1]>=pred_inf[-1] and (vector_menor_que_vector(np.zeros(len(pred_inf))-1, pred_inf)))
  if condicion_arriba_inf or condicion_abajo_inf: 

    # Se definen los errores de esa predicción
    temp_inf = error_cuadratico_medio(pred_inf, infectados_predichos)

    # Se revisa si las cotas son mayores e igual de aptas que alguna otra
    # que ya se use
    if ( error_inf_up<temp_inf ) and ( vector_menor_que_vector(infectados_predichos, pred_inf) ):
      infectados_cota_superior = pred_inf.copy()
      error_inf_up = temp_inf
              
    if ( error_inf_down<temp_inf ) and ( vector_menor_que_vector(pred_inf, infectados_predichos) ):
      infectados_cota_inferior = pred_inf.copy()
      error_inf_down = temp_inf

reporte_eje_x = np.array( range(numero_datos-30, numero_datos) )


if dias_de_corte>0:
  predicciones_graficas(reporte_eje_x, infectados_activos,
                      infectados_cota_inferior, infectados_predichos,
                      infectados_cota_superior, periodo_de_prediccion,
                      {"nombre": "Infected people"},
                      valores_comparacion=valores_reales["Infectados activos"],
                      dias_extra=dias_de_corte)
else:
  predicciones_graficas(reporte_eje_x, infectados_activos,
                      infectados_cota_inferior, infectados_predichos,
                      infectados_cota_superior, periodo_de_prediccion,
                      {"nombre": "Infected people"})
if dias_de_corte>0: 
  predicciones_graficas(reporte_eje_x, recuperados_acumulados,
                      inmunes_cota_inferior, inmunes_predichos,
                      inmunes_cota_superior, periodo_de_prediccion,
                      {"nombre": "Recovered",
                       "escala": rho,
                       "error": rho_error},
                      valores_comparacion=valores_reales["Recuperados"],
                      dias_extra=0)
else:
  predicciones_graficas(reporte_eje_x, recuperados_acumulados,
                      inmunes_cota_inferior, inmunes_predichos,
                      inmunes_cota_superior, periodo_de_prediccion,
                      {"nombre": "Recovered",
                       "escala": rho,
                       "error": rho_error})
if dias_de_corte>0: 
  predicciones_graficas(reporte_eje_x, recuperados_acumulados,
                      inmunes_cota_inferior, inmunes_predichos,
                      inmunes_cota_superior, periodo_de_prediccion,
                      {"nombre": "Recovered",
                       "escala": rho,
                       "error": rho_error},
                      valores_comparacion=valores_reales["Recuperados"],
                      dias_extra=0)
else:
  predicciones_graficas(reporte_eje_x, difuntos_acumulados,
                      inmunes_cota_inferior, inmunes_predichos,
                      inmunes_cota_superior, periodo_de_prediccion,
                      {"nombre": "Deceased",
                       "escala": delta,
                       "error": delta_error})
rho_up = rho+rho_error
rho_down = rho-rho_error
delta_up = delta+delta_error
delta_down = delta-delta_error

prediction_info = {
  "infected":[infectados_cota_inferior[-1],
            infectados_predichos[-1],
            infectados_cota_superior[-1]],
  "recovered":[rho_down[0]*inmunes_cota_inferior[-1]+rho_down[1],
              rho[0]*inmunes_predichos[-1]+rho[1],
              rho_up[0]*inmunes_cota_superior[-1]+rho_up[1]],
  "deceased":[delta_down[0]*inmunes_cota_inferior[-1]+delta_down[1],
            delta[0]*inmunes_predichos[-1]+delta[1],
            delta_up[0]*inmunes_cota_superior[-1]+delta_up[1]]
  }

pass
