# What gets imported and what stays pending

When you connect RentmanBiz, the platform brings across from Rentman what it needs for your team to be able to clock in. This article explains what comes in, what is deliberately left out, and why some things arrive **pending completion**.

## Before importing: the preview

Importing never starts blind. First a **preview** is generated that writes nothing and answers the reasonable question: *what is this about to put into my platform?*

You will see how many jobs would become work sites, how many are discarded, how many people can be created and how many cannot, and how many tasks would be generated. Only when the result looks right does it run for real.

## What is imported

### People

Each person on your Rentman crew is first looked up among your CheckBiz360 employees **by email address**. If they already exist, they are linked — never duplicated, because splitting someone's history in two is worse than not importing them.

If they do not exist and they have an email, they are created with their access and receive their welcome email.

### Work sites

Two kinds come in:

- **Jobs**: every Rentman project **that has crew assigned**. That is the criterion, not the project type: if nobody is assigned, nobody will clock in there.
- **Warehouses**: your equipment locations, which are permanent sites where people clock in daily.

For both, the address is taken and coordinates calculated to propose the geofence.

### Responsibilities

Each person is linked to the sites where they work: the warehouse assigned in their Rentman record, and any jobs they are assigned to. With their function as job title — technician, rigger, stagehand — and the hourly cost you already have defined there.

**Everyone comes in as a worker.** A Rentman function is a trade, not a permission level: mounting lights at an event does not make someone responsible for a work site. To promote somebody, you do it by hand and on purpose.

### Tasks

One task per role on each job, with all the people in that role. And, if you enable it, warehouse tasks for dry hires and sales: prepare the equipment before it goes out, check it back in when it returns.

## What is discarded, and why

| Discarded | Reason |
|---|---|
| Projects with no crew | Sales and dry hires: nobody sets foot anywhere, nowhere to clock in |
| Projects outside the window | Only the last month and the next three, so history is not dragged in |
| Equipment, quotes, invoices | Out of scope for the integration |

## What stays pending

Rentman does not store everything CheckBiz360 needs. Rather than inventing it or discarding the record, the platform imports it flagged as **pending**, with the reason, and shows an alert with a direct link to the record where it is fixed.

| Pending | What it means | What to do |
|---|---|---|
| **No email** | Rentman rarely stores it, and in CheckBiz360 it is the employee's login | Add the email to their record. They then get their access and welcome email |
| **Geofence not confirmed** | Rentman gives no coordinates: they were calculated from the address | Review the point on the site and activate it |
| **No address** | That job has no address in Rentman | Complete it, or leave the site unused |
| **No hourly cost** | That role has no rate defined in Rentman | Set it, or those shifts will show zero cost in reports |

Two important points about pending items:

**Nothing pending can do harm while it stays pending.** A site without a confirmed geofence is created **inactive**: it exists, but it neither validates nor invalidates anyone's clock-in. A person without an email is created **inactive and without access**.

**And nothing pending is billed to you.** Since billing is per active employee, someone who cannot yet work does not count. They start counting when you complete their email and they become active — which is when they can actually clock in.

The alert disappears on its own once nothing is left to complete.

## Importing again

You can repeat the import safely: what already exists is not duplicated, and anything you configured by hand — geofences, schedules, breaks — is **never overwritten**. Only what is new in Rentman is added.

## Related articles

- [RentmanBiz](94-rentmanbiz.md)
- [Connecting RentmanBiz step by step](95-connect-rentmanbiz.md)
