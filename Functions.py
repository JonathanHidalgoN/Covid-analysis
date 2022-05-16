# Para análisis de datos
import pandas as pd
import numpy as np
from scipy.stats import t
import scipy.stats as st


# Para hacer ajustes de curvas
from scipy.optimize import curve_fit

# Para graficar
import matplotlib.pyplot as plt

# Para calcular intervalos de confianza y de predicción
from scipy.stats import t

# Para evolucionar el modelo con integración numérica
from scipy.integrate import odeint

# Una función de proporcionalidad directa
def proporcionalidad(x, a):
  return a*x

def dias_de_ajuste_optimo(arreglo_x, arreglo_y, numero_de_datos):
  diferencia_dias = numero_de_datos
  while True:
    eje_x = arreglo_x[numero_de_datos-diferencia_dias:]
    eje_y = arreglo_y[numero_de_datos-diferencia_dias:]
    
    ajuste, ajuste_varianza = np.polyfit(eje_x, eje_y, 1, cov=True)
    ajuste_error = [np.sqrt(ajuste_varianza[0][0]), np.sqrt(ajuste_varianza[1][1])]

    cota_superior = (ajuste[0]+ajuste_error[0]) * arreglo_x[-1] + ajuste[1]+ajuste_error[1]
    cota_inferior = (ajuste[0]-ajuste_error[0]) * arreglo_x[-1] + ajuste[1]-ajuste_error[1]

    if arreglo_y[-1]<=cota_superior and cota_inferior<=arreglo_y[-1]:

      diferencia_dias_2 = diferencia_dias-1
      error_guia = abs(arreglo_y[-1] - (ajuste[0]*eje_x[-1]+ajuste[1]))
      
      while True:
        eje_x = arreglo_x[numero_de_datos-diferencia_dias_2:]
        eje_y = arreglo_y[numero_de_datos-diferencia_dias_2:]
        
        ajuste, ajuste_varianza = np.polyfit(eje_x, eje_y, 1, cov=True)
        ajuste_error = [np.sqrt(ajuste_varianza[0][0]), np.sqrt(ajuste_varianza[1][1])]

        error_temporal = abs(arreglo_y[-1] - (ajuste[0]*eje_x[-1]+ajuste[1]))

        if error_temporal<=error_guia:
          error_guia = error_temporal
        else:
          return diferencia_dias_2-1
        
        diferencia_dias_2-=1

    diferencia_dias-=1


def error_cuadratico_medio(x, y):
  return np.square( np.subtract(x, y) ).mean()

def vector_menor_que_vector(x, y):
  j=0

  for i in range(len(x)):
    if x[i]<y[i]:
      j=j+1

  return j==len(x)


#Para obtener intervalos de confianza y de predicción
def intervalos_confianza_prediccion(x_continuo, eje_x, datos, ajuste, numero_coeficientes):
  
  #Tamaño de la muestra
  n = len(datos)
  #Grados de libertad
  gdl = n - numero_coeficientes

  #Cálculo del t_value asociado a uno de los extremos de una prueba bilateral
  #usando una distribución t
  t_value = t.ppf(0.975, gdl)

  #Cálculo de residuos
  residuos = datos - ajuste

  #Error estándar
  error = np.sqrt( np.sum(residuos**2) / gdl )

  #Cálculo de los intervalos de confianza
  confianza = t_value * error * np.sqrt( 1/n + ( x_continuo-np.mean(eje_x) )**2 / np.sum( (x_continuo - np.mean(eje_x) )**2 ) ) 
  prediccion = t_value * error * np.sqrt( 1 + 1/n + ( x_continuo-np.mean(eje_x) )**2 / np.sum( (x_continuo - np.mean(eje_x) )**2 ) )

  return [confianza, prediccion]


#Para hacer gráficas con intervalos de confianza y de predicción
def grafica_con_intervalos(eje_x, datos, ajuste, funcion, numero_coeficientes, etiquetas):

  #Se construye un intervalo de valores que tenga los mismos extremos que los datos
  #del eje_x pero que sea más uniforme
  x_continuo = np.linspace(eje_x.min(), eje_x.max(), endpoint=True)
  ajuste_continuo = funcion(x_continuo)

  #Se construyen los intervalos de confianza y de predicción
  confianza, prediccion = intervalos_confianza_prediccion(x_continuo, eje_x, datos,
                                                          ajuste, numero_coeficientes)

  #Se hace la gráfica
  fig, ax = plt.subplots()
  
  #Intervalos de confianza
  ax.fill_between(x_continuo, ajuste_continuo-confianza,
                  ajuste_continuo+confianza, color="#282828", alpha=0.2)

  #Intervalos de predicción
  ax.fill_between(x_continuo, ajuste_continuo-prediccion,
                  ajuste_continuo+prediccion, color="#0D3580", alpha=0.2)

  #Los datos reales y el ajuste teórico
  plt.scatter(eje_x, datos, c="r", marker=".")
  plt.plot(eje_x, ajuste, c="black")

  #Se usa un diccionario para extraer los títulos y etiquetas
  try:
    plt.title(etiquetas["title"])
    plt.ylabel(etiquetas["y"])
    plt.xlabel(etiquetas["x"])

    plt.legend()
    plt.show()

  #Si no hay etiquetas, se imprime una gráfica sin etiquetas
  except:
    plt.show()

