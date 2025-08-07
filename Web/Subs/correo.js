  // Función para obtener la IP pública
  async function obtenerIP() {
    try {
      const respuesta = await fetch('https://api.ipify.org?format=json');
      const datos = await respuesta.json();
      
      // Mostrar la IP en la página
      document.getElementById('direccion').textContent = "Dirección IP: " + datos.ip;
      document.getElementById('estado').textContent = "Estado: Captura completada";
      
      // Mensaje técnico de advertencia
      document.getElementById('mensaje').textContent = 
        "⚠ Tu IP está expuesta. Refuerza tu anonimato con VPN/Tor.";
    } catch (error) {
      document.getElementById('mensaje').textContent = "Error al obtener la IP.";
    }
  }

  // Ejecutar al cargar la página
  obtenerIP();