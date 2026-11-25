# What the employment contract says: occupation, working hours and hourly rate

When you upload a person's employment contract, CheckBiz360 reads it and proposes what it needs for that person to count correctly in costs: their **occupation**, their **working hours**, their **collective agreement** and their **hourly rate**. Each item comes with the sentence of the contract it is taken from, and nothing changes in the record until you apply it.

This is done in the document's record, **What the contract says** block. Only the **owner and administrators** see and use it.

---

## What it solves

- **No typing up the contract.** Occupation, category, working hours, contract type, dates and salary are read out, with their quote.
- **An hourly rate with a basis.** If the contract gives the salary, it is converted into an hourly rate with the annual hours set by the agreement; if the contract says "per the tables", the salary comes from the agreement's table. That rate is the one used by the cost reports and by customer profitability.
- **Seeing what does not add up.** A salary below the minimum for those hours, an agreement that cannot be identified or tables from an earlier year appear as warnings, so you can review them before applying.

---

## Before you start

- The document must be of the **Contract** type, assigned to **one person** (*Employee* scope) and be a **PDF with text**. A PDF scanned as an image cannot be read: the block says so and the record has to be filled in by hand.
- For it to propose the agreement, your company must have referenced it beforehand: agreements belong to each company. See [Collective agreements](139-collective-agreements.md).
- If the person's occupation is already in your **job catalogue**, the reading matches it. If it is not, when applying you can **create the position** with the name the contract gives.

---

## Uploading the contract

1. In **Document Management**, upload the PDF with the **Contract** type and **Employee** scope, like any contract (see [Payslips and contracts](32-payslips-and-contracts.md)).
2. If you know which agreement the person is under, choose it in **Collective agreement (optional)**. If you leave it as *Not specified*, it is looked up in the catalogue when the contract is read.
3. Publish. The reading starts on its own. You can stay on the record or carry on working: when it finishes, you will see it on **Home** and you will receive an email.

In the document's record, the **What the contract says** block goes from *We are reading the contract* to the data read. If you want to repeat the reading (for example, after referencing a new agreement), press **Read again**.

---

## What it proposes

Each item has **Where it comes from**, which expands the sentence of the contract: *From the contract: "…"*. What the contract does not say appears as *Not in the contract*.

| Item | What it is |
|---|---|
| **Occupation** | The short name of the job ("home care assistant", "waiter") and, if the contract includes it, the occupation code. |
| **Agreement** | The agreement the contract cites and its scope (national, regional, provincial or company). |
| **Category** | The professional group and level, as the contract writes them. |
| **Weekly hours** | The hours per week. |
| **Contract type** | Permanent, temporary, training or seasonal permanent. |
| **Dates** | From when and, if it has one, until when. |
| **Salary** | The gross base salary with its period, the number of payments and whether extra payments are pro-rated or separate. |
| **Suggested hourly price** | Gross euros per hour, **without employer social security contributions**, and below it **Calculation**: which figure and which hours it comes from. It carries the **Estimated** mark when the salary comes from the tables or when there is no agreement and the legal maximum hours are used. |

Below, the **warnings**: only what changes a decision for you. For example, that the contract's salary is below the minimum for those hours, that a supplement is not included in the base salary, that the agreement's saved tables are from an earlier year or that the end date has been worked out from a duration.

> **The hourly rate is a gross cost.** It does not include employer social security contributions or other costs. If your company counts costs differently, correct it when applying.

---

## The Agreement block

The agreement decides the **annual hours** used to go from salary to hourly rate and, if the contract refers to the tables, the **salary**. The **Agreement** block says what has been used:

- **This contract is under "…" · 2025 tables**, with **View document** to open the gazette the tables come from.
- **Row used**: the table category, its amount and its payments ("Home care assistant: €1,145.81 × 14 payments"). If the agreement has several tables (one per scope, area or type of establishment), the row carries its block in brackets: "Administrative assistant (Care homes)".
- **No table row**: the salary is the one the contract states and only the hours are taken from the agreement.

What you can do:

| Button | What for |
|---|---|
| **Change agreement** | Choose another from your company's list. Those without tables yet cannot be chosen. |
| **Change row** / **Choose row** | Choose the table category if the proposed one is not this person's, or if the reading could not tell which it was. The dialogue shows each row with its group, its level, its block and, if it has one, that block's full-time hours. |
| **Type the price by hand** | Leave the agreement out and type the hourly rate yourself. |
| **Back to the proposed agreement** | Undo the changes. |

If you change the agreement or the row, the proposed hourly rate no longer stands: **it is recalculated when applying**, with the chosen table, and the block warns you.

When the catalogue has no agreement for this contract, the block says so (*There is no agreement for this contract in the catalogue*) and offers you **Choose agreement** or **Reference another agreement**. If there are several possible ones, it asks you to choose the one that applies. While there is no agreement, the rate is worked out with the legal maximum hours and is marked as estimated.

---

## Applying to the record

The **Apply to the employee record** block passes what was read to the person's record:

1. **Position from the catalogue.** If the occupation matches a position in your catalogue, it comes proposed. If not, **Create the position “…”** comes proposed with the name the contract gives; you can also choose another one from the catalogue or leave **Keep their current position**. The new position is created with its name only: the rate belongs to the person, not to the position, and if there was already one identical except for capitals or accents, that one is used.
2. **Hourly rate (€).** It comes proposed; you can correct it. If it is per agreement, *per agreement* appears: it is worked out when you apply.
3. **Branches where it applies.** If the person is at several, tick which ones. Each row shows *what they have now → what they will have*.
4. Press **Apply to profile** and confirm. The window shows **Before** and **After**. The job catalogue only changes if the contract's position is created; existing ones are not touched.

From then on, that person counts in costs with their new position and their hourly rate at those branches.

---

## Common problems

**The block says the PDF has no text.** It is scanned as an image. Ask for the contract as a PDF with text or fill in the position and the rate by hand in the person's record.

**It says it does not look like an employment contract.** Check that you uploaded the right document. An annex, a payslip or a contract with a customer are not read here.

**It says the contract seems to belong to someone else.** The name on the contract is not that of the person you uploaded the document to. Review it before applying anything.

**The hourly rate comes out as "Estimated" and it does not add up.** Look at **Calculation**: it says which salary and which hours have been used. If the agreement is not the right one, change it; if the category is not theirs, change the row; if you prefer your own figure, **Type the price by hand**.

**There is no agreement for this contract.** Your company has not referenced the agreement the contract cites. Press **Reference another agreement** and give it the link to the gazette or its PDF, without leaving the record. See [Collective agreements](139-collective-agreements.md).

**The tables are from an earlier year.** The agreement has tables up to 2025 and the contract starts in 2026. The most recent one available is used and you are warned. When the gazette publishes the new ones, reference the agreement again with that document: the new years are added.

---

## Related articles

- [Collective agreements](139-collective-agreements.md)
- [Payslips and contracts](32-payslips-and-contracts.md)
- [Who sees each document](136-who-sees-each-document.md)
- [Create and manage employees](../02-employees/06-create-and-manage-employees.md)
- [Cost analysis](../07-operational-intelligence/54-cost-analysis.md)
