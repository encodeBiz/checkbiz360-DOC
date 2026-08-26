# Advanced branch configuration

Each branch in CheckBiz360 supports settings that adapt the system's behaviour to the particularities of that workplace: how far the clocking zone extends, how hours are counted and how breaks are recorded. This article describes each parameter, where it is configured, its effect and when it is worth modifying.

## Where to find each setting

A branch's advanced configuration is split across two places, depending on what you want to adjust:

- **The branch record** (**Branches** in the side menu → edit) holds the site's details and the **operational configuration**: the check zone.
- **The calendar** (**Calendar** in the side menu → **Branch** tab) holds the weekly schedule, the breaks, the workday mode and the break mode.

## Parameter table

| Parameter | Where | Type | Description |
|---|---|---|---|
| Check zone in metres | Branch record | Integer (metres) | Radius around the coordinates within which clocking is accepted |
| Check zone enabled | Branch record | Boolean | When disabled, the geofence stops being validated at this branch |
| Status | Branch record | Active / Inactive | An inactive branch does not accept clock records |
| Additional data | Branch record | Key/value | Free fields specific to your organisation |
| Weekly schedule and breaks | Calendar | Time windows | Shifts per day and breaks within each shift |
| Strict / flexible workday | Calendar | Boolean | Count the official schedule or the time actually worked |
| Strict / flexible break | Calendar | Boolean | Deduct a fixed duration or the actual break time |
| Break time (minutes) | Calendar | Integer (minutes) | Duration deducted when the break is strict |

> **Note:** there is no "entry tolerance" or "automatic timestamp adjustment" parameter. What decides whether time worked outside the window counts or not is the workday mode. See [Strict and flexible workday](../04-calendar-and-schedules/28-flexible-schedule.md).

## Detailed description of each parameter

### Check zone enabled

When this option is disabled, the system accepts clock records from any GPS location without checking whether the employee is within the defined radius. The GPS coordinate is still recorded in the system, but is not used as a validation criterion.

**When to use it:** branches where employees work on the move, at client premises or in spaces with poor GPS coverage (basements, warehouses with thick walls). It is also useful during the initial configuration period, when the radius has not yet been adjusted precisely.

> **Warning:** Disabling the geofence removes a layer of anti-fraud control. Use this parameter only when there are justified operational reasons and inform the compliance team if your company is subject to time control audits.

### Break mode

Breaks have two modes, chosen in the branch calendar:

- **Strict break**: the system deducts exactly the minutes configured. The employee **does not mark** the start or end of the break, and longer or shorter breaks are not recognised.
- **Flexible break**: the employee **marks** the start and end of each break from the app, and the system counts the effective duration.

**When to use strict:** fixed breaks set by collective agreement, the same every day, where requiring two more clock records a day adds nothing. **When to use flexible:** variable breaks depending on workload, or when the real duration of breaks has to be evidenced.

### Break time

When the break is strict, this value —in minutes— is what is deducted from the workday. Set it to the break time stipulated in the collective agreement applicable at that branch.

With a flexible break the field does not apply: the time the employee records governs.

### Workday mode

Decides whether counting follows the official schedule (**strict workday**) or the time actually worked (**flexible workday**). It is the setting with the greatest impact on hours reports and is explained in detail in [Strict and flexible workday](../04-calendar-and-schedules/28-flexible-schedule.md).

## Interaction between parameters

- The **workday mode** and the **break mode** are independent: you can have a strict workday with a flexible break, or the other way round.
- The **break time** only applies with a strict break; with a flexible one it is ignored.
- **Disabling the check zone** is independent of the rest and can be combined with any configuration.
- Everything in the calendar follows the organisation → branch → employee **inheritance**: whatever the branch does not define, it inherits from the organisation.

> **Warning:** Changes take effect on subsequent clock records. They do not modify records already existing in the history.

---

> **Role note:** Advanced branch configuration is available only to the **Owner** and **Manager** roles with organisation administration permissions. The **Supervisor** and **Worker** roles have no access to this section.

## Related articles

- [Create and manage branches](57-create-and-manage-branches.md)
- [Branch statuses](59-branch-statuses.md)
- [Assign employees to branches](60-assign-employees-to-branches.md)
- [Organisation configuration](61-organisation-settings.md)
