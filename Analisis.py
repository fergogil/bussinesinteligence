############### VOLUMEN #################
import pandas as pd
import time

# Medimos el tiempo para ver la velocidad de procesamiento
inicio = time.time()

# Cargamos los 2 millones de filas
# Usamos una técnica de "low_memory=False" para que Python sea más eficiente
df = pd.read_csv('Recursos_humanos.csv', low_memory=False)

fin = time.time()

print(f"✅ ¡Éxito! Se cargaron {len(df):,} registros.")
print(f"⏱️ Tiempo de carga: {round(fin - inicio, 2)} segundos.")

# Mostramos un resumen de las columnas que tiene tu archivo
print("\n--- Estructura de tus datos ---")
print(df.info())

# Vistazo a los primeros datos
print("\n--- Primeras 5 filas ---")
display(df.head())


################ VELOCIDAD ####################
# 1. Análisis de Nómina Masiva
print("--- 💰 Análisis de Salarios por Departamento ---")
inicio = time.time()
reporte_salarios = df.groupby('Department')['Salary'].agg(['mean', 'max', 'min', 'count']).round(2)
fin = time.time()
print(reporte_salarios)
print(f"\n⏱️ Tiempo de procesamiento: {round(fin - inicio, 4)} segundos.")

# Buscar a todos los empleados de un país específico con alto desempeño
print("\n--- 🔍 Filtro Complejo: Países y Desempeño ---")
inicio = time.time()
filtro = df[(df['Country'] == 'Germany') & (df['Performance_Rating'] == 'Excellent')]
fin = time.time()
print(f"Se encontraron {len(filtro):,} empleados que cumplen el criterio.")
print(f"⏱️ Tiempo de búsqueda: {round(fin - inicio, 4)} segundos.")


################ VARIEDAD Y/O VERACIDAD ################
# ¿Qué tan confiables son mis datos? (Veracidad) 
print("--- 🛠️ Chequeo de Calidad de Datos ---") 
nulos = df.isnull().sum() print("Columnas con datos faltantes:") print(nulos[nulos > 0]) 
# ¿Cuál es el promedio de salario por nivel de trabajo y modo de trabajo? 
# Esto crea una tabla cruzada (como una dinámica pero instantánea) 
pivot = df.pivot_table(values='Salary', index='Job_Level', columns='Work_Mode', aggfunc='mean').round(2) 
print("\n--- 📊 Matriz Salarial (Nivel vs Modalidad) ---") 
print(pivot)


############### VISUALIZACIÓN ######################
import matplotlib.pyplot as plt
import seaborn as sns

# Configuramos el estilo visual
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 10))

# 1. ¿Cómo se distribuyen los salarios por Nivel de Trabajo? (Boxplot)
# El Boxplot es perfecto para ver el "Volumen" y detectar "Outliers" (valores atípicos)
plt.subplot(2, 2, 1)
sns.boxplot(x='Job_Level', y='Salary', data=df, palette='Set2')
plt.title('Distribución Salarial por Nivel')

# 2. ¿Cuál es la tendencia de contrataciones a través de los años? (Line chart)
# Aquí vemos la evolución histórica de nuestro volumen de datos
plt.subplot(2, 2, 2)
df_years = df.groupby('Hire_Year').size()
df_years.plot(kind='line', marker='o', color='teal')
plt.title('Contrataciones por Año')
plt.ylabel('Cantidad de Empleados')

# 3. Relación entre Edad y Salario (Histograma 2D / Hexbin)
# En Big Data, para evitar que los puntos se amontonen, usamos "densidad"
plt.subplot(2, 2, 3)
plt.hexbin(df['Age'], df['Salary'], gridsize=30, cmap='Blues')
plt.colorbar(label='Densidad de Empleados')
plt.title('Densidad: Edad vs Salario')
plt.xlabel('Edad')
plt.ylabel('Salario')

# 4. Distribución del Desempeño (Pie Chart)
plt.subplot(2, 2, 4)
df['Performance_Rating'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Calificación de Desempeño General')
plt.ylabel('')

plt.tight_layout()
plt.show()


