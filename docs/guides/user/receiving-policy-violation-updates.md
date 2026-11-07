# Receive policy violation updates

Configure an alert to report changes to the matched vulnerabilities of an existing component policy violation.

!!! note "Unreleased feature"

    This guide requires the API server change proposed in
    [PR #7908](https://github.com/DependencyTrack/dependency-track/pull/7908)
    and a frontend that exposes the new notification groups.
    No released version currently includes these notification groups.

## Prerequisites

- Permission to [edit component policies](managing-component-policies.md).
- The `SYSTEM_CONFIGURATION` permission to configure alerts.
- An enabled [KEV data source](../administration/configuring-kev-sources.md).
- A configured [notification publisher](../../reference/notifications/publishers.md) and a destination you control.

## Return the matched identifiers

1. Open **Policy Management → Policies**, and select the component policy to edit.
2. Add or edit a condition with the **Expression** subject and **Security** violation type.
3. Use this expression to record the matched KEV identifiers:

    ```js
    vulns.filter(vuln, vuln.is_kev).map(vuln, vuln.id).join(",")
    ```

4. Save the condition.

Include every identifier that matters to your alert, and avoid time-dependent values in the message.
For the message length limit and result semantics, see [Condition expression results](../../reference/policies/condition-expressions.md#result).

## Subscribe to changes

1. Open **Administration → Notifications → Alerts**.
2. Create an alert with the **Portfolio** scope, **Event** trigger, **Informational** level, and your chosen publisher. Select **Create**.
3. Open the alert for editing. You can also use an existing alert with these scope, trigger, and level settings.
4. Select **POLICY_VIOLATION_UPDATED** for changes to violations that are neither approved nor suppressed.
5. If you also want changes while a violation remains approved or suppressed, select **POLICY_VIOLATION_UPDATED_REVIEWED**.
6. Keep **POLICY_VIOLATION** selected if you also want notifications when violations first appear.
7. Configure the destination, project or tag restrictions, and optional filter expression. Turn on **Enabled**, and select **Submit**.

The [update group reference](../../reference/notifications/groups.md#policy-violation-updates) describes review decisions, field presence, and events that do not trigger a notification.

## Verify delivery

1. Select **Perform Test** on the alert to check the destination.
2. Trigger project analysis for a project that matches the policy.
3. When the matching KEV identifiers change, check the delivered notification's previous and current messages and violation UUID.
4. Run analysis again without changing the matches, and check that no new update event appears.

For approved or suppressed violations, check delivery to an alert that explicitly includes **POLICY_VIOLATION_UPDATED_REVIEWED**.
Adding that subscription does not send past message changes. See [Message change behavior](../../reference/notifications/groups.md#message-change-behavior).

If an expected notification does not arrive, follow [Debugging missing notifications](../administration/debugging-notifications.md).
For a custom template, add an [update notification branch](../../reference/notifications/templating.md#policy-violation-updates).
