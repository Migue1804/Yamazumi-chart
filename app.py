import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    st.sidebar.markdown("# Instrucciones")
    st.sidebar.markdown("Por favor sigue las instrucciones paso a paso para utilizar la herramienta correctamente.")
    # Pasos para el Yamazumi Chart
    st.sidebar.markdown("### Pasos:")
    st.sidebar.markdown("- **Paso 1:** Ingresa el Tiempo Takt en minutos.")
    st.sidebar.markdown("- **Paso 2:** Ingresa el número de estaciones de trabajo.")
    st.sidebar.markdown("- **Paso 3:** Para cada estación de trabajo, ingresa el nombre y los tiempos de ciclo, inspección y espera.")
    st.sidebar.markdown("- **Paso 4:** Observa el gráfico que muestra los tiempos por estación de trabajo.")
    st.sidebar.markdown("- **Paso 5:** ¡Listo! Puedes ver los datos ingresados en la tabla debajo del gráfico.")

    st.image("Yamazumi.jpg", width=720)  

    st.sidebar.header("Yamazumi Chart")

    takt_time = st.sidebar.number_input("Ingrese el Tiempo Takt (minutos)", min_value=0.0, step=0.1, value=1.0)  

    num_workstations = st.sidebar.number_input('Número de Estaciones de Trabajo', min_value=0, step=1, value=1, format='%d')

    if num_workstations < 1:
        st.sidebar.warning("Debe ingresar al menos una estación de trabajo.")
        return

    workstation_data = []

    for i in range(num_workstations):
        station_name = st.sidebar.text_input(f'Nombre de la Estación {i+1}')
        st.sidebar.markdown(f"**Estación {i+1}**")  
        operator_cycle_time = st.sidebar.number_input(f'Tiempo de Ciclo del Operador (min) - Estación {i+1}', min_value=0.0, step=0.1, value=0.0)
        machine_cycle_time = st.sidebar.number_input(f'Tiempo de Ciclo de Máquina (min) - Estación {i+1}', min_value=0.0, step=0.1, value=0.0)
        inspection_time = st.sidebar.number_input(f'Inspecciones (min) - Estación {i+1}', min_value=0.0, step=0.1, value=0.0)
        wait_time = st.sidebar.number_input(f'Esperas (min) - Estación {i+1}', min_value=0.0, step=0.1, value=0.0)
        
        workstation_data.append((station_name, operator_cycle_time, machine_cycle_time, inspection_time, wait_time))

    plot_yamazumi_chart(workstation_data, takt_time)

    # Mostrar los datos ingresados en forma de tabla
    df = pd.DataFrame(workstation_data, columns=['Nombre de la Estación', 'Tiempo de Ciclo del Operador', 'Tiempo de Ciclo de Máquina', 'Inspecciones', 'Esperas'])
    st.write(df)

def plot_yamazumi_chart(workstation_data, takt_time):
    labels = [data[0] for data in workstation_data]
    operator_cycle_times = [data[1] for data in workstation_data]
    machine_cycle_times = [data[2] for data in workstation_data]
    inspection_times = [data[3] for data in workstation_data]
    wait_times = [data[4] for data in workstation_data]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(labels, operator_cycle_times, label='Tiempo de Ciclo del Operador', color='green')
    ax.bar(labels, machine_cycle_times, bottom=operator_cycle_times, label='Tiempo de Ciclo de Máquina', color='green', alpha=0.5)
    ax.bar(labels, inspection_times, bottom=np.add(operator_cycle_times, machine_cycle_times), label='Inspecciones', color='yellow')
    ax.bar(labels, wait_times, bottom=np.add(np.add(operator_cycle_times, machine_cycle_times), inspection_times), label='Esperas', color='red')
    ax.axhline(y=takt_time, color='red', linestyle='--', label='Takt Time')

    ax.set_ylabel('Tiempo (minutos)')
    ax.set_xlabel('Estaciones de Trabajo')
    ax.set_title('Yamazumi Chart')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

if __name__ == "__main__":
    main()
