# Branch statuses

In CheckBiz360, each branch has a status that determines whether the employees assigned can operate normally or whether the site is temporarily suspended. Understanding the meaning of each status and the consequences of changing it is essential to avoid unplanned interruptions in attendance recording.

## Possible statuses

A branch can be in one of the following two statuses:

### Active

This is the normal operating status. When a branch is active:

- The employees assigned can clock in from the app without restrictions related to the branch status.
- The effective calendar and the configured schedules are in force.
- Reports and analyses include that branch's data.
- Notifications and alerts relating to the branch work normally.

Every newly created branch is active by default.

### Inactive

An inactive branch is temporarily suspended. Its effects are as follows:

- Employees attempting to clock in from the app at that branch will receive an error indicating that the branch is not available.
- It is not possible to create new attendance records linked to that branch from the app.
- Managers can still access the branch from the back office to consult historical data and modify the configuration.
- Employee assignments to the branch are kept intact.
- The history of clock records, workdays and documents associated with the branch remains intact and can be consulted.

> **Warning:** Deactivating a branch takes effect immediately. If there are employees attempting to clock in at the moment of the change, their clock records will be rejected. Plan status changes outside the working hours of the staff affected, or communicate them in advance.

## The difference between deactivating and deleting

Deactivating and deleting are different operations with very different consequences:

| Action | Effect on the data | Reversibility | Recommended for |
|---|---|---|---|
| **Deactivate** | Historical data is retained in full | Reversible at any time | Temporary closures, refurbishments, restructuring |
| **Delete** | The branch's data is unlinked from the active structure | Irreversible | Branches created in error with no associated data |

> **Warning:** CheckBiz360 does not allow branches with associated clock records, workdays or documents to be deleted. If you need to permanently close a branch with historical data, the correct operation is to deactivate it and ask the support team for definitive unlinking should it be necessary for data protection compliance.

In practice, the vast majority of branch closures —whether temporary or permanent— should be handled through deactivation, not through deletion.

## How to change a branch's status

### Deactivating an active branch

1. Go to the web back office and navigate to **Branches**.
2. Find the branch in the list. Active branches are shown with a green indicator.
3. Press the edit icon or the branch name to open its record.
4. In the **Status** field, select **Inactive**.
5. The system will show a warning with the number of employees assigned to the branch who will be affected.
6. Confirm the operation and press **Save changes**.

### Reactivating an inactive branch

1. Go to **Branches**.
2. In the list, enable the filter to show inactive branches if they do not appear by default.
3. Press the edit icon for the branch you want to reactivate.
4. In the **Status** field, select **Active**.
5. Press **Save changes**.

Reactivation is immediate. The employees assigned will be able to clock in again as soon as the change has been saved.

## Impact on historical data

A branch's status does not alter any historical data. Regardless of whether a branch is active or inactive:

- Clock records stored before the status change remain in the system with their original information.
- Reports for previous periods reflect the real data for those periods.
- Documents and tasks associated with the branch remain accessible to managers from the back office.
- Cost and hours-worked calculations for past periods are unaffected.

A branch's status is, in essence, an operational switch controlling whether employees can continue generating new records from that branch. It has no retroactive effect.

---

> **Role note:** Changing a branch's status is available to the **Owner** and **Manager** roles with organisation administration permissions. The **Supervisor** role can consult the status of the branches they are assigned to, but cannot modify it.

## Related articles

- [Create and manage branches](57-create-and-manage-branches.md)
- [Advanced branch configuration](58-advanced-branch-settings.md)
- [Assign employees to branches](60-assign-employees-to-branches.md)
- [Multi-branch global view](62-multi-branch-global-view.md)
