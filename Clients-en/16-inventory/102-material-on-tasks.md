# Material on tasks

Inventory is designed so that material is tracked in the same place the work is tracked: the task. This guide walks through the whole cycle, from planning to closing.

---

## The cycle, in four steps

| Step | Who | What happens |
|---|---|---|
| **1. Reserve** | Whoever plans | Decides what material the task needs. It is committed in the warehouse but does not leave yet. |
| **2. Issue** (optional) | Whoever runs the warehouse | From the warehouse or item record, **Issue** and, under **Where does it go?**, **Task**: the material leaves for that job. If nobody does it, the consumption records the issue. |
| **3. Declare** | The worker | States how much was used, planned or not. |
| **4. Settle** | Whoever validates | What was left undeclared is resolved: of what went out, how much came back; of what was reserved, how much was used. The rest goes back to the warehouse. |

Assigning material is not using it: until it is declared or settled, the platform does not count it as consumed.

---

## 1. Assign material when creating the task

The **New task** form shows the **Material for the task** block:

1. First choose the **branch**: the warehouses come from it.
2. Click **Add material** and search for the item.
3. If it gets used up, enter the **quantity** (and the warehouse, if the branch has several). If it is lent out, choose the **unit**.
4. Create the task. The material is reserved at that moment.

If there is not enough stock, it is reserved anyway and you are warned. If a unit is already reserved by another task in that time slot, you are told which task it clashes with.

---

## 2. Material in the task detail

The task detail shows a table with all of its material, whatever the type:

- For what gets used up: what was reserved, issued, used, returned and **not declared**.
- For what is lent out: the unit, its time slot and the reservation status.

From there, **Add material** reserves more and **Declare consumption** records what was used from the back office, on what was reserved or on unplanned material, without recording any issue first: the practical option when the task is planned and closed from the back office. Issues are not made from the task but from the warehouse or the item. A unit can be **released** if it is no longer needed: the platform asks **Where does it stay?** —at the task or in a warehouse—, because releasing it does not return it to the warehouse (see [Where each piece of equipment is](./106-where-each-piece-of-equipment-is.md)). A **non-compliant** one can still be reserved after accepting the warning.

---

## 3. In the app: the worker only declares consumption

The worker sees the task's material in the task itself in the app and has a single button, **Declare consumption**: preloaded with what was reserved; if everything was used, just confirm. They can correct quantities and add what they used without it being planned. They never record an issue: if the warehouse did not, the platform records it on declaring.

If the branch has several warehouses and they add something unplanned, the app asks which one it came from.

Each piece of equipment's card says where it is. A supervisor or above can **release** it from the app, saying whether it stays at the task or goes back to a warehouse; the worker sees that it is released when the task is completed.

---

## 4. Settle on validation

When validating a completed task, if some material is still undeclared, the platform asks you to **settle** it before validating:

- Of what **went out** and nobody declared: how much came back; the rest counts as used.
- Of what was **reserved** but never recorded as issued: how much was used (preloaded with everything reserved); the rest goes back to the warehouse.

That way no task is closed with material lost along the way. On a closed task, the material table shows what was reserved, what was released on closing and, if nothing was recorded, says so.

---

## Related articles

| Article | Description |
|---|---|
| [Stock, warehouses and receipts](./101-stock-warehouses-and-receipts.md) | How material is added |
| [Task validation](../06-tasks/45-task-validation.md) | The validation step where material is settled |
| [Task reports](../06-tasks/48-task-reports.md) | Each task's material in the report |
| [Where each piece of equipment is](./106-where-each-piece-of-equipment-is.md) | Releasing equipment, what needs collecting and receiving it in the warehouse |