#Esta función hace predicciones del modelo SIR
def resolver_SIR(infectados_iniciales, inmunes_iniciales, gamma, beta_S, Kay, N, t):

  #Sistema SIR con beta_S
  def sir_beta_S(y,x):
    #Se lee el vector de infectados e inmunes
    I = y[0]
    R_tilde = y[1]

    #Se calcula el factor escala del término beta_S,
    #dado el valor local de la tasa de detección
    escala = ( 1 - (I+R_tilde) ) / ( 1 - Kay*( I+R_tilde ) )
    

    #Se definen las expresiones de las ecuaciones del modelo SIR
    dI_dt = escala * np.exp( beta_S(x) )*I - gamma*I
    dR_tilde_dt = gamma*I

    return [dI_dt, dR_tilde_dt]

  #Se escalan los datos al caso en el que N=1
  #también se implementa la tasa de detección Kay
  infectados_escalados = infectados_iniciales / (Kay*N)
  inmunes_escalados = inmunes_iniciales / (Kay*N)

  #Se construye el vector de poblaciones para introducir a la función sir_beta_S
  y_0= np.array([infectados_escalados, inmunes_escalados])

  #Se evoluciona el sistema con la función sir_beta_S para el período de tiempo t
  solucion = odeint(sir_beta_S, y_0, t)
  
  #Se extraen las poblaciones predichas y se deshace el escalamiento para que
  #los valores consistan con el dataset con el que se trabaja
  I = Kay*N*solucion[:,0]
  Rtilde = Kay*N*solucion[:,1]

  return [I,Rtilde]


#Función para graficar resultados
def predicciones_graficas(eje_x, datos, cota_inferior, prediccion, cota_superior, periodo, etiquetas,ultima_fecha=None):
    
    numero_datos = len(datos)
    if ultima_fecha is None : ultima_fecha = numero_datos 
    fig, ax = plt.subplots()

    try:
        pendiente = etiquetas["escala"][0]
        pendiente_up = etiquetas["escala"][0] + etiquetas["error"][0]
        pendiente_down = etiquetas["escala"][0] - etiquetas["error"][0]

        interseccion = etiquetas["escala"][1]

        interseccion_up = etiquetas["escala"][1] + etiquetas["error"][1]
        interseccion_down = etiquetas["escala"][1] - etiquetas["error"][1]

        ax.vlines(periodo[0],
                min(datos[numero_datos-30],
                    pendiente_down*cota_inferior[0]+interseccion_down,
                    pendiente_down*cota_inferior[-1]+interseccion_down),
                max(datos[numero_datos-30],
                    pendiente_up*cota_superior[0]+interseccion_up,
                    pendiente_up*cota_superior[-1]+interseccion_up),
                linestyles ="dotted", colors ="#0D3580",label=ultima_fecha)
        
        ax.fill_between(periodo, pendiente_down*cota_inferior+interseccion_down,
                        pendiente_up*cota_superior+interseccion_up, color="#1761B0",
                        edgecolor="0.5", label="Error bounds", alpha=0.25)
        
        ax.fill_between(periodo, pendiente_down*prediccion+interseccion_down,
                        pendiente_up*prediccion+interseccion_up,
                        color="#0D3580", label="Uncertainty", alpha=0.3)
        
        plt.plot(periodo, pendiente*prediccion+interseccion, color="black", label="Prediction")

    except:
        ax.vlines(periodo[0],
                min(datos[numero_datos-30],
                    cota_inferior[0], cota_inferior[-1]),
                max(datos[numero_datos-30],
                    cota_superior[0], cota_superior[-1]),
                linestyles ="dotted", colors ="#0D3580",label=ultima_fecha)

        ax.fill_between(periodo, cota_inferior, cota_superior, color="#1761B0",
                    edgecolor="0.5", label="Error bounds", alpha=0.25)
        plt.ylim([1.2*cota_inferior[-1],1.2*cota_superior[-1]])
        plt.plot(periodo, prediccion, color="black", label="Prediction")
    
    
    
    plt.scatter(eje_x, datos[numero_datos-30:], c="r", marker=".")

    plt.xlabel("Days")
    plt.ylabel(etiquetas["nombre"])
    plt.title(etiquetas["nombre"]+" in function of the day")
    plt.legend(loc="upper left")

    plt.show()


