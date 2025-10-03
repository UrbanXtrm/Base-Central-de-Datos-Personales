const parkingData = {
  Madrid: {
    center: [40.4168, -3.7038],
    zoom: 12,
    parkings: [
      {
        id: "mad-1",
        name: "Parking Público Plaza Mayor",
        address: "Calle de la Sal, 4",
        type: "public",
        totalSpaces: 320,
        available: 58,
        pricePerHour: 0,
        coordinates: [40.4154, -3.7074],
      },
      {
        id: "mad-2",
        name: "Garaje Privado San Miguel",
        address: "Calle Conde de Miranda, 3",
        type: "private",
        totalSpaces: 90,
        available: 12,
        pricePerHour: 3.5,
        coordinates: [40.4159, -3.7089],
      },
      {
        id: "mad-3",
        name: "Parking Público Atocha",
        address: "Glorieta del Emperador Carlos V",
        type: "public",
        totalSpaces: 600,
        available: 102,
        pricePerHour: 0,
        coordinates: [40.4077, -3.6919],
      },
      {
        id: "mad-4",
        name: "Parking Privado Gran Vía",
        address: "Calle de Tudescos, 1",
        type: "private",
        totalSpaces: 220,
        available: 0,
        pricePerHour: 4.2,
        coordinates: [40.4203, -3.7058],
      },
      {
        id: "mad-5",
        name: "Parking Público Parque del Retiro",
        address: "Avenida de Menéndez Pelayo, 67",
        type: "public",
        totalSpaces: 180,
        available: 34,
        pricePerHour: 0,
        coordinates: [40.4152, -3.6826],
      },
    ],
  },
  Barcelona: {
    center: [41.3851, 2.1734],
    zoom: 12,
    parkings: [
      {
        id: "bcn-1",
        name: "Parking Público Ciutat Vella",
        address: "Carrer de la Princesa, 19",
        type: "public",
        totalSpaces: 260,
        available: 65,
        pricePerHour: 0,
        coordinates: [41.3854, 2.182],
      },
      {
        id: "bcn-2",
        name: "Parking Privado Passeig de Gràcia",
        address: "Passeig de Gràcia, 74",
        type: "private",
        totalSpaces: 150,
        available: 21,
        pricePerHour: 4.8,
        coordinates: [41.3921, 2.1645],
      },
      {
        id: "bcn-3",
        name: "Parking Público Sagrada Família",
        address: "Carrer de Provença, 463",
        type: "public",
        totalSpaces: 280,
        available: 48,
        pricePerHour: 0,
        coordinates: [41.4036, 2.1744],
      },
      {
        id: "bcn-4",
        name: "Parking Privado Maremagnum",
        address: "Moll d'Espanya",
        type: "private",
        totalSpaces: 200,
        available: 5,
        pricePerHour: 5.5,
        coordinates: [41.3753, 2.1825],
      },
      {
        id: "bcn-5",
        name: "Parking Público Montjuïc",
        address: "Avinguda de l'Estadi, 22",
        type: "public",
        totalSpaces: 180,
        available: 0,
        pricePerHour: 0,
        coordinates: [41.3643, 2.1556],
      },
    ],
  },
  Valencia: {
    center: [39.4699, -0.3763],
    zoom: 13,
    parkings: [
      {
        id: "vlc-1",
        name: "Parking Público Ayuntamiento",
        address: "Plaça de l'Ajuntament, 1",
        type: "public",
        totalSpaces: 210,
        available: 37,
        pricePerHour: 0,
        coordinates: [39.469, -0.3779],
      },
      {
        id: "vlc-2",
        name: "Parking Privado Ruzafa",
        address: "Carrer de Cadis, 70",
        type: "private",
        totalSpaces: 120,
        available: 9,
        pricePerHour: 3.2,
        coordinates: [39.4638, -0.3731],
      },
      {
        id: "vlc-3",
        name: "Parking Público Ciudad de las Artes",
        address: "Av. del Professor López Piñero, 7",
        type: "public",
        totalSpaces: 450,
        available: 88,
        pricePerHour: 0,
        coordinates: [39.4551, -0.3529],
      },
      {
        id: "vlc-4",
        name: "Parking Privado Malvarrosa",
        address: "Passeig Marítim, 5",
        type: "private",
        totalSpaces: 160,
        available: 24,
        pricePerHour: 2.5,
        coordinates: [39.4796, -0.32],
      },
      {
        id: "vlc-5",
        name: "Parking Público Bioparc",
        address: "Av. Pío Baroja, 3",
        type: "public",
        totalSpaces: 300,
        available: 0,
        pricePerHour: 0,
        coordinates: [39.4789, -0.4134],
      },
    ],
  },
};

