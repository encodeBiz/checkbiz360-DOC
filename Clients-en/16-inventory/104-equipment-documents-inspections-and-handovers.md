# Equipment: documents, inspections and handovers

In a labour inspection a company has to answer two questions with paperwork: **was each worker given their protective equipment?** and **has the machine they work with passed its mandatory inspections?** Inventory keeps both proofs next to the equipment itself, and warns you before anything expires.

All of this applies to material that is **lent** (machines, vehicles, tools, PPE with a serial number), not to material that is used up.

---

## Each piece of equipment's documents

The equipment page (**Inventory → Stock → the equipment**) has a **Documents** section. It holds its ownership record or invoice, CE declaration, user manual, insurance, the mandatory inspection that applies to it, maintenance checks and risk assessment.

There are two ways to add one:

- **Upload document**: choose the type, title, expiry date (for an inspection, the date of the next one), the result if it is an inspection, and who carried it out.
- **Link existing**: if the document is already in **Document management**, search for it and link it without uploading it again.

In both cases, **Applies to** decides whether the document covers **all units** (a manual, a CE declaration) or **a single one** (one van's roadworthiness test, one machine's insurance).

You can also do it from **Document management**: when uploading, with the **Equipment** scope; or from an existing document's page, with **Link to equipment**. It is always the same document: it shows in both places, and **unlinking does not delete it**.

---

## What is compliant and what is not

Each unit shows whether it is compliant according to its documents:

| Mark | Meaning |
|---|---|
| **Compliant** | It has documents and none has expired |
| **Check documents** (amber) | A document expires within 30 days, or a non-mandatory one has expired |
| **Not compliant** (red) | The mandatory inspection has expired or its result was "fail" |

Equipment with no documents has no mark. If a new inspection is uploaded, the latest one counts: the old one shows as **Superseded**.

The mark shows in the list of units on the equipment page, in **Stock** (how many are not compliant) and when choosing material for a task.

**Non-compliant equipment is not blocked.** Taking it out of service is the company's decision, not the software's. But when you reserve it for a task or hand it to someone, a warning shows the reason and you have to tick that you know before continuing. Who accepted it is recorded.

---

## Warnings before expiry

The managers of the equipment's warehouse get a warning when one of its documents will expire within 30 days, and another when it has expired or an inspection result is "fail". If the document covers all units, the warning goes to the company's managers. Each warning is sent once.

---

## Handing equipment to a person

From the equipment page or from Stock, **Hand over** assigns a unit to a worker together with its documents: the user manual, the manufacturer's leaflet or the responsibility commitment. Those the equipment has marked **With each handover** in its documents section come pre-selected, and you can untick one or upload another on the spot. Only documents visible to workers can go with a handover, which is how equipment documents are created. The worker confirms they received the equipment and the related documents and agree with the handover; the record keeps which documents they were and in which version. The confirmation is **signed with their phone's key** and verified by the platform, as with documents (see [Read receipt and electronic signature](../05-document-management/35-electronic-signature.md)); the "Equipment and PPE" report says in its "Signature" column whether it was verified. The worker gets a notification on their phone and confirms it in **My equipment** with their fingerprint, face or unlock code; if their phone has no lock, with their account password. They can also say they did not receive it or do not agree, and the warehouse manager is notified.

On return you record how it came back: in good condition, damaged or not returned. If it comes back damaged or is not returned, it becomes unavailable with that reason. The equipment is then in the warehouse that receives it (see [Where each piece of equipment is](./106-where-each-piece-of-equipment-is.md)). What each worker holds also shows on their page, in the **Material** tab.

---

## The "Equipment and PPE" report

It is generated from **Reports**, in Excel, with two sheets:

- **Handovers**: what was handed to each worker, with which documents and in which version, by whom, what they confirmed, when and how, and how it was returned.
- **Equipment and inspections**: each unit with its status, who holds it now and each document with its type, result, expiry and status.

This is what you present in an inspection. Without inventory, the report appears in red in the list and explains what to do to get it.

---

## Related articles

| Article | Description |
|---|---|
| [What is inventory](./100-what-is-inventory.md) | What problems it solves |
| [Stock, warehouses and receipts](./101-stock-warehouses-and-receipts.md) | Adding material and each unit |
| [Report types](../11-reports-and-exports/76-report-types.md) | All the platform's reports |
