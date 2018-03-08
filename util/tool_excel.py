#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import xlrd
from xlwt import Workbook
from xlwt import XFStyle
from xlwt import Font
from xlwt import Alignment
from xlwt import Pattern

class ToolExcel(object):
    def __init__(self, fn, mode="r"):
        self._fn = fn
        if mode == "r":
            self._workbook_rd = xlrd.open_workbook(fn)
        elif mode == "w":
            self._workbook_wt = Workbook(encoding='utf-8')
        self._row_col_dict = {}

    def _set_style(self, name, height, color, bold, fore_color):

        # 字体
        font = Font()
        font.name = name
        font.bold = bold
        font.color_index = color
        font.height = height
        # 居中
        alignment = Alignment()
        alignment.horz = Alignment.HORZ_CENTER
        alignment.vert = Alignment.VERT_CENTER
        # 风格
        style = XFStyle()
        style.font = font
        style.alignment = alignment
        # 模式
        if fore_color:
            pattern = Pattern()
            pattern.pattern = Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 15
            style.pattern = pattern
        return style

    def add_sheet_data(self, sheet_name, record_dict):
        if self._row_col_dict.get(sheet_name) is None:
            # 判断是否是新建
            self._row_col_dict[sheet_name] = {"row": 0, "col":0}
            self._workbook_wt.add_sheet(sheet_name, cell_overwrite_ok=True)
            # 写入列名
            sheet = self._workbook_wt.get_sheet(sheet_name)
            row_keys = record_dict.keys()
            for i in range(0, len(row_keys)):
                sheet.write(0, i, row_keys[i], self._set_style("Arial", 240, 2, True, True))
        # 写入数据
        sheet = self._workbook_wt.get_sheet(sheet_name)
        row_values = record_dict.values()
        self._row_col_dict[sheet_name]["row"] += 1
        row = self._row_col_dict.get(sheet_name).get("row")
        for i in range(0, len(row_values)):
            sheet.write(row, i, row_values[i], self._set_style("Arial", 200, 2, False, False))
        # 保存
        self._workbook_wt.save(self._fn)


