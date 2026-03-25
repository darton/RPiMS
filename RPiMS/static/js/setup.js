// ===============================
//  GENERATING RANDOM PSK
// ===============================

// Generate a random hexadecimal string of given length
function generateHexString(length) {
    const hex = "0123456789abcdef";
    return Array.from({ length }, () => hex[Math.floor(Math.random() * hex.length)]).join("");
}

// Fill an input field with a random PSK
function fillRandomPSK(length, elementId) {
    const el = document.getElementById(elementId);
    if (!el) return; // Safety check
    el.value = generateHexString(length);
}



// ===============================
//  SHOWING / HIDING SECTIONS
// ===============================

// Toggle visibility of a section using W3.CSS classes
function toggleSection(id, show) {
    const el = document.getElementById(id);
    if (!el) return;

    el.classList.toggle("w3-show", show);
    el.classList.toggle("w3-hide", !show);
}



// ===============================
//  CHECKBOX-DRIVEN SECTIONS
// ===============================

// Mapping: checkbox ID → section ID
const SENSOR_SECTIONS = {
    use_zabbix_agent: "zabbix_config",
    use_serial_display: "serial_display",
    use_picamera: "picamera",
    use_weather_station: "weather_station",
    use_dht_sensor: "DHT_sensor",
    use_bme280_sensor: "BME280_sensor",
    id1_BME280_use: "id1_BME280",
    id2_BME280_use: "id2_BME280",
    id3_BME280_use: "id3_BME280",
    use_ds18b20_sensor: "DS18B20_sensor",
    use_cpu_sensor: "CPU_sensor"
};

// Bind a checkbox to a section it controls
function toggleSectionByCheckbox(checkboxId, sectionId) {
    const checkbox = document.getElementById(checkboxId);
    const section = document.getElementById(sectionId);

    if (!checkbox || !section) return; // Safety check

    // Function that updates visibility based on checkbox state
    const update = () => {
        const show = checkbox.checked;
        section.classList.toggle("w3-show", show);
        section.classList.toggle("w3-hide", !show);
    };

    checkbox.addEventListener("change", update); // React to user clicks
    update(); // Set initial state on page load
}

// Initialize all checkbox-driven sections
function initSensorToggles() {
    for (const [checkboxId, sectionId] of Object.entries(SENSOR_SECTIONS)) {
        toggleSectionByCheckbox(checkboxId, sectionId);
    }
}



// ===============================
//  BME280 SELECT SYNCHRONIZATION
// ===============================

// Hide options in one select if they are selected in the other
function syncSelects(selectA, selectB) {
    const valA = selectA.value;
    const valB = selectB.value;

    // --- Python-style version (clear, explicit, recommended for readability) ---
    for (let opt of selectA.options) {
        opt.hidden = (opt.value === valB);
    }

    for (let opt of selectB.options) {
        opt.hidden = (opt.value === valA);
    }

    /*
    // --- Modern JavaScript version (short, idiomatic, optional) ---
    [...selectA.options].forEach(opt => opt.hidden = opt.value === valB);
    [...selectB.options].forEach(opt => opt.hidden = opt.value === valA);
    */
}

// Initialize BME280 port selection logic
function initBME280Selects() {
    const s2 = document.getElementById("id2_BME280_serial_port_select");
    const s3 = document.getElementById("id3_BME280_serial_port_select");

    if (!s2 || !s3) return; // Safety check

    const update = () => syncSelects(s2, s3);

    s2.addEventListener("change", update);
    s3.addEventListener("change", update);

    update(); // Set initial state
}



// ===============================
//  GPIO INPUT HANDLING
// ===============================

// Show additional settings for specific GPIO input types
function initGPIOInputs() {
    const inputs = document.querySelectorAll(".gpioinputs");

    inputs.forEach(select => {
        const baseId = `${select.id}_DS`;

        // Update visibility and default values based on selected type
        const update = () => {
            const type = select.value;
            const show = type === "ContactSensor" || type === "ShutdownButton";

            const section = document.getElementById(baseId);
            if (!section) return;

            section.classList.toggle("w3-show", show);
            section.classList.toggle("w3-hide", !show);

            // Set default hold time if section becomes visible
            if (show) {
                const holdTime = document.getElementById(`${baseId}_HT`);
                if (holdTime) holdTime.value = "1";
            }
        };

        select.addEventListener("change", update);
        update(); // Set initial state
    });
}



// ===============================
//  MAIN INITIALIZATION
// ===============================

// Run all initialization logic when the page is ready
document.addEventListener("DOMContentLoaded", () => {
    initSensorToggles();
    initBME280Selects();
    initGPIOInputs();
});

