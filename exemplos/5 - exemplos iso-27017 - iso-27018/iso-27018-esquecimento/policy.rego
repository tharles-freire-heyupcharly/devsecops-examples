# OPA Policy - Validação Direito ao Esquecimento ISO 27018
package terraform.right_to_erasure

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_lambda_function"
    is_erasure_function(resource)
    to_number(resource.change.after.timeout) < 300
    msg := sprintf("Lambda de esquecimento deve ter timeout >= 300s para processar exclusões (ISO 27018)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_sqs_queue"
    to_number(resource.change.after.message_retention_seconds) < 1209600  # 14 dias
    msg := sprintf("Fila SQS deve reter mensagens por >= 14 dias (ISO 27018/LGPD)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudwatch_log_group"
    is_erasure_audit_log(resource)
    to_number(resource.change.after.retention_in_days) < 2555  # 7 anos
    msg := sprintf("Logs de auditoria devem ter retenção >= 7 anos (LGPD Art. 37)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_dynamodb_table"
    is_deletion_registry(resource)
    not has_point_in_time_recovery(resource)
    msg := sprintf("Tabela de registro de exclusões deve ter PITR habilitado (ISO 27018)", [])
}

is_erasure_function(lambda) {
    contains(lambda.change.after.function_name, "esquecimento")
}

is_erasure_audit_log(log_group) {
    log_group.change.after.tags.Purpose == "AuditoriaEsquecimento"
}

is_deletion_registry(table) {
    table.change.after.tags.LGPD == "RegistroExclusoes"
}

has_point_in_time_recovery(table) {
    table.change.after.point_in_time_recovery.enabled == true
}
