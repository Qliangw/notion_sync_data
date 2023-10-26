# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(941, 600)
        self.gridLayout = QGridLayout(MainPages)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_config = QWidget()
        self.page_config.setObjectName(u"page_config")
        self.page_config.setEnabled(True)
        self.page_config.setMinimumSize(QSize(850, 590))
        self.page_config.setMaximumSize(QSize(850, 590))
        self.formLayout = QFormLayout(self.page_config)
        self.formLayout.setObjectName(u"formLayout")
        self.label_notion = QLabel(self.page_config)
        self.label_notion.setObjectName(u"label_notion")
        font = QFont()
        font.setFamilies([u"\u4eff\u5b8b"])
        font.setPointSize(12)
        self.label_notion.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_notion)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_token = QLabel(self.page_config)
        self.label_token.setObjectName(u"label_token")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_token)

        self.lineEdit_token = QLineEdit(self.page_config)
        self.lineEdit_token.setObjectName(u"lineEdit_token")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit_token)

        self.label_pageid = QLabel(self.page_config)
        self.label_pageid.setObjectName(u"label_pageid")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pageid)

        self.lineEdit_pageid = QLineEdit(self.page_config)
        self.lineEdit_pageid.setObjectName(u"lineEdit_pageid")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_pageid)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.formLayout_2)

        self.label_douban = QLabel(self.page_config)
        self.label_douban.setObjectName(u"label_douban")
        self.label_douban.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_douban)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_dbuser = QLabel(self.page_config)
        self.label_dbuser.setObjectName(u"label_dbuser")

        self.gridLayout_2.addWidget(self.label_dbuser, 0, 0, 1, 1)

        self.lineEdit_dbuser = QLineEdit(self.page_config)
        self.lineEdit_dbuser.setObjectName(u"lineEdit_dbuser")

        self.gridLayout_2.addWidget(self.lineEdit_dbuser, 0, 1, 1, 1)

        self.label_dbcookies = QLabel(self.page_config)
        self.label_dbcookies.setObjectName(u"label_dbcookies")

        self.gridLayout_2.addWidget(self.label_dbcookies, 1, 0, 1, 1)

        self.lineEdit_dbcookies = QLineEdit(self.page_config)
        self.lineEdit_dbcookies.setObjectName(u"lineEdit_dbcookies")

        self.gridLayout_2.addWidget(self.lineEdit_dbcookies, 1, 1, 1, 1)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.gridLayout_2)

        self.pushButton_save = QPushButton(self.page_config)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pushButton_save)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.spinBox = QSpinBox(self.page_config)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(9999)
        self.spinBox.setValue(30)

        self.gridLayout_3.addWidget(self.spinBox, 0, 1, 1, 1)

        self.label_5 = QLabel(self.page_config)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 2, 1, 1)

        self.label_7 = QLabel(self.page_config)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)


        self.formLayout.setLayout(2, QFormLayout.LabelRole, self.gridLayout_3)

        self.pages.addWidget(self.page_config)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setMinimumSize(QSize(850, 590))
        self.page_home.setMaximumSize(QSize(850, 590))
        self.page_home.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_home)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QFrame(self.page_home)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)

        self.pages.addWidget(self.page_home)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 233, 256))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setPointSize(16)
        self.title_label.setFont(font1)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.empty_page_label = QLabel(self.page_3)
        self.empty_page_label.setObjectName(u"empty_page_label")
        self.empty_page_label.setFont(font1)
        self.empty_page_label.setAlignment(Qt.AlignCenter)

        self.page_3_layout.addWidget(self.empty_page_label)

        self.pages.addWidget(self.page_3)

        self.gridLayout.addWidget(self.pages, 0, 1, 1, 1)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
#if QT_CONFIG(tooltip)
        self.pages.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_notion.setText(QCoreApplication.translate("MainPages", u"Notion \u53c2\u6570\u914d\u7f6e", None))
        self.label_token.setText(QCoreApplication.translate("MainPages", u"token", None))
        self.lineEdit_token.setPlaceholderText(QCoreApplication.translate("MainPages", u"\u3010\u5fc5\u586b\u3011\u5728https://www.notion.so/my-integrations\u83b7\u53d6", None))
        self.label_pageid.setText(QCoreApplication.translate("MainPages", u"page_id", None))
        self.lineEdit_pageid.setPlaceholderText(QCoreApplication.translate("MainPages", u"\u3010\u5fc5\u586b\u3011notion\u7684\u9875\u9762ID", None))
        self.label_douban.setText(QCoreApplication.translate("MainPages", u"\u8c46\u74e3\u53c2\u6570\u914d\u7f6e", None))
        self.label_dbuser.setText(QCoreApplication.translate("MainPages", u"\u7528\u6237\u540d", None))
        self.lineEdit_dbuser.setPlaceholderText(QCoreApplication.translate("MainPages", u"\u3010\u5fc5\u586b\u3011\u8c46\u74e3\u7528\u6237\u540d", None))
        self.label_dbcookies.setText(QCoreApplication.translate("MainPages", u"cookies", None))
        self.lineEdit_dbcookies.setPlaceholderText(QCoreApplication.translate("MainPages", u"\u3010\u9009\u586b\u3011\u586b\u5199\u540e\u53ef\u89e3\u51b3\u67d0\u4e9b\u5bfc\u5165\u5931\u8d25\u7684\u95ee\u9898\uff0c\u6709\u88ab\u8c46\u74e3\u5c01\u53f7\u7684\u98ce\u9669", None))
        self.pushButton_save.setText(QCoreApplication.translate("MainPages", u"\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.spinBox.setToolTip(QCoreApplication.translate("MainPages", u"\u6700\u59279999\u5929\uff0c\u8bbe\u7f6e\u4e3a0\u65f6\u540c\u6b65\u6240\u6709", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainPages", u"\u5929", None))
        self.label_7.setText(QCoreApplication.translate("MainPages", u"\u5bfc\u5165", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To PyOneDark GUI", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi

