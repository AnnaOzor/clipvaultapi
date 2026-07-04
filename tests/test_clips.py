TEST_CLIP = {
    "title": "Holiday",
    "filename": "holiday.mp4",
    "status": "uploaded"
}


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_clip(client):
    response = client.post("/clips", json=TEST_CLIP)

    assert response.status_code == 201
    assert response.json()["clip"]["title"] == TEST_CLIP["title"]


def test_duplicate_filename(client):
    client.post("/clips", json=TEST_CLIP)

    response = client.post("/clips", json=TEST_CLIP)

    assert response.status_code == 409


def test_invalid_filename(client):
    payload = {
        "title": "Holiday",
        "filename": "holiday.txt",
        "status": "uploaded"
    }

    response = client.post("/clips", json=payload)

    assert response.status_code == 422


def test_get_all_clips(client):
    client.post("/clips", json=TEST_CLIP)

    response = client.get("/clips")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_clip_by_id(client):
    create = client.post("/clips", json=TEST_CLIP)

    clip_id = create.json()["clip"]["id"]

    response = client.get(f"/clips/{clip_id}")

    assert response.status_code == 200
    assert response.json()["id"] == clip_id


def test_get_nonexistent_clip(client):
    response = client.get("/clips/999")

    assert response.status_code == 404


def test_update_clip_status(client):
    create = client.post("/clips", json=TEST_CLIP)

    clip_id = create.json()["clip"]["id"]

    response = client.patch(
        f"/clips/{clip_id}",
        json={"status": "ready"}
    )

    assert response.status_code == 200
    assert response.json()["clip"]["status"] == "ready"


def test_update_nonexistent_clip(client):
    response = client.patch(
        "/clips/999",
        json={"status": "ready"}
    )

    assert response.status_code == 404


def test_delete_clip(client):
    create = client.post("/clips", json=TEST_CLIP)

    clip_id = create.json()["clip"]["id"]

    response = client.delete(f"/clips/{clip_id}")

    # 204 No Content must not return a response body.
    assert response.status_code == 204
    assert response.text == ""

    # Verify the clip no longer exists.
    response = client.get(f"/clips/{clip_id}")
    assert response.status_code == 404


def test_delete_nonexistent_clip(client):
    response = client.delete("/clips/999")

    assert response.status_code == 404