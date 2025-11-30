<template>
  <div class="diagnostico-form">
    <h2>Formulario de Diagnóstico</h2>

    <form @submit.prevent="enviarDiagnostico" class="formulario">
      <div class="form-group">
        <label for="marca">Marca:</label>
        <input id="marca" v-model="form.marca" required />
      </div>

      <div class="form-group">
        <label for="modelo">Modelo:</label>
        <input id="modelo" v-model="form.modelo" required />
      </div>

      <div class="form-group">
        <label for="anio">Año:</label>
        <input id="anio" type="number" v-model.number="form.anio" required min="1900" max="2100"/>
      </div>

      <div class="form-group">
        <label for="kilometraje">Kilometraje:</label>
        <input id="kilometraje" type="number" v-model.number="form.kilometraje" required min="0"/>
      </div>

      <div class="form-group">
        <label for="ultimo_mantenimiento">Último mantenimiento:</label>
        <input id="ultimo_mantenimiento" type="date" v-model="form.ultimo_mantenimiento" required />
      </div>

      <div class="form-group">
        <label for="descripcion_sintomas">Descripción de síntomas:</label>
        <textarea id="descripcion_sintomas" v-model="form.descripcion_sintomas" required></textarea>
      </div>

      <button type="submit" class="btn-enviar">Enviar</button>
    </form>

    <div v-if="diagnostico" class="resultado">
      <h3>Diagnóstico</h3>
      <ul>
        <li><strong>Falla:</strong> {{ diagnostico.resultado.falla.prediccion }} (Confiabilidad: {{ diagnostico.resultado.falla.confiabilidad }})</li>
        <li><strong>Subfalla:</strong> {{ diagnostico.resultado.subfalla.prediccion }} (Confiabilidad: {{ diagnostico.resultado.subfalla.confiabilidad }})</li>
        <li><strong>Gravedad:</strong> {{ diagnostico.resultado.gravedad.prediccion }} (Confiabilidad: {{ diagnostico.resultado.gravedad.confiabilidad }})</li>
        <li><strong>Solución:</strong> {{ diagnostico.resultado.solucion.prediccion }} (Confiabilidad: {{ diagnostico.resultado.solucion.confiabilidad }})</li>
      </ul>
    </div>

    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
.diagnostico-form {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.formulario .form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  margin-bottom: 0.3rem;
}

input, textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.btn-enviar {
  width: 100%;
  padding: 0.7rem;
  background-color: #007bff;
  color: #fff;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-enviar:hover {
  background-color: #0056b3;
}

.resultado {
  margin-top: 2rem;
  padding: 1rem;
  border-left: 4px solid #007bff;
  background-color: #eef6ff;
  border-radius: 4px;
}

.resultado ul {
  list-style-type: none;
  padding: 0;
}

.resultado li {
  margin-bottom: 0.5rem;
}

.error {
  margin-top: 1.5rem;
  color: #b00020;
  background-color: #fdd;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #b00020;
}
</style>


<script>
export default {
  name: "DiagnosticoForm",
  data() {
    return {
      form: {
        marca: "",
        modelo: "",
        anio: null,
        kilometraje: null,
        ultimo_mantenimiento: "",
        descripcion_sintomas: ""
      },
      diagnostico: null,
      error: null
    };
  },
  methods: {
    async enviarDiagnostico() {
      this.error = null;
      this.diagnostico = null;

      try {
        // const apiUrl = import.meta.env.VUE_APP_API_URL;
        const res = await fetch(`${import.meta.env.VITE_API_URL}/prueba-ia`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form)
        });

        const data = await res.json();

        if (!res.ok) {
          this.error = data.error || "Error al obtener el diagnóstico";
        } else {
          this.diagnostico = data;
        }
      } catch (err) {
        this.error = "No se pudo conectar con el servidor";
        console.error(err);
      }
    }

  }
};
</script>

