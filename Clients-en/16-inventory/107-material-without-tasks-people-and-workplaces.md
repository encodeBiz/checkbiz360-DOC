# Material without tasks: people and workplaces

In many companies work is not organised in tasks: a cleaning company has its staff at the client's premises for the whole working day. This guide explains how material is handed out and tracked in that case. It requires the inventory add-on, subscribed or on trial.

---

## Where the material goes

Material leaves the warehouse towards one of three destinations:

| Destination | For | Example |
|---|---|---|
| **Task** | Material for a specific job | "30 towels for Thursday's cleaning" |
| **Person** | Material someone carries | "5 litres of bleach to María" |
| **Workplace** | Material sent to a site for whoever works there | "20 litres for the month to the South site" |

The same things are done with all three: allocate, issue, declare usage and settle what is left. What changes is where you see it. Material on tasks is explained in [Material on tasks](./102-material-on-tasks.md).

---

## Issue to a person or a workplace

1. Open the warehouse or item record and, on the item's row, click **Issue**.
2. Under **Where does it go?**, choose **Person** or **Workplace** and search for it.
3. Enter the quantity and click **Issue**.

You can also do it from the employee or workplace record, on the **Material** tab, with the **Issue** button.

---

## Allocate an allowance

Allocating says what a person or a site is entitled to, without the material leaving yet: "María gets 5 litres a week". It is set aside in the warehouse until it goes out.

On the record's **Material** tab, click **Allocate** and choose the item, the warehouse and the quantity. If there is not enough, it is allocated anyway and you are warned.

With allowances in place, the panel can tell who uses more than they were allocated.

---

## Declare what is used

Workers declare it from the app:

- **At the workplace.** With the working day started, the clock-in screen shows **Workplace material** with the **Declare consumption** button. What was sent to the workplace is already loaded; anything unplanned can be added.
- **Their own.** **My equipment** also shows the consumables they carry, with **Declare consumption** and **Return**.

Nobody has to issue anything first: if someone declares something that was not recorded as issued, the issue is recorded at the same time.

From the panel, on the record's **Material** tab, the declare icon does the same. On a workplace you can say who used it.

---

## Settle what is left

On a task, material is settled when the task is validated. A person or a workplace has no such moment, so it is settled when needed, from the **Material** tab on their record. Click the item's settle icon and enter:

- **Used**: what was used and nobody declared.
- **Returned**: what goes back to the warehouse.
- **Allocation that will not go out**: the part of the allowance that will no longer be handed out.

Whatever you do not resolve stays where it is: **with them** for a person, **at the workplace** for a workplace. It stays visible until someone resolves it.

---

## What material is outside the warehouse

In **Inventory → Stock**, the **Outside the warehouse** tab lists all material that has gone out and nobody has declared used or returned: on tasks, with people and at workplaces. You can filter by destination and warehouse, and each row takes you to the record where it is settled.

---

## Workplace as a destination or a warehouse at the workplace

They are two ways of working and can be combined:

- **Sending material to the workplace** tells you how much was sent and how much was used.
- **A warehouse at the workplace** keeps stock, minimums and counts at that site. It is replenished with transfers from the main warehouse.

---

## Who can do what

| Role | Can |
|---|---|
| Worker | Declare and return their own material and that of the workplace where they work |
| Supervisor, Manager, Owner | Also allocate, issue to anyone, settle and see what is outside the warehouse |

---

## Related articles

| Article | Description |
|---|---|
| [Material on tasks](./102-material-on-tasks.md) | The same cycle, when work is organised in tasks |
| [Stock, warehouses and receipts](./101-stock-warehouses-and-receipts.md) | Keeping track of what you have |
| [Consumption report and movements](./103-consumption-report-and-movements.md) | Where material goes and what it costs |
