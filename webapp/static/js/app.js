let ejecutando = false;

document.getElementById("operationForm").addEventListener(
    "submit", evento => evento.preventDefault()
);

async function ejecutar(operacion) {

    if (ejecutando) return;

    const ssh = document.getElementById("ssh_password");
    const vault = document.getElementById("vault_password");
    const consola = document.getElementById("consoleOutput");
    const estado = document.getElementById("operationStatus");

    const requiereVault = [
        "alta",
        "simular_alta"
    ].includes(operacion);

    if (!ssh.value) {
        alert("Ingresá la contraseña SSH.");
        return;
    }

    if (requiereVault && !vault.value) {
        alert("Ingresá la contraseña de Ansible Vault.");
        return;
    }

    let confirmacion = "";

    if (["alta", "baja", "guardar"].includes(operacion)) {

        const mensajes = {
            alta: "¿Confirmás el alta REAL de R7?",
            baja: "¿Confirmás la baja REAL de R7?",
            guardar: "¿Confirmás guardar las configuraciones de los siete routers?"
        };

        if (!confirm(mensajes[operacion])) return;

        confirmacion = operacion;
    }

    const datos = new FormData();

    datos.append("operacion", operacion);
    datos.append("ssh_password", ssh.value);
    datos.append("vault_password", vault.value);
    datos.append("confirmacion", confirmacion);

    datos.append(
        "csrf_token",
        document.querySelector(
            '#operationForm input[name="csrf_token"]'
        ).value
    );

    ssh.value = "";
    vault.value = "";

    ejecutando = true;

    const botones = document.querySelectorAll(
        "#operationForm button"
    );

    botones.forEach(boton => boton.disabled = true);

    estado.textContent = "Ejecutando operación...";
    estado.style.color = "#38bdf8";
    consola.style.color = "#38bdf8";

    consola.textContent =
        "Iniciando Ansible...\n" +
        "Operación: " + operacion + "\n" +
        "Esperando resultado de los routers...";

    consola.scrollIntoView({behavior: "smooth"});

    try {

        const respuesta = await fetch("/api/ejecutar", {
            method: "POST",
            body: datos
        });

        if (respuesta.status === 401) {
            window.location.href = "/login";
            return;
        }

        const resultado = await respuesta.json();

        consola.textContent =
            resultado.output || "Sin salida disponible.";

        if (resultado.success) {
            estado.textContent = "Operación completada.";
            estado.style.color = "#4ade80";
            consola.style.color = "#4ade80";
        } else {
            estado.textContent = "Operación con errores.";
            estado.style.color = "#f87171";
            consola.style.color = "#f87171";
        }

    } catch (error) {

        consola.textContent =
            "No se recibió respuesta del servidor. " +
            "Verificá el estado de los routers antes de repetir.";

        estado.textContent = "Error de comunicación.";
        estado.style.color = "#f87171";

    } finally {

        ejecutando = false;
        botones.forEach(boton => boton.disabled = false);

    }
}
