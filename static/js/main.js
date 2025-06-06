// Funktionen für Einkaufslisten
async function createList(name) {
    try {
        const response = await fetch('/api/lists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });
        const data = await response.json();
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Erstellen der Liste');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Erstellen der Liste');
    }
}

async function updateList(listId, name) {
    try {
        const response = await fetch(`/api/lists/${listId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });
        const data = await response.json();
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Aktualisieren der Liste');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Aktualisieren der Liste');
    }
}

async function deleteList(listId) {
    if (!confirm('Möchten Sie diese Liste wirklich löschen?')) return;
    
    try {
        const response = await fetch(`/api/lists/${listId}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Löschen der Liste');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Löschen der Liste');
    }
}

// Funktionen für Items
async function createItem(listId, name, icon) {
    try {
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ list_id: listId, name, icon }),
        });
        const data = await response.json();
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Hinzufügen des Artikels');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Hinzufügen des Artikels');
    }
}

async function updateItem(itemId, updates) {
    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates),
        });
        const data = await response.json();
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Aktualisieren des Artikels');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Aktualisieren des Artikels');
    }
}

async function deleteItem(itemId) {
    if (!confirm('Möchten Sie diesen Artikel wirklich löschen?')) return;
    
    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            location.reload();
        } else {
            alert('Fehler beim Löschen des Artikels');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Fehler beim Löschen des Artikels');
    }
}

// Event Listener für Formulare
document.addEventListener('DOMContentLoaded', () => {
    const newListForm = document.getElementById('newListForm');
    if (newListForm) {
        newListForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = newListForm.querySelector('[name="name"]').value;
            createList(name);
            hideNewListModal();
        });
    }

    const addItemForm = document.getElementById('addItemForm');
    if (addItemForm) {
        addItemForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const listId = addItemForm.querySelector('[name="list_id"]').value;
            const name = addItemForm.querySelector('[name="name"]').value;
            const icon = addItemForm.querySelector('[name="icon"]').value;
            createItem(listId, name, icon);
            hideAddItemModal();
        });
    }
}); 