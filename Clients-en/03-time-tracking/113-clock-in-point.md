# Clock-in point: clocking in from a device at the site

Some people do not want to install anything on their personal phone, and at some sites the company gives nobody a device. There are also sites where one person ends up swiping everyone's card. The **clock-in point** solves both: a fixed device at the site, a tablet or a low-cost phone, where each person clocks in with their QR or their code and the device takes a photo at that moment.

It works alongside the app. Whoever wants to keeps clocking in with their phone, and whoever does not clocks in at the wall.

> **Status: Partially available.** It is subscribed and managed from the panel. The device at the site needs the next version of the CheckBiz360 app, which is being published.

---

## What it solves

- **Clocking in without your own phone.** Everyone clocks in, app or no app.
- **Knowing who was standing there.** Every clock-in carries the photo of whoever pressed the button. If one person clocks in for others, their photos show it.
- **Clocking in at the site and nowhere else.** The device only works near its branch's address, and only on one device at a time.
- **Seeing what looks odd without checking everything.** Several clock-ins in a row on the same device are flagged as a burst and come first in the review.

**No biometrics.** The clock-in point does not read fingerprints or recognise faces. A person looks at the photo when needed. That is why it does not process special-category data or require an impact assessment for biometrics.

---

## How it works at the site

1. The person holds their **QR card** up to the camera, or types their **6-digit code** if they do not have it with them.
2. The device greets them by name and offers the clock-in that is due: **Clock in**, **Clock out**, **Start break** or **End break**.
3. When they press it, the front camera takes the photo and the clock-in is recorded with the server's time.

With the card, clocking in is one gesture and one tap. Before the photo, the screen explains that it helps prevent fraud and may be reviewed by a manager. If the device cannot see a face, it says so and lets them retake the photo. If the person clocks in anyway, the clock-in is saved and flagged as **No face** for the review. A clock-in never fails because of the light or the camera.

The rules are the usual ones: their calendar, their shifts, the sequence of check-ins and check-outs, and public holidays. A clock-in the app would reject, the clock-in point rejects too, with the same reason.

### My week

From the home screen, **See my week** shows the person their schedule for this week and next, with their tasks. To see it they also identify themselves and a photo is taken, as when clocking in. That way nobody can look at someone else's schedule.

---

## Subscribing

The clock-in point is a paid add-on, like inventory. It is in the panel's side menu, under **Clock-in point**.

| | |
|---|---|
| Price | **€19 a month**, covering up to **20 active clock-in points** |
| From the 21st | **€0.90 a month** for each active clock-in point |
| Trial | **15 days** on your first subscription |
| Invoice | Separate from your plan |

Only **active** clock-in points are charged. Subscribing does not activate any: you choose which branches you will use it in. Only the account owner can subscribe.

---

## Setting it up at a branch

When you subscribe, every branch with a geolocated address has its clock-in point ready. A branch without an address does not get one until you add it, because without an address there is no site to measure from.

1. In **Clock-in point**, find the branch in the table and click **Activate**. The panel tells you the price before you confirm.
2. The **email**, **password** and **unlock PIN** for that clock-in point are created. You can see, copy or print them whenever you want from **View credentials**.
3. On the device at the site, open the CheckBiz360 app and sign in with that email and password. The app starts in **kiosk mode**, which is what the app calls the clock-in point.
4. Hand out the QR cards and the codes to your staff (see below).

With many branches, setting up takes a moment. Meanwhile, the screen shows how many are ready.

### What the device needs

Before signing in, the app checks the device. If it does not meet the requirements, it says why and does not sign in.

- **Location turned on**, with permission for the app while it is in use.
- **An accurate position**, of 100 m or better. Tablets with a SIM have GPS. A wifi-only tablet that locates itself well over the network also works.
- **A front camera.**
- **Android 10 or iOS 15** or later.

A tablet of 8 inches or more helps when there is a queue, but a low-cost phone on a wall mount also works.

### Only near the site, and on one device at a time

