# OPA Policy - Validação de Localização de Dados ISO 27018
package terraform.data_residency

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    is_personal_data_bucket(resource)
    not has_region_tag(resource)
    msg := sprintf("Bucket de dados pessoais '%s' deve ter tag 'Region' definida (ISO 27018)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    is_personal_data_bucket(resource)
    not has_lgpd_tag(resource)
    msg := sprintf("Bucket de dados pessoais '%s' deve ter tag 'LGPD' para conformidade (ISO 27018)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_replication_configuration"
    replication := resource.change.after.rule[_]
    replication.status == "Enabled"
    msg := sprintf("Replicação cross-region deve ser desabilitada para dados pessoais (ISO 27018/LGPD)", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_lifecycle_configuration"
    rule := resource.change.after.rule[_]
    to_number(rule.expiration.days) > 1825  # 5 anos
    msg := sprintf("Retenção de dados pessoais não deve exceder 5 anos (LGPD Art. 15)", [])
}

is_personal_data_bucket(bucket) {
    bucket.change.after.tags.DataType == "PersonalData"
}

has_region_tag(bucket) {
    bucket.change.after.tags.Region
}

has_lgpd_tag(bucket) {
    bucket.change.after.tags.LGPD == "true"
}
