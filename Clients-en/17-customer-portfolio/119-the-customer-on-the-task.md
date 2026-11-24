# The customer on the task

A task with its customer knows where it is done, carries to whoever does the work what they need to know on arrival, and counts towards that customer's hours, contract and analysis. It is all decided in the same form as always, **Create task**.

---

## What problems it solves

- **No more retyping the address.** The customer's address serves as the work site, with its margin.
- **Staff arrive knowing what to expect.** Instructions, contacts to call and the customer record, in the task itself in the app.
- **Protecting what must not get out.** The customer's name is only shown if you authorise it.
- **Knowing which contract each job belongs to**, or making it clear that it belongs to none.

---

## Choose the customer when creating a task

1. In **Task management**, press the new task button.
2. Choose the **branch** first: the customers come from it.
3. In **Customer**, choose one of the customers assigned to that branch or available in all branches, or leave **No customer**. If there is none for that branch, the field does not appear.
4. If the customer has contracts, **Contract** appears: choose which one the task belongs to or **No contract** (see below).
5. If the customer has an address, **Use the customer's address as the work site** appears ticked, with the address below and its **Margin** in metres.
6. Fill in the rest of the task as usual and save.

If you change the branch, the customer and the contract are cleared: you have to choose them again.

An internal task (a meeting, office work) does not belong to any customer: leave it as **No customer**.

---

## The customer's address as the work site

With **Use the customer's address as the work site** ticked, the task can only be started from that address, just as with an [own work site](../06-tasks/40-create-a-task.md#own-work-site).

- **Margin.** The metres around the address from which it can be started. If you do not change it, it takes the branch's. *A garage or a warehouse needs a wider margin than a doorway.* The margin you set is saved with the task and kept when you edit it again.
- **Another address.** If today's work is not at the customer's address, untick the box and enter the address in **Work site (optional)**.

---

## The task's contract

The **Contract** drop-down appears as soon as the customer has a contract:

- **When creating the task**, if the customer has a single contract in force on those dates, it is suggested. You can change it.
- **No contract** leaves the task out of all contracts. This is respected: creating a new contract later does not take it.
- A task only changes contract when you choose it on the task.

Tasks that do not go through this form (imported, created from the app or from the assistant) take, when created, the customer's contract in force if they only have one. If it did not belong to that contract, edit it and choose another or **No contract**.

More about contracts in [Contracts and profitability](./121-contracts-and-profitability.md).

---

## The customer card on the task page

On the page of a task with a customer, the **Customer** card appears, with everything that goes with it:

- The customer's name and a tag that says whether **Staff can see the name** or **Staff can't see the name**. **View** takes you to the customer record.
- The **Contract**, as a link: it opens the customer record with that contract expanded.
- The **Customer address**.
- The **Field notes**.
- The **Contact people**, with those visible to staff marked **Visible in the field**, and the **Call** and **Send an email** buttons.
- The **Documents** staff see from the task, to open or download them.

If the task has a customer, the page also shows the **Expenses** block (only to owners and administrators). See [Contract and task expenses](./122-contract-and-task-expenses.md).

---

## What staff see in the app

In the task detail, the assigned person sees the **Additional details** card, above **Team**, with:

- The customer's **Field notes**.
- The **Contacts** marked as visible, with the **Call** button.
- The **Customer documents** marked for workers.

The **customer's name** only appears if **Show the customer's name to staff** is ticked in their record. If the customer has no details for staff, the card does not appear. Contracts, quotes and everything marked "Administration" are never visible from the app.

To see the card, staff need the app updated to the latest version.

---

## Find tasks by customer

- **Task list.** As soon as the company has customers, the **Customer** filter appears next to the employee filter.
- **Task report.** If any task in the report has a customer, the Excel file adds the **Customer** column after **Site**. See [Task reports](../06-tasks/48-task-reports.md).

---

## Common problems

**The Customer field does not appear.** The chosen branch has no customers assigned and no customer is available in all branches. Assign the customer to that branch from their record or, if tasks are created from a branch other than the one serving them, tick **Available in all branches** (see [Add customers](./118-add-customers.md)).

**The Contract drop-down does not appear.** The customer has no active contracts.

**Staff cannot start the task.** With the customer's address as the work site, it can only be started within the margin. If the place is large (a warehouse, a car park), increase the **Margin**.

**Staff do not see the customer's details.** Check that the app is up to date, that the contacts are marked **Visible to field staff** and that the documents are marked for workers.

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](../06-tasks/40-create-a-task.md) | All the fields of the task form |
| [Add customers](./118-add-customers.md) | Address, contacts, field notes and the name checkbox |
| [Contracts and profitability](./121-contracts-and-profitability.md) | Which contract each task belongs to and how much it leaves |
| [Contract and task expenses](./122-contract-and-task-expenses.md) | What is paid out for the task |
