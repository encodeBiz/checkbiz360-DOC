# Import material from a template

Adding material item by item takes time when there are dozens or hundreds of them. This guide explains how to load everything a warehouse holds at once with an Excel sheet. It requires the inventory add-on, subscribed or on trial.

---

## How it works, in three steps

| Step | What happens |
|---|---|
| **1. Download the template** | From the warehouse record. There is one for consumables and one for operables. |
| **2. Fill it in and upload it** | One row per item, or per unit for an operable. Nothing is saved yet when you upload it. |
| **3. Review and import** | The platform shows what it will do with each row. Only clicking **Import** adds anything. |

The template is always tied to the warehouse it is downloaded from: everything imported goes into that warehouse.

---

## 1. Download the template

1. Go to **Inventory → Warehouses** and open the warehouse record.
2. Click **Import** and choose **Consumables** or **Operables**.
3. Click **Download template**.

There are two templates because a consumable and an operable are not described the same way: the first has a quantity and a minimum; the second, a unit identifier and a usage unit. Whatever you import with either of them then shows in the same **Stock** list.

Each template comes with the header and **two example rows**. Both start with the word **DELETE**: you can remove them or leave them, because they are not imported.

### Columns of the consumables template

| Column | What to enter |
|---|---|
| **Name** * | The item's name: "Towels", "Degreaser". |
| **Reference** | Its code. It is what identifies the item if you upload the file again. |
| **Category** | To group it: cleaning, PPE, stationery. |
| **Unit** | How it is counted: unit, litre, box, metre. |
| **Unit cost** | What each unit costs. Used in the cost reports. |
| **Initial quantity** | What the warehouse holds now. |
| **Minimum** | The level below which the people in charge are warned. |

### Columns of the operables template

| Column | What to enter |
|---|---|
| **Name** * | The item's name: "Industrial scrubber". |
| **Reference** | The model code. |
| **Category** | To group it: machinery, vehicles. |
| **Usage unit** * | Hours, km or days. The template has a drop-down. |
| **Unit cost** | What each unit costs. |
| **Identifier** * | The one on its label: serial number, number plate. |
| **Label** | A short name: "the red scrubber". |
| **Counter reading** | Hours, km or days it has now. |

For operables, **each row is a unit**. Three scrubbers of the same model are three rows with the same name and reference and three different identifiers. The two examples in the template are exactly that.

Columns with an asterisk are required. Numbers can be written with a decimal comma or point.

---

## 2. Upload the file

Click **Choose file**, select the filled-in template and click **Review**. Excel (.xlsx) or CSV files up to 2 MB are accepted. A CSV saved from a Spanish-language Excel, with semicolons, is read correctly too.

If you upload the wrong template —the operables one from **Consumables**, or the other way round—, the platform says so and reads nothing.

---

## 3. Review what will happen

Before importing, each row says what will happen to it:

| What it says | Meaning |
|---|---|
| **New** | The item does not exist and will be created. |
| **Updated** | The item already exists and its details change: name, category, unit or cost. |
| **Reactivated** | The item was archived and becomes active again. |
| **Unchanged** | The item already exists and the file changes nothing. |
| **New unit** / **Unit updated** | For operables, the same for each unit. |
| **Initial quantity** | The quantity goes into the warehouse. |
| **Already has stock: the quantity is not applied** | See below. |
| **Example: not imported** | One of the rows starting with DELETE. |
| **Not imported** | The row has an error, explained next to it. |

What needs attention comes first: rows with errors, and those that look like an item that already exists ("Looks like “Towel”: check it is not the same one").

Rows with errors are not imported; the rest are. To include them, fix the file and click **Upload another file**. If you close the window without importing, nothing is saved.

When you are happy, click **Import**. With many rows it takes a moment and you can see the progress; you can close the window and the import keeps going.

---

## How it knows whether an item already exists

1. **By reference.** If the row has a reference that an item already has, it is that item.
2. **By name**, if the row has no reference or one that does not exist: "Towels" and "towels" are the same item; "Towels" and "Small towels" are not.
3. If it matches nothing, it is **new**.

That is why it is worth entering the reference: you can upload the same file again, corrected or extended, and what already exists is updated instead of duplicated.

### The initial quantity only goes in once

The **initial quantity** is only added if the item has no stock in that warehouse. If it already has some, it is ignored and the review says so. Changing what a working warehouse holds is a **count**, with its reason, and it is done from the item's row in **Stock**.

---

## Who can import

Whoever can add items and record receipts: **Manager** and **Owner**.

---

## Related articles

| Article | Description |
|---|---|
| [Stock, warehouses and receipts](./101-stock-warehouses-and-receipts.md) | Adding items one by one and controlling stock |
| [What is inventory](./100-what-is-inventory.md) | What problems it solves and how to subscribe |
