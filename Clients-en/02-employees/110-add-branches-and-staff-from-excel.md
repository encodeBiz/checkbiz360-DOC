# Add branches and staff from Excel

The first day with CheckBiz360 usually starts with a list: your accountant sends the staff list, you have the sites in a spreadsheet, and creating forty records and six branches one by one is a whole afternoon. There is no need. One Excel template, one upload and one review are enough to onboard the whole company at once, with nothing created until you confirm.

---

## What it solves

- **The whole staff and all the sites at once**, from one sheet with two tabs.
- **You see it before anything is created.** Each branch and each person appears with what will happen: new, already exists, branches added, no changes or error.
- **An error does not stop you.** Rows with errors are left out; the rest are created. Fix the file and upload it again: what was already created is not duplicated.
- **The welcome, when you decide.** No email is sent on import. Once you have checked everything is right, one button sends the app welcome to the new people.
- **Good for growing, not just for starting.** Upload it again with the new people: existing people are recognised by their email, and branches by their name.

---

## How it works, in three steps

| Step | What happens |
|---|---|
| **1. Download the template** | From the employee list or the branch list, with the **Import** button. |
| **2. Fill it in and upload it** | One sheet for branches and one for people. Nothing is created on upload. |
| **3. Review and confirm** | The platform shows what it will do with each row. Only on confirmation is anything created. |

---

## 1. Download the template

1. Go to **Employees** (or **Branches**) and click **Import**.
2. In the **Import branches and staff** window, click **Download template**.

The template has two sheets, **Branches** and **Employees**, with **example rows that start with DELETE**: you can remove them or leave them, they are not imported.

> If a branch already exists in CheckBiz360, there is no need to repeat it in the Branches sheet: just write its name in each person's row.

### Branches sheet

| Column | What to enter |
|---|---|
| **Name** * | What you call the site. It is the name you will use in the Employees sheet. |
| **Address** * | Street and number. It is where your people will clock in. |
| **Postal code**, **Country** | If left blank, they are completed from the address. |
| **Tax ID** | The site's own, if it has one. |
| **Clock-in radius (m)** | How far from the site clocking in is allowed. Blank means the usual radius. |

An address without a street number is not enough: if it can only be located approximately, the row comes back with an error asking for street and number.

### Employees sheet

| Column | What to enter |
|---|---|
| **Full name** * | First name and surname. |
| **Email** * | Used to sign in to the app and to receive the welcome. It is what identifies the person: if it already exists, no second record is created. |
| **Phone**, **ID number** | Optional. |
| **Job title** | Their occupation. If it is not yet in your job catalogue, it is added; the review tells you which ones are new. |
| **Type** | **Staff** or **Collaborator**. Blank means staff. |
| **Branch** * | The name of their site, as in the Branches sheet or as it is already called in CheckBiz360. If they work at several, separate them with semicolons. |
| **Responsibility** | **Worker**, **Supervisor** or **Manager** at that site. Blank means worker. |
| **Hourly rate** | The one that feeds the cost analysis. Blank means the job title's rate, if it already exists. |
| **Schedule** | **Weekly** (the usual one) or **From tasks**. Blank means weekly. |

Columns marked with an asterisk are required.

---

## 2. Upload the file

Click **Choose file**, select the completed template and click **Review**. Excel (.xlsx) files up to 2 MB and 2,000 people are accepted. If you upload a file that is not the template, the platform says so and reads nothing.

While reading the file it checks the addresses, so with many sites it takes a few seconds.

---

## 3. Review what will be done

Before confirming you see two tables, **Branches** and **People**, each row with its status:

| Status | Meaning |
|---|---|
| **New** | Will be created. For branches, with the address as it was located (exact or approximate on the street). |
| **Already exists** | Not touched. |
| **Branches added** | The person already existed and gains the new sites in their row. |
| **Schedule updated** | Only their schedule mode changes. |
| **No changes** | Nothing to do with that row. |
| **Error** | That row is not imported: the note says why (an imprecise address, a mistyped email, a branch that does not exist). The other rows are imported. |

At the top, a summary: how many new branches and people, how many already existed, how many with errors, and how many active people are added to your invoice.

To fix something, correct the file and click **Upload another file**. If you close the window without confirming, nothing is created.

When you are happy, click **Confirm and import**. Progress is shown; you can close the window and the import carries on. If it does not finish, **Retry** picks up where it left off without duplicating anything.

---

## 4. Send the welcome

When it finishes, the window says how many new people have not yet received the app welcome. Once you have checked their records are right, click **Send welcomes**: each person receives the email they use to sign in to the app for the first time. If you prefer to send them later, close the window: the people stay created.

---

## Who can import

Owners and administrators of the company. Each active person created counts on the invoice from that moment, just as if you had added them by hand.

---

## Related articles

| Article | Description |
|---|---|
| [Create and manage employees](./06-create-and-manage-employees.md) | Adding a single person and the record statuses |
| [Create and manage branches](../08-branches-and-organisation/57-create-and-manage-branches.md) | Adding a site and its address |
| [Roles and responsibility levels](./07-roles-and-responsibility-levels.md) | What a worker, a supervisor and a manager can do |
| [Your operations manager in Claude or ChatGPT](../15-integrations/109-your-operations-manager-in-claude-or-chatgpt.md) | The same onboarding, asked of your assistant from your accountant's list |
