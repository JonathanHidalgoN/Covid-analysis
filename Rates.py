#Importamos la libreria con nuestras funciones.
from tkinter import N
from Functions import *
# Para análisis de datos
import pandas as pd
import numpy as np
# Para realizar productos cartesianos de muchas listas
from itertools import product

class Population():
                
  def __init__(self, infected_people, recovered_people,
              dead_people,vaxinated_people,infection_rate=None,
              population_number=None, dates=None):
    
    self.population_number = 6.167e6 if population_number is None else population_number
    self.infection_rate= 0.1 if infection_rate is None else infection_rate
    self.infected_people = infected_people
    self.recovered_people =recovered_people
    self.dead_people = dead_people
    self.inmune_people = self.recovered_people+self.dead_people
    self.active_infected_people = self.infected_people-self.inmune_people
    self.data_number = len(self.recovered_people)
    self.dates = [i for i in range(self.data_number)] if dates is None else dates
    self.last_date = self.dates[-1]
    self.vaxinated_people = vaxinated_people

  

  def effective_infection_rate(self,graph=None):
    #
    # Se ajusta con los datos de los últimos 150 días
          gamma_eje_x = self.active_infected_people[self.data_number-151:]
          gamma_eje_y = np.diff(self.inmune_people[self.data_number-152:])

          gamma, gamma_varianza = curve_fit( proporcionalidad,
                                            gamma_eje_x,
                                            gamma_eje_y)

          # Se calcula el error estándar de la pendiente
          gamma = gamma[0]
          gamma_error = np.sqrt(gamma_varianza[0][0])

          if graph is not None: grafica_con_intervalos(gamma_eje_x, gamma_eje_y, gamma*gamma_eje_x,
                                lambda x: gamma*x, 1, {"title": "Ajuste de la tasa de recuperación efectiva",
                                "x": "Infectados activos", "y": "Inmunes acumulados diarios"})
          else : pass
          return(gamma,gamma_error)

      


  def transmition_rate_S(self,gamma=None,graph=None):
    #
    if gamma is None:
      gamma = self.effective_infection_rate()

    # Se ajusta con los datos de los últimos 30 días
    # Se define que el primer registro es el día cero del análisis
    beta_eje_x = np.array(range(self.data_number-31, self.data_number))

    beta_eje_y = np.diff(self.active_infected_people[ (self.data_number-2) -30:])
    beta_eje_y = np.divide(beta_eje_y, self.active_infected_people[ (self.data_number-1) -30:]) + gamma

    index = np.where(beta_eje_y<1e-8)
    beta_eje_y = np.delete(beta_eje_y,index)
    beta_eje_x = np.delete(beta_eje_x,index)

    beta_log_eje_y = np.log(beta_eje_y)

    beta, beta_varianza = np.polyfit(beta_eje_x, beta_log_eje_y, 1, cov=True)

    # Se calcula el error estándar de la pendiente
    beta_error = np.sqrt([beta_varianza[0][0], beta_varianza[1][1]])

    # Para evaluar el ajuste
    beta_log_ajuste = np.poly1d(beta)

    if graph is not None: grafica_con_intervalos(beta_eje_x, beta_eje_y, np.exp(beta_log_ajuste(beta_eje_x)),
                            lambda x: np.exp(beta_log_ajuste(x)), 2,
                            {"title": "Ajuste de la tasa de transmisión",
                              "x": "Días", "y": r"$\beta_S$"})
    else: pass
    return(beta,beta_error)
  

  def inmune_recovered_relation(self,graph = None):
    dias_de_ajuste_rho = dias_de_ajuste_optimo(self.inmune_people[:],
                                              self.recovered_people[:], self.data_number)

    # Se ajusta con los datos de los últimos 150 días
    rho_eje_x = self.inmune_people[self.data_number-dias_de_ajuste_rho:]
    rho_eje_y = self.recovered_people[self.data_number-dias_de_ajuste_rho:]

    rho, rho_varianza = np.polyfit(rho_eje_x, rho_eje_y, 1, cov=True)

    # Se calcula el error estándar de la pendiente
    rho_error = [np.sqrt(rho_varianza[0][0]), np.sqrt(rho_varianza[1][1])]

    if graph is not None: grafica_con_intervalos(rho_eje_x, rho_eje_y, rho[0]*rho_eje_x+rho[1],
                          lambda x: rho[0]*x+rho[1], 2,
                          {"title": "Relación entre recuperados e inmunes",
                            "x": "Inmunes acumulados", "y": "Recuperados acumulados"})
    else : pass
    return(rho,rho_error)

  def inmune_dead_relation(self,graph=None):
    dias_de_ajuste_delta = dias_de_ajuste_optimo(self.inmune_people[:],
                                          self.dead_people[:], self.data_number)

    # Se ajusta con los datos de los últimos 150 días
    delta_eje_x = self.inmune_people[ self.data_number-dias_de_ajuste_delta:]
    delta_eje_y = self.dead_people[ self.data_number-dias_de_ajuste_delta:]

    delta, delta_varianza = np.polyfit(delta_eje_x, delta_eje_y, 1, cov=True)

    # Se calcula el error estándar de la pendiente
    delta_error = [np.sqrt(delta_varianza[0][0]), np.sqrt(delta_varianza[1][1])] 
        
        
        
    if graph is not None:
      grafica_con_intervalos(delta_eje_x, delta_eje_y, delta[0]*delta_eje_x+delta[1],
                            lambda x: delta[0]*x+delta[1], 2,{"title": "Relación entre difuntos e inmunes",
                            "x": "Inmunes acumulados", "y": "Difuntos acumulados"})
      plt.show()
    else :pass
    return(delta,delta_error)
    
    
  def vaccunation_vel(self,graph=None):
    
    #Quitamos los 0´s de nuetro vector de vacunación
    Vaux=self.vaxinated_people[np.where(self.vaxinated_people!=0)]
    #Revisamos el primer dia de vacunacion
    primer_dia_vacunacion=self.data_number-len(Vaux)-1
    eje_vac=[]
    Vnew=[]
    for i,_ in enumerate(Vaux):
      if self.vaxinated_people[i+primer_dia_vacunacion]!=self.vaxinated_people[i+primer_dia_vacunacion-1]:
        eje_vac.append(i+primer_dia_vacunacion+1)
        Vnew.append(self.vaxinated_people[i+primer_dia_vacunacion])

    ajuste_vac=np.polyfit(eje_vac,Vnew,1)
    eje_y_vac=np.array ([ (Vnew[i+1]-Vnew[i])/(eje_vac[i+1]-eje_vac[i]) for i in range(len(eje_vac)-1) ])
    eje_vac.pop()
    v_vacunacion,v_vacunacion_varianza=np.polyfit(eje_vac,eje_y_vac,1,cov=True)

    v_vacunacion_error = [np.sqrt(v_vacunacion_varianza[0][0]), np.sqrt(v_vacunacion_varianza[1][1])]
    eje_vac=np.array(eje_vac)
        
    if graph is not None:    
      #Me falta agregar comentarios pero primero entender bien el codigo
      plt.scatter(eje_vac,eje_y_vac)
      plt.plot(eje_vac,v_vacunacion[0]*eje_vac+v_vacunacion[1])
    else : pass
    return(v_vacunacion,v_vacunacion_error)