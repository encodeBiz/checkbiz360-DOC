# Where each piece of equipment is

A piece of equipment —a scrubber, a van, a scaffold— can be free and still not be in the warehouse: it was used on a site and stayed there. This guide explains how the platform knows where each one is and how it gets collected. It requires the inventory add-on, subscribed or on trial.

---

## Free is not the same as in the warehouse

The platform keeps two things apart:

- **Whether it can be reserved.** Equipment stops being reserved when it is released: the task releases it when it closes, or a supervisor does it by hand.
- **Where it is.** Releasing equipment does not return it to the warehouse. It stays where it was until someone says otherwise, and the platform records it.

So free equipment can be reserved straight away for another task, and at the same time everyone knows it is still on site and someone has to go and get it.

---

## What moves equipment

| What happens | Where it stays |
|---|---|
| It is added | In its base warehouse. |
| Its task starts | At the task site. |
| Its task closes | Still at the task site. |
| It is released by hand | Where whoever releases it says: at the task or in a warehouse. |
| It is handed to a person | With that person. |
| It is returned or received in a warehouse | In that warehouse. |
| Its base warehouse is changed | If it was at its base, in the new one. |

Each of these events is recorded with who said it and when.

---

## Release equipment from a task

When a task no longer needs a piece of equipment —it was reserved for the whole day and only used in the morning—, a supervisor or above can release it so another task can use it.

In the task detail, or on the equipment card in the app, click **Release equipment**. The platform asks **Where does it stay?**:

- **Stays at the task**: the equipment stays at the task site until someone collects it.
- **Goes back to the warehouse**: choose which warehouse. Its base warehouse is listed first.

Handing equipment to a person is not releasing it: it is done with **Hand over**, as explained in [Equipment: documents, inspections and handovers](./104-equipment-documents-inspections-and-handovers.md).

In the app, workers do not release equipment: they see **It is released when the task is completed**.

---

## What needs collecting

Free equipment that is not in its base warehouse is marked **Away from base**:

- In **Stock**, the **Away from base** status filter shows only the free equipment that is away. Each row says how many units need collecting.
- In the item's calendar, the unit's row says **Free · away from base** and where it is.

It is the list of what the warehouse has to go and fetch. Being away from base does not prevent reserving it for another task.

---

## Receive equipment in the warehouse

When the equipment comes back, whoever receives it records it from the item record, on the unit's row:

1. Click **Receive in warehouse**.
2. Choose the **Receiving warehouse**.
3. Enter the **Condition**: **Good**, **Damaged** or **Lost**, and a note if you like.
4. Click **Receive**.

If it arrives damaged or has been lost, it becomes **unavailable** with that reason and is not offered for new tasks until someone makes it available again from its record. If the equipment was handed to a person, receiving it also closes that handover.

Equipment that its task has in use cannot be received: it has to be released first.

---

## Where it has been

On the item record, each unit says **where it is** now and since when. **Where it has been** shows its full history: every time it changed place, why and who said so.

---

## Who can do what

| Role | Can |
|---|---|
| Worker | See where the equipment on their tasks is |
| Supervisor, Manager, Owner | Also release equipment from a task and receive it in a warehouse |

---

## Related articles

| Article | Description |
|---|---|
| [Material on tasks](./102-material-on-tasks.md) | How each task's material is reserved and tracked |
| [Equipment: documents, inspections and handovers](./104-equipment-documents-inspections-and-handovers.md) | Handing equipment to a person and returning it |
| [Stock, warehouses and receipts](./101-stock-warehouses-and-receipts.md) | Keeping track of what you have |
