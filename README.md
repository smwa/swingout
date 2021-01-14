# Swingout

## Notes

Request Community(by clicking on map and clicking link to "Add community"):
Community
  label
  lat
  long
  url
  styles[]
  contact(don't show publically) {
    email | phone | facebookUrl
  }[]
  timeAdded

Verify Community is active:
  manually check url, and contact one of the contacts.
  Then add an event saying they are verified, or are marked defunct.

Update community request:
  User can send a message to me by clicking a community,
  clicking update,
  and typing in a free-form message about what needs to change,
  including adding or removing contact info.
  I then add new events manually, which include timestamps.

Actions:
  CommunityAdded(uuid, label, latitude, longitude, url, styles, contacts)
  CommunityUpdateRequested(uuid, message)
  CommunityVerified(uuid, message)
  CommunityFailedVerification(uuid, message)
  CommunityUpdated(uuid, label, latitude, longitude, url, styles, contacts)

<!-- vim: set ts=2 sw=2 : -->
