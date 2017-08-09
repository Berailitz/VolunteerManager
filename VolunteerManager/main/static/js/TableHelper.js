'use strict;'

class TableHelper {
    constructor(targetTable, initialLines) {
        self._htmlTable = targetTable ? targetTable : null
        self._tableLines = initialLines ? initialLines : [];
    }

    set htmlTable(htmlTable) {
        this.htmlTable = htmlTable;
    }

    set tableLines(tableLines) {
        this.tableLines = tableLines;
    }

    get tableLines() {
        return this.tableLines;
    }

    appendRow(rowCount, afterIndex) {
        // self.htmlTable.alter('insert_row', afterIndex ? afterIndex : self.htmlTable.countRows(), rowCount);
        tableLines.push(new RecordLine());
        self.htmlTable.loadData(tableLines);
    }

    checkEmpty(LineData) {
        let isLineEmpty = true;
        let exception_index = 'record_status' in LineData ? 'record_status' : 7;
        $.each(LineData, function (index, value) {
            // console.log(index, value);
            if (value && index != exception_index) {
            isLineEmpty = false;
            }
        });
        // console.log('isLineEmpty: ' + isLineEmpty)
        return isLineEmpty;
    }

    deleteRow(rowCount = 1, afterIndex = self.htmlTable.countRows() - 1) {
    tableLines.splice(afterIndex, rowCount);
    self.htmlTable.loadData(tableLines);
    }

    resetCurcor() {
        self.htmlTable.selectCell(0, 0);
    }

    resetTable() {
        tableLines = [new RecordLine()];
        self.htmlTable.loadData(tableLines);
        this.resetCurcor();
    }
}

// export default TableHelper;