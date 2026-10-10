# Stock, warehouses and receipts

This guide explains how to set up inventory and how to keep track of what you have. It requires the inventory add-on, subscribed or on trial.

---

## 1. Create the warehouses

A warehouse is where material comes from: a cleaning room, a depot, a van. **Every warehouse serves at least one branch**, and a branch can have several warehouses.

1. Go to **Inventory → Warehouses**.
2. Click **New warehouse**, give it a name and choose the branches it serves.

When a task at that branch needs material, the platform only offers that branch's warehouses. If there is only one, it picks it automatically.

Each warehouse has its own **record**, with a summary —items, free units, stock below minimum and discrepancies—, what it contains and its recent movements.

---

## 2. Record the first receipt

Material always comes in through **New receipt**, in **Inventory → Stock**. You do not need to create the item first:

1. Click **New receipt**.
2. In **Item**, type to search for it. If it does not exist, choose **＋ New item** and fill in its record: type, name and unit of measure (or unit of use, for an operable), reference, unit cost and category.
3. Choose the **warehouse**.
4. For a **consumable**, enter the **quantity**. For an **operable**, the receipt is a **new unit**: give it the identifier on its label (registration, serial number) and, if you like, a short name ("the red scrubber").
5. Click **Record receipt**.

> **Tip:** the search starts from the third letter, like every other search in the back office.

If you have many items to add, load them all at once from the warehouse record with **Import**: see [Import material from a template](./105-import-material-from-a-template.md).

---

## 3. Stock: what you have, item by item

**Stock** is the command centre of inventory. Each row is an item in a warehouse:

- A **consumable** shows what is available, what is on hand, what is committed to tasks and its minimum.
- An **operable** shows how many units are free right now, how many are busy and how many are unavailable. If any has expired documents, the row says how many are **not compliant** or **to check**.

The **Status** column summarises whether you need to act:

| Status | Means |
|---|---|
| **OK** | A consumable with no warnings: neither below minimum nor with a discrepancy. |
| **Available** | An operable with at least one unit free right now. |
| **Below minimum** | There is less than the alert minimum set for that warehouse. |
| **Discrepancy** | The balance went negative: more went out than was recorded. A recount is needed. |
| **All busy** | No unit free at this moment. |
| **No units** | An operable registered without any unit yet. |

You can filter by text, type, warehouse and status. If there are discrepancies, a banner at the top shows them in one click. The **Away from base** status leaves only the free equipment that is not in its warehouse: what needs collecting (see [Where each piece of equipment is](./106-where-each-piece-of-equipment-is.md)).

---

## 4. Actions on material

From each row, or from the item's record:

| Action | What for |
|---|---|
| **Receipt** | Material arriving: a purchase, a supplier return, a new unit. |
| **Transfer** | Move a quantity from one warehouse to another, or change a unit's home warehouse. |
| **Recount** | Set what is really there after counting, with a reason. Consumables only. |
| **Minimum** | Set the level below which managers are alerted. Consumables only. |
| **Edit** | Change the record's details. The type cannot be changed. |
| **Issue to a task** | Hand out warehouse material for a specific job, before it starts. It is optional: if nobody does it, consumption records it. |
| **Hand over** | Give a unit to a person, who confirms it from their phone. See [Equipment: documents, inspections and handovers](./104-equipment-documents-inspections-and-handovers.md). |
| **Archive** | Stop offering an item. If it has history, the history is kept. |

---

## 5. The item record

All items have the same record: their details, what there is in each warehouse and their history.

- For a **consumable**: stock per warehouse and movements over the last 30 days, with the year's download in CSV.
- For an **operable**: how many units are free; each unit with its status (free, reserved, in use, handed over, unavailable or retired), its current use and **where it is**; a **calendar** where each reservation is a bar with its time slot, over 7, 14 or 30 days; and its **documents** (roadworthiness test, insurance, inspections, manual), marking whether each unit is compliant.

---

## Who can do what

| Role | Can |
|---|---|
| Worker | See the material in their branches' warehouses, declare consumption on their tasks and confirm the equipment handed to them |
| Supervisor | Also reserve material and units for tasks |
| Manager, Owner | Also create items, warehouses and units, and record receipts, recounts and transfers |

---

## Related articles

| Article | Description |
|---|---|
| [What is inventory](./100-what-is-inventory.md) | What problems it solves and how to subscribe |
| [Material on tasks](./102-material-on-tasks.md) | How each task's material is assigned and tracked |
| [Import material from a template](./105-import-material-from-a-template.md) | Load everything a warehouse holds at once |
| [Where each piece of equipment is](./106-where-each-piece-of-equipment-is.md) | Free equipment away from the warehouse and how it is received |
