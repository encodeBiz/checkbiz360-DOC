# Contracts and profitability

A contract with a customer sets an amount and, often, a number of hours. The hard part is knowing, while the work is under way, whether it will hold: whether the hours will be enough, whether the cost will eat up the margin. In CheckBiz360 each contract brings together its amount, the tasks done for it and what is paid out, and shows the margin while there is still time to do something.

Contracts are in each customer's record, **Details** tab, **Contracts** block.

---

## What problems it solves

- **Knowing whether a contract makes money**, with the real hours and expenses, not an estimate from memory.
- **Seeing the problem coming.** Hours done against estimated, in red when they go over, and the approximate date on which the cost would exceed the amount.
- **No typing up the contract.** AI reads the PDF and proposes amount, dates and hours, with the sentence each figure comes from.
- **Going from the contract to its tasks and back.** Each contract lists its tasks and each task links to its contract.
- **Forecasting the next one.** With the closed contracts, the platform estimates hours, cost and margin for new ones.

---

## Before you start

- Profitability needs people to have their **hourly rate** at the branch. Without it, their hours are counted but cost nothing, and the contract warns that the cost falls short. See [What is the customer portfolio](./117-what-is-the-customer-portfolio.md#before-you-start-what-each-position-costs).
- Creating, editing, closing and deleting contracts, and seeing amounts, costs and margins, is for the **owner and administrators**. Managers and supervisors see their customers' contracts with their hours and tasks, without money.

---

## Create a contract

A customer can have **several contracts at the same time** (for example, the annual maintenance and a one-off job).

1. In the customer record, **Contracts** block, press **New contract**.
2. In **Customer document**, choose the PDF of the contract or quote if you have already uploaded it to **Documents**; or press **Upload PDF** to upload it now (PDF only, up to 10 MB). The document is saved as a contract with the customer, visible only to Administration. If you have no PDF, leave **No PDF**.
3. With a PDF chosen, you can press **Read the PDF** (see below).
4. Fill in or review:
   - **Contract name** (required).
   - **Starts** and **Ends**. Leave **Ends** empty if it is open-ended.
   - **Amount (€)**: the price agreed with the customer, **before VAT**.
   - **Estimated hours**: working hours, not days.
   - **Complexity**, from *1 · Simple* to *5 · Very complex*. It is used to compare with similar contracts when forecasting.
   - **Notes**.
5. Save.

### Read the PDF with AI

**Read the PDF** reads the document and fills in the amount, the dates, the hours and the complexity. Under each figure appears the sentence it comes from, *From the document: "…"*, or *Not in the document*. **Check what was read before saving**: AI proposes, you decide.

If the document does not look like a contract or a quote, the form warns you. A PDF scanned as an image, with no text, cannot be read: fill in the details by hand.

> **Privacy.** Before it is read with AI, the names of people and companies, ID and tax numbers, addresses, phone numbers, emails and bank accounts are removed from the document: only the rest reaches the model. Even so, upload only what needs to be read and never health data. The notice appears in the form itself.

---

## Which tasks belong to a contract

Each task says which contract it belongs to in its **Contract** drop-down (see [The customer on the task](./119-the-customer-on-the-task.md#the-tasks-contract)):

- When creating a task, if the customer has a single contract in force, it is suggested.
- **No contract** leaves it out of all of them, and this is respected.
- Creating a contract, changing its dates or reopening it **does not take any tasks**: a task only changes contract when it is chosen on the task.

---

## The contract card

Each contract is a card with its name, its period (*From … to …* or *Open-ended*) and its status (**Active** or **Closed on …**). If something does not add up, a **warnings** tag. Press **Expand** to see the detail.

| Figure | What it is |
|---|---|
| **Amount** | The contract price, before VAT. |
| **Hours planned / done / estimated** | *Planned*: those added up by its tasks, from their planned start to their deadline, for each assigned person. *Done*: those worked, according to its tasks' check-ins or, if there are none, when they were started and finished. *Estimated*: the contract's **Estimated hours** (if you did not set them, only the first two are shown). In red if hours done exceed the estimate. |
| **Gross cost** | Hours done multiplied by each person's rate (without social security costs), plus the material consumed in its tasks if you have inventory, plus the contract's approved expenses. In red if it already exceeds the amount. |
| **Margin** | What is left of the amount after cost, in euros and as a percentage. |

Below:

- **Tasks (n)**: each task of the contract with its status, date and people, from newest to oldest, 5 at a time with **Load more**. The task name takes you to its page; from the task page, the contract takes you back here.
- The cost of material and what share of the hours has a rate, if not all of them do.
- **Expenses awaiting approval** and **External expenses**. See [Contract and task expenses](./122-contract-and-task-expenses.md).
- **Forecast** (see below).

Above the cards, **Customer total**: the amount contracted, the cost and the margin of all their contracts.

### The warnings

| Warning | What to do |
|---|---|
| *No task belongs to this contract yet.* | Choose the contract on the tasks that belong to it. |
| *Some hours have no rate: the cost falls short.* | Set the hourly rate for those people at their branch. |
| *Some material has no unit cost: it counts in quantity, not amount.* | Set the cost on the inventory item's record. |
| *Some shifts have no check-out: they are not valued.* | Correct those workdays so that they count. |
| *Some tasks have no check-ins: their hours come from when they were started and finished.* | It is for information: those hours are approximate. |

---

## The forecast

Using the contracts already **closed** as a reference, each active contract with estimated hours shows:

- **Expected hours**: a range, with the most likely figure.
- **Expected cost** and **Expected margin**.
- If, at this pace, the cost would exceed the amount, **around which date**.

It is compared with similar contracts (of the same complexity when there are any). While there are not enough closed contracts, it says so: *Not enough closed contracts to forecast yet*. Without estimated hours: *Set the estimated hours to get a forecast*.

---

## Edit, close, reopen and delete

- **Edit** changes the contract's details and lets you add or remove external expenses.
- **Close contract**: when the work ends. Its figures go into the history used to forecast the next ones. It can be reopened with **Reopen**.
- **Delete**: only if no task belongs to that contract. If it already has tasks, close it.

The tasks of a closed contract still belong to it and can be edited. What you cannot do is choose a closed contract for a new task.

---

## Common problems

**The margin is very high or the cost is empty.** Hourly rates are missing: the contract warns you. Set them on each person's link to their branch.

**Hours done are zero even though work has been done.** The tasks do not belong to that contract: open them and choose it in **Contract**.

**"Read the PDF" fills in nothing.** The PDF is a scanned image or is not a contract. Fill in the details by hand.

**I cannot see the amount or the New contract button.** Only owners and administrators see them.

**It will not let me delete a contract.** It has tasks. Close it instead.

---

## Related articles

| Article | Description |
|---|---|
| [The customer on the task](./119-the-customer-on-the-task.md) | The contract drop-down on the task |
| [Contract and task expenses](./122-contract-and-task-expenses.md) | What is paid out and counts towards the cost |
| [Customer documents](./120-customer-documents.md) | The contract PDF and who sees it |
| [The customer in the analyses](./123-the-customer-in-the-analyses.md) | The customer's profitability month by month and the contract alerts |
| [Create and manage employees](../02-employees/06-create-and-manage-employees.md) | Where the hourly rate is set |
