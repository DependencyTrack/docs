# Debugging missing notifications

When users report that an expected notification did not arrive, the
cause typically falls into a small number of categories. This guide walks
through how to narrow it down.

## Common causes

- **Misconfigured alert.** The alert's scope, level, group selection,
  project limits, or tag limits exclude the notification. Verify against
  [Configuring notification alerts](../user/configuring-notifications.md).
- **Filter expression rejects the notification.** A CEL filter on the
  alert evaluates to false. Test the expression as described in
  [Filter expressions](../../reference/notifications/filter-expressions.md).
- **Publisher destination is unreachable.** Network outage, firewall,
  proxy misconfiguration, or expired webhook URL.
- **Local destination blocked.** The destination resolves to a local or
  loopback address and the corresponding `allow-local-connections` flag
  is `false`.
- **Custom template fails to render.** A syntax error or missing
  variable causes the publisher to stop before sending.

## Inspecting the API server logs

The API server logs failed deliveries at level `WARN` or `ERROR`. Search the
logs for the alert's name or the publisher class name. The server does *not*
log successful deliveries by default.

To log successful deliveries for a specific alert, open the alert and
enable *Log successful publishes*. The API server then emits an `INFO`
log line every time the alert delivers.

!!! note
    Enabling this on busy alerts can sharply increase log volume.
    Treat it as a temporary diagnostic, or scope it to alerts that
    deliver rarely.

A successful-publish log line includes the matched alert, the publisher,
and high-level details of the notification (group, level, scope, and
subject identifiers).

```text
INFO ... Notification published successfully [notificationId=..., notificationRuleName=...]
```

Failure log lines include the underlying exception. Common patterns:

- `UnknownHostException` / `ConnectException`: the destination host is
  not reachable from the API server.
- `SSLHandshakeException`: TLS configuration mismatch (expired
  certificate, internal CA not trusted, protocol/cipher mismatch).
- `IOException: Server returned HTTP response code: 4xx`: the
  destination rejected the request. Inspect the response body.
- `PebbleException`: custom template fails to render.

## End-to-end verification with a request bin

For webhook-based publishers (Webhook, Slack, Microsoft Teams,
Mattermost, Webex, Jira), point the alert at a request-bin service to
confirm whether the API server is sending requests at all.

1. Create a private request bin at <https://pipedream.com/requestbin>
   (or a similar service).
2. Edit the alert and replace the destination with the bin's URL.
3. Confirm that you have selected the relevant groups.
4. Trigger an event that matches one of the selected groups. For
   example, upload an SBOM to a project the alert covers, which fires
   `BOM_PROCESSED`.
5. Watch the request bin. If a request arrives, the API server is
   sending; the original destination is the cause.

For non-webhook publishers (email, Kafka), substitute a destination
under the operator's control: a captured SMTP server (such as MailHog)
or a Kafka topic you can inspect directly.

## Quickest local check: the console publisher

The built-in Console publisher writes notifications to the API server's
standard output. For local debugging it removes networking from the
loop entirely:

1. Confirm `dt.notification-publisher.console.enabled` is `true`.
2. Create an alert that uses the Console publisher and selects the
   group of interest.
3. Trigger the matching event.
4. Inspect the API server container logs.

If the Console publisher emits the notification but a parallel alert on
a different publisher does not, the issue is in the second publisher's
configuration or destination.

## See also

- [Notification publishers](../../reference/notifications/publishers.md)
- [Filter expressions](../../reference/notifications/filter-expressions.md)
- [Configuring notification alerts](../user/configuring-notifications.md)
