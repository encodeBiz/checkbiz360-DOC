# Remote clocking in

CheckBiz360 covers working scenarios outside the company's physical premises. Remote work mode lets employees record their attendance without having to be inside the branch geofence, while keeping the authentication and effective schedule validations in place.

---

## What remote work mode is

Remote work in CheckBiz360 is an individual per-employee setting that disables geolocation validation when clocking in. When this mode is active, the system does not check whether the device is within the branch radius. All the other validations (schedule, trusted device and biometrics where applicable) continue to work normally.

This mode is intended for employees who do their work regularly or occasionally away from the premises: teleworkers, geographically distributed teams, or employees on partial teleworking who alternate between the office and home.

---

## How to enable remote work for an employee

Enabling remote work is an operation carried out by users with the **manager** or **owner** role from the employee's configuration panel in the back office.

1. Go to the CheckBiz360 back office.
2. Navigate to the **Employees** section and select the relevant employee.
3. Open the attendance configuration or employment details tab.
4. Enable the **Remote work** field.
5. Save the changes.

From that moment on, the employee's clock records will not include geofence validation.

---

## What changes when remote work is active

### Geolocation disabled

The system skips clocking radius validation entirely. The employee can record their entry and exit from any location without the system generating `checklog/out_of_radius` errors.

### The employee's time zone

When remote work is active, the system uses the employee's time zone for schedule validations, instead of the branch's time zone. This is especially relevant for teams distributed across different countries or regions.

If the employee's time zone is not configured, the system uses the organisation's time zone by default.

### Authentication unchanged

Remote work does not alter the authentication requirements. If the employee has 2FA enabled, they must still clock in from a trusted device. If they have biometrics required, they must continue verifying their biometric identity before every clock-in.

---

## Common use cases

**Full teleworking:** The employee works entirely from home. "Remote work" is enabled permanently and their time zone is configured correctly.

**Partial teleworking:** The employee alternates between office and home depending on the day. In this case, the manager can enable or disable remote mode according to the agreed calendar, or keep it always active if the employee clocks in correctly in both environments.

**Geographically distributed teams:** Companies with employees in different provinces or countries who are not assigned to a specific physical branch. Remote mode makes it possible to centralise attendance control without having to create virtual branches for each location.

**Travel and field work:** Employees who work at client premises or on the move. If the geofence is not applicable to their activity, remote mode avoids unnecessary failed clock records.

---

## How it is reflected in reports

Clock records made in remote mode are identified in the system as remote work records. From the back office, the manager can filter attendance reports by record type to obtain a separate view of on-site and remote workdays.

This distinction is useful for tracking teleworking agreements, for complying with legal limits on remote working days established in collective agreements or internal arrangements, and for productivity analysis by working mode.

---

> **Configuration warning:** Enabling remote work without correctly configuring the employee's time zone can create discrepancies in the calculation of hours if the employee is in a different time zone from the branch. Always check the employee's time zone before enabling this mode.

---

## Roles with access to this feature

Enabling remote work mode requires the **manager** or **owner** role. The employee cannot enable or disable this mode themselves.

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Geofences and clocking radius](16-geofences-and-clocking-radius.md)
- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
