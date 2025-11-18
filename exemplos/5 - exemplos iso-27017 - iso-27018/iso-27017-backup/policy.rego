# OPA Policy - Validação de Backup ISO 27017
package terraform.backup_compliance

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_backup_plan"
    not has_daily_schedule(resource)
    msg := sprintf("Plano de backup '%s' deve ter agendamento diário (ISO 27017)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_backup_plan"
    rule := resource.change.after.rule[_]
    to_number(rule.lifecycle.delete_after) < 30
    msg := sprintf("Backup deve ter retenção mínima de 30 dias (ISO 27017)", [])
}

deny[msg] {
    backup_plan := input.resource_changes[_]
    backup_plan.type == "aws_backup_plan"
    
    not has_backup_selection(backup_plan)
    msg := sprintf("Plano de backup '%s' deve ter seleção de recursos configurada (ISO 27017)", [backup_plan.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_backup_vault"
    not has_notifications(resource)
    msg := sprintf("Vault de backup '%s' deve ter notificações configuradas (ISO 27017)", [resource.name])
}

has_daily_schedule(plan) {
    rule := plan.change.after.rule[_]
    contains(rule.schedule, "cron")
}

has_backup_selection(plan) {
    selection := input.resource_changes[_]
    selection.type == "aws_backup_selection"
    selection.change.after.plan_id == plan.change.after.id
}

has_notifications(vault) {
    notifications := input.resource_changes[_]
    notifications.type == "aws_backup_vault_notifications"
    notifications.change.after.backup_vault_name == vault.change.after.name
}
