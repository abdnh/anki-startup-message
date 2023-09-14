import json
from typing import Optional

import ankiutils.gui.dialog
from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView

from ..config import config
from ..consts import consts


class Dialog(ankiutils.gui.dialog.Dialog):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Dialog,
    ) -> None:
        super().__init__(__name__, parent, flags)
        self.setWindowTitle(consts.name)
        self.setMinimumSize(300, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)
        web_base = self.web_base = f"/_addons/{consts.module}"
        mw.addonManager.setWebExports(consts.module, "(web|user_files)/.*")
        self.web = AnkiWebView(parent=self, title=consts.name)
        layout.addWidget(self.web)
        qconnect(self.web.loadFinished, self._on_loaded)
        self.web.setUrl(QUrl(f"{web_base}/web/startup.html"))

    def _on_loaded(self) -> None:
        url_base = f"{mw.serverURL()}{self.web_base}"
        self.web.eval(
            """
        const style = document.createElement('link');
        style.rel = 'stylesheet';
        style.href = '%s/user_files/startup.css';
        document.head.appendChild(style);
        const p = document.createElement('p');
        p.id = 'message';
        p.innerHTML = %s;
        document.body.appendChild(p);
        """
            % (url_base, json.dumps(config["message"]))
        )
