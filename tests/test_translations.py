from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
from PySide6.QtCore import QCoreApplication, QTranslator

from plugin_manager.translations import _PUBLIC_CONTEXTS


PACKAGE = Path(__file__).resolve().parents[1] / "clipboard_replay"
CONTEXT = "ClipboardReplay"


@pytest.mark.parametrize("locale", ("en_US", "de_DE", "ja_JP", "pl_PL"))
def test_catalog_is_private_complete_and_loadable(qapp, locale):
    source = PACKAGE / "translations" / f"{locale}.ts"
    tree = ET.parse(source)
    assert {node.findtext("name") for node in tree.findall(".//context")} == {CONTEXT}
    assert CONTEXT not in _PUBLIC_CONTEXTS
    messages = tree.findall(".//message")
    assert messages
    translator = QTranslator()
    assert translator.load(str(source.with_suffix(".qm")))
    for message in messages:
        translation = message.find("translation")
        assert translation is not None, message.findtext("source")
        assert translation.get("type") not in ("unfinished", "vanished", "obsolete")
        assert "".join(translation.itertext()).strip(), message.findtext("source")
    assert any(translator.translate(CONTEXT, message.findtext("source")) for message in messages)


def test_plugin_sources_use_private_contexts():
    for source in PACKAGE.rglob("*.py"):
        text = source.read_text(encoding="utf-8")
        assert 'translate("Form"' not in text, source
        assert 'translate("SkinManager"' not in text, source


@pytest.mark.parametrize(("locale", "expected"), [
    ("en_US", "Activity log"),
    ("de_DE", "Aktivitätsprotokoll"),
    ("ja_JP", "動作ログ"),
    ("pl_PL", "Dziennik aktywności"),
])
def test_clipboard_catalog_loads_in_qt(qapp, qtbot, locale, expected):
    from clipboard_replay.widgets import ClipboardReplayWidget

    qm = PACKAGE / "translations" / f"{locale}.qm"
    translator = QTranslator()
    assert translator.load(str(qm))
    assert QCoreApplication.installTranslator(translator)
    try:
        widget = ClipboardReplayWidget()
        qtbot.addWidget(widget)
        assert widget._log_label.text() == expected
    finally:
        QCoreApplication.removeTranslator(translator)



def test_clipboard_view_refreshes_after_language_change(qapp, qtbot):
    from clipboard_replay.widgets import ClipboardReplayWidget

    class Translator(QTranslator):
        def isEmpty(self):
            return False

        def translate(self, context, source, disambiguation=None, n=-1):
            values = {"运行日志": "Activity log", "系统": "System", "监听中": "Listening", "已暂停": "Paused"}
            return values.get(source) if context == CONTEXT else None

    widget = ClipboardReplayWidget()
    qtbot.addWidget(widget)
    widget.show()
    widget.handle_output({"kind": "state", "enabled": True, "message": "ready"})
    translator = Translator()
    assert QCoreApplication.installTranslator(translator)
    try:
        qtbot.waitUntil(lambda: widget.status_label.text() == "Listening")
        assert widget._log_label.text() == "Activity log"
        widget.handle_output({"kind": "state", "enabled": False, "message": "stop"})
        assert widget.status_label.text() == "Paused"
        assert "[System] stop" in widget.log_output.toPlainText()
    finally:
        QCoreApplication.removeTranslator(translator)


def test_plugin_window_starts_hidden(qapp):
    from clipboard_replay.plugin import ClipboardReplayPlugin

    assert ClipboardReplayPlugin.plugin_info().show_window is False
