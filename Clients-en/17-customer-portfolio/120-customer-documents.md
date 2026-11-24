# Customer documents

Each customer has their papers: the record with what you need to know to work in their home or on their premises, the quote, the contract. Some are for whoever goes to do the work; others, for management only. CheckBiz360 keeps them in the customer record and decides, document by document, who sees them.

---

## What problems it solves

- **The customer's papers, next to the customer.** No searching through shared folders.
- **Staff have what they need on the task**, without asking for it by phone.
- **Prices and terms do not leave management.** A contract or a quote is created visible only to the owner and administrator, and is never visible from the app.

---

## Customer document types

| Type | What it is for | Who sees it, by default |
|---|---|---|
| **Customer record** | What whoever does the work needs to know: floor plan, instructions, the customer's protocol. | Whoever you tick. If it includes **Worker**, staff see it from the task. |
| **Quote / rate** | Prices and terms offered to the customer. | **Administration** only. |
| **Contract with the customer** | The signed contract. It is uploaded from **Contracts**, in the record itself. | **Administration** only. |
| **Expense receipt** | The receipt for an approved expense. The platform creates it when the expense is approved; it is not uploaded by hand. | **Administration** only. |
| **Other** | Any other customer paper. | Whoever you tick. |

---

## Upload a document

1. Open the customer record, **Details** tab.
2. In **Documents**, press **Upload document**.
3. Choose the **Document type**, enter the **Title** and, if you wish, a description and an **Expiry date**.
4. Choose the file (PDF, image, Word or Excel, up to 10 MB).
5. In **Visible to**, tick who sees it: **Worker**, **Supervisor**, **Manager** or **Administration**.
6. Press **Upload**.

It can also be uploaded from **Document management**, choosing the **Customer** scope and the customer. There, the **Customer** scope filter brings together the documents of all your customers.

Contracts are uploaded from **Contracts** → **New contract** → **Upload PDF**, so that the contract and its document stay linked. See [Contracts and profitability](./121-contracts-and-profitability.md).

---

## The "Administration" level

**Administration** is the most restricted level:

- It is opened **only by the owner and administrators**, and **only from the panel**.
- **Nobody sees it from the app**, owner included: anyone who signs in through the app is just another employee.
- A document for Administration only does not ask anyone on the staff for a read receipt.

When you choose *Quote / rate*, visibility drops to **Administration** on its own. If you still tick it for supervisors or workers, the form warns you in red: *This is the customer's administrative documentation. If you tick it for supervisors or workers, they will see it from this customer's tasks, with its prices and terms.* It can be done, but knowingly.

---

## What staff see

From a customer's task, the assigned person sees in the app the customer documents marked for **Worker**, in the **Additional details** card. In the panel, the task's customer card shows those same documents under **Documents**, with the note *The ones staff can see from the task*.

If the customer is marked **Available in all branches**, their documents for staff can be opened by **the whole staff of the company**, whether or not they have one of their tasks: some people serve a customer on a fixed schedule with no tasks. So, for those customers, anything that should not be seen goes under **Administration**. The customer form warns you when you tick the box.

---

## Expiry dates

If you set an **Expiry date**, the document shows *Expires on …*. If a contract expires within 30 days or has already expired, the header of the customer record says so in red, and the contract appears in the **Home** alerts (see [The customer in the analyses](./123-the-customer-in-the-analyses.md)).

---

## Archive

From the **Documents** list in the record, **Archive** removes the document from the record and from the task. It can still be consulted in **Document management**.

---

## Common problems

**"Contract with the customer" does not appear in "Document type".** Contracts are uploaded from **Contracts** → **New contract** → **Upload PDF**, in the customer record.

**A manager cannot see a quote.** It is under **Administration**: only the owner and administrators see it. If they should see it, tick **Manager** as well.

**The owner cannot see a document from the app.** That is expected if it is under Administration or not ticked for **Worker**: from the app only what is for staff is shown. Open it from the panel.

**Staff cannot see the customer record.** Check that the record is ticked for **Worker** and that the task has that customer.

**Someone with no tasks for that customer has opened their record.** The customer is marked **Available in all branches**: their documents for staff can be opened by the whole staff. If that should not be so, move them to **Administration** or assign specific branches to the customer.

---

## Related articles

| Article | Description |
|---|---|
| [Upload and organise documents](../05-document-management/31-upload-and-organise-documents.md) | The upload form, the scope and how the archive is organised |
| [Who sees each document](../05-document-management/136-who-sees-each-document.md) | The Administration level, personal documents and the app |
| [Document access permissions](../05-document-management/37-document-access-permissions.md) | Who sees what in document management |
| [Contracts and profitability](./121-contracts-and-profitability.md) | Uploading the contract and reading it with AI |
| [Contract and task expenses](./122-contract-and-task-expenses.md) | The receipt for each approved expense |
