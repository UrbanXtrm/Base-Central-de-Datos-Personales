async function fetchPersons() {
  const list = document.getElementById("person-list");
  list.innerHTML = "<li>Cargando personas...</li>";
  try {
    const response = await fetch("/persons");
    const persons = await response.json();
    if (!persons.length) {
      list.innerHTML = "<li>No hay personas registradas todavía.</li>";
      return;
    }
    list.innerHTML = "";
    persons.forEach((person) => {
      const item = document.createElement("li");
      item.textContent = `${person.first_name} ${person.last_name}`;
      item.addEventListener("click", () => fetchProfile(person.id));
      list.appendChild(item);
    });
  } catch (error) {
    list.innerHTML = `<li>Error al cargar personas: ${error}</li>`;
  }
}

async function fetchProfile(personId) {
  const container = document.getElementById("profile");
  container.innerHTML = "<p>Cargando perfil completo...</p>";
  try {
    const response = await fetch(`/profiles/${personId}`);
    const data = await response.json();
    container.innerHTML = renderProfile(data);
  } catch (error) {
    container.innerHTML = `<p>Error al obtener el perfil: ${error}</p>`;
  }
}

function renderProfile(profile) {
  const person = profile.person;
  const makeList = (items, formatter) =>
    items.length
      ? `<ul>${items.map((item) => `<li>${formatter(item)}</li>`).join("")}</ul>`
      : "<p>No hay registros aún.</p>";

  return `
    <article>
      <h2>${person.first_name} ${person.last_name}</h2>
      <p><strong>Correo:</strong> ${person.email ?? "—"}</p>
      <p><strong>Teléfono:</strong> ${person.phone ?? "—"}</p>
      <p><strong>Dirección:</strong> ${person.address ?? "—"}</p>
      <h3>Historial médico</h3>
      ${makeList(profile.medical_records, (item) => `<strong>${item.title}</strong> (${item.recorded_at}) - ${item.description ?? "Sin descripción"}`)}
      <h3>Formación académica</h3>
      ${makeList(profile.education_records, (item) => `<strong>${item.degree}</strong> - ${item.institution}`)}
      <h3>Experiencia profesional</h3>
      ${makeList(profile.employment_records, (item) => `<strong>${item.position}</strong> en ${item.company}`)}
      <h3>Seguridad social</h3>
      ${makeList(profile.social_security_records, (item) => `<strong>${item.provider}</strong> (${item.affiliation_number})`)}
      <h3>Documentos</h3>
      ${makeList(profile.documents, (item) => `<strong>${item.name}</strong> - ${item.category}`)}
    </article>
  `;
}

async function submitPerson(event) {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form).entries());
  try {
    const response = await fetch("/persons", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error("No se pudo crear la persona");
    }
    form.reset();
    await fetchPersons();
    const created = await response.json();
    document.getElementById("person-feedback").textContent =
      "Persona creada correctamente.";
    fetchProfile(created.id);
  } catch (error) {
    document.getElementById("person-feedback").textContent = error.message;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("person-form");
  if (form) {
    form.addEventListener("submit", submitPerson);
  }
  fetchPersons();
});
