import pytest
from app.app import app, init_db, get_db

@pytest.fixture
def client():
    # Setup: initialize DB and Flask test client
    init_db()
    with app.test_client() as client:
        yield client

def clear_tasks():
    db = get_db()
    db.execute("DELETE FROM tasks")
    db.commit()
    db.close()


def test_index_empty(client):
    """Test GET / with empty DB"""
    clear_tasks()  # ensure DB is empty here
    response = client.get("/")
    assert response.status_code == 200
    # You can improve the assertion here based on your actual template text:
    assert b"Total Tasks" in response.data
    assert b"0" in response.data  # expecting zero tasks count shown on page

def test_add_task(client):
    """Test adding a new task"""
    # POST to /add
    response = client.post("/add", data={"title": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    # The task should appear on index page
    assert b"Test Task" in response.data

def test_edit_task(client):
    """Test editing an existing task"""
    # First add a task directly in DB
    db = get_db()
    db.execute("INSERT INTO tasks (title) VALUES (?)", ("Old Title",))
    db.commit()
    task = db.execute("SELECT * FROM tasks WHERE title = ?", ("Old Title",)).fetchone()
    db.close()

    # POST updated title to /edit/<id>
    response = client.post(f"/edit/{task['id']}", data={"title": "New Title"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"New Title" in response.data
    assert b"Old Title" not in response.data

def test_delete_task(client):
    """Test deleting a task"""
    # Add a task directly in DB
    db = get_db()
    db.execute("INSERT INTO tasks (title) VALUES (?)", ("Task to delete",))
    db.commit()
    task = db.execute("SELECT * FROM tasks WHERE title = ?", ("Task to delete",)).fetchone()
    db.close()

    # GET /delete/<id> and follow redirect to index
    response = client.get(f"/delete/{task['id']}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Task to delete" not in response.data
