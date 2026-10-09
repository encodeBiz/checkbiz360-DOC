# Working off-site

CheckBiz360 covers working scenarios outside the company's premises: set-ups, services at the customer's home, field work or teleworking. The **Works off-site** option lets an employee record their attendance without being inside a branch geofence, while keeping the authentication and effective schedule validations in place.

> **Note:** until September 2026 this option was called **Remote work**. The name changed, not the way it works: "remote" suggested teleworking from home, and the option is meant for anyone who does not clock in at a site.

---

## What working off-site is

It is an individual per-employee setting that disables geolocation validation when clocking in. When it is active, the system does not check whether the device is within the branch radius. All the other validations (schedule, trusted device and biometrics where applicable) continue to work normally.

It is intended for employees who work regularly or occasionally away from the premises: field teams, technicians who travel, set-up or event staff, and teleworkers too.

---

## How to enable it for an employee

It is enabled by users with the **manager** or **owner** role from the employee's record in the back office.

1. Go to the CheckBiz360 back office.
2. Navigate to the **Employees** section and open the employee's record.
3. Press **Edit**.
4. Enable **Works off-site** and complete the employee's address, which becomes required.
5. Save the changes.

From that moment on, the employee's clock records will not include geofence validation. On their record, the situation appears as **Works off-site**; if the option is disabled, as **Clocks in on site**.

> **Tip:** if what you need is to check that the employee is at the location of a specific job —a customer's home, for example—, do not disable the geofence: give the task its own work site. See [Own work site](../06-tasks/40-create-a-task.md#own-work-site).

---

## What changes when it is active

### Geolocation disabled

The system skips clocking radius validation entirely. The employee can record their entry and exit from any location without the system generating `checklog/out_of_radius` errors.

### The employee's time zone

When working off-site is active, the system uses the employee's time zone for schedule validations, instead of the branch's time zone. This is especially relevant for teams distributed across different countries or regions.

If the employee's time zone is not configured, the system uses the organisation's time zone by default.

### Authentication unchanged

Working off-site does not alter the authentication requirements. If the employee has 2FA enabled, they must still clock in from a trusted device. If they have biometrics required, they must continue verifying their biometric identity before every clock-in.

---

## Common use cases

**Travel and field work:** Employees who work at client premises or on the move. If the geofence is not applicable to their activity, working off-site avoids unnecessary failed clock records.

**Geographically distributed teams:** Companies with employees in different provinces or countries who are not assigned to a specific physical branch. The option makes it possible to centralise attendance control without creating virtual branches for each location.

**Full teleworking:** The employee works entirely from home. **Works off-site** is enabled permanently and their time zone is configured correctly.

**Partial teleworking:** The employee alternates between office and home depending on the day. The manager can enable or disable the option according to the agreed calendar, or keep it always active if the employee clocks in correctly in both environments.

---

## How it is reflected in reports

Clock records made off-site are identified as such in the system. From the back office, the manager can filter attendance reports by record type to obtain a separate view of workdays at the site and those carried out off-site.

This distinction is useful for tracking teleworking agreements, for complying with the limits on remote working days established in collective agreements or internal arrangements, and for productivity analysis by working mode.

---

> **Configuration warning:** Enabling working off-site without correctly configuring the employee's time zone can create discrepancies in the calculation of hours if the employee is in a different time zone from the branch. Always check the employee's time zone before enabling this mode.

---

## Roles with access to this feature

Enabling working off-site requires the **manager** or **owner** role. The employee cannot enable or disable this mode themselves.

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Geofences and clocking radius](16-geofences-and-clocking-radius.md)
- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