- The device only signs in within **200 m** of the branch's address. You can change that distance with **Edit radius**.
- If the device leaves the radius or loses an accurate position, the clock-in point becomes **Suspended** and the screen says so. It comes back on its own once the conditions are met again.
- If someone signs in with the same credentials on another device, the previous one is signed out. That is normal when a tablet breaks and is replaced.

To leave kiosk mode on the device itself you need the **unlock PIN**. From the panel you can also **Sign out device** or **Regenerate credentials**, which creates a new password and PIN and signs out whatever device was in.

---

## QR cards and codes

Each person has **their own** QR and **their own** 6-digit code. They are the same at all their branches.

- **QR cards.** One card per person, business-card size, to print and laminate. The QR only works for clocking in at the clock-in point.
- **Send by email.** You can send the card, with the QR and the code, to each person's email, or use **Email everyone** for a whole branch. Anyone without an email does not receive it, and the panel tells you.
- **From the employee record.** **Send card** in the **App access** block sends it to that person without going through the branch.
- **Codes.** The code is for whoever forgets their card. Click the eye to see or copy it. Who did it is recorded.
- **Regenerate.** If someone loses their card, **Regenerate QR** stops accepting the old one as soon as you confirm. **Regenerate code** does the same with the code.

Anyone with the app also sees their QR in it, under **My QR**.

---

## Reviewing the photos

**Review** holds the photos of each clock-in of the day, with name, time and type. **Bursts** come first: three or more clock-ins in a row on the same device, less than 30 seconds apart. Clock-ins with **No face** and those made **Out of radius** are also marked.

There is no need to look at a thousand photos. Check the bursts and whatever catches your eye; the rest is there in case you need it.

If a photo is not the person, tap it and click **Not this person**. The clock-in is voided, and that person's QR and code stop working. They will need a new card and code. The person is notified of any rejected clock-in.

### How long photos are kept

Photos are kept for **30 days** and then deleted automatically. The clock-in is always kept. Photos count towards your company's storage, just like documents.

### What to tell your staff

The photo is ordinary personal data as long as no machine uses it to identify anyone. Tell your staff what the photo is for, who can see it and how long it is kept. If you have a works council, consult it first. Your data protection officer should approve it.

---

## Clock-in point statuses

| Status | What it means |
|---|---|
| **Not active** | It is ready but has no credentials. It is not charged. |
| **Active** | It has credentials and counts on the invoice. |
| **Suspended** | The device is out of the radius or does not have an accurate position. It comes back on its own. |
| **Disabled** | It has been deactivated or the subscription has ended. |

**Deactivate** deletes the password and the PIN, signs out the device and stops it counting on the invoice. Clock-ins and photos are kept, and you can activate it again whenever you want.

---

## Who can manage it

The company's **owner** and **administrators** manage the clock-in point from the panel. Only the owner can subscribe to it or cancel it.

---

## Common problems

| What happens | What to do |
|---|---|
| "This device does not meet the kiosk requirements" | Read the reason. Usually location is off or the position is inaccurate. Turn location on or use a device with GPS. |
| "This kiosk can only be activated at…" | The device is far from the branch's address. Check the address in the panel or widen the radius. |
| "We do not recognise this code" | The code or the QR does not belong to anyone in this company, or it was regenerated. Hand over the current code from **Codes**. |
| "Too many attempts" | Several wrong codes were typed in a row. Wait the seconds shown. |
| "This site is not assigned to you" | The person is not assigned to that branch. Assign it from their record. |
| "Outside your shift" | The clock-in does not fit their schedule, just as would happen in the app. Check their calendar. |
| A branch does not appear with its clock-in point | It has no geolocated address. Add it and the clock-in point is created automatically. |

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Geofences and clocking radius](16-geofences-and-clocking-radius.md)
- [Review and approval of clock records](20-reviewing-and-approving-clock-records.md)
- [App access and email change](../02-employees/116-app-access-and-email-change.md)
- [Plans, prices and features](../14-reference/91-plans-and-features.md)
