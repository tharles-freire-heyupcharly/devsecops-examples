# OPA Policy - Validação de Criptografia ISO 27017
package terraform.s3_encryption

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not has_encryption(resource)
    msg := sprintf("Bucket S3 '%s' deve ter criptografia habilitada (ISO 27017)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_server_side_encryption_configuration"
    encryption := resource.change.after.rule[_]
    encryption.apply_server_side_encryption_by_default.sse_algorithm != "aws:kms"
    msg := sprintf("Bucket deve usar KMS (sse_algorithm: aws:kms) para ISO 27017", [])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_kms_key"
    resource.change.after.enable_key_rotation != true
    msg := sprintf("Chave KMS '%s' deve ter rotação automática habilitada (ISO 27017)", [resource.name])
}

has_encryption(bucket) {
    encryption := input.resource_changes[_]
    encryption.type == "aws_s3_bucket_server_side_encryption_configuration"
    encryption.change.after.bucket == bucket.change.after.id
}
