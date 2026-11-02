import json

from storage import save_data, load_data


def test_save_and_load(tmp_path, monkeypatch):
    import storage

    test_file = tmp_path / "bank_data.json"
    monkeypatch.setattr(storage, "PATH", str(test_file))

    customers = {"C001": {"name": "Ahmed"}}
    accounts = {"A001": {"balance": 1000}}
    transactions = {}

    save_data(customers, accounts, transactions)

    loaded_customers, loaded_accounts, loaded_transactions = load_data()

    assert loaded_customers == customers
    assert loaded_accounts == accounts
    assert loaded_transactions == transactions


def test_missing_file(tmp_path, monkeypatch):
    import storage

    test_file = tmp_path / "missing.json"
    monkeypatch.setattr(storage, "PATH", str(test_file))

    assert load_data() == ({}, {}, {})


def test_corrupted_file(tmp_path, monkeypatch):
    import pytest
    import storage
    from exceptions import DataPersistenceError

    test_file = tmp_path / "bank_data.json"
    test_file.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(storage, "PATH", str(test_file))

    with pytest.raises(DataPersistenceError):
        load_data()


def test_save_creates_missing_directory_and_leaves_no_temp_files(tmp_path, monkeypatch):
    import storage

    test_file = tmp_path / "nested" / "bank_data.json"
    monkeypatch.setattr(storage, "PATH", test_file)

    save_data({}, {}, {})

    assert test_file.exists()
    assert [p.name for p in test_file.parent.iterdir()] == ["bank_data.json"]


def test_failed_save_keeps_existing_file(tmp_path, monkeypatch):
    import pytest
    import storage
    from exceptions import DataPersistenceError

    test_file = tmp_path / "bank_data.json"
    monkeypatch.setattr(storage, "PATH", test_file)
    save_data({"C001": {"name": "Ahmed"}}, {}, {})
    original = test_file.read_text(encoding="utf-8")

    with pytest.raises(TypeError):
        save_data({"C001": object()}, {}, {})  # not JSON-serializable

    assert test_file.read_text(encoding="utf-8") == original
    assert [p.name for p in tmp_path.iterdir()] == ["bank_data.json"]
