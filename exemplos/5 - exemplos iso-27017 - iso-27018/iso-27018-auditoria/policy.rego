# OPA Policy - Validação de Auditoria ISO 27018
package terraform.audit_compliance

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudtrail"
    resource.change.after.enable_log_file_validation != true
    msg := sprintf("CloudTrail '%s' deve ter validação de logs habilitada (ISO 27018)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudtrail"
    resource.change.after.is_multi_region_trail != true
    msg := sprintf("CloudTrail deve ser multi-região para auditoria completa (ISO 27018)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudtrail"
    not has_data_events(resource)
    msg := sprintf("CloudTrail deve capturar eventos de acesso a dados (ISO 27018/LGPD)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_lifecycle_configuration"
    is_audit_logs_bucket(resource)
    rule := resource.change.after.rule[_]
    to_number(rule.expiration.days) < 2555  # 7 anos
    msg := sprintf("Logs de auditoria devem ter retenção mínima de 7 anos (LGPD Art. 37)", [])
}

deny[msg] {
    cloudtrail := input.resource_changes[_]
    cloudtrail.type == "aws_cloudtrail"
    not has_anomaly_detection(cloudtrail)
    msg := sprintf("CloudTrail deve ter detecção de anomalias configurada (ISO 27018)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    is_audit_bucket(resource)
    not has_versioning_enabled(resource)
    msg := sprintf("Bucket de auditoria deve ter versionamento habilitado (ISO 27018)", [])
}

has_data_events(trail) {
    event_selector := trail.change.after.event_selector[_]
    event_selector.data_resource
}

is_audit_logs_bucket(lifecycle) {
    bucket := input.resource_changes[_]
    bucket.type == "aws_s3_bucket"
    bucket.change.after.tags.Purpose == "AuditLogs"
    lifecycle.change.after.bucket == bucket.change.after.id
}

has_anomaly_detection(trail) {
    alarm := input.resource_changes[_]
    alarm.type == "aws_cloudwatch_metric_alarm"
    alarm.change.after.tags.Compliance == "ISO-27018"
}

is_audit_bucket(bucket) {
    bucket.change.after.tags.Purpose == "AuditLogs"
}

has_versioning_enabled(bucket) {
    versioning := input.resource_changes[_]
    versioning.type == "aws_s3_bucket_versioning"
    versioning.change.after.bucket == bucket.change.after.id
    versioning.change.after.versioning_configuration.status == "Enabled"
}
