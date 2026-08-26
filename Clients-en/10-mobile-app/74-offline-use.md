# Offline use

CheckBiz360 is designed to work with an active internet connection. The platform's critical operations — clocking in above all — require real-time validation with the servers and cannot be carried out without connectivity. Offline, the application has very limited functionality: it only allows consultation of data already loaded into the device's cache during previous sessions.

This article explains what is available offline, what strictly requires connectivity and what is planned for future versions.

---

## What works offline (consulting cached data only)

When no connection is available, the application allows the information downloaded during previous sessions with an active connection to be consulted. This information is not updated until connectivity is restored.

### Consulting attendance records already downloaded

You can review the clocking history that was loaded in the last session with a connection. The information shown corresponds to the last synchronised state; you will not see changes made after that synchronisation.

### Consulting previously downloaded documents

Employment documents you have already opened or downloaded while you had a connection (payslips, contracts or other files from the documents section) remain available for consultation offline.

### Consulting downloaded tasks

Tasks that were loaded during the last session with a connection can be consulted. You will be able to see the detail of each task, its downloaded attachments and its status at the moment of the last synchronisation.

---

## What does NOT work offline

The following functions strictly require an internet connection and are not available in offline mode:

### Making clock records

Clocking (check-in, check-out and breaks) requires a connection at the moment it is carried out. The system needs to validate in real time your identity, your GPS location in relation to the site's geofence, the status of your active shift and the authorised device rules. None of these validations can be performed without connectivity.

> **Warning:** If you try to clock in offline, the application will inform you that the operation cannot be completed. There is no queue of pending clock records: the record's timestamp has to correspond to the real moment it occurs, and the validations cannot be postponed.

### Downloading new documents

If your organisation publishes a document while you have no connection, you will not be able to download or view it until you regain internet access.

### Synchronising changes to tasks

Task status changes (marking as completed, updating progress) require a connection to be transmitted to the server. If you update a task offline, the change may be saved locally but will not be visible to your manager until it synchronises.

### Signing in for the first time on the device

The initial authentication process always requires a connection to verify credentials. If you have never signed in on that device, you will not be able to access the application without connectivity.

---

## Offline mode with a synchronisation queue

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

In a future version, CheckBiz360 will incorporate a robust offline mode with a synchronisation queue allowing clock records to be made offline and sent to the server as soon as connectivity is restored. This mode will include deferred validation of the clocking conditions (geofence, device, schedule) and conflict resolution mechanisms. For now, clocking requires an active connection at the moment it is carried out.

---

## Synchronisation on regaining the connection

When CheckBiz360 detects that the connection has been restored, it automatically performs a background synchronisation to update the cached data. No manual action is needed; the application does it as soon as it detects connectivity.

---

## Recommendations for environments with intermittent connectivity

If you work in environments where the connection is not stable, bear the following in mind:

1. **Make your clock records as soon as you have a connection.** Do not wait: if you have enough signal, clock in immediately.
2. **Open documents in advance.** If you know you will need to consult a document, open it while you have a connection so that it is cached.
3. **Review your tasks before losing the connection.** Load the list while you have a connection so that the information is available afterwards.
4. **Turn on WiFi when it is available.** A stable WiFi connection is preferable to mobile data in environments with fluctuating coverage.
5. **Report connectivity problems to your manager.** If connection problems recurrently affect your clock records, inform your manager so that there is a record and they can handle the records manually.

> **Warning:** If on a given day you were unable to make any clock record because of connectivity problems, you should inform your manager and request the creation of a manual workday from the "My records" section. See the article on attendance records for the complete procedure.

---

## Role note

This article is aimed at **employees** who use the app in environments where connectivity may be limited or intermittent.

---

## Related articles

- [My attendance records](73-my-attendance-records.md)
- [Main app navigation](71-main-app-navigation.md)
- [App updates](75-app-updates.md)
