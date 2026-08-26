# RentmanBiz — the Rentman integration

**RentmanBiz** is the add-on that connects CheckBiz360 with Rentman, the software many event, AV and equipment rental companies use to plan their projects, crew and warehouse.

## What Rentman is missing (and why this matters)

Rentman knows **what is planned**: which job is on, what equipment goes out, who should be there and for how many hours. What it does not know is **what actually happened**: whether that person turned up, at what time, whether they were at the venue or at home, and how many hours they really worked.

Today that gap is filled by hand. Someone asks, someone writes it down, someone types the hours in at the end of the week. And when the end client questions an invoice, or a worker questions their payslip, all there is is each side's word.

RentmanBiz closes that gap in both directions: it brings **who works and where** from Rentman, and sends back **the hours actually clocked**.

## What it gives you, specifically

### Hours stop being typed

When a worker closes their shift in CheckBiz360, those hours appear on their own in the matching Rentman project within the next quarter of an hour. No spreadsheets in between, no reminders, nobody transcribing anything.

### Verifiable hours, not declared ones

This is the difference that counts. *"The technician says he was there ten hours"* is not the same as *"it is on record that he clocked in at 08:02 inside the venue, from his authorised device, and clocked out at 18:10 from the same place"*.

That changes two conversations: the one with the end client about an invoice, and the one with a worker about their payslip.

### The legal time record, which Rentman does not cover

Rentman is a production tool, not a legal time-keeping system. The law requires a daily record of working hours, kept, accessible and tamper-proof. CheckBiz360 provides it — with exportable reports — without changing how anyone works: planning stays in Rentman.

### The event becomes a place to clock in

Every job with crew assigned becomes a work site with its own **geofence**, taken from the venue address. In this industry nobody clocks in at the office: they clock in at the arena, the theatre or the warehouse where the build happens. And nobody has to create sites by hand every week.

**Warehouses** come in the same way, as permanent sites: that is where people clock in every day.

### Everyone knows what they are doing on arrival

Rentman assignments become tasks inside CheckBiz360. Workers open the app and see which job they are going to, with what role and what schedule, and tick off what they complete. They stop arriving and asking.

### Who prepared each order, and how long it took

This is probably the change that shows up most in the daily life of a rental company.

A dry hire or a sale takes nobody to an event, but somebody has to prepare that equipment before the client picks it up, and somebody has to check it back in when it returns. Today that is arranged verbally — *"I'll sort it out this afternoon"* — and recorded nowhere.

With RentmanBiz, each operation generates its task at the right warehouse, dated by when the equipment goes out. From there:

- **You know who has to do it**: the manager shares those tasks among the warehouse crew, and each person sees theirs on their phone.
- **You know who did it**, because the task carries their name and is marked complete.
- **And you know how long it took**, because that person is clocked in at that warehouse while preparing it.

That opens questions you could not even ask before: what a typical order really costs to prepare, whether two people take the same time on the same job, whether the warehouse's busy spells match what was planned, or how many people you need on the Friday of a heavy weekend.

It ships **off by default**, because not every company wants to run its warehouse through tasks, and a rental company has dozens of these operations a week.

### What a job really cost

The hours posted are **net**, with the break already deducted, and they carry the hourly cost of each role that you already have defined in Rentman. The gap between planned and actual stops being a hunch.

### And nobody touches the record unnoticed

If someone edits already-posted hours in Rentman, **your CheckBiz360 clock-in is not changed**. The difference is detected, flagged and shown to you with both versions side by side so you decide. The legal record is never silently overwritten.

## What it does not do

Just as important:

- **It does not modify your clock-ins** based on Rentman data.
- **It does not send open or incomplete shifts**: no clock-out, nothing to send.
- **It does not create crew or assignments in Rentman.** Their API does not allow it: people and assignments travel from Rentman to CheckBiz360, never the other way.
- **It does not sync equipment, quotes or invoices.**
- **It does not send your tasks to Rentman.** Planned for later.

## Current status

| Feature | Status | Comment |
|---|---|---|
| Closed shifts posted to Rentman | **Available** | Automatic every 15 minutes, or on demand |
| Net hours with break and hourly cost | **Available** | Same figure as the legal report |
| Alert when hours are edited in Rentman | **Available** | With both versions compared |
| Crew import | **Available** | Matched by email; anyone without one stays pending |
| Jobs and warehouses as work sites | **Available** | Created inactive until the geofence is confirmed |
| Assignments turned into tasks | **Available** | One task per role, with its people |
| Warehouse tasks (dry hires and sales) | **Available** | Off by default |
| Configuration screen in the backoffice | **In development** | During the beta, the Encodebiz team sets it up |
| Sending CheckBiz360 tasks to Rentman | **Pending development** | Planned for a future release |
| Equipment, quotes and invoices | **Not available** | Out of scope |

## What you need to start

A Rentman account with permission to create an API token, CheckBiz360 time tracking active, and some time to review what the first import leaves pending — usually missing emails and geofences to confirm.

## Related articles

- [Connecting RentmanBiz step by step](95-connect-rentmanbiz.md)
- [What gets imported and what stays pending](97-import-and-pending.md)
- [Posted hours and alerts](96-posted-hours-and-alerts.md)
