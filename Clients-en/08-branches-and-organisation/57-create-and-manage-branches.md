# Create and manage branches

A branch in CheckBiz360 represents a physical or logical operational unit that employees are assigned to and from which clocking is controlled. It can correspond to a store, an office, a workplace or any other unit the company needs to manage independently. This article explains how to create the first branch, how to complete its configuration and how to edit or deactivate it afterwards.

## Prerequisites

To create and manage branches you need to access the web back office with an **Owner** or **Manager** role holding branch administration permissions. If you do not have the necessary permissions, contact your organisation's Owner.

## Create a branch

### Required fields

When creating a branch you will have to complete the following fields:

- **Name**: the branch's visible identifier throughout the system. Use a clear, unique name within your organisation (for example, "Madrid Centre" or "North Warehouse").
- **Address**: the workplace's complete postal address. The system automatically geocodes this address to obtain the GPS coordinates that will be used as the central point of the clocking geofence. It is important that the address is accurate to guarantee the coordinates are exact.
- **Clocking radius**: distance in metres from the branch's central point within which the system considers a geolocated clock-in valid. A radius of 100 metres is the recommended value for offices in urban environments; it can be widened for industrial facilities or open spaces.
- **Time zone**: it forms part of the address and determines how clocking times are interpreted and how workdays are calculated. It is especially relevant in organisations with sites in different countries or regions. If it is not stated, the branch inherits the organisation's time zone.

### Optional fields

- **Tax ID**: the site's tax identifier, when it differs from the organisation's.
- **Status**: active or inactive. By default, a newly created branch is active.
- **Additional data**: free key/value fields for information specific to your organisation.
- **Calendar**: weekly schedule, breaks and workday mode. If it is not configured, the branch inherits the organisation's calendar.

### Steps to create the first branch

1. Go to the back office at `saas.encodebiz.com` and sign in with your credentials.
2. In the side menu, inside CheckBiz, select **Branches**.
3. Press the create branch button.
4. Enter the branch name in the corresponding field.
5. Type the complete postal address in the **Address** field. Select the suggestion that appears in the autocomplete dropdown to make sure the system obtains the correct coordinates.
6. Check that the interactive map shows the marker in the right position. If the position is not exact, you can drag the marker manually to adjust it.
7. Enter the clocking radius in metres. If you have no defined criterion, start with 100 metres and adjust it after the first few weeks of operation.
8. Check the time zone associated with the address.
9. Complete the optional fields if you consider it necessary.
10. Press **Save**. The system will confirm the creation with a success message and the new branch will appear in the list.

> **Warning:** If geocoding the address does not return precise coordinates, the system will indicate this with a warning. In that case, adjust the marker manually on the map before saving. Incorrect coordinates will generate unjustified clocking rejections for the employees assigned.

## Edit a branch

To modify an existing branch's details:

1. Go to **Branches** in the side menu.
2. Find the branch you want to edit and click on its name or the edit icon.
3. Modify the fields you need to update.
4. If you change the address, the system will geocode again and update the coordinates. Check the map before saving.
5. Press **Save changes**.

> **Warning:** Changes to the clocking radius or to the coordinates take effect immediately. Employees attempting to clock in at that moment may be temporarily affected.

## Deactivate a branch

Deactivating a branch prevents the employees assigned to it from clocking in there, but preserves all the historical data. This operation is reversible.

1. Go to **Branches**.
2. Press the edit icon for the branch you want to deactivate.
3. Change the **Status** field to **Inactive**.
4. Press **Save changes**.

The system will show you a warning indicating how many employees are assigned to that branch and will be affected. See the article on branch statuses to understand the full impact of this action.

---

> **Role note:** Creating and editing branches is available to the **Owner** and **Manager** roles with organisation administration permissions. Consulting the branch list is also available to **Supervisor**.

## Related articles

- [Advanced branch configuration](58-advanced-branch-settings.md)
- [Branch statuses](59-branch-statuses.md)
- [Assign employees to branches](60-assign-employees-to-branches.md)
- [Organisation configuration](61-organisation-settings.md)
- [Multi-branch global view](62-multi-branch-global-view.md)
