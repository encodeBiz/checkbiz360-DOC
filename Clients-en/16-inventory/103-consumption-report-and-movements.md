# Consumption report and movements

Inventory answers two management questions: **where material goes** and **what it costs**. It has three outputs for that.

---

## Consumption report

Open it from **Inventory → Stock → More actions → Report**.

1. Choose the **period**.
2. Choose how to **group**: by item, task, employee, branch or warehouse.
3. If needed, filter by warehouse, item, branch or employee.
4. Click **Generate**.

Each line shows the quantity consumed, the cost (valued at the unit cost on the item's record), the number of entries and the date of the first and last one. It can be **exported to CSV**.

It tells you which customer or site consumes the most, which person uses more than usual or which warehouse empties first.

---

## Movement ledger

Everything that happens in inventory is recorded: receipts, reservations, issues, consumption, returns, recounts and transfers, with who recorded it, in whose name and on which task.

It is downloaded in **Excel**, with the whole history from day one:

| From | Button | What it contains |
|---|---|---|
| A warehouse record | **Download history** | That warehouse |
| The warehouse list | **Download history of all** | An overall summary and one sheet per warehouse |
| An item record | **Download history** | That item, in every warehouse it has been in |
| The consumption report | **History for the period (Excel)** | The chosen period, warehouse and item |

Each warehouse comes with its **summary per item** (receipts, transfers, issues, returns, adjustments, usage, stock and its value), the **movements** in order with the stock after each one and what each issue was for (a task, a person or a workplace, by name), its **equipment** and **where each unit has been**. If the stock rebuilt from the history does not match the current stock, the row says **Review**. It is the record to turn to when a count does not add up.

---

## Material in the task report

With inventory subscribed, the Excel **task report** includes each task's material, its cost and what was left unsettled. See [Task reports](../06-tasks/48-task-reports.md#material-for-each-task).

---

## Related articles

| Article | Description |
|---|---|
| [What is inventory](./100-what-is-inventory.md) | What problems it solves |
| [Report types](../11-reports-and-exports/76-report-types.md) | All the platform's reports |