const typeLabels = {
  public: "Público",
  private: "Privado",
};

let map;
let markersLayer;

document.addEventListener("DOMContentLoaded", () => {
  const citySelect = document.getElementById("citySelect");
  const filterPublic = document.getElementById("filterPublic");
  const filterPrivate = document.getElementById("filterPrivate");

  Object.keys(parkingData)
    .sort((a, b) => a.localeCompare(b, "es"))
    .forEach((cityKey) => {
      const option = document.createElement("option");
      option.value = cityKey;
      option.textContent = cityKey;
      citySelect.append(option);
    });

  map = L.map("map", {
    zoomControl: true,
    attributionControl: false,
  }).setView(parkingData[citySelect.value || Object.keys(parkingData)[0]].center, 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contribuidores',
  }).addTo(map);

  markersLayer = L.layerGroup().addTo(map);

  const defaultCity = citySelect.value || Object.keys(parkingData)[0];
  citySelect.value = defaultCity;

  const updateView = () => {
    const selectedCity = citySelect.value;
    const showPublic = filterPublic.checked;
    const showPrivate = filterPrivate.checked;
    renderCity(selectedCity, { showPublic, showPrivate });
  };

  citySelect.addEventListener("change", updateView);
  filterPublic.addEventListener("change", updateView);
  filterPrivate.addEventListener("change", updateView);

  updateView();
});

function renderCity(cityKey, filters) {
  const city = parkingData[cityKey];
  if (!city) return;

  map.setView(city.center, city.zoom);
  markersLayer.clearLayers();

  const allowedTypes = new Set();
  if (filters.showPublic) allowedTypes.add("public");
  if (filters.showPrivate) allowedTypes.add("private");

  const availableParkings = city.parkings.filter(
    (parking) => parking.available > 0 && allowedTypes.has(parking.type)
  );

  const totalFreeSpots = availableParkings.reduce((acc, parking) => acc + parking.available, 0);

  availableParkings.forEach((parking) => {
    const marker = L.marker(parking.coordinates, {
      icon: createMarkerIcon(parking.type),
    }).addTo(markersLayer);

    marker.bindPopup(`
      <strong>${parking.name}</strong><br />
      ${parking.address}<br />
      ${typeLabels[parking.type]} · ${parking.available} plazas libres
    `);
  });

  updateSummary(city, availableParkings.length, totalFreeSpots, allowedTypes);
  renderParkingList(city, allowedTypes);
}

function updateSummary(city, parkingCount, totalFreeSpots, allowedTypes) {
  const summary = document.getElementById("summary");
  const typesDescription = Array.from(allowedTypes)
    .map((type) => typeLabels[type])
    .join(" y ") || "ningún tipo";

  summary.innerHTML = `
    <strong>${parkingCount}</strong> aparcamientos con plazas libres (${typesDescription})<br />
    <strong>${totalFreeSpots}</strong> plazas libres en total
  `;
}

function renderParkingList(city, allowedTypes) {
  const list = document.getElementById("parkingList");
  list.innerHTML = "";

  const title = document.createElement("h2");
  title.textContent = "Detalle de aparcamientos";
  list.append(title);

  city.parkings
    .filter((parking) => allowedTypes.has(parking.type))
    .sort((a, b) => b.available - a.available)
    .forEach((parking) => {
      list.append(createParkingCard(parking));
    });
}

function createParkingCard(parking) {
  const card = document.createElement("article");
  card.className = "parking-card";

  const badge = document.createElement("span");
  badge.className = `badge ${parking.type}${parking.available === 0 ? " full" : ""}`;
  badge.textContent = `${typeLabels[parking.type]}${
    parking.available === 0 ? " · Completo" : ""
  }`;

  card.innerHTML = `
    <h3>${parking.name}</h3>
    <div class="meta">${parking.address}</div>
    <div class="meta">Capacidad: ${parking.totalSpaces} plazas</div>
    <div><strong>${parking.available}</strong> plazas libres</div>
    <div>${
      parking.pricePerHour === 0
        ? "Tarifa: gratuito"
        : `Tarifa: €${parking.pricePerHour.toFixed(2)} / hora`
    }</div>
  `;

  card.prepend(badge);
  return card;
}

function createMarkerIcon(type) {
  const colors = {
    public: "#2d9c5a",
    private: "#d46c2a",
  };

  const color = colors[type] || "#2a77d4";

  return L.divIcon({
    className: "custom-marker",
    html: `<span style="
      background:${color};
      color:#fff;
      padding:6px 10px;
      border-radius:999px;
      font-weight:600;
      box-shadow:0 2px 6px rgba(0,0,0,0.35);
      display:inline-block;">
      ${type === "public" ? "P" : "R"}
    </span>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -12],
  });
}
