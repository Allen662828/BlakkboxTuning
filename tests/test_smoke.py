from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_root_reports_online():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "online"
    }


def test_analyze_accepts_matching_bin_sizes():
    original = bytes([0]) * 1024
    modified = bytes([0]) * 512 + b"\x01" + bytes([0]) * 511

    response = client.post(
        "/analyze",
        files={
            "original": ("original.bin", original),
            "modified": ("modified.bin", modified),
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "complete"
    assert body["analysis"]["processor_analysis"]["cluster_count"] == 1


def test_analyze_rejects_mismatched_bin_sizes():
    response = client.post(
        "/analyze",
        files={
            "original": ("original.bin", b"\x00"),
            "modified": ("modified.bin", b"\x00\x01"),
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "BIN size mismatch"
    }
