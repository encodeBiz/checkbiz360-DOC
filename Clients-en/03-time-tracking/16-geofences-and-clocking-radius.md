# Geofences and clocking radius

The geofence is the mechanism by which CheckBiz360 guarantees that an employee is physically at the workplace at the moment they record their attendance. This article explains what a geofence is, how to configure it correctly and what happens when an employee tries to clock in outside the permitted area.

---

## What a geofence is

A geofence is a circular perimeter defined around a branch's GPS coordinates. Its function is to establish the area within which an on-site clock-in is considered valid. When an employee presses the clock-in button, the app sends their device's coordinates and the system calculates the distance between that point and the centre of the branch. If the distance exceeds the configured radius, the clock-in is rejected.

The radius is expressed in metres and can be adjusted to the area and the physical characteristics of each site.

---

## How to configure the clocking radius

The clocking radius is configured at branch level, accepting a whole number in metres.

1. Sign in to the CheckBiz360 back office with the **manager** or **owner** role.
2. Navigate to the **Branches** section and select the branch you want to configure.
3. Open the attendance configuration or branch settings tab.
4. Find the **Clocking radius** field and enter the value in metres.
5. Make sure the branch's GPS coordinates are correctly defined. The radius is of no use if the centre point is not properly located.
6. Save the changes. The new configuration applies immediately to subsequent clock-ins.

---

## How to disable geofence validation

In some situations, geofence validation is not applicable: branches with no fixed address, field working environments or premises with imprecise GPS coordinates.

To disable the geofence at a specific branch, enable the "disable geofence validation" option in that branch's configuration.

1. Go to the branch configuration as described in the previous section.
2. Enable the **Disable geofence validation** field.
3. Save the changes.

With this option active, the system skips the distance check for every employee assigned to that branch. The other validations (schedule, device, biometrics) continue to apply normally.

> **Note:** This option is different from per-employee remote work mode. "Disable geofence validation" affects every employee at the branch, whereas "remote work" is an individual setting.

---

## What happens when the employee is outside the radius

If the employee tries to clock in from a location outside the permitted radius, the system:

1. Records the clock-in attempt with status `failed`.
2. Assigns the error code `checklog/out_of_radius`.
3. Stores the actual distance between the device's location and the centre of the geofence, along with the radius configured at that moment.

This information is available in the employee's history and can be consulted by the manager from the back office. It makes it possible to identify whether the problem is one-off (the employee was in another building on the site) or systematic (the radius is badly sized).

The employee sees a message in the app indicating that they are outside the clocking zone.

---

## Radius recommendations by type of site

Choosing the right radius depends on the size and physical layout of the workplace. Indicative values are given below:

| Type of site | Recommended radius |
|---|---|
| Small office or retail unit | 50 – 100 metres |
| Industrial unit or warehouse | 200 – 500 metres |
| University campus or large industrial site | 500 – 1,000 metres |
| Multi-storey office building | 100 – 200 metres |

These values are indicative. Validating the radius on site is recommended: ask an employee to make a test clock-in from the furthest points of the site to check that the radius covers the working area properly.

An excessively small radius generates unnecessary failed clock records. An excessively large radius reduces the effectiveness of presence control. Look for the balance that matches the physical reality of the site.

---

> **Warning about GPS devices:** The accuracy of geolocation depends on the mobile device and the conditions of the environment (indoors, areas with a weak signal, devices with GPS disabled). In environments with low GPS accuracy, consider widening the radius slightly to avoid false rejections.

---

## Roles with access to this feature

Configuring geofences and the clocking radius requires the **manager** or **owner** role. Employees have no access to this configuration.

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Remote clocking in](15-remote-clocking-in.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
