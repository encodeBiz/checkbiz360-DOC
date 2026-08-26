# Quick start guide

This guide lets you get CheckBiz360 fully operational —with your first branch configured, an active employee and a validated clock-in— in under fifteen minutes. It is aimed at the account manager (Owner role) who has just registered and wants to verify that everything works correctly before rolling the platform out to the rest of the team.

Follow the ten steps in order. Each one builds on the previous one.

**Estimated time:** 10-15 minutes.

**Prerequisites:**
- An internet connection.
- An Android (5.0 or later) or iOS (13 or later) device.
- A corporate email address for the Owner account.

---

## The 10 steps

### Step 1. Create the account and the organisation

Go to `saas.encodebiz.com` and register with your corporate email, your phone number and a password. When you submit the form, the system takes you straight to creating the organisation: **company name**, **legal name** and **address** are required; the tax ID and the billing email are optional.

The time zone is resolved from the address and serves as the default for branches.

> **Note:** to be able to subscribe to a plan you will need complete legal details and a payment method. See [Plans, prices and features](../14-reference/91-plans-and-features.md).

### Step 2. Create the first branch with a geofence

Go to **Branches** and create one:

- **Name** of the branch (for example, "Head Office").
- Full **address** of the site; the coordinates and the time zone come from it.
- **Check zone in metres**: start at **100** if you have no reference point.

Save the branch.

### Step 3. Configure the branch schedule

Go to **Calendar** and open the **Branch** tab:

1. Select the working days (for example, Monday to Friday).
2. Set the start and finish time for each day (for example, 09:00-17:00).
3. Choose the **workday mode**: strict, if the official schedule governs; flexible, if the time actually worked governs.
4. Save the calendar.

This schedule is the reference against which the system validates every clock-in.

> **Note:** you can add several shifts per day and breaks within each shift. For this first set-up, a simple schedule is enough. Automatic A/B week alternation is not available; see [Rotating shifts](../04-calendar-and-schedules/27-rotating-shifts.md).

### Step 4. Create the first employee

Go to **Employees** and create a new one with the required details: **full name**, **email address**, **phone** and **relationship type** (internal or contractor).

Save. Then, from the employee's record, **link them to the branch**: that is where you choose their responsibility —for this set-up, *worker*—, their position and their hourly rate.

### Step 5. The employee receives the welcome email

The system will automatically send the employee an email with:

- The link to activate the account and set their password.
- The instructions for downloading the app.

> **Note:** if the email does not arrive within a few minutes, ask the employee to check their spam folder and confirm the address is spelled correctly on their record. See [Common problems and solutions](../13-support-and-incidents/88-common-problems-and-solutions.md).

### Step 6. The employee downloads the CheckBiz360 app

The employee downloads the application from the official store for their device:

- **iOS**: App Store — search for "CheckBiz360".
- **Android**: Google Play — search for "CheckBiz360".

Installation takes under a minute on most devices with a WiFi connection.

### Step 7. The employee signs in to the app

With the app installed, the employee:

1. Opens the CheckBiz360 app.
2. Enters their email address and the password they set when activating the account.
3. Selects the organisation if more than one appears (common when an employee works for several companies).
4. Reaches the main clocking screen.

### Step 8. The employee sets up two-factor authentication (2FA)

Although optional, activating 2FA at the first sign-in is recommended. The employee activates it from the security section of their profile, following the on-screen instructions to link their account with an authentication app.

> **Note:** 2FA can be configured as mandatory for all employees from the organisation settings in the back office. If your company handles sensitive data or has audit requirements, activating this option is recommended.

### Step 9. First clock-in from the app

With the employee already at the branch or nearby:

1. The employee opens the CheckBiz360 app.
2. Taps the **Clock in** button.
3. The app validates the GPS location against the branch geofence.
4. If the location is correct, the clock-in is recorded and a confirmation message appears.

If the location is not valid, the app will indicate that the device is outside the defined perimeter.

### Step 10. Check the record in the back office

In the back office, go to **Attendance**.

Check that:

- The employee's record appears with status **valid**.
- The time matches the clock-in that was made.

If the record appears as **failed**, the detail indicates the reason code —outside the check zone, outside the schedule— which you can look up in [Complete error codes](../14-reference/90-complete-error-codes.md).

---

## Result after completing the 10 steps

At the end of this guide, your CheckBiz360 account has:

- An organisation and a branch configured.
- An active employee with access to the app.
- The first attendance record validated and visible in the back office.

From this point on, you can repeat the process for the rest of the branches and employees, or explore the advanced modules: cost analysis, regulatory compliance reports and document management.

## Related articles

- [Create an account and set up the organisation](03-create-account-and-set-up-organisation.md)
- [Platform structure](05-platform-structure.md)
- [Check-in and check-out from the app](../03-time-tracking/14-check-in-and-check-out-from-the-app.md)
- [Create and manage branches](../08-branches-and-organisation/57-create-and-manage-branches.md)
