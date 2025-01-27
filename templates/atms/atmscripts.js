let atmData, atmStatus;

document.addEventListener("DOMContentLoaded", async () => {
    await loadData();
    renderErrorTable('all');
    renderStatusTable();
});

async function loadData() {
    const response1 = await fetch('../../jsons/atm_data.json');
    atmData = await response1.json();

    const response2 = await fetch('../../jsons/atmstatus.json');
    atmStatus = await response2.json();
}

function renderErrorTable(filter) {
    const tbody = document.getElementById("errorTbody");
    tbody.innerHTML = '';

    let errors = [];
    if (filter === 'all') {
        errors = [...atmData.Criticalerrors, ...atmData.errors, ...atmData.nonerrors];
    } else if (filter === 'errors') {
        errors = [...atmData.errors];
    } else if (filter === 'critical') {
        errors = [...atmData.Criticalerrors];
    }

    errors.forEach(err => {
        const row = tbody.insertRow();
        row.innerHTML = `<td>${err.date} - ${err.id}</td><td>${err.error}</td>`;
    });
}

function renderStatusTable() {
    const tbody = document.getElementById("statusTbody");
    tbody.innerHTML = '';

    for (let [id, status] of Object.entries(atmStatus)) {
        const row = tbody.insertRow();
        row.innerHTML = `<td>${id}</td><td>${status.askfor}</td><td><button onclick="deleteStatus('${id}')">Удалить</button></td>`;
        
        if (status.lvl === 1) {
            row.style.backgroundColor = "lightyellow";
        } else if (status.lvl === 2) {
            row.style.backgroundColor = "#f08080"; // Light red
        }
    }
}

function addAtm() {
    document.getElementById("formContainer").style.display = "block";
}

function closeForm() {
    document.getElementById("formContainer").style.display = "none";
}

function saveAtm() {
    const address = document.getElementById("atmAddress").value;
    const coords = document.getElementById("atmCoords").value;

    // Update atmStatus
    for (let id in atmStatus) {
        atmStatus[id].address = address;
        atmStatus[id].coords = coords;
    }

    fetch('atmstatus.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(atmStatus)
    }).then(() => {
        closeForm();
        renderStatusTable();
    });
}

function deleteStatus(id) {
    delete atmStatus[id];

    // Save changes in the JSON file again
    fetch('atmstatus.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(atmStatus)
    }).then(() => {
        renderStatusTable();
    });
}

function filterData(filter) {
    renderErrorTable(filter);
}