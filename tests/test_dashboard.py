"""Smoke test the actual Streamlit application with the cleaned synthetic fixture."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_streamlit_dashboard_renders_without_exception():
    app = AppTest.from_file(str(ROOT / "app" / "streamlit_app.py"), default_timeout=30).run()
    assert not app.exception
    assert any("Student Performance and Attendance Dashboard" in item.value for item in app.title)
    assert len(app.tabs) == 5
